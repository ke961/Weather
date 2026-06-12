from datetime import datetime
from logging import root
from tkinter import Label, Tk
from zoneinfo import ZoneInfo
import time
import threading
import requests



#for the sound of alarm
try:
    from pygame import mixer
    mixer.init()
    sound_available = True

except:
    sound_available = False



#for the window
root = Tk()
root.title("Smart Weather App")
root.geometry("15000x9000")
root.configure(bg="#2596be")


#for the title
title_label = Label(root, text="Current Time in Different Cities",
                     font=("Helvetica", 16)).pack(pady=10)



# Get current time in different cities
Dhaka_label = Label(root, text="Dhaka Time", font=("Helvetica", 12))
Dhaka_label.pack(pady=5)

Busan_label = Label(root, text="Busan Time", font=("Helvetica", 12))
Busan_label.pack(pady=5)

Tokyo_label = Label(root, text="Tokyo Time", font=("Helvetica", 12))
Tokyo_label.pack(pady=5)

Seoul_label = Label(root, text="Seoul Time", font=("Helvetica", 12))
Seoul_label.pack(pady=5)

Shenzhen_label = Label(root, text="Shenzhen Time", font=("Helvetica", 12))
Shenzhen_label.pack(pady=5)

def update_time():
    Dhaka_time = datetime.now(ZoneInfo("Asia/Dhaka")).strftime("%Y-%m-%d %H:%M:%S")
    Busan_time = datetime.now(ZoneInfo("Asia/Seoul")).strftime("%Y-%m-%d %H:%M:%S")
    Tokyo_time = datetime.now(ZoneInfo("Asia/Tokyo")).strftime("%Y-%m-%d %H:%M:%S")
    Seoul_time = datetime.now(ZoneInfo("Asia/Seoul")).strftime("%Y-%m-%d %H:%M:%S")
    Shenzhen_time = datetime.now(ZoneInfo("Asia/Shanghai")).strftime("%Y-%m-%d %H:%M:%S")

    Dhaka_label.config(text=f"Dhaka Time: {Dhaka_time}")
    Busan_label.config(text=f"Busan Time: {Busan_time}")
    Tokyo_label.config(text=f"Tokyo Time: {Tokyo_time}")
    Seoul_label.config(text=f"Seoul Time: {Seoul_time}")
    Shenzhen_label.config(text=f"Shenzhen Time: {Shenzhen_time}")

    root.after(1000, update_time)  # Update every second

update_time()  # Initial call to start the time updates
time.sleep(3)  # Sleep for a short time to allow the window to initialize
root.mainloop()



