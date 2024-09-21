import tkinter as tk
from datetime import datetime
import AddMedicine
import ReadNews
import AITalk
import ChangeDosage
import DeleteMedicine
import PlayAudio
from threading import Thread
import threading
import time
import Control
import sys
import os

os.chdir("/home/pill/smart-pill-box")
sys.path.append("/home/pill/smart-pill-box")
import box

font_button = ("song ti", 40)
font_title = ("song ti", 50)
font_time = ("song ti", 60)


class MainMenu(tk.Frame):
    def __init__(self, master=None):
        super().__init__(master, height=600, width=1024, bg="white")
        self.master = master
        self.create_self()
        Control.LoadMedicineList()
        box._init()
        Thread(target=Control.WhenControl, daemon=True).start()
        self.create_pages()
        self.pack()
        self.pause_event = threading.Event()
        self.pause_event.set()
        Thread(target=self.show_time, daemon=True).start()

    def create_self(self):
        tk.Button(self, text="         ", font=font_title, bg="white", command=self.demo).place(x=512, y=60, anchor="center")
        tk.Label(self, text="智能药盒", font=font_title, bg="white").place(x=512, y=60, anchor="center")
        tk.Button(
            self,
            text="药品添加",
            font=font_button,
            bg="palegreen",
            command=self.add_medicine,
        ).place(x=350, y=280, anchor="center")
        tk.Button(
            self,
            text="修改用量",
            font=font_button,
            bg="palegreen",
            command=self.change_dosage,
        ).place(x=350, y=380, anchor="center")
        tk.Button(
            self,
            text="删除药品",
            font=font_button,
            bg="palegreen",
            command=self.delete_medicine,
        ).place(x=350, y=480, anchor="center")
        tk.Button(
            self,
            text="报纸阅读",
            font=font_button,
            bg="palegreen",
            command=self.read_news,
        ).place(x=674, y=280, anchor="center")
        tk.Button(
            self,
            text="音频播放",
            font=font_button,
            bg="palegreen",
            command=self.play_audio,
        ).place(x=674, y=380, anchor="center")
        tk.Button(
            self,
            text="AI聊天",
            font=font_button,
            bg="palegreen",
            command=self.ai_talk,
        ).place(x=674, y=480, anchor="center")

    def pause_time(self):
        self.pause_event.clear()

    def resume_time(self):
        self.pause_event.set()

    def show_time(self):
        self.l1 = tk.Label(self)
        self.l2 = tk.Label(self)
        while True:
            self.pause_event.wait()
            current_time = datetime.now()
            self.time_str = current_time.strftime("%Y-%m-%d %H:%M")
            self.l2 = tk.Label(self, text=self.time_str, font=font_time, bg="white")
            self.l2.place(x=512, y=160, anchor="center")
            time.sleep(0.2)
            self.l1.destroy()
            self.l1 = self.l2

    def create_pages(self):
        self.add_medicine_page = AddMedicine.AddMedicine(self)
        self.read_news_page = ReadNews.ReadNews(self)
        self.ai_talk_page = AITalk.AITalk(self)
        self.play_audio_page = PlayAudio.PlayAudio(self)

    def add_medicine(self):
        self.add_medicine_page.pack()

    def read_news(self):
        self.read_news_page.pack()

    def ai_talk(self):
        self.ai_talk_page.pack()

    def change_dosage(self):
        id_list = []
        for id in range(1, 7):
            if Control.Medicine.MedicineList[id] != None:
                id_list.append(id)
        if id_list == []:
            box.sysaudio("Empty_Error")
        else:
            self.change_dosage_page = ChangeDosage.ChangeDosage(self)
            self.change_dosage_page.pack()
            self.change_dosage_page.update_idletasks()
            box.read_medicine(id_list)

    def delete_medicine(self):
        id_list = []
        for id in range(1, 7):
            if Control.Medicine.MedicineList[id] != None:
                id_list.append(id)
        if id_list == []:
            box.sysaudio("Empty_Error")
        else:
            self.delete_medicine_page = DeleteMedicine.DeleteMedicine(self)
            self.delete_medicine_page.pack()
            self.delete_medicine_page.update_idletasks()
            box.read_medicine(id_list)

    def play_audio(self):
        self.play_audio_page.pack()

    def demo(self):
        def get_pill():
            if Control.Medicine.MedicineList[self.MediceToChange.get()] == None:
                box.sysaudio("Delete_Fail_NoMedicine")
            else:
                box.get_pill(self.MediceToChange.get(), 1)
            f.destroy()

        f = tk.Frame(self, height=600, width=1024, bg="white")
        tk.Label(f, text="出药演示", font=font_title, bg="white").place(x=512, y=60, anchor="center")
        tk.Label(f, text="您要取出几号\n药盒的药品", font=font_button, bg="white").place(x=256, y=320, anchor="center")
        self.MediceToChange = tk.IntVar()
        tk.Radiobutton(
            f,
            text="1",
            font=font_button,
            variable=self.MediceToChange,
            value=1,
            bg="white",
        ).place(x=532, y=280, anchor="center")
        tk.Radiobutton(
            f,
            text="2",
            font=font_button,
            variable=self.MediceToChange,
            value=2,
            bg="white",
        ).place(x=652, y=280, anchor="center")
        tk.Radiobutton(
            f,
            text="3",
            font=font_button,
            variable=self.MediceToChange,
            value=3,
            bg="white",
        ).place(x=772, y=280, anchor="center")
        tk.Radiobutton(
            f,
            text="4",
            font=font_button,
            variable=self.MediceToChange,
            value=4,
            bg="white",
        ).place(x=532, y=360, anchor="center")
        tk.Radiobutton(
            f,
            text="5",
            font=font_button,
            variable=self.MediceToChange,
            value=5,
            bg="white",
        ).place(x=652, y=360, anchor="center")
        tk.Radiobutton(
            f,
            text="6",
            font=font_button,
            variable=self.MediceToChange,
            value=6,
            bg="white",
        ).place(x=772, y=360, anchor="center")
        self.MediceToChange.set(1)
        tk.Button(
            f,
            text="取药",
            font=font_button,
            bg="palegreen",
            command=get_pill,
        ).place(x=400, y=480, anchor="center")
        tk.Button(
            f,
            text="返回",
            font=font_button,
            bg="palegreen",
            command=f.destroy,
        ).place(x=624, y=480, anchor="center")
        f.pack()
