import tkinter as tk
import Control

# from tkinter import messagebox
import sys
import os

os.chdir("/home/pill/smart-pill-box")
sys.path.append("/home/pill/smart-pill-box")
import box

font_button = ("song ti", 40)
font_title = ("song ti", 50)
font_label = ("song ti", 35)


class AddMedicine(tk.Frame):
    def __init__(self, master=None):
        super().__init__(master, height=600, width=1024, bg="white")
        self.master = master
        self.create_self()

    def create_self(self):
        tk.Label(self, text="药品添加", font=font_title, bg="white").place(x=512, y=60, anchor="center")
        tk.Button(
            self,
            text="扫描添加",
            font=font_button,
            bg="palegreen",
            command=self.add_by_photo,
        ).place(x=512, y=270, anchor="center")
        tk.Button(
            self,
            text="手动添加",
            font=font_button,
            bg="palegreen",
            command=self.manual_add,
        ).place(x=512, y=340, anchor="center")
        tk.Button(
            self,
            text="补充药品",
            font=font_button,
            bg="palegreen",
            command=self.add_by_box,
        ).place(x=512, y=410, anchor="center")
        tk.Button(
            self,
            text="返回",
            font=font_button,
            bg="palegreen",
            command=self.pack_forget,
        ).place(x=512, y=480, anchor="center")

    def add_by_photo(self):
        def Conf():
            id = Control.Medicine.FindBox()
            if id == None:
                # messagebox.showerror(
                #     title="错误",
                #     message="药盒已满",
                # )
                box.sysaudio("Add_Fail_BoxFull")
            else:
                times, dosage_per_time = box.add_medicine()
                if times == None or dosage_per_time == None:
                    # messagebox.showerror(
                    #     title="错误",
                    #     message="未识别到药品信息",
                    # )
                    box.sysaudio("Add_Fail_NotDetected")
                    return
                box.sysaudio("Add_Name")
                box.add_medicine_name(id)
                Control.AddMedicine(times, dosage_per_time, id)
                # messagebox.showinfo(
                #     title="提示",
                #     message=f"添加成功\n请将药品放入{id}号药盒",
                # )
                box.sysaudio(f"Add_{id}")
                box.get_pill_box(id)
            addmenu.destroy()

        addmenu = tk.Frame(self, height=600, width=1024, bg="white")
        tk.Label(addmenu, text="药品录入", font=font_title, bg="white").place(x=512, y=60, anchor="center")
        tk.Label(
            addmenu,
            text="请将说明书放置在摄像头处\n按下确定开始拍照",
            font=font_label,
            bg="white",
        ).place(x=512, y=330, anchor="center")
        tk.Button(
            addmenu,
            text="确定",
            font=font_button,
            bg="palegreen",
            command=Conf,
        ).place(x=350, y=480, anchor="center")
        tk.Button(
            addmenu,
            text="返回",
            font=font_button,
            bg="palegreen",
            command=addmenu.destroy,
        ).place(x=624, y=480, anchor="center")
        addmenu.pack()

    def manual_add(self):
        def Conf():
            id = Control.Medicine.FindBox()
            if id == None:
                # messagebox.showerror(
                #     title="错误",
                #     message="药盒已满",
                # )
                box.sysaudio("Add_Fail_BoxFull")
            else:
                box.sysaudio("Add_Name")
                box.add_medicine_name(id)
                Control.AddMedicine(times.get(), dosage_per_time.get(), id)
                # messagebox.showinfo(
                #     title="提示",
                #     message=f"添加成功\n请将药品放入{id}号药盒",
                # )
                box.sysaudio(f"Add_{id}")
                box.get_pill_box(id)
            addmenu.destroy()

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

        addmenu = tk.Frame(self, height=600, width=1024, bg="white")
        tk.Label(addmenu, text="药品录入", font=font_title, bg="white").place(x=512, y=60, anchor="center")
        times = tk.IntVar()
        dosage_per_time = tk.IntVar()
        tk.Label(addmenu, text="每日次数：", font=font_label, bg="white").place(x=256, y=280, anchor="center")
        tk.Label(addmenu, text="每次用量：", font=font_label, bg="white").place(x=256, y=380, anchor="center")
        times.set(1)
        dosage_per_time.set(1)
        times_label = tk.Label(
            addmenu,
            text="1",
            font=font_label,
            bg="white",
        )
        times_label.place(x=592, y=280, anchor="center")
        tk.Button(
            addmenu,
            text="-",
            font=font_button,
            bg="palegreen",
            command=times_minus,
        ).place(x=462, y=280, anchor="center")
        tk.Button(
            addmenu,
            text="+",
            font=font_button,
            bg="palegreen",
            command=times_plus,
        ).place(x=722, y=280, anchor="center")
        dosage_label = tk.Label(
            addmenu,
            text="1",
            font=font_label,
            bg="white",
        )
        dosage_label.place(x=592, y=380, anchor="center")
        tk.Button(
            addmenu,
            text="-",
            font=font_button,
            bg="palegreen",
            command=minus,
        ).place(x=462, y=380, anchor="center")
        tk.Button(
            addmenu,
            text="+",
            font=font_button,
            bg="palegreen",
            command=plus,
        ).place(x=722, y=380, anchor="center")
        tk.Button(
            addmenu,
            text="确认",
            font=font_button,
            bg="palegreen",
            command=Conf,
        ).place(x=400, y=500, anchor="center")
        tk.Button(
            addmenu,
            text="返回",
            font=font_button,
            bg="palegreen",
            command=addmenu.destroy,
        ).place(x=600, y=500, anchor="center")
        addmenu.pack()

    def add_by_box(self):
        def Conf():
            try:
                box.read_medicine_thread.stop()
                del box.read_medicine_thread
            finally:
                if Control.Medicine.MedicineList[id.get()] == None:
                    # messagebox.showerror(
                    #     title="错误",
                    #     message="该药盒尚未录入药品",
                    # )
                    box.sysaudio("Add_Fail_BoxEmpty")
                else:
                    box.sysaudio("Add_Again")
                    box.get_pill_box(id.get())
                addmenu.destroy()

        def Back():
            try:
                box.read_medicine_thread.stop()
                del box.read_medicine_thread
            finally:
                addmenu.destroy()

        addmenu = tk.Frame(self, height=600, width=1024, bg="white")
        tk.Label(addmenu, text="补充药品", font=font_title, bg="white").place(x=512, y=60, anchor="center")
        tk.Label(addmenu, text="您要向几号\n药盒补充药品", font=font_button, bg="white").place(x=256, y=320, anchor="center")
        id = tk.IntVar()
        tk.Radiobutton(
            addmenu,
            text="1",
            font=font_button,
            variable=id,
            value=1,
            bg="white",
        ).place(x=532, y=280, anchor="center")
        tk.Radiobutton(
            addmenu,
            text="2",
            font=font_button,
            variable=id,
            value=2,
            bg="white",
        ).place(x=652, y=280, anchor="center")
        tk.Radiobutton(
            addmenu,
            text="3",
            font=font_button,
            variable=id,
            value=3,
            bg="white",
        ).place(x=772, y=280, anchor="center")
        tk.Radiobutton(
            addmenu,
            text="4",
            font=font_button,
            variable=id,
            value=4,
            bg="white",
        ).place(x=532, y=360, anchor="center")
        tk.Radiobutton(
            addmenu,
            text="5",
            font=font_button,
            variable=id,
            value=5,
            bg="white",
        ).place(x=652, y=360, anchor="center")
        tk.Radiobutton(
            addmenu,
            text="6",
            font=font_button,
            variable=id,
            value=6,
            bg="white",
        ).place(x=772, y=360, anchor="center")
        id.set(1)
        tk.Button(
            addmenu,
            text="确认",
            font=font_button,
            bg="palegreen",
            command=Conf,
        ).place(x=400, y=480, anchor="center")
        tk.Button(
            addmenu,
            text="返回",
            font=font_button,
            bg="palegreen",
            command=Back,
        ).place(x=624, y=480, anchor="center")
        addmenu.update_idletasks()
        id_list = []
        for i in range(1, 7):
            if Control.Medicine.MedicineList[i] != None:
                id_list.append(i)
        if id_list == []:
            # messagebox.showerror(
            #     title="错误",
            #     message="所有药盒均为空",
            # )
            box.sysaudio("Empty_Error")
            addmenu.destroy()
        else:
            addmenu.pack()
            box.read_medicine(id_list)
