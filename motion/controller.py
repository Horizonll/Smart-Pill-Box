import time
import getch
import serial


def controller(id, para):
    try:
        ser = serial.Serial("/dev/ttyCH341USB0", 9600, timeout=0.1)
        # if id==5:
        #     ser.write(bytes(f"{id} {para+500}\n", encoding="utf-8"))
        #     print("id: %d, angle: %i" % (id, para))
        #     time.sleep(1)
        ser.write(bytes(f"{id} {para}\n", encoding="utf-8"))
        print("id: %d, angle: %i" % (id, para))
    finally:
        ser.close()
        if id == 1 or id == 2:
            time.sleep(abs(para) / 1000 + 0.2)
        elif id == 3:
            time.sleep(0.5)
        else:
            time.sleep(2)


def check():
    ser = serial.Serial("/dev/ttyCH341USB0", 9600, timeout=0.1)
    cnt = 0
    while True:
        try:
            data = ser.read()
            if data == b"1":
                cnt += 1
            elif data == b"0":
                cnt -= 1
            if cnt >= 5:
                ser.close()
                return True
            elif cnt <= -5:
                ser.close()
                return False
            time.sleep(0.1)
        except:
            pass


param = [650, 980, 1320, 1650, 1990, 2330]
p = 1320
if __name__ == "__main__":
    while True:
        check()


# 5
# 1盒
# 2泵
# 3继电器
# 4重启
