from paddleocr import PaddleOCR
import re
import cv2
import os
import sys

os.chdir("/home/pill/smart-pill-box")
sys.path.append("/home/pill/smart-pill-box")
from camera.camera import Camera


class OCRProcessor:
    def __init__(self):
        self.model = PaddleOCR(
            use_angle_cls=True,
            lang="ch",
            show_log=False,
            # use_tensorrt=True,
            # ir_optim=True,
        )

    def find_last_number_between_patterns(self, text, start_pattern, end_pattern):
        pattern = re.compile(f"{re.escape(start_pattern)}(.*?)({re.escape(end_pattern)})")
        match = pattern.search(text)
        if match:
            number_pattern = re.compile(r"\d+")
            numbers = number_pattern.findall(match.group(1))
            if numbers:
                return int(numbers[-1])
        return None

    def find_text_between_patterns(self, text, start_pattern, end_pattern):
        pattern = re.compile(f"{re.escape(start_pattern)}(.*?)({re.escape(end_pattern)})", re.DOTALL)
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


if __name__ == "__main__":
    ocr_processor = OCRProcessor()
    camera = Camera()
    camera.capture_image()
    image_path = "image.jpg"
    image = cv2.imread(image_path)
    ocr_processor.ocr_image(image)
    print(ocr_processor.text)
    ocr_processor.get_dosage(image)
    if ocr_processor.dosage_per_day is not None:
        print(f"一日{ocr_processor.dosage_per_day}次")
        if ocr_processor.dosage_per_time is not None:
            print(f"一次{ocr_processor.dosage_per_time}片")
        else:
            print("未能提取到用法用量信息")
    else:
        print("未能提取到用法用量信息")
