from tkinter import *
from tkcalendar import Calendar
from datetime import datetime
from zoneinfo import ZoneInfo
import requests
import threading


# Weather Display
Dhaka = datetime.now(ZoneInfo('Asia/Dhaka'))
Busan = datetime.now(ZoneInfo('Asia/Busan'))
Tokyo = datetime.now(ZoneInfo('Asia/Tokyo'))
Seoul = datetime.now(ZoneInfo('Asia/Seoul'))
Shenzhen = datetime.now(ZoneInfo('Asia/Shenzhen'))


print("Dhaka:", Dhaka.strftime("%Y-%m-%d %H:%M:%S"))
print("Busan:", Busan.strftime("%Y-%m-%d %H:%M:%S"))
print("Tokyo:", Tokyo.strftime("%Y-%m-%d %H:%M:%S"))
print("Seoul:", Seoul.strftime("%Y-%m-%d %H:%M:%S"))
print("Shenzhen:", Shenzhen.strftime("%Y-%m-%d %H:%M:%S"))
