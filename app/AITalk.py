import tkinter as tk
import os
import sys

os.chdir("/home/pill/smart-pill-box")
sys.path.append("/home/pill/smart-pill-box")
import box

os.chdir("/home/pill/smart-pill-box")
font_button = ("song ti", 40)
font_title = ("song ti", 50)


class AITalk(tk.Frame):
    def __init__(self, master=None):
        super().__init__(master, height=600, width=1024, bg="white")
        self.master = master
        self.create_self()

    def create_self(self):
        tk.Label(self, text="AI聊天", font=font_title, bg="white").place(
            x=512, y=60, anchor="center"
        )
        tk.Button(
            self,
            text="开始聊天",
            font=font_button,
            bg="palegreen",
            command=box.chat_bot,
        ).place(x=512, y=280, anchor="center")
        tk.Button(
            self,
            text="结束聊天",
            font=font_button,
            bg="palegreen",
            command=self.end_chat,
        ).place(x=512, y=380, anchor="center")

    def end_chat(self):
        try:
            box.chat_bot_thread.stop()
        except:
            pass
        self.pack_forget()
