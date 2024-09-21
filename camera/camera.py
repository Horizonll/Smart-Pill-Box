import cv2
import os, time
import pygame


class Camera:
    def __init__(self, width=2304, height=1296):
        """
        初始化摄像头，设置分辨率。
        :param width: 图像宽度
        :param height: 图像高度
        """
        self.cap = cv2.VideoCapture(0)
        if not self.cap.isOpened():
            raise IOError("Cannot open webcam")
        self.cap.set(cv2.CAP_PROP_FRAME_WIDTH, width)
        self.cap.set(cv2.CAP_PROP_FRAME_HEIGHT, height)

    def capture_image(self, file_name="image.jpg"):
        """
        捕获图像并保存到指定文件。
        :param file_name: 保存的文件名
        """
        os.chdir("/home/pill/smart-pill-box")
        os.system("rm image.jpg")
        print("正在拍照")
        t = time.time()
        while time.time() - t < 2:
            self.cap.read()
        ret, frame = self.cap.read()

        if not ret:
            print("拍照失败")
            return
        self.cap.release()
        cv2.imwrite(file_name, frame)
        print(f"照片已保存为 {file_name}")
        pygame.mixer.init()
        pygame.mixer.music.load("camera/camera_finish.wav")
        pygame.mixer.music.play()
        while pygame.mixer.music.get_busy():
            continue


if __name__ == "__main__":
    try:
        camera = Camera()
        camera.capture_image()
    except Exception as e:
        print(f"发生错误: {e}")
