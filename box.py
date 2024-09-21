from melo.api import TTS
import os
import sys
import cv2
import time
import re
import shutil
import threading
import pygame
from transformers import AutoModelForCausalLM, AutoTokenizer
import whisper
import speech_recognition as sr
import torch
from pydub import AudioSegment
import socket
import qianfan
from dotenv import load_dotenv

os.environ["HF_ENDPOINT"] = "https://hf-mirror.com"
os.chdir("/home/pill/smart-pill-box")
sys.path.append("/home/pill/smart-pill-box")
from paddleocr import PaddleOCR
from camera.camera import Camera
from motion.controller import controller, check

params_add = [650, 980, 1320, 1650, 1990, 2330]

params_supply = [1650, 1990, 2330, 650, 980, 1320]
load_dotenv()


# ASR
class ASRProcessor:
    def __init__(self):
        self.recognizer = sr.Recognizer()
        self.model = whisper.load_model("base")

    def recognize(self):
        with sr.Microphone() as source:
            print("Please say something")
            self.recognizer.adjust_for_ambient_noise(source)
            audio = self.recognizer.listen(source)
            print("Recording finished")
        with open("llm/in.wav", "wb") as f:
            f.write(audio.get_wav_data())
        result = self.model.transcribe("llm/in.wav")
        print(result["text"])
        return result["text"]


# OCR
class OCRProcessor:
    def __init__(self):
        self.model = PaddleOCR(use_angle_cls=True, lang="ch", show_log=False)

    def find_last_number_between_patterns(self, text, start_pattern, end_pattern):
        pattern = re.compile(
            f"{re.escape(start_pattern)}(.*?)({re.escape(end_pattern)})"
        )
        match = pattern.search(text)
        if match:
            number_pattern = re.compile(r"\d+")
            numbers = number_pattern.findall(match.group(1))
            if numbers:
                return int(numbers[-1])
        return None

    def find_text_between_patterns(self, text, start_pattern, end_pattern):
        pattern = re.compile(
            f"{re.escape(start_pattern)}(.*?)({re.escape(end_pattern)})", re.DOTALL
        )
        match = pattern.search(text)
        if match:
            return match.group(1).strip()
        return None

    def ocr_image(self, img):
        self.ocr_result = self.model.ocr(img)
        if not self.ocr_result[0]:
            self.text = ""
            return
        self.text = "".join(line[1][0] for line in self.ocr_result[0])

    def get_dosage(self, img):
        self.ocr_image(img)
        dosage = self.find_text_between_patterns(self.text, "用法用量", "不良反应")
        if not dosage:
            self.dosage_per_day = None
            self.dosage_per_time = None
            return
        self.dosage_per_day = self.find_last_number_between_patterns(dosage, "日", "次")
        self.dosage_per_time = self.find_last_number_between_patterns_with_units(dosage)

    def find_last_number_between_patterns_with_units(self, text):
        """
        尝试从不同的单位（片、粒、颗、袋）中提取每次用药量。
        """
        units = ["片", "粒", "颗", "袋"]
        for unit in units:
            dosage_per_time = self.find_last_number_between_patterns(text, "次", unit)
            if dosage_per_time is not None:
                return dosage_per_time
        return None


# TTS
class TTSProcessor:
    def __init__(self):
        os.chdir("/home/pill/smart-pill-box")
        self.model = TTS(
            language="ZH_MIX_EN",
            ckpt_path="tts/checkpoint.pth",
            config_path="tts/config.json",
        )
        self.speaker_ids = self.model.hps.data.spk2id

    def tts_to_file(self, text, speaker_id, file_path):
        self.model.tts_to_file(text, speaker_id, file_path)


# LLM
class LLM:
    def __init__(self):
        self.device = "cuda"
        self.model = AutoModelForCausalLM.from_pretrained(
            "/home/pill/.cache/huggingface/hub/models--Qwen--Qwen2-0.5B-Instruct/snapshots/c291d6fce4804a1d39305f388dd32897d1f7acc4",
            torch_dtype="auto",
            device_map="auto",
        )
        self.tokenizer = AutoTokenizer.from_pretrained(
            "/home/pill/.cache/huggingface/hub/models--Qwen--Qwen2-0.5B-Instruct/snapshots/c291d6fce4804a1d39305f388dd32897d1f7acc4"
        )
        self.conversation_history = [
            {
                "role": "user",
                "content": "你是一个老人陪伴助手",
            }
        ]

    def ask_question(self, prompt):
        self.conversation_history.append({"role": "user", "content": prompt})
        text = self.tokenizer.apply_chat_template(
            self.conversation_history, tokenize=False, add_generation_prompt=True
        )
        model_inputs = self.tokenizer([text], return_tensors="pt").to(self.device)
        generated_ids = self.model.generate(model_inputs.input_ids, max_new_tokens=512)
        generated_ids = [
            output_ids[len(input_ids) :]
            for input_ids, output_ids in zip(model_inputs.input_ids, generated_ids)
        ]
        response = self.tokenizer.batch_decode(generated_ids, skip_special_tokens=True)[
            0
        ]
        self.conversation_history.append({"role": "assistant", "content": response})
        return response


class ImageProcessingThread(threading.Thread):
    def __init__(self, tts_processor: TTSProcessor, ocr_processor: OCRProcessor):
        super().__init__()
        torch.cuda.empty_cache()
        self.tts_processor = tts_processor
        self.ocr_processor = ocr_processor
        self._stop_event = threading.Event()

    def get_img(self):
        camera = Camera()
        camera.capture_image()
        image_path = "image.jpg"
        image = cv2.imread(image_path)
        return image

    def run(self):
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
            self.tts_processor.tts_to_file(
                part, self.tts_processor.speaker_ids["ZH"], output_path
            )

    def split_text(self, text, max_length=150):
        return [text[i : i + max_length] for i in range(0, len(text), max_length)]

    def stop(self):
        self._stop_event.set()


class AudioPlaybackThread(threading.Thread):
    def __init__(self):
        super().__init__()
        os.chdir("/home/pill/smart-pill-box")
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
            audio = AudioSegment.from_file(output_path)
            audio.export(output_path, format="wav")
            try:
                pygame.mixer.music.load(output_path)
                while self.paused and not self._stop_event.is_set():
                    time.sleep(0.1)
                pygame.mixer.music.play()
                while True:
                    if self._stop_event.is_set():
                        pygame.mixer.music.stop()
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
            except:
                print(f"加载音频{i}失败")
                continue
        print("播放结束")
        print("-" * 10 + "read news end" + "-" * 10)

    def pause(self):
        self.paused = True

    def unpause(self):
        self.paused = False

    def stop(self):
        self._stop_event.set()


class ChatBotThread(threading.Thread):
    def __init__(
        self, llm: LLM, asr_processor: ASRProcessor, tts_processor: TTSProcessor
    ):
        super().__init__()
        torch.cuda.empty_cache()
        os.system("rm llm/*.wav")
        self._stop_event = threading.Event()
        self.llm = llm
        self.tts_processor = tts_processor
        self.asr_processor = asr_processor

    def run(self):
        if not test_internet_connection():
            while not self._stop_event.is_set():
                user_input = self.asr_processor.recognize()
                if user_input.lower() in ["exit", "quit"] or self._stop_event.is_set():
                    self._stop_event.set()
                    return
                answer = self.llm.ask_question(user_input)
                print("Assistant:", answer)
                if self._stop_event.is_set():
                    return
                self.tts_processor.tts_to_file(
                    answer, self.tts_processor.speaker_ids["ZH"], "llm/out.wav"
                )
                if self._stop_event.is_set():
                    return
                self.play_audio()
        else:
            chat_comp = qianfan.ChatCompletion()
            chat_history = []

            while True:
                user_input = self.asr_processor.recognize()
                if user_input.lower() in ["exit", "quit"] or self._stop_event.is_set():
                    self._stop_event.set()
                    return
                if user_input != "":
                    try:
                        chat_history.append({"role": "user", "content": user_input})
                        resp = chat_comp.do(
                            model="ERNIE-Lite-8K", messages=chat_history
                        )
                        print(f'\nassistant: {resp["body"]["result"]}\n')
                        chat_history.append(
                            {"role": "assistant", "content": resp["body"]["result"]}
                        )
                        if self._stop_event.is_set():
                            return
                        self.tts_processor.tts_to_file(
                            resp["body"]["result"],
                            self.tts_processor.speaker_ids["ZH"],
                            "llm/out.wav",
                        )
                        if self._stop_event.is_set():
                            return
                        self.play_audio()
                    except:
                        pass

    def stop(self):
        self._stop_event.set()

    def play_audio(self):
        pygame.mixer.init()
        pygame.mixer.music.load("llm/out.wav")
        pygame.mixer.music.play()
        while pygame.mixer.music.get_busy() and not self._stop_event.is_set():
            continue
        pygame.mixer.music.stop()


def _init():
    print("-" * 10 + "init start" + "-" * 10)
    global num_files, condition, ocr_processor, tts_processor, asr_processor, llm
    tts_processor = TTSProcessor()
    ocr_processor = OCRProcessor()
    llm = LLM()
    asr_processor = ASRProcessor()
    num_files = 0
    condition = threading.Condition()
    print("-" * 10 + "init finished" + "-" * 10)


def test_internet_connection():
    host = "www.baidu.com"
    port = 80
    timeout = 2

    try:
        socket.setdefaulttimeout(timeout)
        socket.socket(socket.AF_INET, socket.SOCK_STREAM).connect((host, port))
        print("网络连接正常")
        return True
    except socket.error as ex:
        print("网络连接异常：" + str(ex))
        return False


def read_news():
    torch.cuda.empty_cache()
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
    torch.cuda.empty_cache()
    try:
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
    except:
        print("OCR识别失败")
        return None, None


def get_usb():
    directory = "/media/pill"
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
    directory = f"/media/pill/{usb[0]}"
    audio_extensions = [".mp3", ".wav", ".flac", ".aac", ".ogg", ".wma", ".m4a"]
    try:
        for entry in os.listdir(directory):
            full_path = os.path.join(directory, entry)
            if (
                os.path.isfile(full_path)
                and os.path.splitext(entry)[1].lower() in audio_extensions
            ):
                audio_files.append(entry)
    except FileNotFoundError:
        print(f"Directory {directory} does not exist.")
    return audio_files


def copy_audio_file(files):
    print(files)
    usb = get_usb()
    for file in files:
        shutil.copy(f"/media/pill/{usb[0]}/{file}", f"audio/{file}")


def delete_audio_file(files):
    for file in files:
        os.remove(f"audio/{file}")


class AudioPlayThread(threading.Thread):
    def __init__(self, file_name):
        super().__init__()
        self.paused = False
        self._stop_event = threading.Event()
        self.file_path = file_name

    def run(self):
        os.chdir("/home/pill/smart-pill-box")
        if not os.path.exists(self.file_path):
            print(f"{self.file_path}不存在")
            return
        try:
            pygame.mixer.init()
            pygame.mixer.music.load(self.file_path)
            pygame.mixer.music.play()
            while True:
                if self._stop_event.is_set():
                    pygame.mixer.music.stop()
                    return
                paused = self.paused
                if paused:
                    pygame.mixer.music.pause()
                else:
                    pygame.mixer.music.unpause()
                if not paused and pygame.mixer.music.get_busy() == 0:
                    break
                time.sleep(0.1)
            print(f"{self.file_path}播放结束")
        except Exception as e:
            print(f"{self.file_path}加载失败")
            print(f"Exception occurred: {e}")

    def pause(self):
        self.paused = True

    def unpause(self):
        self.paused = False

    def stop(self):
        self._stop_event.set()


def play_audio(file_name):
    global audio_play_thread
    audio_play_thread = AudioPlayThread(f"audio/{file_name}")
    audio_play_thread.start()
    audio_play_thread.pause()


def chat_bot():
    torch.cuda.empty_cache()
    global chat_bot_thread, llm, asr_processor, tts_processor
    chat_bot_thread = ChatBotThread(llm, asr_processor, tts_processor)
    chat_bot_thread.start()


def sysaudio(file):
    sysaudio = AudioPlayThread(f"sys_audio/{file}.wav")
    sysaudio.start()
    sysaudio.join()


def get_pill(id, num):
    i = 0
    flag = 0
    bias = [0, 20, -20, 30, -25]
    while i < num:
        controller(5, params_add[id - 1] + bias[flag])
        controller(3, 1)
        controller(2, -2800)
        controller(2, 3000)
        if check():
            print("出药失败")
            flag += 1
            flag %= 5
            continue
        else:
            print("出药成功")
            flag = 0
        controller(1, 1300)
        controller(3, 0)
        time.sleep(2)
        controller(2, -510)
        controller(1, -470)
        controller(2, 1500)
        i += 1


def get_pill_box(id):
    controller(5, params_supply[id - 1])
    print(id - 1)


def add_medicine_name(id):
    global asr_processor
    torch.cuda.empty_cache()
    with sr.Microphone() as source:
        print("Please say something")
        asr_processor.recognizer.adjust_for_ambient_noise(source)
        audio = asr_processor.recognizer.listen(source)
        print("Recording finished")
    with open(f"sys_audio/Medicine_{id}.wav", "wb") as f:
        f.write(audio.get_wav_data())


class ReadMedicineThread(threading.Thread):
    def __init__(self, id_list):
        super().__init__()
        self.id_list = id_list
        self._stop_event = threading.Event()

    def run(self):
        sysaudio("Current_List")
        if self._stop_event.is_set():
            return
        for id in self.id_list:
            sysaudio(f"Box_{id}")
            if self._stop_event.is_set():
                return
            sysaudio(f"Medicine_{id}")
            if self._stop_event.is_set():
                return

    def stop(self):
        self._stop_event.set()


def read_medicine(id_list):
    global read_medicine_thread
    read_medicine_thread = ReadMedicineThread(id_list)
    read_medicine_thread.start()
