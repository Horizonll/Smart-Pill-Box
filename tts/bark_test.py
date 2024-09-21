# sudo apt-get install ffmpeg
import os
import sys
import cv2
import time
import soundfile
import threading
import pygame
from pydub import AudioSegment
from transformers import pipeline

os.chdir("/home/pill/smart-pill-box")
sys.path.append("/home/pill/smart-pill-box")
from ocr.paddleocr_test import OCRProcessor
from camera.camera import Camera

num_files = 0
condition = threading.Condition()


class TTSProcessor:
    def __init__(self):
        self.synthesiser = pipeline("text-to-speech", "suno/bark-small", device="cuda")


class ImageProcessingThread(threading.Thread):
    def __init__(self, tts_processor: TTSProcessor, ocr_processor: OCRProcessor):
        super().__init__()
        self.tts_processor = tts_processor
        self.ocr_processor = ocr_processor
        self._stop_event = threading.Event()
        self.t1 = time.time()
        self.t2 = 0

    def run(self):
        self.read_img()

    def stop(self):
        self._stop_event.set()

    def get_img(self):
        camera = Camera()
        try:
            camera.capture_image()
            camera.release()
            image_path = "image.jpg"
            image = cv2.imread(image_path)
            return image
        finally:
            camera.release()

    def read_img(self):
        self.ocr_processor.ocr_image(self.get_img())
        self.t2 = time.time()
        if self.ocr_processor.text != "":
            print(f"OCR用时: {self.t2-self.t1}")
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
            wavs = self.tts_processor.synthesiser(part, forward_params={"do_sample": True})
            output_path = f"tts/output_{i}.wav"
            soundfile.write(output_path, wavs["audio"][0], wavs["sampling_rate"])
            if i == 0:
                self.t2 = time.time()
                print(f"用户等待总时间: {self.t2-self.t1}")
                print("开始播放")

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
            audio = AudioSegment.from_file(output_path)
            audio.export(output_path, format="wav")
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

    def pause(self):
        self.paused = True

    def unpause(self):
        self.paused = False

    def stop(self):
        self._stop_event.set()


if __name__ == "__main__":
    t1 = time.time()
    ocr_processor = OCRProcessor()
    tts_processor = TTSProcessor()
    t2 = time.time()
    print(f"模型初始化时间：{t2-t1}")
    image_processing_thread = ImageProcessingThread(tts_processor, ocr_processor)
    audio_playback_thread = AudioPlaybackThread()

    image_processing_thread.start()
    audio_playback_thread.start()

    image_processing_thread.join()
    audio_playback_thread.join()
