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


class DeleteMedicine(tk.Frame):
    def __init__(self, master=None):
        super().__init__(master, height=600, width=1024, bg="white")
        self.master = master
        self.create_self()

    def create_self(self):
        tk.Label(self, text="删除药品", font=font_title, bg="white").place(x=512, y=60, anchor="center")
        tk.Label(self, text="您要删除几号\n药盒的药品", font=font_button, bg="white").place(x=256, y=320, anchor="center")
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
            text="删除",
            font=font_button,
            bg="palegreen",
            command=self.delete_medicine,
        ).place(x=400, y=480, anchor="center")
        tk.Button(
            self,
            text="返回",
            font=font_button,
            bg="palegreen",
            command=self.Back,
        ).place(x=624, y=480, anchor="center")

    def delete_medicine(self):
        try:
            box.read_medicine_thread.stop()
            del box.read_medicine_thread
        except Exception as e:
            print(f"Exception occurred: {e}")
        finally:
            if Control.Medicine.MedicineList[self.MediceToChange.get()] == None:
                box.sysaudio("Delete_Fail_NoMedicine")
            else:
                Control.Medicine.MedicineList[self.MediceToChange.get()] = None
                box.sysaudio(f"Delete_Remove_{self.MediceToChange.get()}")
                Control.SaveMedicineList()
                box.get_pill_box(self.MediceToChange.get())
            self.destroy()

    def Back(self):
        try:
            box.read_medicine_thread.stop()
            del box.read_medicine_thread
        finally:
            self.destroy()
