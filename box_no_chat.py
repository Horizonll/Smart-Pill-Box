# sudo apt install ffmpeg
import os
import sys
import cv2
import time
import re
import shutil
import threading
import pygame
from melo.api import TTS

# from pydub import AudioSegment

os.chdir("/home/pill/smart-pill-box")
sys.path.append("/home/pill/smart-pill-box")
from paddleocr import PaddleOCR
from camera.camera import Camera


# OCR
class OCRProcessor:
    def __init__(self):
        self.ocr = PaddleOCR(use_angle_cls=True, lang="ch", show_log=False)

    def find_last_number_between_patterns(self, text, start_pattern="日", end_pattern="次"):
        pattern = re.compile(f"{re.escape(start_pattern)}(.*?)({re.escape(end_pattern)})")
        match = pattern.search(text)
        if match:
            number_pattern = re.compile(r"\d+")
            numbers = number_pattern.findall(match.group(1))
            if numbers:
                last_number = int(numbers[-1])
                return last_number
        return None

    def find_text_between_patterns(self, text, start_pattern="用法用量", end_pattern="不良反应"):
        pattern = re.compile(f"{re.escape(start_pattern)}(.*?)({re.escape(end_pattern)})", re.DOTALL)
        match = pattern.search(text)
        if match:
            return match.group(1).strip()
        return None

    def ocr_image(self, img):
        self.ocr_result = self.ocr.ocr(img, cls=True)
        if not self.ocr_result[0]:
            self.text = ""
            return
        self.text = "".join(line[1][0] for line in self.ocr_result[0])

    def get_dosage(self, img):
        self.ocr_image(img)
        dosage = self.find_text_between_patterns(self.text)
        if not dosage:
            self.dosage_per_day = None
            self.dosage_per_time = None
            return
        self.dosage_per_day = self.find_last_number_between_patterns(dosage)
        self.dosage_per_time = self.find_last_number_between_patterns(dosage, "次", "片")
        if self.dosage_per_time is None:
            self.dosage_per_time = self.find_last_number_between_patterns(dosage, "次", "粒")
        if self.dosage_per_time is None:
            self.dosage_per_time = self.find_last_number_between_patterns(dosage, "次", "颗")
        if self.dosage_per_time is None:
            self.dosage_per_time = self.find_last_number_between_patterns(dosage, "次", "袋")


# TTS
class TTSProcessor:
    def __init__(self):
        os.chdir("/home/pill/smart-pill-box")
        self.model = TTS(language="ZH_MIX_EN", ckpt_path="tts/checkpoint.pth", config_path="tts/config.json")
        self.speaker_ids = self.model.hps.data.spk2id


class ImageProcessingThread(threading.Thread):
    def __init__(self, tts_processor: TTSProcessor, ocr_processor: OCRProcessor):
        super().__init__()
        self.tts_processor = tts_processor
        self.ocr_processor = ocr_processor
        self._stop_event = threading.Event()

    def run(self):
        self.read_img()

    def stop(self):
        self._stop_event.set()

    def get_img(self):
        camera = Camera()
        camera.capture_image()
        image_path = "image.jpg"
        image = cv2.imread(image_path)
        return image

    def read_img(self):
        self.ocr_processor.ocr_image(self.get_img())
        if self.ocr_processor.text != "":
            print("识别结果:")
            print(self.ocr_processor.text)
            print("开始合成")
            self.generate_audio(self.ocr_processor.text)
        else:
            print("未识别到文字")
            global num_files
            num_files = -1
            with condition:
                condition.notify_all()

    def generate_audio(self, text):
        parts = self.split_text(text)
        global num_files
        with condition:
            num_files = len(parts)
            condition.notify_all()
        for i, part in enumerate(parts):
            if self._stop_event.is_set():
                return
            output_path = f"tts/output_{i}.wav"
            self.tts_processor.model.tts_to_file(part, self.tts_processor.speaker_ids["ZH"], output_path)

    def split_text(self, text, max_length=100):
        return [text[i : i + max_length] for i in range(0, len(text), max_length)]


class AudioPlaybackThread(threading.Thread):
    def __init__(self):
        super().__init__()
        os.system("rm tts/*.wav")
        self.paused = False
        self._stop_event = threading.Event()

    def run(self):
        global num_files
        with condition:
            while num_files == 0 and not self._stop_event.is_set():
                condition.wait()
        if num_files == -1 or self._stop_event.is_set():
            return
        pygame.mixer.init()
        for i in range(num_files):
            if self._stop_event.is_set():
                return
            output_path = f"tts/output_{i}.wav"
            while not os.path.exists(output_path) and not self._stop_event.is_set():
                time.sleep(0.1)
            # audio = AudioSegment.from_file(output_path)
            # audio.export(output_path, format="wav")
            try:
                pygame.mixer.music.load(output_path)
            except:
                print(f"加载音频{i}失败")
                continue
            while self.paused and not self._stop_event.is_set():
                time.sleep(0.1)
            pygame.mixer.music.play()
            while True:
                if self._stop_event.is_set():
                    pygame.mixer.music.stop()
                    pygame.mixer.quit()
                    return
                paused = self.paused
                if paused:
                    pygame.mixer.music.pause()
                else:
                    pygame.mixer.music.unpause()
                if not paused and pygame.mixer.music.get_busy() == 0:
                    break
                time.sleep(0.1)
            os.remove(output_path)
        print("播放结束")
        pygame.mixer.quit()
        print("-" * 10 + "read news end" + "-" * 10)

    def pause(self):
        self.paused = True

    def unpause(self):
        self.paused = False

    def stop(self):
        self._stop_event.set()


def _init():
    global tts_processor, ocr_processor, num_files, condition
    tts_processor = TTSProcessor()
    ocr_processor = OCRProcessor()
    num_files = 0
    condition = threading.Condition()
    print("-" * 10 + "init finished" + "-" * 10)


def read_news():
    global num_files, condition, ocr_processor, tts_processor, image_processing_thread, audio_playback_thread
    ocr_processor.text = None
    num_files = 0
    image_processing_thread = ImageProcessingThread(tts_processor, ocr_processor)
    audio_playback_thread = AudioPlaybackThread()
    print("-" * 10 + "start read news" + "-" * 10)
    image_processing_thread.start()
    audio_playback_thread.start()
    audio_playback_thread.pause()


def add_medicine():
    global ocr_processor
    camera = Camera()
    camera.capture_image()
    image_path = "image.jpg"
    image = cv2.imread(image_path)
    ocr_processor.ocr_image(image)
    print("说明书:")
    print(ocr_processor.text)
    ocr_processor.get_dosage(image)
    if ocr_processor.dosage_per_day is not None:
        print(f"用法用量:一日{ocr_processor.dosage_per_day}次")
    if ocr_processor.dosage_per_time is not None:
        print(f"一次{ocr_processor.dosage_per_time}片")
    return ocr_processor.dosage_per_day, ocr_processor.dosage_per_time


def get_usb():
    directory = "/medipill/a"
    usb = []
    try:
        for entry in os.listdir(directory):
            full_path = os.path.join(directory, entry)
            if os.path.isdir(full_path):
                usb.append(entry)
    except FileNotFoundError:
        print(f"Directory {directory} does not exist.")
    return usb


def get_audio_files():
    audio_files = []
    usb = get_usb()
    print(usb)
    if not usb:
        return audio_files
    directory = f"/medipill/pill/{usb[0]}"
    audio_extensions = [".mp3", ".wav", ".flac", ".aac", ".ogg", ".wma"]
    try:
        for entry in os.listdir(directory):
            full_path = os.path.join(directory, entry)
            if os.path.isfile(full_path) and os.path.splitext(entry)[1].lower() in audio_extensions:
                audio_files.append(entry)
    except FileNotFoundError:
        print(f"Directory {directory} does not exist.")
    return audio_files


def copy_audio_file(files):
    print(files)
    usb = get_usb()
    for file in files:
        shutil.copy(f"/medipill/pill/{usb[0]}/{file}", f"audio/{file}")


def delete_audio_file(files):
    for file in files:
        os.remove(f"audio/{file}")


class AudioPlayThread(threading.Thread):
    def __init__(self, file_name):
        super().__init__()
        self.paused = False
        self._stop_event = threading.Event()
        self.file_path = f"audio/{file_name}"

    def run(self):
        pygame.mixer.init()
        try:
            pygame.mixer.music.load(self.file_path)
        except:
            print(f"加载音频失败")
        pygame.mixer.music.play()
        while True:
            if self._stop_event.is_set():
                pygame.mixer.music.stop()
                pygame.mixer.quit()
                return
            paused = self.paused
            if paused:
                pygame.mixer.music.pause()
            else:
                pygame.mixer.music.unpause()
            if not paused and pygame.mixer.music.get_busy() == 0:
                break
            time.sleep(0.1)
        print("播放结束")
        pygame.mixer.quit()

    def pause(self):
        self.paused = True

    def unpause(self):
        self.paused = False

    def stop(self):
        self._stop_event.set()


def play_audio(file_name):
    global audio_play_thread
    audio_play_thread = AudioPlayThread(file_name)
    audio_play_thread.start()
    audio_play_thread.pause()
