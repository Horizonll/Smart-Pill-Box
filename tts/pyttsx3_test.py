# sudo apt-get install espeak
import sys
import os
import pyttsx3
import cv2

os.chdir("/home/pill/smart-pill-box")
sys.path.append("/home/pill/smart-pill-box")
from ocr.paddleocr_test import OCRProcessor


class TTSProcessor(OCRProcessor):
    def __init__(self):
        super().__init__()
        self.engine = pyttsx3.init(driverName="espeak")
        self.engine.setProperty("rate", 150)
        self.engine.setProperty("volume", 1)
        self.engine.setProperty("voice", "zh")

    def speak(self, text):
        self.engine.say(text)
        self.engine.runAndWait()

    def read_img(self, img):
        self.ocr_image(img)
        self.speak(self.text)


if __name__ == "__main__":
    tts_processor = TTSProcessor()
    image_path = "tts/2.jpeg"
    image = cv2.imread(image_path)
    tts_processor.read_img(image)
    print(tts_processor.text)
