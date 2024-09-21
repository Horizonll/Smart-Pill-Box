import pickle
import os
from datetime import datetime
import time
from tkinter import messagebox
import sys

os.chdir("/home/pill/smart-pill-box")
sys.path.append("/home/pill/smart-pill-box")
import box


class Medicine:
    NumOfBoxes = 6
    MedicineList = [None] * (NumOfBoxes + 1)

    def __init__(self, times, dosage_per_time, id):
        self.times = times
        self.dosage_per_time = dosage_per_time
        self.id = id
        self.time_list = Get_Time(times)

    @classmethod
    def FindBox(cls):
        for i in range(1, cls.NumOfBoxes + 1):
            if cls.MedicineList[i] == None:
                return i
        return None


def LoadMedicineList():
    os.chdir(os.path.dirname(__file__))
    try:
        with open("MedicineList.pkl", "rb") as f:
            Medicine.MedicineList = pickle.load(f)
    except FileNotFoundError:
        pass


def SaveMedicineList():
    os.chdir(os.path.dirname(__file__))
    with open("MedicineList.pkl", "wb") as f:
        pickle.dump(Medicine.MedicineList, f)


def AddMedicine(times, dosage_per_time, id):
    if Medicine.FindBox == None:
        messagebox.showerror(
            title="错误",
            message="药盒已满",
        )
    else:
        Medicine.MedicineList[id] = Medicine(times, dosage_per_time, id)
        SaveMedicineList()


def Get_Time(times):
    total_time = 12 * 60
    time_list = []
    if times > 1:
        interval = total_time / (times - 1)
        for i in range(times):
            time = interval * i
            hour = time // 60 + 8
            minute = round(time % 60)
            if minute == 60:
                hour += 1
                minute = 0
            if hour < 10:
                hour = "0" + str(hour)
            if minute < 10:
                minute = "0" + str(minute)
            time_list.append(f"{hour}:{minute}")
    else:
        time_list.append("12:00")
    return time_list


def WhenControl():
    while True:
        current_time = datetime.now()
        time_str = current_time.strftime("%H:%M")
        flag = False
        for medicine in Medicine.MedicineList:
            if medicine == None:
                continue
            else:
                if time_str in medicine.time_list:
                    flag = True
                    print(f"Time to take medicine {medicine.id}")
                    box.get_pill(medicine.id, medicine.dosage_per_time)
        if not flag:
            time.sleep(30)
        else:
            time.sleep(60)
