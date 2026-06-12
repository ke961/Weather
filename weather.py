from datetime import datetime
from tkinter import LEFT, Frame, Label, Tk, Entry, Button
from zoneinfo import ZoneInfo
import requests
from tkcalendar import Calendar
from PIL import Image, ImageTk

root = Tk()
root.title("Smart Weather App")
root.geometry("1500x900")
root.configure(bg="#1f2235")

# Load background image
#img = Image.open("bg.jpg")
#img = img.resize((1500, 900))

#bg_image = ImageTk.PhotoImage(img)

#bg_label = Label(root, image=bg_image)
#bg_label.place(x=0, y=0, relwidth=1, relheight=1)


# ALARM 



alarm_time = None

def set_alarm():
    global alarm_time
    alarm_time = alarm_entry.get()
    alarm_status.config(text=f"Alarm set: {alarm_time}")

def check_alarm():
    if alarm_time:
        current_time = datetime.now().strftime("%H:%M:%S")
        if current_time == alarm_time:
            alarm_status.config(text="⏰ Alarm Time Reached!")
    root.after(1000, check_alarm)



#  WEATHER 




def fetch_weather(city):
    api_key = "f039303aee5d5b8a2d6691f4fd6c1223"
    url = f"http://api.openweathermap.org/data/2.5/weather?q={city}&appid={api_key}&units=metric"

    try:
        data = requests.get(url).json()
        if data.get("cod") == 200:
            temp = data["main"]["temp"]
            desc = data["weather"][0]["description"]
            weather_label.config(text=f"{city}: {temp}°C, {desc}")
        else:
            weather_label.config(text=f"{city}: Not found")
    except:
        weather_label.config(text="Weather error")




#  CLOCK 




def update_clocks():
    now = datetime.now()

    # Day/Night Theme
    hour = now.hour

    if 6 <= hour < 18:
        # Day Theme
        root.configure(bg="#87CEEB")

        main_clock.config(bg="#87CEEB", fg="black")
        day_label.config(bg="#87CEEB", fg="navy")
        date_label.config(bg="#87CEEB", fg="darkorange")

    else:
        # Night Theme
        root.configure(bg="#1f2235")

        main_clock.config(bg="#1f2235", fg="white")
        day_label.config(bg="#1f2235", fg="#66ccff")
        date_label.config(bg="#1f2235", fg="orange")

    # Update Clock
    main_clock.config(text=now.strftime("%I:%M:%S %p"))
    day_label.config(text=now.strftime("%A"))
    date_label.config(text=now.strftime("%d %B %Y"))

    Dhaka_label.config(
        text=datetime.now(ZoneInfo("Asia/Dhaka")).strftime("Dhaka %I:%M:%S %p")
    )
    Tokyo_label.config(
        text=datetime.now(ZoneInfo("Asia/Tokyo")).strftime("Tokyo %I:%M:%S %p")
    )
    Seoul_label.config(
        text=datetime.now(ZoneInfo("Asia/Seoul")).strftime("Seoul %I:%M:%S %p")
    )

    root.after(1000, update_clocks)




 #UI



Label( root,
    text="🌤 Smart Weather Dashboard",
    font=("Segoe UI", 28, "bold"),
    fg="white",
    bg="#1f2235").pack(pady=10)

main_clock = Label(root, font=("Consolas", 30, "bold"), fg="white", bg="#232433")
main_clock.pack()

day_label = Label(root, font=("Arial", 18,'bold'), fg="navy", bg="#232433")
day_label.pack()

date_label = Label(root, font=("Segoe UI", 14,'bold'), fg="orange", bg="#232433")
date_label.pack()





# Weather



weather_label = Label(root, text="Weather loading...", bg="#2596be", fg="black", font=("Arial", 14, "bold"))
weather_label.pack(pady=10)

Button(
    root,
    text="Get Dhaka Weather",
    command=lambda: fetch_weather("Dhaka"),
    font=("Segoe UI", 12, "bold"),
    bg="#3498db",
    fg="white",
).pack(pady=5)

Button(
    root,
    text="Get Tokyo Weather",
    command=lambda: fetch_weather("Tokyo"),
    font=("Segoe UI", 12, "bold"),
    bg="#3498db",
    fg="white",
).pack(pady=5)

Button(
    root,
    text="Get Seoul Weather",
    command=lambda: fetch_weather("Seoul"),
    font=("Segoe UI", 12, "bold"),
    bg="#3498db",
    fg="white",
).pack(pady=5)




# Clocks





clock_frame = Frame(root, bg="#2596be")
clock_frame.pack(pady=10)

Dhaka_label = Label(clock_frame, fg="white", bg="#1f2235", font=("Consolas", 20, "bold")); Dhaka_label.pack()
Tokyo_label = Label(clock_frame, fg="white", bg="#1f2235", font=("Consolas", 20, "bold")); Tokyo_label.pack()
Seoul_label = Label(clock_frame, fg="white", bg="#1f2235", font=("Consolas", 20, "bold")); Seoul_label.pack()





# Alarm UI



alarm_frame = Frame(root, bg="#2596be")
alarm_frame.pack(pady=10)

alarm_entry = Entry(alarm_frame)
alarm_entry.pack(side=LEFT)

Button(alarm_frame, text="Set Alarm", command=set_alarm).pack(side=LEFT)

alarm_status = Label(root, text="No alarm set", bg="#2596be", fg="yellow", font=("Arial", 14, 'bold'))
alarm_status.pack()




# Calendar



Calendar(root,bg="#0e4255",fg="Black").pack(pady=20)





# START 
update_clocks()
check_alarm()

root.mainloop()