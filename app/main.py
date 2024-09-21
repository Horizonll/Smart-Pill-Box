import tkinter as tk
from MainMenu import *
import os

os.chdir("/home/pill/smart-pill-box")

root = tk.Tk()
root.title("智能药盒")
root.geometry("1024x600")
MainMenu(root)
root.mainloop()
