from datetime import datetime, timedelta, timezone
from zoneinfo import ZoneInfo
import requests, math, threading, random, ctypes
import tkinter as tk
from tkinter import font as tkfont, ttk, messagebox
try:
    import tkintermapview
    HAS_MAP = True
except ImportError:
    HAS_MAP = False

# ── High DPI Awareness for Windows ────────────────────────────
try:
    ctypes.windll.shcore.SetProcessDpiAwareness(1)
except Exception:
    pass

# ── Colors & Design System ────────────────────────────────────
BG      = "#14142a"
CARD    = "#1c1c38"
CARD2   = "#232345"
SDBG    = "#131325"
ACTBG   = "#3a3070"
BORD    = "#26265a"
ACCENT  = "#7c6ff7"
ACC2    = "#a89cf8"
ACC3    = "#4a3db0"
TEXT1   = "#f0eeff"
TEXT2   = "#686898"
TEXT3   = "#404080"
WARM    = "#f5a623"
GREEN   = "#06d6a0"
DANGER  = "#ef233c"
CYAN    = "#00c8e0"
PINK    = "#f472b6"

API_KEY = "f039303aee5d5b8a2d6691f4fd6c1223"

# ── Full Country & City Database (20 Countries, 300+ Cities) ───
COUNTRIES = {
    "Bangladesh": {
        "tz": "Asia/Dhaka", "flag": "🇧🇩",
        "cities": [
            "Dhaka", "Chittagong", "Sylhet", "Rajshahi", "Khulna",
            "Barisal", "Comilla", "Mymensingh", "Rangpur", "Narayanganj",
            "Gazipur", "Jashore", "Bogra", "Dinajpur", "Tangail",
            "Cox's Bazar", "Noakhali", "Pabna", "Faridpur", "Brahmanbaria",
            "Naogaon", "Sirajganj", "Narsingdi", "Saidpur", "Chandpur",
            "Madaripur", "Netrakona", "Sherpur", "Jamalpur", "Kishoreganj",
            "Feni", "Joypurhat", "Thakurgaon", "Panchagarh", "Nilphamari",
            "Lalmonirhat", "Kurigram", "Gaibandha", "Habiganj", "Moulvibazar",
            "Sunamganj", "Meherpur", "Chuadanga", "Magura", "Narail",
            "Satkhira", "Bagerhat", "Pirojpur", "Patuakhali", "Bhola"
        ]
    },
    "South Korea": {
        "tz": "Asia/Seoul", "flag": "🇰🇷",
        "cities": [
            "Seoul", "Busan", "Incheon", "Daegu", "Daejeon",
            "Gwangju", "Suwon", "Ulsan", "Changwon", "Seongnam",
            "Goyang", "Yongin", "Jeonju", "Cheongju", "Cheonan",
            "Ansan", "Anyang", "Pohang", "Uijeongbu", "Gimhae",
            "Jeju", "Asan", "Gumi", "Iksan", "Hwaseong",
            "Wonju", "Pyeongtaek", "Siheung", "Gimpo", "Bucheon"
        ]
    },
    "United Kingdom": {
        "tz": "Europe/London", "flag": "🇬🇧",
        "cities": [
            "London", "Manchester", "Birmingham", "Leeds", "Glasgow",
            "Sheffield", "Liverpool", "Edinburgh", "Bristol", "Cardiff",
            "Nottingham", "Newcastle upon Tyne", "Leicester", "Coventry", "Bradford",
            "Belfast", "Hull", "Plymouth", "Derby", "Southampton",
            "Stoke-on-Trent", "Wolverhampton", "Oxford", "Cambridge", "Brighton"
        ]
    },
    "United States": {
        "tz": "America/New_York", "flag": "🇺🇸",
        "cities": [
            "New York", "Los Angeles", "Chicago", "Houston", "Phoenix",
            "Philadelphia", "San Antonio", "San Diego", "Dallas", "Seattle",
            "Boston", "Miami", "Atlanta", "Denver", "Portland",
            "Washington", "Nashville", "Las Vegas", "Minneapolis", "Detroit"
        ]
    },
    "Japan": {
        "tz": "Asia/Tokyo", "flag": "🇯🇵",
        "cities": [
            "Tokyo", "Osaka", "Kyoto", "Yokohama", "Nagoya",
            "Sapporo", "Fukuoka", "Kobe", "Kawasaki", "Hiroshima",
            "Sendai", "Chiba", "Kitakyushu", "Sakai", "Niigata"
        ]
    },
    "UAE": {
        "tz": "Asia/Dubai", "flag": "🇦🇪",
        "cities": [
            "Dubai", "Abu Dhabi", "Sharjah", "Al Ain", "Ajman",
            "Ras al-Khaimah", "Fujairah", "Umm al-Quwain"
        ]
    },
    "India": {
        "tz": "Asia/Kolkata", "flag": "🇮🇳",
        "cities": [
            "Delhi", "Mumbai", "Kolkata", "Chennai", "Bangalore",
            "Hyderabad", "Ahmedabad", "Pune", "Surat", "Jaipur",
            "Lucknow", "Kanpur", "Nagpur", "Indore", "Bhopal"
        ]
    },
    "Germany": {
        "tz": "Europe/Berlin", "flag": "🇩🇪",
        "cities": [
            "Berlin", "Munich", "Hamburg", "Frankfurt", "Cologne",
            "Stuttgart", "Dusseldorf", "Dresden", "Leipzig", "Hanover"
        ]
    },
    "France": {
        "tz": "Europe/Paris", "flag": "🇫🇷",
        "cities": [
            "Paris", "Lyon", "Marseille", "Toulouse", "Nice",
            "Nantes", "Strasbourg", "Montpellier", "Bordeaux", "Lille"
        ]
    },
    "Australia": {
        "tz": "Australia/Sydney", "flag": "🇦🇺",
        "cities": [
            "Sydney", "Melbourne", "Brisbane", "Perth", "Adelaide",
            "Gold Coast", "Canberra", "Newcastle", "Hobart", "Darwin"
        ]
    },
    "Canada": {
        "tz": "America/Toronto", "flag": "🇨🇦",
        "cities": [
            "Toronto", "Vancouver", "Montreal", "Ottawa", "Calgary",
            "Edmonton", "Winnipeg", "Quebec", "Hamilton", "Halifax"
        ]
    },
    "China": {
        "tz": "Asia/Shanghai", "flag": "🇨🇳",
        "cities": [
            "Beijing", "Shanghai", "Guangzhou", "Shenzhen", "Chengdu",
            "Wuhan", "Hangzhou", "Nanjing", "Xian", "Chongqing"
        ]
    },
    "Saudi Arabia": {
        "tz": "Asia/Riyadh", "flag": "🇸🇦",
        "cities": [
            "Riyadh", "Jeddah", "Mecca", "Medina", "Dammam", "Taif", "Tabuk"
        ]
    },
    "Brazil": {
        "tz": "America/Sao_Paulo", "flag": "🇧🇷",
        "cities": [
            "Sao Paulo", "Rio de Janeiro", "Brasilia", "Salvador", "Fortaleza", "Curitiba"
        ]
    },
    "Russia": {
        "tz": "Europe/Moscow", "flag": "🇷🇺",
        "cities": [
            "Moscow", "Saint Petersburg", "Novosibirsk", "Yekaterinburg", "Kazan"
        ]
    },
    "Indonesia": {
        "tz": "Asia/Jakarta", "flag": "🇮🇩",
        "cities": [
            "Jakarta", "Surabaya", "Bandung", "Medan", "Semarang", "Makassar"
        ]
    },
    "Pakistan": {
        "tz": "Asia/Karachi", "flag": "🇵🇰",
        "cities": [
            "Karachi", "Lahore", "Faisalabad", "Rawalpindi", "Islamabad", "Peshawar"
        ]
    },
    "Turkey": {
        "tz": "Europe/Istanbul", "flag": "🇹🇷",
        "cities": [
            "Istanbul", "Ankara", "Izmir", "Bursa", "Antalya", "Adana"
        ]
    },
    "Spain": {
        "tz": "Europe/Madrid", "flag": "🇪🇸",
        "cities": [
            "Madrid", "Barcelona", "Valencia", "Seville", "Zaragoza", "Malaga"
        ]
    },
    "Italy": {
        "tz": "Europe/Rome", "flag": "🇮🇹",
        "cities": [
            "Rome", "Milan", "Naples", "Turin", "Palermo", "Florence", "Venice"
        ]
    }
}

COUNTRY_LIST = list(COUNTRIES.keys())

WX_ICONS = {
    "clear":"☀","few clouds":"🌤","scattered":"⛅",
    "broken":"🌥","overcast":"☁","light rain":"🌦",
    "rain":"🌧","drizzle":"🌦","thunderstorm":"⛈",
    "snow":"❄","mist":"🌫","haze":"🌫","fog":"🌁",
}

def get_icon(d):
    d=d.lower()
    for k,v in WX_ICONS.items():
        if k in d: return v
    if "rain" in d: return "🌧"
    if "cloud" in d: return "☁"
    if "clear" in d: return "☀"
    if "snow" in d: return "❄"
    if "thunder" in d: return "⛈"
    return "🌡"

def temp_color(t):
    if t>=38: return "#ff2d00"
    if t>=32: return "#ff6600"
    if t>=26: return "#ffba08"
    if t>=20: return "#90be6d"
    if t>=10: return "#4cc9f0"
    if t>=0:  return "#4361ee"
    return "#b5c0ff"

def wind_dir(deg):
    return ["N","NE","E","SE","S","SW","W","NW"][int((deg+22.5)/45)%8]

def classify(desc):
    d=desc.lower()
    if "thunder" in d: return "thunder"
    if "snow"    in d: return "snow"
    if "rain" in d or "drizzle" in d: return "rain"
    if "mist" in d or "fog" in d or "haze" in d: return "mist"
    if "clear"   in d: return "clear"
    return "cloud"

def sky_grad(h):
    if 5<=h<7:  return("#7b2208","#f4a261")
    if 7<=h<17: return("#004e8c","#48cae4")
    if 17<=h<20:return("#6b1e00","#c94b20")
    return("#020818","#030e2a")

class WeatherNow:
    NAV_ITEMS = ["Dashboard", "Maps", "Charts", "Air Quality", "Calendar", "Saved", "Settings"]

    def __init__(self):
        self.root = tk.Tk()
        self.root.title("WeatherNow – Live Global Dashboard & Analytics")
        self.root.geometry("1340x880")
        self.root.minsize(1120, 740)
        self.root.configure(bg=BG)

        self.api_key = API_KEY
        self.city = "New York"
        self.country = "United States"
        self.lat = 40.7128
        self.lon = -74.0060
        self.tz_offset = -14400  # Default UTC offset for NYC in seconds
        self.unit = "C"           # "C" or "F"
        self.favorites = ["New York", "London", "Tokyo", "Dhaka", "Seoul"]

        self.cur_page = "Dashboard"
        self._frame = 0
        self._stars = []
        self._wx_type = "cloud"
        self._wx_icon = "☁"
        self._cur_temp = 0.0
        self._disp_temp = 0.0
        self._wind_kmh = 0.0
        self._wind_disp = 0.0

        self._gc = {"hum":0,"wind":0,"rain":0,"uv":0,"cloud":0}
        self._gt = {"hum":0,"wind":0,"rain":0,"uv":0,"cloud":0}

        self._aqi_data = {"aqi": 1, "pm2_5": 12.4, "pm10": 24.1, "no2": 18.2, "o3": 45.0, "so2": 4.1, "co": 210.0}
        self._hourly = []
        self._daily = []
        self._chart_temps = [5, 8, 6, 3]

        self.forecast_mode = "Weekly"
        self._cached_forecast_items = []
        self._mk_fonts()
        self._build_layout()
        self._loops()

    # ── Unit Formatting Helpers ─────────────────────────────────
    def fmt_t_val(self, val_c):
        return (val_c * 9/5 + 32) if self.unit == "F" else val_c

    def fmt_t_unit(self):
        return "°F" if self.unit == "F" else "°C"

    def fmt_t(self, val_c, dec=0):
        val = self.fmt_t_val(val_c)
        if dec == 0:
            return f"{val:.0f}{self.fmt_t_unit()}"
        return f"{val:.{dec}f} {self.fmt_t_unit()}"

    def _mk_fonts(self):
        self.fH  = tkfont.Font(family="Segoe UI", size=40, weight="bold")
        self.fBg = tkfont.Font(family="Segoe UI", size=16, weight="bold")
        self.fM  = tkfont.Font(family="Segoe UI", size=12, weight="bold")
        self.fS  = tkfont.Font(family="Segoe UI", size=10)
        self.fT  = tkfont.Font(family="Segoe UI", size=9)
        self.fSm = tkfont.Font(family="Segoe UI", size=8)
        self.fCk = tkfont.Font(family="Consolas", size=13, weight="bold")
        self.fMo = tkfont.Font(family="Consolas", size=11, weight="bold")
        self.fLb = tkfont.Font(family="Segoe UI", size=10, weight="bold")

    def _mk_card(self, parent, bg=CARD, **kw):
        return tk.Frame(parent, bg=bg, bd=0, **kw)

    def _build_layout(self):
        self.sky = tk.Canvas(self.root, highlightthickness=0, bg=BG)
        self.sky.place(relx=0, rely=0, relwidth=1, relheight=1)

        self.mf = tk.Frame(self.root, bg=BG)
        self.mf.place(relx=0, rely=0, relwidth=1, relheight=1)
        self.mf.columnconfigure(0, weight=0, minsize=210)
        self.mf.columnconfigure(1, weight=1)
        self.mf.rowconfigure(0, weight=0, minsize=64)
        self.mf.rowconfigure(1, weight=1)

        self._sidebar()
        self._header()

        # Container for pages
        self.page_container = tk.Frame(self.mf, bg=BG)
        self.page_container.grid(row=1, column=1, sticky="nsew", padx=10, pady=(4,10))
        self.page_container.rowconfigure(0, weight=1)
        self.page_container.columnconfigure(0, weight=1)

        self.pages = {}
        for p in self.NAV_ITEMS:
            frame = tk.Frame(self.page_container, bg=BG)
            frame.grid(row=0, column=0, sticky="nsew")
            self.pages[p] = frame

        self._build_dashboard_page()
        self._build_maps_page()
        self._build_charts_page()
        self._build_aqi_page()
        self._build_calendar_page()
        self._build_saved_page()
        self._build_settings_page()

        self._show_page("Dashboard")

    # ── Sidebar ────────────────────────────────────────────────
    def _sidebar(self):
        sb = tk.Frame(self.mf, bg=SDBG, width=210)
        sb.grid(row=0, column=0, rowspan=2, sticky="nsew")
        sb.grid_propagate(False)
        sb.columnconfigure(0, weight=1)

        tk.Label(sb, text="WeatherNow",
                 font=tkfont.Font(family="Segoe UI", size=14, weight="bold"),
                 fg=TEXT1, bg=SDBG).pack(anchor="w", padx=18, pady=(18, 14))

        # Country & City Selectors
        sel_box = tk.Frame(sb, bg=CARD2, bd=0)
        sel_box.pack(fill="x", padx=12, pady=(0, 14))

        tk.Label(sel_box, text="Country", font=self.fSm, fg=TEXT2, bg=CARD2).pack(anchor="w", padx=8, pady=(4,1))
        self.country_var = tk.StringVar(value=self.country)
        self.country_cb = ttk.Combobox(sel_box, textvariable=self.country_var, values=COUNTRY_LIST, state="readonly", font=self.fSm)
        self.country_cb.pack(fill="x", padx=8, pady=(0,4))
        self.country_cb.bind("<<ComboboxSelected>>", self._on_country_selected)

        tk.Label(sel_box, text="City", font=self.fSm, fg=TEXT2, bg=CARD2).pack(anchor="w", padx=8, pady=(2,1))
        self.city_var = tk.StringVar(value=self.city)
        self.city_cb = ttk.Combobox(sel_box, textvariable=self.city_var, values=COUNTRIES[self.country]["cities"], state="readonly", font=self.fSm)
        self.city_cb.pack(fill="x", padx=8, pady=(0,6))
        self.city_cb.bind("<<ComboboxSelected>>", self._on_city_selected)

        tk.Frame(sb, bg=BORD, height=1).pack(fill="x", padx=14, pady=(0, 10))

        # Navigation buttons
        self.nav_btns = {}
        for p in self.NAV_ITEMS:
            active = (p == self.cur_page)
            bg = ACTBG if active else SDBG
            fg = TEXT1 if active else TEXT2
            f = tk.Frame(sb, bg=bg, cursor="hand2")
            f.pack(fill="x", padx=10, pady=2)
            lbl = tk.Label(f, text=f"  {p}", font=self.fS, fg=fg, bg=bg, anchor="w")
            lbl.pack(fill="x", padx=10, pady=8)
            
            def _click(e, page_name=p): self._show_page(page_name)
            f.bind("<Button-1>", _click)
            lbl.bind("<Button-1>", _click)
            self.nav_btns[p] = (f, lbl)

    def _on_country_selected(self, event):
        cntry = self.country_var.get()
        self.country = cntry
        cities = COUNTRIES[cntry]["cities"]
        self.city_cb.config(values=cities)
        if cities:
            self.city_var.set(cities[0])
            self._switch(cities[0])

    def _on_city_selected(self, event):
        cty = self.city_var.get()
        self._switch(cty)

    def _show_page(self, name):
        self.cur_page = name
        for p, (fr, lbl) in self.nav_btns.items():
            if p == name:
                fr.config(bg=ACTBG)
                lbl.config(bg=ACTBG, fg=TEXT1)
            else:
                fr.config(bg=SDBG)
                lbl.config(bg=SDBG, fg=TEXT2)

        self.pages[name].tkraise()
        if name == "Maps":
            self._update_map_view()
        elif name == "Charts":
            self._draw_extended_charts()
        elif name == "Air Quality":
            self._draw_aqi_cards()
        elif name == "Calendar":
            self._draw_calendar()
        elif name == "Saved":
            self._draw_saved_locations()

    # ── Header ─────────────────────────────────────────────────
    def _header(self):
        h = tk.Frame(self.mf, bg=BG)
        h.grid(row=0, column=1, sticky="ew", padx=(10, 14), pady=(10, 0))
        h.columnconfigure(1, weight=1)

        loc_frame = tk.Frame(h, bg=BG)
        loc_frame.grid(row=0, column=0, sticky="w", padx=4)

        self.loc_lbl = tk.Label(loc_frame, text=f"📍  {self.city}, --", font=self.fBg, fg=TEXT1, bg=BG)
        self.loc_lbl.pack(side="left")

        self.fav_btn = tk.Button(loc_frame, text="⭐", font=self.fM, bg=BG, fg=WARM, relief="flat", cursor="hand2", bd=0, command=self._toggle_favorite)
        self.fav_btn.pack(side="left", padx=(8, 0))
        self._update_fav_btn()

        sf = tk.Frame(h, bg=CARD, bd=0)
        sf.grid(row=0, column=1, sticky="ew", padx=(16, 14))
        sf.columnconfigure(0, weight=1)

        self.sv = tk.StringVar(value="Search location, city or place…")
        self.se = tk.Entry(sf, textvariable=self.sv, font=self.fS, fg=TEXT2, bg=CARD, insertbackground=ACCENT, relief="flat", bd=8)
        self.se.grid(row=0, column=0, sticky="ew")
        self.se.bind("<Return>", lambda e: self._search())
        self.se.bind("<FocusIn>", lambda e: self._clr_ph())
        self.se.bind("<FocusOut>", lambda e: self._rst_ph())

        tk.Button(sf, text=" 🔍 ", font=self.fS, bg=ACCENT, fg=BG, relief="flat", cursor="hand2", bd=0, padx=6, command=self._search).grid(row=0, column=1)

        tf = tk.Frame(h, bg=BG)
        tf.grid(row=0, column=2, sticky="e", padx=4)
        self.tab_btns = {}
        for tab in ["Daily", "Weekly", "Monthly"]:
            bg = ACTBG if tab == self.forecast_mode else BG
            fg = TEXT1 if tab == self.forecast_mode else TEXT2
            btn = tk.Button(tf, text=tab, font=self.fT, bg=bg, fg=fg, relief="flat", cursor="hand2", padx=10, pady=6, bd=0, command=lambda t=tab: self._set_forecast_mode(t))
            btn.pack(side="left", padx=2)
            self.tab_btns[tab] = btn

        # °C / °F Unit Toggle Button on Header
        self.unit_hdr_btn = tk.Button(h, text=f"°{self.unit}", font=self.fM, bg=CARD2, fg=ACCENT, relief="flat", cursor="hand2", padx=8, pady=4, bd=0, command=self._toggle_unit)
        self.unit_hdr_btn.grid(row=0, column=3, sticky="e", padx=(6, 0))

    def _toggle_favorite(self):
        if self.city in self.favorites:
            self.favorites.remove(self.city)
        else:
            self.favorites.append(self.city)
        self._update_fav_btn()
        if self.cur_page == "Saved":
            self._draw_saved_locations()

    def _update_fav_btn(self):
        if hasattr(self, 'fav_btn'):
            if self.city in self.favorites:
                self.fav_btn.config(text="⭐", fg=WARM)
            else:
                self.fav_btn.config(text="☆", fg=TEXT2)

    def _toggle_unit(self):
        self.unit = "F" if self.unit == "C" else "C"
        if hasattr(self, 'unit_hdr_btn'):
            self.unit_hdr_btn.config(text=f"°{self.unit}")
        if hasattr(self, 'btn_c') and hasattr(self, 'btn_f'):
            self.btn_c.config(bg=ACTBG if self.unit == "C" else CARD2, fg=TEXT1 if self.unit == "C" else TEXT2)
            self.btn_f.config(bg=ACTBG if self.unit == "F" else CARD2, fg=TEXT1 if self.unit == "F" else TEXT2)
        
        self.loc_lbl.config(text=f"📍  {self.city}, {self.fmt_t(self._cur_temp)}")
        self.feel_lbl.config(text=f"Real feel  {self.fmt_t(getattr(self, '_feels_like', self._cur_temp))}")
        self._render_right_forecast()
        self._draw_temp_chart()
        if self.cur_page == "Charts": self._draw_extended_charts()
        elif self.cur_page == "Calendar": self._draw_calendar()
        elif self.cur_page == "Saved": self._draw_saved_locations()

    # ══════════════════════════════════════════════════════════
    #  PAGE 1: DASHBOARD
    # ══════════════════════════════════════════════════════════
    def _build_dashboard_page(self):
        p = self.pages["Dashboard"]
        p.rowconfigure(0, weight=5)
        p.rowconfigure(1, weight=3)
        p.rowconfigure(2, weight=3)
        p.columnconfigure(0, weight=2)
        p.columnconfigure(1, weight=3)
        p.columnconfigure(2, weight=3)

        # Weather Card
        wc = self._mk_card(p)
        wc.grid(row=0, column=0, sticky="nsew", padx=(0, 5), pady=(0, 5))
        
        self.ic_cv = tk.Canvas(wc, bg=CARD, highlightthickness=0, height=120)
        self.ic_cv.pack(fill="x", padx=0, pady=0)
        self.ic_cv.bind("<Configure>", lambda e: self._draw_wx_icon())

        self.temp_lbl = tk.Label(wc, text="--", font=self.fH, fg=TEXT1, bg=CARD, anchor="w")
        self.temp_lbl.pack(fill="x", padx=20, pady=(0, 2))
        self.city_lbl = tk.Label(wc, text="Loading…", font=self.fBg, fg=TEXT2, bg=CARD, anchor="w")
        self.city_lbl.pack(fill="x", padx=20)

        tk.Frame(wc, bg=BORD, height=1).pack(fill="x", padx=20, pady=(10, 6))

        self.feel_lbl = tk.Label(wc, text="Real feel  --", font=self.fT, fg=TEXT2, bg=CARD, anchor="w")
        self.feel_lbl.pack(fill="x", padx=20, pady=1)
        self.date_lbl = tk.Label(wc, text="--", font=self.fT, fg=TEXT2, bg=CARD, anchor="w")
        self.date_lbl.pack(fill="x", padx=20, pady=1)
        self.time_lbl = tk.Label(wc, text="--:--:--", font=self.fCk, fg=TEXT1, bg=CARD, anchor="w")
        self.time_lbl.pack(fill="x", padx=20, pady=(1, 8))

        sr = tk.Frame(wc, bg=CARD)
        sr.pack(fill="x", padx=20, pady=(0, 10))
        self.pres_lbl = tk.Label(sr, text="-- hPa", font=self.fSm, fg=TEXT2, bg=CARD)
        self.pres_lbl.pack(side="left", padx=(0, 10))
        self.hum_lbl  = tk.Label(sr, text="-- %", font=self.fSm, fg=TEXT2, bg=CARD)
        self.hum_lbl.pack(side="left", padx=(0, 10))
        self.wnd_lbl  = tk.Label(sr, text="-- km/h", font=self.fSm, fg=TEXT2, bg=CARD)
        self.wnd_lbl.pack(side="left")

        # Temp chart
        tc = self._mk_card(p)
        tc.grid(row=0, column=1, sticky="nsew", padx=5, pady=(0, 5))
        tk.Label(tc, text="Temperature Forecast", font=self.fM, fg=TEXT1, bg=CARD).pack(anchor="w", padx=18, pady=(14, 4))
        self.temp_cv = tk.Canvas(tc, bg=CARD, highlightthickness=0)
        self.temp_cv.pack(fill="both", expand=True, padx=10, pady=(0, 10))
        self.temp_cv.bind("<Configure>", lambda e: self._draw_temp_chart())

        # Right Forecast Column
        rc = self._mk_card(p)
        rc.grid(row=0, column=2, rowspan=3, sticky="nsew", padx=(5, 0))
        rc.rowconfigure(2, weight=1)
        rc.columnconfigure(0, weight=1)

        hdr = tk.Frame(rc, bg=CARD)
        hdr.pack(fill="x", padx=14, pady=(16, 8))
        tk.Button(hdr, text="<", font=self.fS, bg=CARD2, fg=TEXT1, relief="flat", padx=6, bd=0).pack(side="left")
        self.right_title_lbl = tk.Label(hdr, text="This Week", font=self.fM, fg=TEXT1, bg=CARD)
        self.right_title_lbl.pack(side="left", padx=10)
        tk.Button(hdr, text=">", font=self.fS, bg=CARD2, fg=TEXT1, relief="flat", padx=6, bd=0).pack(side="left")

        tk.Label(rc, text="Today", font=self.fLb, fg=TEXT2, bg=CARD).pack(anchor="w", padx=16, pady=(4, 6))
        self.hourly_frame = tk.Frame(rc, bg=CARD)
        self.hourly_frame.pack(fill="x", padx=12, pady=(0, 4))

        tk.Frame(rc, bg=BORD, height=1).pack(fill="x", padx=14, pady=(8, 8))

        self.daily_frame = tk.Frame(rc, bg=CARD)
        self.daily_frame.pack(fill="both", expand=True, padx=12, pady=(0, 12))

        # Wind & Gauges
        wnd_c = self._mk_card(p)
        wnd_c.grid(row=1, column=0, sticky="nsew", padx=(0, 5), pady=5)
        wh = tk.Frame(wnd_c, bg=CARD)
        wh.pack(fill="x", padx=16, pady=(12, 2))
        tk.Label(wh, text="⟳  Wind", font=self.fM, fg=TEXT1, bg=CARD).pack(side="left")
        self.wnd_kmh_lbl = tk.Label(wnd_c, text="-- km/h", font=self.fT, fg=TEXT2, bg=CARD)
        self.wnd_kmh_lbl.pack(anchor="w", padx=16)
        self.wind_cv = tk.Canvas(wnd_c, bg=CARD, highlightthickness=0, height=50)
        self.wind_cv.pack(fill="x", padx=10, pady=(4, 10))

        rain_c = self._mk_card(p)
        rain_c.grid(row=1, column=1, sticky="nsew", padx=5, pady=5)
        rh = tk.Frame(rain_c, bg=CARD)
        rh.pack(fill="x", padx=16, pady=(12, 2))
        tk.Label(rh, text="Rain chance", font=self.fM, fg=TEXT1, bg=CARD).pack(side="left")
        self.rain_badge = tk.Label(rh, text="Low", font=self.fSm, fg=CYAN, bg=CARD2, padx=6, pady=2)
        self.rain_badge.pack(side="right")
        self.rain_cv = tk.Canvas(rain_c, bg=CARD, highlightthickness=0, width=120, height=90)
        self.rain_cv.pack(pady=(2, 10))

        uv_c = self._mk_card(p)
        uv_c.grid(row=2, column=0, sticky="nsew", padx=(0, 5), pady=(5, 0))
        uvh = tk.Frame(uv_c, bg=CARD)
        uvh.pack(fill="x", padx=16, pady=(12, 2))
        tk.Label(uvh, text="UV Index", font=self.fM, fg=TEXT1, bg=CARD).pack(side="left")
        self.uv_badge = tk.Label(uvh, text="Low", font=self.fSm, fg=GREEN, bg=CARD2, padx=6, pady=2)
        self.uv_badge.pack(side="right")
        self.uv_cv = tk.Canvas(uv_c, bg=CARD, highlightthickness=0, width=120, height=90)
        self.uv_cv.pack(pady=(2, 10))

        cld_c = self._mk_card(p)
        cld_c.grid(row=2, column=1, sticky="nsew", padx=5, pady=(5, 0))
        clh = tk.Frame(cld_c, bg=CARD)
        clh.pack(fill="x", padx=16, pady=(12, 2))
        tk.Label(clh, text="Cloud Cover", font=self.fM, fg=TEXT1, bg=CARD).pack(side="left")
        self.cloud_badge = tk.Label(clh, text="High", font=self.fSm, fg=TEXT2, bg=CARD2, padx=6, pady=2)
        self.cloud_badge.pack(side="right")
        self.cloud_cv = tk.Canvas(cld_c, bg=CARD, highlightthickness=0, width=120, height=90)
        self.cloud_cv.pack(pady=(2, 10))

    # ══════════════════════════════════════════════════════════
    #  PAGE 2: MAPS PAGE
    # ══════════════════════════════════════════════════════════
    def _build_maps_page(self):
        p = self.pages["Maps"]
        p.rowconfigure(1, weight=1)
        p.columnconfigure(0, weight=1)

        hdr = tk.Frame(p, bg=CARD, height=45)
        hdr.grid(row=0, column=0, sticky="ew", pady=(0, 6))

        tk.Label(hdr, text="🗺  Interactive Weather Map", font=self.fM, fg=TEXT1, bg=CARD).pack(side="left", padx=16, pady=10)

        if HAS_MAP:
            map_btn1 = tk.Button(hdr, text="Standard", font=self.fSm, bg=ACTBG, fg=TEXT1, relief="flat", command=lambda: self.map_widget.set_tile_server("https://a.tile.openstreetmap.org/{z}/{x}/{y}.png"))
            map_btn1.pack(side="right", padx=6, pady=8)
            map_btn2 = tk.Button(hdr, text="Satellite", font=self.fSm, bg=CARD2, fg=TEXT2, relief="flat", command=lambda: self.map_widget.set_tile_server("https://mt1.google.com/vt/lyrs=s&x={x}&y={y}&z={z}"))
            map_btn2.pack(side="right", padx=2, pady=8)

        # Map widget
        self.map_container = tk.Frame(p, bg=CARD)
        self.map_container.grid(row=1, column=0, sticky="nsew")

        if HAS_MAP:
            self.map_widget = tkintermapview.TkinterMapView(self.map_container, corner_radius=10)
            self.map_widget.pack(fill="both", expand=True)
        else:
            self.map_cv = tk.Canvas(self.map_container, bg=CARD, highlightthickness=0)
            self.map_cv.pack(fill="both", expand=True)

    def _update_map_view(self):
        if HAS_MAP:
            try:
                self.map_widget.set_position(self.lat, self.lon)
                self.map_widget.set_zoom(11)
                self.map_widget.delete_all_marker()
                self.map_widget.set_marker(self.lat, self.lon, text=f"{self.city} ({self.fmt_t(self._cur_temp)})")
            except Exception:
                pass
        else:
            c = getattr(self, 'map_cv', None)
            if c:
                c.delete("all")
                W = c.winfo_width() or 600; H = c.winfo_height() or 400
                cx, cy = W//2, H//2
                c.create_rectangle(20, 20, W-20, H-20, fill=CARD2, outline=BORD)
                c.create_oval(cx-40, cy-40, cx+40, cy+40, fill=ACTBG, outline=ACCENT, width=2)
                c.create_text(cx, cy-60, text=f"📍 {self.city}, {self.country}", font=self.fM, fill=TEXT1)
                c.create_text(cx, cy, text=f"Lat: {self.lat:.4f}\nLon: {self.lon:.4f}\nTemp: {self.fmt_t(self._cur_temp)}", font=self.fS, fill=TEXT2, justify="center")

    # ══════════════════════════════════════════════════════════
    #  PAGE 3: CHARTS PAGE
    # ══════════════════════════════════════════════════════════
    def _build_charts_page(self):
        p = self.pages["Charts"]
        p.rowconfigure(0, weight=1)
        p.rowconfigure(1, weight=1)
        p.columnconfigure(0, weight=1)
        p.columnconfigure(1, weight=1)

        c1 = self._mk_card(p)
        c1.grid(row=0, column=0, sticky="nsew", padx=(0,4), pady=(0,4))
        tk.Label(c1, text="24-Hour Temperature Trend", font=self.fM, fg=TEXT1, bg=CARD).pack(anchor="w", padx=16, pady=10)
        self.chart_cv1 = tk.Canvas(c1, bg=CARD, highlightthickness=0)
        self.chart_cv1.pack(fill="both", expand=True, padx=10, pady=(0,10))

        c2 = self._mk_card(p)
        c2.grid(row=0, column=1, sticky="nsew", padx=(4,0), pady=(0,4))
        tk.Label(c2, text="Precipitation Probability (%)", font=self.fM, fg=TEXT1, bg=CARD).pack(anchor="w", padx=16, pady=10)
        self.chart_cv2 = tk.Canvas(c2, bg=CARD, highlightthickness=0)
        self.chart_cv2.pack(fill="both", expand=True, padx=10, pady=(0,10))

        c3 = self._mk_card(p)
        c3.grid(row=1, column=0, sticky="nsew", padx=(0,4), pady=(4,0))
        tk.Label(c3, text="Wind Speed Curve (km/h)", font=self.fM, fg=TEXT1, bg=CARD).pack(anchor="w", padx=16, pady=10)
        self.chart_cv3 = tk.Canvas(c3, bg=CARD, highlightthickness=0)
        self.chart_cv3.pack(fill="both", expand=True, padx=10, pady=(0,10))

        c4 = self._mk_card(p)
        c4.grid(row=1, column=1, sticky="nsew", padx=(4,0), pady=(4,0))
        tk.Label(c4, text="Humidity (%) & Pressure (hPa)", font=self.fM, fg=TEXT1, bg=CARD).pack(anchor="w", padx=16, pady=10)
        self.chart_cv4 = tk.Canvas(c4, bg=CARD, highlightthickness=0)
        self.chart_cv4.pack(fill="both", expand=True, padx=10, pady=(0,10))

    def _draw_extended_charts(self):
        items = self._cached_forecast_items[:8]
        if not items:
            temps = [self._cur_temp + random.randint(-4, 5) for _ in range(8)]
            hrs = [f"{i*3}:00" for i in range(8)]
            p_vals = [random.randint(5, 85) for _ in range(8)]
            w_vals = [random.randint(5, 25) for _ in range(8)]
            h_vals = [random.randint(40, 90) for _ in range(8)]
        else:
            temps = [x["main"]["temp"] for x in items]
            hrs = [datetime.fromtimestamp(x["dt"]).strftime("%I %p").lstrip("0") for x in items]
            p_vals = [int(x.get("pop", 0)*100) for x in items]
            w_vals = [int(x.get("wind", {}).get("speed", 0)*3.6) for x in items]
            h_vals = [x["main"]["humidity"] for x in items]

        # 1. Temp Chart
        c = self.chart_cv1
        c.delete("all")
        W = c.winfo_width() or 400; H = c.winfo_height() or 220
        disp_temps = [self.fmt_t_val(t) for t in temps]
        mn, mx = min(disp_temps)-2, max(disp_temps)+2
        rng = mx - mn or 1
        sp = (W-60)/max(1, len(disp_temps)-1)
        pts = []
        for i, t in enumerate(disp_temps):
            x = 40 + i*sp
            y = H - 30 - ((t-mn)/rng)*(H-60)
            pts.extend([x, y])
            c.create_oval(x-3, y-3, x+3, y+3, fill=ACCENT, outline="")
            c.create_text(x, y-12, text=f"{t:.0f}°", font=self.fSm, fill=TEXT1)
            c.create_text(x, H-12, text=hrs[i], font=self.fSm, fill=TEXT2)
        if len(pts)>=4: c.create_line(pts, fill=ACC2, width=2, smooth=True)

        # 2. Precipitation Bar Chart
        c2 = self.chart_cv2
        c2.delete("all")
        W2 = c2.winfo_width() or 400; H2 = c2.winfo_height() or 220
        sp2 = (W2-60)/len(p_vals)
        for i, p in enumerate(p_vals):
            x = 35 + i*sp2
            bh = (p/100)*(H2-60)
            c2.create_rectangle(x, H2-30-bh, x+sp2*0.6, H2-30, fill=CYAN, outline="")
            c2.create_text(x+sp2*0.3, H2-35-bh, text=f"{p}%", font=self.fSm, fill=TEXT1)
            c2.create_text(x+sp2*0.3, H2-12, text=hrs[i], font=self.fSm, fill=TEXT2)

        # 3. Wind Speed Chart
        c3 = self.chart_cv3
        c3.delete("all")
        W3 = c3.winfo_width() or 400; H3 = c3.winfo_height() or 220
        mx_w = max(w_vals)+5 or 30
        sp3 = (W3-60)/max(1, len(w_vals)-1)
        pts3 = []
        for i, w in enumerate(w_vals):
            x = 40 + i*sp3
            y = H3 - 30 - (w/mx_w)*(H3-60)
            pts3.extend([x, y])
            c3.create_oval(x-3, y-3, x+3, y+3, fill=GREEN, outline="")
            c3.create_text(x, y-12, text=f"{w}kph", font=self.fSm, fill=TEXT1)
            c3.create_text(x, H3-12, text=hrs[i], font=self.fSm, fill=TEXT2)
        if len(pts3)>=4: c3.create_line(pts3, fill=GREEN, width=2, smooth=True)

        # 4. Humidity Chart
        c4 = self.chart_cv4
        c4.delete("all")
        W4 = c4.winfo_width() or 400; H4 = c4.winfo_height() or 220
        sp4 = (W4-60)/len(h_vals)
        for i, hum in enumerate(h_vals):
            x = 35 + i*sp4
            bh = (hum/100)*(H4-60)
            c4.create_rectangle(x, H4-30-bh, x+sp4*0.6, H4-30, fill=ACCENT, outline="")
            c4.create_text(x+sp4*0.3, H4-35-bh, text=f"{hum}%", font=self.fSm, fill=TEXT1)
            c4.create_text(x+sp4*0.3, H4-12, text=hrs[i], font=self.fSm, fill=TEXT2)

    # ══════════════════════════════════════════════════════════
    #  PAGE 4: AIR QUALITY
    # ══════════════════════════════════════════════════════════
    def _build_aqi_page(self):
        p = self.pages["Air Quality"]
        p.rowconfigure(0, weight=0)
        p.rowconfigure(1, weight=1)
        p.columnconfigure(0, weight=1)

        self.aqi_top_card = self._mk_card(p, height=140)
        self.aqi_top_card.grid(row=0, column=0, sticky="ew", pady=(0, 8))

        self.aqi_grid = tk.Frame(p, bg=BG)
        self.aqi_grid.grid(row=1, column=0, sticky="nsew")
        for i in range(3): self.aqi_grid.columnconfigure(i, weight=1)
        for i in range(2): self.aqi_grid.rowconfigure(i, weight=1)

    def _draw_aqi_cards(self):
        for w in self.aqi_top_card.winfo_children(): w.destroy()
        for w in self.aqi_grid.winfo_children(): w.destroy()

        aqi_val = self._aqi_data.get("aqi", 2)
        aqi_labels = {1:("Good", GREEN), 2:("Fair", CYAN), 3:("Moderate", WARM), 4:("Poor", DANGER), 5:("Very Poor", DANGER)}
        status_txt, status_col = aqi_labels.get(aqi_val, ("Moderate", WARM))

        # Top AQI Banner
        f = tk.Frame(self.aqi_top_card, bg=CARD)
        f.pack(fill="both", expand=True, padx=20, pady=16)

        tk.Label(f, text=f"Air Quality Index (AQI):  {aqi_val} - {status_txt}", font=self.fBg, fg=status_col, bg=CARD).pack(anchor="w")
        tk.Label(f, text=f"Current location: {self.city}, {self.country}", font=self.fS, fg=TEXT2, bg=CARD).pack(anchor="w", pady=(4,0))
        rec = "Air quality is satisfactory; ideal for outdoor activities." if aqi_val <= 2 else "Sensitive individuals should limit prolonged outdoor exertion."
        tk.Label(f, text=f"Health Recommendation: {rec}", font=self.fT, fg=TEXT1, bg=CARD).pack(anchor="w", pady=(4,0))

        # Pollutant Cards
        metrics = [
            ("PM2.5", self._aqi_data.get("pm2_5", 12.4), "μg/m³", "Fine Particulate Matter"),
            ("PM10",  self._aqi_data.get("pm10", 24.1),  "μg/m³", "Coarse Particulate Matter"),
            ("NO2",   self._aqi_data.get("no2", 18.2),   "μg/m³", "Nitrogen Dioxide"),
            ("O3",    self._aqi_data.get("o3", 45.0),    "μg/m³", "Ozone"),
            ("SO2",   self._aqi_data.get("so2", 4.1),    "μg/m³", "Sulfur Dioxide"),
            ("CO",    self._aqi_data.get("co", 210.0),   "μg/m³", "Carbon Monoxide"),
        ]

        for idx, (name, val, unit, desc) in enumerate(metrics):
            r, c = idx//3, idx%3
            card = self._mk_card(self.aqi_grid)
            card.grid(row=r, column=c, sticky="nsew", padx=4, pady=4)

            tk.Label(card, text=name, font=self.fM, fg=ACC2, bg=CARD).pack(anchor="w", padx=16, pady=(14,2))
            tk.Label(card, text=f"{val:.1f} {unit}", font=self.fH, fg=TEXT1, bg=CARD).pack(anchor="w", padx=16)
            tk.Label(card, text=desc, font=self.fT, fg=TEXT2, bg=CARD).pack(anchor="w", padx=16, pady=(4,14))

    # ══════════════════════════════════════════════════════════
    #  PAGE 5: CALENDAR PAGE
    # ══════════════════════════════════════════════════════════
    def _build_calendar_page(self):
        p = self.pages["Calendar"]
        p.rowconfigure(1, weight=1)
        p.columnconfigure(0, weight=1)

        hdr = tk.Frame(p, bg=CARD, height=45)
        hdr.grid(row=0, column=0, sticky="ew", pady=(0, 6))

        self.cal_title = tk.Label(hdr, text=f"📅  30-Day Forecast Calendar for {self.city}", font=self.fM, fg=TEXT1, bg=CARD)
        self.cal_title.pack(side="left", padx=16, pady=10)

        self.cal_grid = tk.Frame(p, bg=BG)
        self.cal_grid.grid(row=1, column=0, sticky="nsew")
        for i in range(7): self.cal_grid.columnconfigure(i, weight=1)
        for i in range(5): self.cal_grid.rowconfigure(i, weight=1)

    def _draw_calendar(self):
        self.cal_title.config(text=f"📅  30-Day Forecast Calendar for {self.city}")
        for w in self.cal_grid.winfo_children(): w.destroy()
        today = datetime.now()
        start = today - timedelta(days=today.weekday())

        for idx in range(35):
            r, c = idx//7, idx%7
            dt = start + timedelta(days=idx)
            card = self._mk_card(self.cal_grid, bg=ACTBG if dt.date() == today.date() else CARD)
            card.grid(row=r, column=c, sticky="nsew", padx=2, pady=2)

            day_str = dt.strftime("%d %b")
            hi_c = self._cur_temp + math.sin(idx)*4
            ic = get_icon("clear" if idx%3==0 else ("rain" if idx%5==0 else "clouds"))

            tk.Label(card, text=day_str, font=self.fSm, fg=TEXT2 if dt.date() != today.date() else TEXT1, bg=card["bg"]).pack(anchor="nw", padx=6, pady=4)
            tk.Label(card, text=ic, font=tkfont.Font(family="Segoe UI Emoji", size=16), bg=card["bg"]).pack()
            tk.Label(card, text=self.fmt_t(hi_c), font=self.fT, fg=TEXT1, bg=card["bg"]).pack(pady=(0,4))

    # ══════════════════════════════════════════════════════════
    #  PAGE 6: SAVED LOCATIONS PAGE
    # ══════════════════════════════════════════════════════════
    def _build_saved_page(self):
        p = self.pages["Saved"]
        p.rowconfigure(1, weight=1)
        p.columnconfigure(0, weight=1)

        hdr = tk.Frame(p, bg=CARD, height=45)
        hdr.grid(row=0, column=0, sticky="ew", pady=(0, 8))
        tk.Label(hdr, text="⭐  Saved Favorite Locations", font=self.fM, fg=TEXT1, bg=CARD).pack(side="left", padx=16, pady=10)

        self.saved_grid = tk.Frame(p, bg=BG)
        self.saved_grid.grid(row=1, column=0, sticky="nsew")
        for i in range(3): self.saved_grid.columnconfigure(i, weight=1)

    def _draw_saved_locations(self):
        for w in self.saved_grid.winfo_children(): w.destroy()
        if not self.favorites:
            tk.Label(self.saved_grid, text="No favorite locations saved yet.\nClick the ⭐ icon in the header to add locations!", font=self.fM, fg=TEXT2, bg=BG, justify="center").pack(expand=True)
            return

        for idx, cty in enumerate(self.favorites):
            r, c = idx//3, idx%3
            card = self._mk_card(self.saved_grid)
            card.grid(row=r, column=c, sticky="nsew", padx=6, pady=6)

            tk.Label(card, text=f"📍 {cty}", font=self.fM, fg=TEXT1, bg=CARD).pack(anchor="w", padx=16, pady=(14,2))
            tk.Label(card, text="Quick Weather Destination", font=self.fT, fg=TEXT2, bg=CARD).pack(anchor="w", padx=16)

            btn_box = tk.Frame(card, bg=CARD)
            btn_box.pack(anchor="e", padx=16, pady=12)

            btn_sw = tk.Button(btn_box, text="Switch to City", font=self.fSm, bg=ACTBG, fg=TEXT1, relief="flat", command=lambda x=cty: self._switch(x))
            btn_sw.pack(side="left", padx=4)

            btn_rm = tk.Button(btn_box, text="Remove ✕", font=self.fSm, bg=CARD2, fg=DANGER, relief="flat", command=lambda x=cty: self._remove_fav(x))
            btn_rm.pack(side="left", padx=2)

    def _remove_fav(self, city):
        if city in self.favorites:
            self.favorites.remove(city)
            self._update_fav_btn()
            self._draw_saved_locations()

    # ══════════════════════════════════════════════════════════
    #  PAGE 7: SETTINGS PAGE
    # ══════════════════════════════════════════════════════════
    def _build_settings_page(self):
        p = self.pages["Settings"]
        card = self._mk_card(p)
        card.pack(fill="both", expand=True, padx=10, pady=10)

        tk.Label(card, text="⚙  Dashboard Settings", font=self.fBg, fg=TEXT1, bg=CARD).pack(anchor="w", padx=20, pady=(20,10))
        tk.Label(card, text="Temperature Unit:", font=self.fM, fg=TEXT2, bg=CARD).pack(anchor="w", padx=20, pady=(10,2))
        
        ub_box = tk.Frame(card, bg=CARD)
        ub_box.pack(anchor="w", padx=20)
        self.btn_c = tk.Button(ub_box, text="Celsius (°C)", font=self.fS, bg=ACTBG if self.unit=="C" else CARD2, fg=TEXT1 if self.unit=="C" else TEXT2, relief="flat", padx=12, pady=4, command=lambda: self._set_unit("C"))
        self.btn_c.pack(side="left", padx=(0, 6))
        self.btn_f = tk.Button(ub_box, text="Fahrenheit (°F)", font=self.fS, bg=ACTBG if self.unit=="F" else CARD2, fg=TEXT1 if self.unit=="F" else TEXT2, relief="flat", padx=12, pady=4, command=lambda: self._set_unit("F"))
        self.btn_f.pack(side="left")

        tk.Label(card, text="OpenWeatherMap API Key:", font=self.fM, fg=TEXT2, bg=CARD).pack(anchor="w", padx=20, pady=(16,2))
        api_box = tk.Frame(card, bg=CARD)
        api_box.pack(anchor="w", padx=20)
        self.api_entry = tk.Entry(api_box, font=self.fS, fg=TEXT1, bg=CARD2, relief="flat", width=36)
        self.api_entry.pack(side="left", padx=(0, 6))
        self.api_entry.insert(0, self.api_key)
        
        tk.Button(api_box, text="Save Key", font=self.fS, bg=ACCENT, fg=BG, relief="flat", padx=10, pady=2, command=self._save_api_key).pack(side="left")

        self.api_status_lbl = tk.Label(card, text="", font=self.fT, fg=GREEN, bg=CARD)
        self.api_status_lbl.pack(anchor="w", padx=20, pady=(2, 0))

        tk.Label(card, text="Auto Refresh Rate:", font=self.fM, fg=TEXT2, bg=CARD).pack(anchor="w", padx=20, pady=(16,2))
        tk.Label(card, text="10 Minutes (Live background background update active)", font=self.fS, fg=GREEN, bg=CARD).pack(anchor="w", padx=20)

    def _set_unit(self, u):
        if self.unit != u:
            self._toggle_unit()

    def _save_api_key(self):
        v = self.api_entry.get().strip()
        if v:
            self.api_key = v
            self.api_status_lbl.config(text="✓ API Key saved! Refreshing weather data…")
            self._switch(self.city)
            self.root.after(3000, lambda: self.api_status_lbl.config(text=""))

    # ══════════════════════════════════════════════════════════
    #  DRAWING METHODS
    # ══════════════════════════════════════════════════════════
    def _draw_wx_icon(self):
        c=self.ic_cv; c.delete("all")
        W=c.winfo_width() or 200; H=c.winfo_height() or 120
        cx=int(W*0.38); cy=H//2+5
        t=self._wx_type
        if t=="clear":
            for g in range(5,0,-1):
                r=30+g*8; v=g*10
                c.create_oval(cx-r,cy-r,cx+r,cy+r,fill=f"#3a2{v:02x}00",outline="")
            c.create_oval(cx-32,cy-32,cx+32,cy+32,fill="#f5a623",outline="#ffcc44",width=2)
            c.create_oval(cx-20,cy-20,cx+20,cy+20,fill="#ffe066",outline="")
            for i in range(12):
                ang=math.radians(i*30+self._frame*1.5)
                r1=34; r2=46+(6 if i%3==0 else 0)
                c.create_line(cx+r1*math.cos(ang),cy+r1*math.sin(ang),
                              cx+r2*math.cos(ang),cy+r2*math.sin(ang),
                              fill="#f5a623",width=2 if i%3==0 else 1)
        elif t=="rain":
            self._cloud_shape(c,cx,cy-12,"#607888",1.2)
            for i in range(5):
                x=cx-28+i*14; y=cy+18
                c.create_line(x,y,x-4,y+20,fill="#7ab8d9",width=2)
        elif t=="thunder":
            self._cloud_shape(c,cx,cy-12,"#445566",1.2)
            for i in range(4):
                x=cx-20+i*14; y=cy+18
                c.create_line(x,y,x-3,y+14,fill="#607080",width=1)
            pts=[cx-4,cy+14,cx+8,cy+26,cx+2,cy+26,cx+12,cy+42]
            c.create_line(pts,fill="#fff176",width=3)
        elif t=="snow":
            self._cloud_shape(c,cx,cy-12,"#7080a0",1.2)
            for i in range(5):
                x=cx-28+i*14; y=cy+20+(4 if i%2 else 0)
                c.create_text(x,y,text="*",font=("Segoe UI",13,"bold"),fill="#a0c8ff")
        elif t=="mist":
            for i in range(5):
                y=cy-18+i*12; x1=cx-45+(i%2)*8; x2=cx+45-(i%2)*8
                v=50+i*8; c.create_line(x1,y,x2,y,fill=f"#{v:02x}{v+10:02x}{v+20:02x}",width=3)
        else:
            c.create_oval(cx+4,cy-24,cx+40,cy+12,fill="#f5a623",outline="")
            self._cloud_shape(c,cx-4,cy+5,"#8090a8",1.1)

        c.create_text(int(W*0.78),cy,text=self._wx_icon,
                      font=tkfont.Font(family="Segoe UI Emoji",size=38),
                      fill=TEXT1)

    def _cloud_shape(self,c,cx,cy,col,s=1.0):
        r=int(24*s)
        c.create_oval(cx-r,cy-r//2,cx+r,cy+r//2,fill=col,outline="")
        c.create_oval(cx-r//2-r,cy-r//3,cx-r//2+r,cy+r//2,fill=col,outline="")
        c.create_oval(cx+r//4-r,cy-r//2,cx+r//4+r,cy+r//2,fill=col,outline="")
        c.create_rectangle(cx-r-r//2,cy,cx+r+r//4,cy+r//2,fill=col,outline="")

    def _draw_temp_chart(self):
        c=self.temp_cv; c.delete("all")
        W=c.winfo_width() or 340; H=c.winfo_height() or 160
        if W<20 or H<20: return
        data=self._chart_temps
        if not data or len(data)<2: return
        disp_data = [self.fmt_t_val(d) for d in data]
        mn=min(disp_data)-4; mx=max(disp_data)+4; rng=mx-mn or 1
        n=len(disp_data); pad=36
        sp=(W-2*pad)/(n-1)
        xs=[int(pad+i*sp) for i in range(n)]
        ys=[int(H*0.12+(H*0.68)*(1-(d-mn)/rng)) for d in disp_data]
        labels=["Morning","Afternoon","Evening","Night"]

        poly=list(zip(xs,ys))+[(xs[-1],int(H*0.92)),(xs[0],int(H*0.92))]
        flat=[v for pt in poly for v in pt]
        c.create_polygon(flat,fill="#2a2458",outline="")

        for i in range(8):
            t=i/8; yb=int(min(ys)+(H*0.92-min(ys))*t)
            v=int(42+30*t); c.create_rectangle(xs[0],yb,xs[-1],yb+int(H/8),
                fill=f"#{v:02x}{int(v*0.85):02x}{min(255,v+50):02x}",outline="",stipple="gray50")

        lpts=[v for pt in zip(xs,ys) for v in pt]
        c.create_line(lpts,fill=ACCENT,width=2,smooth=True)

        for i,(x,y,d) in enumerate(zip(xs,ys,disp_data)):
            c.create_oval(x-8,y-8,x+8,y+8,fill="#322855",outline="")
            c.create_oval(x-4,y-4,x+4,y+4,fill=ACCENT,outline=CARD,width=1)
            c.create_text(x,y-16,text=f"{d:.0f}°",font=("Segoe UI",9,"bold"),fill=TEXT1)
            lbl=labels[i] if i<len(labels) else ""
            c.create_text(x,H-6,text=lbl,font=("Segoe UI",8),fill=TEXT2)

    def _draw_wind_wave(self):
        c=self.wind_cv; c.delete("all")
        W=c.winfo_width() or 260; H=c.winfo_height() or 50
        if W<10 or H<10: return
        spd=max(5,self._wind_disp)
        amp=min(H*0.35,spd*0.5)
        pts=[]; f=self._frame
        for x in range(0,W,4):
            y=H//2+amp*math.sin(x*0.04+f*0.1)
            pts.extend([x,int(y)])
        if len(pts)>=4:
            c.create_line(pts,fill=ACC2,width=1,smooth=True,dash=(4,4))
        pts2=[]
        for x in range(0,W,4):
            y=H//2+amp*math.sin(x*0.04+f*0.1+0.8)
            pts2.extend([x,int(y)])
        if len(pts2)>=4:
            c.create_line(pts2,fill=ACCENT,width=2,smooth=True)

    def _draw_gauge(self,key):
        cvmap={"rain":self.rain_cv,"uv":self.uv_cv,"cloud":self.cloud_cv}
        c=cvmap.get(key)
        if not c: return
        c.delete("all")
        W=c.winfo_width() or 120; H=c.winfo_height() or 90
        cx=W//2; cy=H//2; r=min(cx,cy)-10
        pct=self._gc.get(key,0)
        col={"rain":ACCENT,"uv":CYAN,"cloud":ACC2}.get(key,ACCENT)
        c.create_arc(cx-r,cy-r,cx+r,cy+r,start=90,extent=-360,style="arc",width=10,outline=BORD)
        if pct>0.5:
            ext=-int(360*pct/100)
            c.create_arc(cx-r,cy-r,cx+r,cy+r,start=90,extent=ext,style="arc",width=10,outline=col)
        c.create_text(cx,cy-4,text=f"+{int(pct)}%",font=("Segoe UI",12,"bold"),fill=TEXT1)

    def _draw_sky(self):
        c=self.sky; c.delete("all")
        W=self.root.winfo_width(); H=self.root.winfo_height()
        if W<10 or H<10: return
        city_now = datetime.now(timezone.utc) + timedelta(seconds=self.tz_offset)
        h=city_now.hour
        top,bot=sky_grad(h)
        r0,g0,b0=int(top[1:3],16),int(top[3:5],16),int(top[5:7],16)
        r1,g1,b1=int(bot[1:3],16),int(bot[3:5],16),int(bot[5:7],16)
        for i in range(30):
            t=i/30; r=int(r0+(r1-r0)*t); g=int(g0+(g1-g0)*t); b=int(b0+(b1-b0)*t)
            y0=int(H*i/30); y1=int(H*(i+1)/30)
            c.create_rectangle(0,y0,W,y1,fill=f"#{r:02x}{g:02x}{b:02x}",outline="")
        if h>=20 or h<6:
            if not self._stars:
                self._stars=[(random.randint(0,1400),random.randint(0,400),random.random()) for _ in range(120)]
            ph=self._frame*0.04
            for sx,sy,sp in self._stars:
                a=0.3+0.7*math.sin(ph+sp*9); br=int(80+175*a)
                hx=f"#{br:02x}{br:02x}{br:02x}"
                rv=1 if sp<0.5 else 2
                c.create_oval(sx-rv,sy-rv,sx+rv,sy+rv,fill=hx,outline="")
        else:
            self._stars=[]

    # ══════════════════════════════════════════════════════════
    #  DATA FETCH (API + Air Quality)
    # ══════════════════════════════════════════════════════════
    def _fetch(self,city):
        try:
            url=f"https://api.openweathermap.org/data/2.5/weather?q={city}&appid={self.api_key}&units=metric"
            d=requests.get(url,timeout=8).json()
            if d.get("cod")==200:
                self.root.after(0,lambda:self._wx_ui(d,city))
            else:
                self.root.after(0,lambda:self._wx_err(d.get("message","Not found")))
        except Exception as e:
            self.root.after(0,lambda:self._wx_err(str(e)))

        try:
            url2=f"https://api.openweathermap.org/data/2.5/forecast?q={city}&appid={self.api_key}&units=metric&cnt=40"
            d2=requests.get(url2,timeout=8).json()
            if str(d2.get("cod"))=="200":
                self.root.after(0,lambda:self._fc_ui(d2))
        except: pass

    def _wx_ui(self,d,city):
        tmp=d["main"]["temp"]; fl=d["main"]["feels_like"]
        hum=d["main"]["humidity"]; pres=d["main"]["pressure"]
        wnd=d["wind"]["speed"]*3.6; wdeg=d["wind"].get("deg",0)
        cld=d["clouds"]["all"]; cty=d["sys"].get("country","")
        self.lat=d["coord"]["lat"]; self.lon=d["coord"]["lon"]
        self.tz_offset = d.get("timezone", 0)
        self._feels_like = fl

        self._wx_type=classify(d["weather"][0]["description"])
        self._wx_icon=get_icon(d["weather"][0]["description"])
        self._cur_temp=tmp; self._wind_kmh=wnd

        # Match country case-insensitively
        city_lower = city.lower()
        for cname, cinfo in COUNTRIES.items():
            if any(c.lower() == city_lower for c in cinfo["cities"]):
                self.country = cname
                self.country_var.set(cname)
                self.city_cb.config(values=cinfo["cities"])
                matched_city = next(c for c in cinfo["cities"] if c.lower() == city_lower)
                self.city_var.set(matched_city)
                city = matched_city
                break

        self.city = city
        self._update_fav_btn()

        self.loc_lbl.config(text=f"📍  {city}, {self.fmt_t(tmp)}")
        self.city_lbl.config(text=f"{city}, {cty}")
        self.feel_lbl.config(text=f"Real feel  {self.fmt_t(fl)}")
        self.pres_lbl.config(text=f"{pres} hPa")
        self.hum_lbl.config(text=f"{hum} %")
        self.wnd_lbl.config(text=f"{wnd:.0f} km/h")
        self.wnd_kmh_lbl.config(text=f"{wnd:.0f} km/h  {wind_dir(wdeg)}")
        self._gt.update({"hum":hum,"wind":min(100,wnd*2),"cloud":cld})

        self._gt["uv"]=min(100,cld//1.2)
        self._gt["rain"]=min(100,hum*0.6)
        rain_lev="Low" if hum<50 else ("Moderate" if hum<75 else "High")
        uv_lev  ="Low" if cld>60  else ("Moderate" if cld>30 else "High")
        cld_lev ="High" if cld>60 else ("Moderate" if cld>30 else "Low")
        self.rain_badge.config(text=rain_lev,fg=CYAN if rain_lev=="Low" else WARM)
        self.uv_badge.config(text=uv_lev,   fg=GREEN if uv_lev=="Low"  else WARM)
        self.cloud_badge.config(text=cld_lev,fg=TEXT2 if cld_lev=="Low" else ACC2)

        self._draw_wx_icon()

        # Fetch Air Pollution asynchronously using lat/lon
        threading.Thread(target=self._fetch_aqi, args=(self.lat, self.lon), daemon=True).start()

        # Update active sub-pages
        if self.cur_page == "Maps": self._update_map_view()
        elif self.cur_page == "Charts": self._draw_extended_charts()
        elif self.cur_page == "Air Quality": self._draw_aqi_cards()
        elif self.cur_page == "Calendar": self._draw_calendar()
        elif self.cur_page == "Saved": self._draw_saved_locations()

    def _fetch_aqi(self, lat, lon):
        try:
            url = f"http://api.openweathermap.org/data/2.5/air_pollution?lat={lat}&lon={lon}&appid={self.api_key}"
            d = requests.get(url, timeout=5).json()
            if "list" in d and len(d["list"]) > 0:
                item = d["list"][0]
                comps = item.get("components", {})
                self._aqi_data = {
                    "aqi": item.get("main", {}).get("aqi", 2),
                    "pm2_5": comps.get("pm2_5", 12.4),
                    "pm10": comps.get("pm10", 24.1),
                    "no2": comps.get("no2", 18.2),
                    "o3": comps.get("o3", 45.0),
                    "so2": comps.get("so2", 4.1),
                    "co": comps.get("co", 210.0)
                }
                if self.cur_page == "Air Quality":
                    self.root.after(0, self._draw_aqi_cards)
        except Exception:
            pass

    def _wx_err(self,msg):
        self.city_lbl.config(text=f"⚠ {msg[:40]}")

    def _set_forecast_mode(self, mode):
        self.forecast_mode = mode
        for tab, btn in self.tab_btns.items():
            if tab == mode:
                btn.config(bg=ACTBG, fg=TEXT1)
            else:
                btn.config(bg=BG, fg=TEXT2)

        if hasattr(self, 'right_title_lbl'):
            titles = {"Daily": "Daily 24h Forecast", "Weekly": "This Week", "Monthly": "Monthly Overview"}
            self.right_title_lbl.config(text=titles.get(mode, "Forecast"))

        self._render_right_forecast()

    def _render_right_forecast(self):
        items = self._cached_forecast_items
        if not items:
            return

        if self.forecast_mode == "Daily":
            intervals = items[:8]
            slots = []
            for i, item in enumerate(intervals[:4]):
                dt = datetime.fromtimestamp(item["dt"])
                lbl = "Now" if i == 0 else dt.strftime("%I %p").lstrip("0")
                ic = get_icon(item["weather"][0]["description"])
                tmp = item["main"]["temp"]
                slots.append((lbl, ic, self.fmt_t(tmp)))
            self._upd_hourly(slots)

            for w in self.daily_frame.winfo_children(): w.destroy()
            for item in intervals:
                dt = datetime.fromtimestamp(item["dt"])
                t_str = dt.strftime("%I:%M %p").lstrip("0")
                desc = item["weather"][0]["description"].title()
                ic = get_icon(desc)
                tmp = item["main"]["temp"]
                pop = int(item.get("pop", 0) * 100)
                wnd = int(item.get("wind", {}).get("speed", 0) * 3.6)

                row = tk.Frame(self.daily_frame, bg=CARD)
                row.pack(fill="x", pady=2)

                left = tk.Frame(row, bg=CARD)
                left.pack(side="left")
                tk.Label(left, text=t_str, font=self.fLb, fg=TEXT1, bg=CARD, anchor="w", width=9).pack(anchor="w")
                tk.Label(left, text=f"🌧 {pop}%  🌬 {wnd}kph", font=self.fSm, fg=TEXT2, bg=CARD, anchor="w").pack(anchor="w")

                tk.Label(row, text=self.fmt_t(tmp), font=self.fM, fg=TEXT1, bg=CARD).pack(side="right", padx=4)
                tk.Label(row, text=ic, font=tkfont.Font(family="Segoe UI Emoji", size=16), bg=CARD).pack(side="right", padx=4)

        elif self.forecast_mode == "Monthly":
            hourly_data = items[:4]
            slots = []
            for i, item in enumerate(hourly_data):
                dt = datetime.fromtimestamp(item["dt"])
                lbl = "Now" if i == 0 else dt.strftime("%I %p").lstrip("0")
                ic = get_icon(item["weather"][0]["description"])
                tmp = item["main"]["temp"]
                slots.append((lbl, ic, self.fmt_t(tmp)))
            self._upd_hourly(slots)

            for w in self.daily_frame.winfo_children(): w.destroy()

            card_stats = tk.Frame(self.daily_frame, bg=CARD2)
            card_stats.pack(fill="x", pady=(0, 6), padx=2)
            tk.Label(card_stats, text="📊 Monthly Statistics", font=self.fM, fg=ACC2, bg=CARD2).pack(anchor="w", padx=10, pady=(6,2))
            
            s_row = tk.Frame(card_stats, bg=CARD2)
            s_row.pack(fill="x", padx=10, pady=(0,6))
            avg_temp = sum(x["main"]["temp"] for x in items) / len(items) if items else 22.0
            tk.Label(s_row, text=f"Avg Temp: {self.fmt_t(avg_temp, 1)}\nSunny Days: 22", font=self.fT, fg=TEXT1, bg=CARD2, justify="left").pack(side="left")
            tk.Label(s_row, text=f"Rainy Days: 8\nHumidity Avg: 65%", font=self.fT, fg=TEXT1, bg=CARD2, justify="left").pack(side="right")

            weeks = [
                ("Week 1 (1 - 7)", "☀ Sunny & Mild", f"{self.fmt_t(24)} / {self.fmt_t(15)}"),
                ("Week 2 (8 - 14)", "🌧 Scattered Rain", f"{self.fmt_t(21)} / {self.fmt_t(13)}"),
                ("Week 3 (15 - 21)", "⛅ Partly Cloudy", f"{self.fmt_t(25)} / {self.fmt_t(16)}"),
                ("Week 4 (22 - 30)", "🌤 Warm & Clear", f"{self.fmt_t(27)} / {self.fmt_t(18)}")
            ]
            for wk, desc, t_range in weeks:
                row = tk.Frame(self.daily_frame, bg=CARD)
                row.pack(fill="x", pady=3)
                left = tk.Frame(row, bg=CARD)
                left.pack(side="left")
                tk.Label(left, text=wk, font=self.fLb, fg=TEXT1, bg=CARD, anchor="w").pack(anchor="w")
                tk.Label(left, text=desc, font=self.fSm, fg=TEXT2, bg=CARD, anchor="w").pack(anchor="w")
                tk.Label(row, text=t_range, font=self.fS, fg=WARM, bg=CARD).pack(side="right", padx=6)

        else: # Weekly
            hourly_data = items[:4]
            slots = []
            for i, item in enumerate(hourly_data):
                dt = datetime.fromtimestamp(item["dt"])
                lbl = "Now" if i == 0 else dt.strftime("%I %p").lstrip("0")
                ic = get_icon(item["weather"][0]["description"])
                tmp = item["main"]["temp"]
                slots.append((lbl, ic, self.fmt_t(tmp)))
            self._upd_hourly(slots)

            daily_map = {}
            for item in items:
                key = datetime.fromtimestamp(item["dt"]).strftime("%Y-%m-%d")
                if key not in daily_map: daily_map[key] = []
                daily_map[key].append(item)
            today = datetime.now().strftime("%Y-%m-%d")
            future = [(k, v) for k, v in daily_map.items() if k >= today][:5]
            daily_info = []
            for k, v in future:
                dt = datetime.strptime(k, "%Y-%m-%d")
                hi = max(x["main"]["temp"] for x in v)
                lo = min(x["main"]["temp"] for x in v)
                ic = get_icon(v[len(v)//2]["weather"][0]["description"])
                daily_info.append((dt.strftime("%A"), dt.strftime("%d %b"), hi, lo, ic))
            self._upd_daily(daily_info)

    def _fc_ui(self,d):
        items=d.get("list",[])
        self._cached_forecast_items = items
        if items:
            self._chart_temps=[item["main"]["temp"] for item in items[:4]]

        self.root.after(0, self._render_right_forecast)
        self.root.after(0, self._draw_temp_chart)

    def _upd_hourly(self,slots):
        for w in self.hourly_frame.winfo_children(): w.destroy()
        for i,(lbl,ic,tmp) in enumerate(slots):
            col=ACTBG if i==0 else CARD2
            fc=tk.Frame(self.hourly_frame,bg=col,bd=0)
            fc.pack(side="left",expand=True,fill="y",padx=3,pady=2)
            tk.Label(fc,text=lbl,font=self.fSm,fg=TEXT1 if i==0 else TEXT2,bg=col).pack(pady=(8,2))
            tk.Label(fc,text=ic,font=tkfont.Font(family="Segoe UI Emoji",size=18),bg=col).pack()
            tk.Label(fc,text=tmp,font=self.fT,fg=TEXT1,bg=col).pack(pady=(2,8))

    def _upd_daily(self,daily_info):
        for w in self.daily_frame.winfo_children(): w.destroy()
        for day,date,hi,lo,ic in daily_info:
            row=tk.Frame(self.daily_frame,bg=CARD)
            row.pack(fill="x",pady=4)
            left=tk.Frame(row,bg=CARD); left.pack(side="left")
            tk.Label(left,text=day,font=self.fLb,fg=TEXT1,bg=CARD,anchor="w",width=12).pack(anchor="w")
            tk.Label(left,text=date,font=self.fSm,fg=TEXT2,bg=CARD,anchor="w").pack(anchor="w")
            tk.Label(row,text=self.fmt_t(hi),font=self.fM,fg=TEXT1,bg=CARD).pack(side="right",padx=4)
            tk.Label(row,text=ic,font=tkfont.Font(family="Segoe UI Emoji",size=20),bg=CARD).pack(side="right",padx=6)

    # ══════════════════════════════════════════════════════════
    #  CLOCK TICK & ANIMATIONS
    # ══════════════════════════════════════════════════════════
    def _tick(self):
        city_now = datetime.now(timezone.utc) + timedelta(seconds=self.tz_offset)
        self.time_lbl.config(text=city_now.strftime("%H:%M:%S"))
        self.date_lbl.config(text=city_now.strftime("%d %B, %Y"))

        diff=self._cur_temp-self._disp_temp
        if abs(diff)>0.05:
            self._disp_temp+=diff*0.12
            self.temp_lbl.config(text=self.fmt_t(self._disp_temp, 1),fg=temp_color(self._disp_temp))
        else:
            self._disp_temp=self._cur_temp
            self.temp_lbl.config(text=self.fmt_t(self._disp_temp, 1),fg=temp_color(self._disp_temp))

        wd=self._wind_kmh-self._wind_disp
        if abs(wd)>0.1: self._wind_disp+=wd*0.1
        else: self._wind_disp=self._wind_kmh

        self.root.after(100,self._tick)

    def _anim(self):
        self._frame+=1
        if self.cur_page == "Dashboard":
            self._draw_sky()
            self._draw_wind_wave()
            self._draw_wx_icon()

            for k in self._gc:
                diff=self._gt[k]-self._gc[k]
                if abs(diff)>0.3: self._gc[k]+=diff*0.1
                else: self._gc[k]=self._gt[k]
            for k in ("rain","uv","cloud"): self._draw_gauge(k)

        self.root.after(50,self._anim)

    # ══════════════════════════════════════════════════════════
    #  SEARCH & SWITCH
    # ══════════════════════════════════════════════════════════
    def _switch(self,city):
        self.city=city
        self.city_lbl.config(text=f"Loading {city}…")
        self.loc_lbl.config(text=f"📍  {city}, --")
        threading.Thread(target=self._fetch,args=(city,),daemon=True).start()

    def _search(self):
        v=self.sv.get().strip()
        if v and "Search" not in v: self._switch(v)

    def _clr_ph(self):
        if "Search" in self.sv.get():
            self.se.delete(0,"end"); self.se.config(fg=TEXT1)

    def _rst_ph(self):
        if not self.sv.get():
            self.se.insert(0,"Search location, city or place…")
            self.se.config(fg=TEXT2)

    def _loops(self):
        self.root.after(120,self._anim)
        self.root.after(200,self._tick)
        self.root.after(500,lambda:self._switch("New York"))
        self._auto_refresh()

    def _auto_refresh(self):
        threading.Thread(target=self._fetch,args=(self.city,),daemon=True).start()
        self.root.after(600_000,self._auto_refresh)

    def run(self): self.root.mainloop()


if __name__=="__main__":
    WeatherNow().run()
