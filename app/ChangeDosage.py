import tkinter as tk
import Control

# from tkinter import messagebox
import os
import sys

os.chdir("/home/pill/smart-pill-box")
sys.path.append("/home/pill/smart-pill-box")
import box

font_button = ("song ti", 40)
font_title = ("song ti", 50)
font_label = ("song ti", 35)


class ChangeDosage(tk.Frame):
    def __init__(self, master=None):
        super().__init__(master, height=600, width=1024, bg="white")
        self.master = master
        self.create_self()

    def create_self(self):
        tk.Label(self, text="修改用量", font=font_title, bg="white").place(x=512, y=60, anchor="center")
        tk.Label(self, text="您要修改几号\n药盒的用法用量", font=font_button, bg="white").place(x=256, y=320, anchor="center")
        self.MediceToChange = tk.IntVar()
        tk.Radiobutton(
            self,
            text="1",
            font=font_button,
            variable=self.MediceToChange,
            value=1,
            bg="white",
        ).place(x=532, y=280, anchor="center")
        tk.Radiobutton(
            self,
            text="2",
            font=font_button,
            variable=self.MediceToChange,
            value=2,
            bg="white",
        ).place(x=652, y=280, anchor="center")
        tk.Radiobutton(
            self,
            text="3",
            font=font_button,
            variable=self.MediceToChange,
            value=3,
            bg="white",
        ).place(x=772, y=280, anchor="center")
        tk.Radiobutton(
            self,
            text="4",
            font=font_button,
            variable=self.MediceToChange,
            value=4,
            bg="white",
        ).place(x=532, y=360, anchor="center")
        tk.Radiobutton(
            self,
            text="5",
            font=font_button,
            variable=self.MediceToChange,
            value=5,
            bg="white",
        ).place(x=652, y=360, anchor="center")
        tk.Radiobutton(
            self,
            text="6",
            font=font_button,
            variable=self.MediceToChange,
            value=6,
            bg="white",
        ).place(x=772, y=360, anchor="center")
        self.MediceToChange.set(1)
        tk.Button(
            self,
            text="确认",
            font=font_button,
            bg="palegreen",
            command=self.Conf,
        ).place(x=400, y=480, anchor="center")
        tk.Button(
            self,
            text="返回",
            font=font_button,
            bg="palegreen",
            command=self.Back,
        ).place(x=624, y=480, anchor="center")

    def Conf(self):
        try:
            box.read_medicine_thread.stop()
            del box.read_medicine_thread
        finally:
            if Control.Medicine.MedicineList[self.MediceToChange.get()] == None:
                # messagebox.showerror("错误", "您还没有录入这个药盒")
                box.sysaudio("Change_Fail_BoxEmpty")
                return
            else:
                self.change_dosage()
                return

    def change_dosage(self):
        def Conf():
            Medicine.times = times.get()
            Medicine.dosage_per_time = dosage_per_time.get()
            Control.SaveMedicineList()
            # messagebox.showinfo("提示", "修改成功")
            box.sysaudio("Change_Success")
            changepage.destroy()

        def plus():
            dosage_per_time.set(dosage_per_time.get() + 1)
            dosage_label.config(text=str(dosage_per_time.get()))

        def minus():
            if dosage_per_time.get() > 1:
                dosage_per_time.set(dosage_per_time.get() - 1)
                dosage_label.config(text=str(dosage_per_time.get()))

        def times_plus():
            times.set(times.get() + 1)
            times_label.config(text=str(times.get()))

        def times_minus():
            if times.get() > 1:
                times.set(times.get() - 1)
                times_label.config(text=str(times.get()))

        changepage = tk.Frame(self, height=600, width=1024, bg="white")
        tk.Label(changepage, text="修改用量", font=font_title, bg="white").place(x=512, y=60, anchor="center")
        Medicine = Control.Medicine.MedicineList[self.MediceToChange.get()]
        tk.Label(
            changepage,
            text=f"目前用量：每天{Medicine.times}次，每次{Medicine.dosage_per_time}片/粒",
            font=font_button,
            bg="white",
        ).place(x=512, y=250, anchor="center")
        times = tk.IntVar()
        dosage_per_time = tk.IntVar()
        tk.Label(
            changepage,
            text="每日次数改为：",
            font=font_button,
            bg="white",
        ).place(x=256, y=330, anchor="center")
        tk.Label(
            changepage,
            text="每次用量改为：",
            font=font_button,
            bg="white",
        ).place(x=256, y=400, anchor="center")
        times.set(1)
        dosage_per_time.set(1)
        times_label = tk.Label(
            changepage,
            text="1",
            font=font_label,
            bg="white",
        )
        times_label.place(x=592, y=330, anchor="center")
        tk.Button(
            changepage,
            text="-",
            font=font_button,
            bg="palegreen",
            command=times_minus,
        ).place(x=462, y=330, anchor="center")
        tk.Button(
            changepage,
            text="+",
            font=font_button,
            bg="palegreen",
            command=times_plus,
        ).place(x=722, y=330, anchor="center")
        dosage_label = tk.Label(
            changepage,
            text="1",
            font=font_label,
            bg="white",
        )
        dosage_label.place(x=592, y=400, anchor="center")
        tk.Button(
            changepage,
            text="-",
            font=font_button,
            bg="palegreen",
            command=minus,
        ).place(x=462, y=400, anchor="center")
        tk.Button(
            changepage,
            text="+",
            font=font_button,
            bg="palegreen",
            command=plus,
        ).place(x=722, y=400, anchor="center")
        tk.Button(changepage, text="确认", font=font_button, bg="palegreen", command=Conf).place(x=400, y=480, anchor="center")
        tk.Button(
            changepage,
            text="返回",
            font=font_button,
            bg="palegreen",
            command=changepage.destroy,
        ).place(x=624, y=480, anchor="center")
        changepage.pack()

    def Back(self):
        try:
            box.read_medicine_thread.stop()
            del box.read_medicine_thread
        finally:
            self.destroy()
