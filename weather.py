from datetime import datetime
from tkinter import LEFT, Frame, Label, Tk, Entry, Button
from zoneinfo import ZoneInfo
import requests
from tkcalendar import Calendar
from PIL import Image, ImageTk
import random

cities = ["Dhaka", "Tokyo", "Seoul"]

city_timezones = {
    "Dhaka": "Asia/Dhaka",
    "Tokyo": "Asia/Tokyo",
    "Seoul": "Asia/Seoul"
}

selected_city = random.choice(cities)










root = Tk()
root.title(
    f"🌤 Smart Weather Dashboard - {selected_city}"
)
root.geometry("1200x800")
root.configure(bg="#1f2235")
root.fg=fg="#FFFFFF"

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

    url = f"https://api.openweathermap.org/data/2.5/weather?q={city}&appid={api_key}&units=metric"

    try:
        response = requests.get(url)
        print(response.text)  # Debug output

        data = response.json()

        if data.get("cod") == 200:
            temp = data["main"]["temp"]
            desc = data["weather"][0]["description"].lower()

            color = "#FFFFFF"
            icon = "🌤"

            if "clear" in desc:
                color = "#F1C40F"
                icon = "☀"

            elif "rain" in desc:
                color = "#3498DB"
                icon = "🌧"

            elif "cloud" in desc:
                color = "#BDC3C7"
                icon = "☁"

            elif "snow" in desc:
                color = "#ECF0F1"
                icon = "❄"

            weather_label.config(
                text=f"{icon} {city}: {temp}°C, {desc.title()}",
                fg=color
            )

        else:
            weather_label.config(
                text=f"Error: {data.get('message')}",
                fg="red"
            )

    except Exception as e:
        weather_label.config(
            text=f"Error: {e}",
            fg="red"
        )


#  CLOCK 




def update_clocks():

    city_now = datetime.now(
        ZoneInfo(city_timezones[selected_city])
    )

    hour = city_now.hour

    # DAY THEME
    if 6 <= hour < 18:

        root.configure(bg="#87CEEB")

        main_clock.config(
            fg="#1F2937",
            bg="#87CEEB"
        )

        day_label.config(
            fg="#0C4A6E",
            bg="#87CEEB"
        )

        date_label.config(
            fg="#F59E0B",
            bg="#87CEEB"
        )

        city_label.config(
            fg="#0C4A6E",
            bg="#87CEEB"
        )

        weather_label.config(
            bg="#DFF6FF"
        )

        clock_frame.config(
            bg="#87CEEB"
        )

        alarm_frame.config(
            bg="#87CEEB"
        )

        alarm_status.config(
            bg="#87CEEB"
        )

        Dhaka_label.config(bg="#87CEEB")
        Tokyo_label.config(bg="#87CEEB")
        Seoul_label.config(bg="#87CEEB")

    # NIGHT THEME
    else:

        root.configure(bg="#1F2235")

        main_clock.config(
            fg="#FFFFFF",
            bg="#1F2235"
        )

        day_label.config(
            fg="#60A5FA",
            bg="#1F2235"
        )

        date_label.config(
            fg="#FBBF24",
            bg="#1F2235"
        )

        city_label.config(
            fg="#FFFFFF",
            bg="#1F2235"
        )

        weather_label.config(
            bg="#2C3E50"
        )

        clock_frame.config(
            bg="#1F2235"
        )

        alarm_frame.config(
            bg="#1F2235"
        )

        alarm_status.config(
            bg="#1F2235"
        )

        Dhaka_label.config(bg="#1F2235")
        Tokyo_label.config(bg="#1F2235")
        Seoul_label.config(bg="#1F2235")

    # Main Clock
    now = datetime.now()

    main_clock.config(
        text=now.strftime("%I:%M:%S %p")
    )

    day_label.config(
        text=now.strftime("%A")
    )

    date_label.config(
        text=now.strftime("%d %B %Y")
    )

    Dhaka_label.config(
        text=datetime.now(
            ZoneInfo("Asia/Dhaka")
        ).strftime("Dhaka  %I:%M:%S %p")
    )

    Tokyo_label.config(
        text=datetime.now(
            ZoneInfo("Asia/Tokyo")
        ).strftime("Tokyo  %I:%M:%S %p")
    )

    Seoul_label.config(
        text=datetime.now(
            ZoneInfo("Asia/Seoul")
        ).strftime("Seoul  %I:%M:%S %p")
    )

    root.after(1000, update_clocks)



 #UI



Label( root,
    text="🌤 Smart Weather Dashboard",
    font=("Segoe UI", 30, "bold"),
    fg="white",
    bg="#1f2235").pack(pady=10)

main_clock = Label(
    root,
    font=("Consolas", 25, "bold"),
    fg="#FFFFFF",
    bg="#1F2235"
)
main_clock.pack()

day_label = Label(root, font=("Arial", 18,'bold'), fg="navy", bg="#232433")
day_label.pack()

date_label = Label(root, font=("Segoe UI", 14,'bold'), fg="orange", bg="#232433")
date_label.pack()

city_label = Label(
    root,
    text=f"Selected City: {selected_city}",
    font=("Segoe UI", 18, "bold"),
    fg="white",
    bg="#1F2235"
)
city_label.pack(pady=5)

def change_city():
    global selected_city

    selected_city = random.choice(cities)

    root.title(
        f"🌤 Smart Weather Dashboard - {selected_city}"
    )

    city_label.config(
        text=f"Selected City: {selected_city}"
    )

    fetch_weather(selected_city)

    root.after(10000, change_city)







# Weather



weather_label = Label(
    root,
    text="Weather loading...",
    bg="#2C3E50",
    fg="white",
    font=("Segoe UI", 14, "bold"),
    padx=10,
    pady=5
)
weather_label.pack(pady=10)

# Weather Buttons

Button(
    root,
    text="Get Dhaka Weather",
    command=lambda: fetch_weather("Dhaka"),
    bg="#3498DB",
    fg="white",
    activebackground="#2980B9",
    activeforeground="white",
    relief="flat",
    font=("Segoe UI", 10, "bold"),
    cursor="hand2"
).pack(pady=10)

Button(
    root,
    text="Get Tokyo Weather",
    command=lambda: fetch_weather("Tokyo"),
    bg="#3498DB",
    fg="white",
    activebackground="#2980B9",
    activeforeground="white",
    relief="flat",
    font=("Segoe UI", 10, "bold"),
    cursor="hand2"
).pack(pady=10)

Button(
    root,
    text="Get Seoul Weather",
    command=lambda: fetch_weather("Seoul"),
    bg="#3498DB",
    fg="white",
    activebackground="#2980B9",
    activeforeground="white",
    relief="flat",
    font=("Segoe UI", 10, "bold"),
    cursor="hand2"
).pack(pady=10)






# Clocks





clock_frame = Frame(root, bg="#2596be")
clock_frame.pack(pady=10)

Dhaka_label = Label(clock_frame, fg="#E5E7EB",bg="#1F2235", font=("Consolas", 15, "bold")); Dhaka_label.pack()
Tokyo_label = Label(clock_frame, fg="#E5E7EB", bg="#1F2235", font=("Consolas", 15, "bold")); Tokyo_label.pack()
Seoul_label = Label(clock_frame, fg="#E5E7EB", bg="#1F2235", font=("Consolas", 15, "bold")); Seoul_label.pack()





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
fetch_weather(selected_city)

update_clocks()
check_alarm()
change_city()

root.mainloop()

root.mainloop()