import tkinter as tk

# from tkinter import messagebox
import sys
import os

os.chdir("/home/pill/smart-pill-box")
sys.path.append("/home/pill/smart-pill-box")
import box

font_button = ("song ti", 40)
font_title = ("song ti", 50)
font_label = ("song ti", 35)
font_list = ("song ti", 30)


class PlayAudio(tk.Frame):
    def __init__(self, master=None):
        super().__init__(master, height=600, width=1024, bg="white")
        self.master = master
        self.f = tk.Frame(self.master, width=1024, height=600, bg="white")
        self.plane = tk.Frame(self.f, width=624, height=460, bg="white")
        self.plane.pack_propagate(False)
        self.create_self()
        self.reset()

    def create_self(self):
        tk.Label(self, text="播放音频", font=font_title, bg="white").place(
            x=512, y=60, anchor="center"
        )
        tk.Button(
            self,
            text="导入音频",
            font=font_button,
            bg="palegreen",
            command=self.add_audio,
        ).place(x=350, y=280, anchor="center")
        tk.Button(
            self,
            text="播放音频",
            font=font_button,
            bg="palegreen",
            command=self.play_audio,
        ).place(x=674, y=280, anchor="center")
        tk.Button(
            self,
            text="删除音频",
            font=font_button,
            bg="palegreen",
            command=self.delete_audio,
        ).place(x=350, y=380, anchor="center")
        tk.Button(
            self,
            text="返回",
            font=font_button,
            bg="palegreen",
            command=self.pack_forget,
        ).place(x=674, y=380, anchor="center")

    def add_audio(self):
        def Conf():
            list_out = []
            for key in self.files_chosen:
                if self.files_chosen[key].get() == 1:
                    list_out.append(key)
            box.copy_audio_file(list_out)
            # messagebox.showinfo("提示", "音频导入成功")
            box.sysaudio("Play_AddSuccess")
            self.Return()

        self.reset()
        self.audio_files = box.get_audio_files()
        if len(self.audio_files) == 0:
            # messagebox.showinfo("提示", "未找到音频文件")
            box.sysaudio("Play_FileNotFound")
            return
        self.pack_forget()
        self.master.pause_time()
        self.audio_files_split = self.split_list(self.audio_files, 10)
        self.files_chosen = {}
        for file in self.audio_files:
            self.files_chosen[file] = tk.IntVar()
        self.show_page(self.index_current)
        tk.Button(
            self.f,
            text="确认",
            font=font_button,
            bg="palegreen",
            command=Conf,
        ).place(x=400, y=460, anchor="n")
        tk.Button(
            self.f,
            text="返回",
            font=font_button,
            bg="palegreen",
            command=self.Return,
        ).place(x=624, y=460, anchor="n")
        tk.Button(
            self.f,
            text="↑",
            font=font_button,
            bg="palegreen",
            command=self.up,
        ).place(x=800, y=150, anchor="center")
        tk.Button(
            self.f,
            text="↓",
            font=font_button,
            bg="palegreen",
            command=self.down,
        ).place(x=800, y=250, anchor="center")
        self.plane.place(x=100, y=0, anchor="nw")
        self.f.pack()
        self.f.lift()

    def play_audio(self):
        def Conf():
            def Back():
                box.audio_play_thread.stop()
                del box.audio_play_thread
                frame.destroy()

            frame = tk.Frame(self.f, width=1024, height=600, bg="white")
            box.play_audio(self.file_chosen.get())
            tk.Label(
                frame,
                text=self.file_chosen.get(),
                font=font_title,
                bg="white",
            ).place(x=512, y=120, anchor="center")
            tk.Button(
                frame,
                text="开始",
                font=font_button,
                bg="palegreen",
                command=box.audio_play_thread.unpause,
            ).place(x=312, y=350, anchor="center")
            tk.Button(
                frame,
                text="暂停",
                font=font_button,
                bg="palegreen",
                command=box.audio_play_thread.pause,
            ).place(x=512, y=350, anchor="center")
            tk.Button(
                frame,
                text="返回",
                font=font_button,
                bg="palegreen",
                command=Back,
            ).place(x=712, y=350, anchor="center")
            frame.pack()

        self.reset()
        if len(self.audio_files) == 0:
            # messagebox.showinfo("提示", "未找到音频文件")
            box.sysaudio("Play_FileNotFound")
            return
        self.pack_forget()
        self.master.pause_time()
        self.type = 1
        self.show_page(self.index_current)
        tk.Button(
            self.f,
            text="选择",
            font=font_button,
            bg="palegreen",
            command=Conf,
        ).place(x=400, y=460, anchor="n")
        tk.Button(
            self.f,
            text="返回",
            font=font_button,
            bg="palegreen",
            command=self.Return,
        ).place(x=624, y=460, anchor="n")
        tk.Button(
            self.f,
            text="↑",
            font=font_button,
            bg="palegreen",
            command=self.up,
        ).place(x=800, y=150, anchor="center")
        tk.Button(
            self.f,
            text="↓",
            font=font_button,
            bg="palegreen",
            command=self.down,
        ).place(x=800, y=250, anchor="center")
        self.plane.place(x=100, y=0, anchor="nw")
        self.f.pack()
        self.f.lift()

    def delete_audio(self):
        def Conf():
            list_out = []
            for key in self.files_chosen:
                if self.files_chosen[key].get() == 1:
                    list_out.append(key)
            box.delete_audio_file(list_out)
            # messagebox.showinfo("提示", "音频删除成功")
            box.sysaudio("Play_DeleteSuccess")
            self.Return()

        self.reset()
        if len(self.audio_files) == 0:
            # messagebox.showinfo("提示", "未找到音频文件")
            box.sysaudio("Play_FileNotFound")
            return
        self.pack_forget()
        self.master.pause_time()
        self.show_page(self.index_current)
        tk.Button(
            self.f,
            text="删除",
            font=font_button,
            bg="palegreen",
            command=Conf,
        ).place(x=400, y=460, anchor="n")
        tk.Button(
            self.f,
            text="返回",
            font=font_button,
            bg="palegreen",
            command=self.Return,
        ).place(x=624, y=460, anchor="n")
        tk.Button(
            self.f,
            text="↑",
            font=font_button,
            bg="palegreen",
            command=self.up,
        ).place(x=800, y=150, anchor="center")
        tk.Button(
            self.f,
            text="↓",
            font=font_button,
            bg="palegreen",
            command=self.down,
        ).place(x=800, y=250, anchor="center")
        self.plane.place(x=100, y=0, anchor="nw")
        self.f.pack()
        self.f.lift()

    def split_list(self, lst, group_size):
        return [lst[i : i + group_size] for i in range(0, len(lst), group_size)]

    def reset(self):
        os.chdir("/home/pill/smart-pill-box")
        self.index_current = 0
        self.type = 0
        self.file_chosen = tk.StringVar()
        directory = "audio"
        files_in_directory = os.listdir(directory)
        self.audio_files = [
            file
            for file in files_in_directory
            if os.path.isfile(os.path.join(directory, file))
        ]
        self.audio_files_split = self.split_list(self.audio_files, 10)
        self.files_chosen = {}
        for file in self.audio_files:
            self.files_chosen[file] = tk.IntVar()

    def up(self):
        if self.index_current > 0:
            self.index_current -= 1
            self.show_page(self.index_current)

    def down(self):
        if self.index_current < len(self.audio_files_split) - 1:
            self.index_current += 1
            self.show_page(self.index_current)

    def show_page(self, index):
        for widget in self.plane.winfo_children():
            widget.destroy()
        if self.type == 0:
            for file in self.audio_files_split[index]:
                tk.Checkbutton(
                    self.plane,
                    text=file,
                    font=font_list,
                    bg="white",
                    anchor="w",
                    variable=self.files_chosen[file],
                    onvalue=1,
                    offvalue=0,
                ).pack(side="top", fill="x")
        else:
            for file in self.audio_files_split[index]:
                tk.Radiobutton(
                    self.plane,
                    text=file,
                    font=font_list,
                    bg="white",
                    anchor="w",
                    variable=self.file_chosen,
                    value=file,
                ).pack(side="top", fill="x")
            self.file_chosen.set(self.audio_files_split[index][0])

    def Return(self):
        self.f.pack_forget()
        self.master.resume_time()
        self.pack()
