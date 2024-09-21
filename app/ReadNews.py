import tkinter as tk

# from tkinter import messagebox
import time
import sys
import os

os.chdir("/home/pill/smart-pill-box")
sys.path.append("/home/pill/smart-pill-box")
import box

font_button = ("song ti", 40)
font_title = ("song ti", 50)
font_label = ("song ti", 35)


class ReadNews(tk.Frame):
    def __init__(self, master=None):
        super().__init__(master, height=600, width=1024, bg="white")
        self.master = master
        self.create_self()

    def create_self(self):
        tk.Label(self, text="报纸阅读", font=font_title, bg="white").place(x=512, y=60, anchor="center")
        tk.Label(
            self,
            text="请将报纸或书籍放置在摄像头处\n点击拍照按钮，识别后可点击开始",
            font=font_label,
            bg="white",
        ).place(x=512, y=280, anchor="center")
        tk.Button(
            self,
            text="拍照",
            font=font_button,
            bg="palegreen",
            command=self.read_page,
        ).place(x=512, y=400, anchor="center")
        tk.Button(
            self,
            text="返回",
            font=font_button,
            bg="palegreen",
            command=self.pack_forget,
        ).place(x=512, y=500, anchor="center")

    def read_page(self):
        def return_to_photo():
            box.audio_playback_thread.stop()
            box.image_processing_thread.stop()
            del box.audio_playback_thread
            del box.image_processing_thread
            f.destroy()

        box.read_news()
        while box.ocr_processor.text == None:
            time.sleep(1)
        if box.ocr_processor.text == "":
            # messagebox.showerror("错误", "识别失败\n请重新拍照")
            box.sysaudio("Read_PhotoAgain")
            box.audio_playback_thread.stop()
            box.image_processing_thread.stop()
            del box.audio_playback_thread
            del box.image_processing_thread
            return
        f = tk.Frame(self, background="white", height=600, width=1024)
        tk.Label(f, text="报纸阅读", font=font_title, bg="white").place(x=512, y=60, anchor="center")
        tk.Button(
            f,
            text="开始",
            font=font_button,
            bg="palegreen",
            command=box.audio_playback_thread.unpause,
        ).place(x=400, y=300, anchor="center")
        tk.Button(
            f,
            text="暂停",
            font=font_button,
            bg="palegreen",
            command=box.audio_playback_thread.pause,
        ).place(x=624, y=300, anchor="center")
        tk.Button(
            f,
            text="返回",
            font=font_button,
            bg="palegreen",
            command=return_to_photo,
        ).place(x=512, y=450, anchor="center")
        f.pack()
