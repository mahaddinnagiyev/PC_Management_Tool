from tkinter import *
from tkinter import ttk
from tkinter import ttk, messagebox
import tkinter as tk
from tkinter import filedialog
import platform
import psutil
from PIL import Image, ImageTk

# Brightness
import screen_brightness_control as pct

# Audio
from ctypes import cast, POINTER
from comtypes import CLSCTX_ALL
from pycaw.pycaw import AudioUtilities, IAudioEndpointVolume

# Weather
from datetime import datetime
import requests

# Clock
from time import strftime

# Calendar
from tkcalendar import *

# Google
import pyautogui

import subprocess
import webbrowser as wb

class App(tk.Tk):

    def __init__(self):
        super().__init__()
        
        # Title
        self.title('PC-Soft Tool')

        # Size and Position 
        self.geometry('500x300')
        self.resizable(False, False)
        self.configure(bg='#292e2e')

        screen_width = 1000
        screen_height = 600

        user_screen_width = self.winfo_screenwidth()
        user_screen_height = self.winfo_screenheight()

        middle_x = int((user_screen_width / 2) - (screen_width / 2))
        middle_y = int((user_screen_height / 2) - (screen_height / 2))

        self.geometry(f"{screen_width}x{screen_height}+{middle_x}+{middle_y}")
        self.resizable(False, False)
        self.configure(bg='#292e2e')

        # Icon
        image_icon = PhotoImage(file="images/icon_logo.png")
        self.iconphoto(True, image_icon)    

        self.Body = Frame(self, width=1000, height=600, bg="#d6d6d6")
        self.Body.pack(padx=20, pady=20)

        ########################### LEFT HAND SIDE ###########################
        self.LHS=Frame(self.Body, width=400, height=540, bg="#f4f5f5", highlightbackground="#adacb1", highlightthickness=1)
        self.LHS.place(x=10, y=10)

        # Logo
        my_system = platform.uname()

        if my_system.system == "Windows":
            image_path = "images/windows.png"
        else: 
            image_path = "images/macbook.png"
            
        resized_image = Image.open(image_path).resize((330, 200), Image.Resampling.LANCZOS)
        photo = ImageTk.PhotoImage(resized_image)
        self.my_image = Label(self.LHS, image=photo, background="#f4f5f5")
        self.my_image.image = photo
        self.my_image.place(x=30, y=30)

        l1 = Label(self.LHS, text=f"Device Name: {my_system.node}", bg="#f4f5f5", font=("Acumin Variable Concept", 15, "bold"), justify="center")
        l1.place(x=20, y=260)

        l2 = Label(self.LHS, text=f"Version: {my_system.version}", bg="#f4f5f5", font=("Acumin Variable Concept", 8, "bold"), justify="center")
        l2.place(x=20, y=290)

        l3 = Label(self.LHS, text=f"System: {my_system.system}", bg="#f4f5f5", font=("Acumin Variable Concept", 15, "bold"), justify="center")
        l3.place(x=20, y=320)

        l4 = Label(self.LHS, text=f"Machine: {my_system.machine}", bg="#f4f5f5", font=("Acumin Variable Concept", 12, "bold"), justify="center")
        l4.place(x=20, y=355)

        l5 = Label(self.LHS, text=f"Total RAM Installed: {round(psutil.virtual_memory().total / 1000000000, 2)} GB", bg="#f4f5f5", font=("Acumin Variable Concept", 12, "bold"), justify="center")
        l5.place(x=20, y=390)

        l6 = Label(self.LHS, text=f"Processor: {my_system.processor}", bg="#f4f5f5", font=("Acumin Variable Concept", 7, "bold"), justify="center", wraplength=390)
        l6.place(x=20, y=420)

        #######################################################################

        ########################### RIGHT HAND SIDE ###########################

        RHS=Frame(self.Body, width=520, height=260, bg="#f4f5f5", highlightbackground="#adacb1", highlightthickness=1)
        RHS.place(x=430, y=10)

        system = Label(RHS, text="System", font=("Acumin Variable Concept", 15), bg="#f4f5f5")
        system.place(x=10, y=10)

        # Batery
        def convertTime(seconds):
            minutes, seconds = divmod(seconds, 60)
            hours, minutes = divmod(minutes, 60)
            return f"{hours}:{minutes:02}:{seconds:02}"

        self.button_mode = True

        def none():

            global battery_png
            global battery_label

            battery = psutil.sensors_battery()
            percent = battery.percent

            time = convertTime(battery.secsleft)

            lbl.config(text=f"{percent}%")
            lbl_plug.config(text=f"Plug in: {str(battery.power_plugged)}")
            lbl_time.config(text=f"{time} remaining")

            battery_label = Label(RHS, background="#f4f5f5")
            battery_label.place(x=15, y=50)

            lbl.after(1000, none)

            if battery.power_plugged == True:
                battery_image_path = "images/battery-low-icon.png"

            else:
                battery_image_path = "images/battery-level-full-icon.png"

            resized_image = Image.open(battery_image_path).resize((100, 80), Image.Resampling.LANCZOS)
            
            battery_png = ImageTk.PhotoImage(resized_image)
            
            if self.button_mode:
                battery_label.config(image=battery_png, bg="#f4f5f5")
            else:
                battery_label.config(image=battery_png, bg="#292e2e")


        lbl=Label(RHS, font=("Acumin Variable Concept", 40, "bold"), bg="#f4f5f5")
        lbl.place(x=200, y=40)

        lbl_plug=Label(RHS, font=("Acumin Variable Concept", 10, "bold"), bg="#f4f5f5")
        lbl_plug.place(x=20, y=135)

        lbl_time=Label(RHS, font=("Acumin Variable Concept", 15), bg="#f4f5f5")
        lbl_time.place(x=200, y=130)

        none()

        # Speaker 
        lbl_speaker = Label(RHS, text="Speaker:", font=("Arial", 10, "bold"), bg="#f4f5f5")
        lbl_speaker.place(x=10, y=180)

        volume_value = tk.DoubleVar()

        def get_current_volume_value():
            return '{:.2f}'.format(volume_value.get())

        def volume_changed(e):
            device = AudioUtilities.GetSpeakers()
            interface = device.Activate(IAudioEndpointVolume._iid_, CLSCTX_ALL, None)
            volume = cast(interface, POINTER(IAudioEndpointVolume))
            volume.SetMasterVolumeLevelScalar(float(get_current_volume_value()) / 100, None)

        try:
            device = AudioUtilities.GetSpeakers()
            interface = device.Activate(IAudioEndpointVolume._iid_, CLSCTX_ALL, None)
            volume = cast(interface, POINTER(IAudioEndpointVolume))
            current_volume = volume.GetMasterVolumeLevelScalar() * 100  
        except Exception as e:
            current_volume = 50  

        volume_value.set(current_volume)

        style = ttk.Style()
        style.configure("TScale", background="#f4f5f5")

        volume = ttk.Scale(RHS, from_=0, to=100, orient="horizontal", command=volume_changed, variable=volume_value)
        volume.place(x=115, y=180)
        volume.set(current_volume)

        # Brightness
        lbl_brightness = Label(RHS, text="Brightness: ", font=("Arial", 10, "bold"), bg="#f4f5f5")
        lbl_brightness.place(x=10, y=220)

        current_value = tk.DoubleVar()

        def get_current_value():
            return '{:.2f}'.format(current_value.get())

        def brightness_change(e):
            pct.set_brightness(int(float(get_current_value()))) 

        try:
            initial_brightness = pct.get_brightness()[0] 
        except Exception as e:
            initial_brightness = 50 

        current_value.set(initial_brightness)

        brightness = ttk.Scale(RHS, from_=0, to=100, orient="horizontal", command=brightness_change, variable=current_value)
        brightness.place(x=115, y=220)
        brightness.set(initial_brightness)

        #########################################################################

        ########################### RIGHT HAND BOTTOM ###########################

        RHB=Frame(self.Body, width=520, height=255, bg="#f4f5f5", highlightbackground="#adacb1", highlightthickness=1)
        RHB.place(x=430, y=295)

        def weather():
            app1=Toplevel()

            app1_middle_x = int((self.winfo_screenwidth() / 2) - 425)
            app1_middle_y = int((self.winfo_screenheight() / 2) - 250)

            app1.geometry(f"850x500+{app1_middle_x}+{app1_middle_y}")
            app1.title('Weather')
            app1.configure(bg="#f4f5f5")
            app1.resizable(False, False)

            # App 1 Icon
            image_icon = PhotoImage(file="images/weather.png")
            app1.iconphoto(False, image_icon)

            def getWeather():
                try:
                    city = text_field.get()
                    if not city:
                        messagebox.showerror("Weather App", "City name cannot be empty!")
                        return

                    api_key = "44c6461c3d16456fb1c222807242712"
                    url = f"http://api.weatherapi.com/v1/current.json?key={api_key}&q={city}"

                    response = requests.get(url)
                    data = response.json()

                    if response.status_code != 200:
                        messagebox.showerror("Weather App", f"Error: {data.get('error', {}).get('message', 'Unknown error')}")
                        return

                    # Extract weather data
                    temp_c = data["current"]["temp_c"]
                    wind_kph = data["current"]["wind_kph"]
                    humidity = data["current"]["humidity"]
                    condition = data["current"]["condition"]["text"]
                    pressure_mb = data["current"]["pressure_mb"]

                    # Update labels
                    t.config(text=f"{temp_c}°C")
                    w.config(text=f"{wind_kph} km/h")
                    h.config(text=f"{humidity}%")
                    d.config(text=condition)
                    p.config(text=f"{pressure_mb} mb")

                    # Update the time
                    clock.config(text=f"{datetime.now().strftime('%I:%M %p')}")
                    name.config(text=f"Weather in {data["location"]["region"]}")

                except Exception as e:
                    messagebox.showerror("Weather App", f"An error occurred: {str(e)}")

            # search box
            search_image = PhotoImage(file="images/searchbar.png")
            myImage = Label(app1, image=search_image, bg="#f4f5f5")
            myImage.place(x=20, y=20)

            text_field = tk.Entry(app1, justify="center", width=17, font=("Poppins", 25, 'bold'), bg="#404040", border=0, fg="white")
            text_field.place(x=50, y=40),
            text_field.focus()

            search_icon_path = "images/search.png"
            search_icon_resize_image = Image.open(search_icon_path).resize((49, 49), Image.Resampling.LANCZOS)
            search_icon = ImageTk.PhotoImage(search_icon_resize_image)
            myImage_icon = Button(app1, image=search_icon, borderwidth=0, cursor="hand2", bg="#404040", command=getWeather)
            myImage_icon.place(x=400, y=40)
            myImage_icon.bind("<Return>", lambda event: getWeather())

            # Logo
            logo_image_path = "images/weather.png"
            logo_resize_image = Image.open(logo_image_path).resize((170, 170), Image.Resampling.LANCZOS)
            logo_image = ImageTk.PhotoImage(logo_resize_image)
            logo = Label(app1, image=logo_image, bg="#f4f5f5")
            logo.place(x=150, y=150)

            # Bottom box
            frame_image_path = "images/box.png"
            frame_resize_image = Image.open(frame_image_path).resize((1000, 175), Image.Resampling.LANCZOS)
            frame_image = ImageTk.PhotoImage(frame_resize_image)
            frame_myImage = Label(app1, image=frame_image, bg="#f4f5f5")
            frame_myImage.pack(padx=(50, 0), pady=5, side=BOTTOM)

            # Time
            name = Label(app1, font=("Arial", 15, "bold"), bg="#f4f5f5")
            name.place(x=30, y=100)
            clock = Label(app1, font=("Helvetica", 20), bg="#f4f5f5")
            clock.place(x=30, y=130)

            # Temperature
            label = Label(app1, text="Temperature", font=("Helvetica", 15, "bold"), bg="#232C40", fg="White")
            label.place(x=450, y=130)

            t = Label(app1, font=("Arial", 20, "bold"), bg="#f4f5f5")
            t.place(x=450, y=170)

            # Wind
            label1 = Label(app1, text="Wind", font=("Helvetica", 15, "bold"), bg="#232C40", fg="White")
            label1.place(x=120, y=375)

            w = Label(app1, font=("Arial", 11, "bold"), fg="White", bg="#232C40")
            w.place(x=125, y=410)

            # Humidity
            label2 = Label(app1, text="Humidity", font=("Helvetica", 15, "bold"), bg="#232C40", fg="White")
            label2.place(x=250, y=375)

            h = Label(app1, font=("Arial", 11, "bold"), fg="White", bg="#232C40")
            h.place(x=255, y=410)

            # Description
            label3 = Label(app1, text="Description", font=("Helvetica", 15, "bold"), bg="#232C40", fg="White")
            label3.place(x=430, y=375)

            d = Label(app1, font=("Arial", 11, "bold"), fg="White", bg="#232C40")
            d.place(x=435, y=410)

            # Pressure
            label4 = Label(app1, text="Pressure", font=("Helvetica", 15, "bold"), bg="#232C40", fg="White")
            label4.place(x=650, y=375)

            p = Label(app1, font=("Arial", 11, "bold"), fg="White", bg="#232C40")
            p.place(x=655, y=410)

            app1.mainloop()

        def clock():
            app2 = Toplevel()

            app2_middle_x = int((self.winfo_screenwidth() / 2) - 425)
            app2_middle_y = int((self.winfo_screenheight() / 2) - 55)

            app2.geometry(f"850x110+{app2_middle_x}+{app2_middle_y}")

            app2.title("Clock")
            app2.configure(bg="#292e2e")
            app2.resizable(False, False)

            # Icon
            image_icon = PhotoImage(file="images/icons8-clock-128.png")
            app2.iconphoto(False, image_icon)

            def clock():
                text = strftime('%H:%M:%S %p')
                lbl.config(text=text)
                lbl.after(1000, clock)

            lbl = Label(app2, font=("Digital-7", 50), width=20, bg="#f4f5f5", fg="#292e2e")
            lbl.pack(anchor="center", pady=20)
            clock()

            app2.mainloop()

        def calendar():
            app3 = Toplevel()

            app3_middle_x = int((self.winfo_screenwidth() / 2) - 150)
            app3_middle_y = int((self.winfo_screenheight() / 2) - 150)

            app3.geometry(f"300x300+{app3_middle_x}+{app3_middle_y}")
            app3.configure(bg="#292e2e")
            app3.resizable(False, False)

            # Icon
            image_icon = PhotoImage(file="images/pngwing.com.png")
            app3.iconphoto(False, image_icon)

            my_cal = Calendar(app3, selectmode="day", date_pattern="d/m/yy")
            my_cal.pack(padx=15, pady=35)

            app3.title("Calendar")

        def mode():
            if self.button_mode:
                self.LHS.config(bg="#292e2e")
                self.my_image.config(bg="#292e2e")
                l1.config(bg="#292e2e", fg="#d6d6d6")
                l2.config(bg="#292e2e", fg="#d6d6d6")
                l3.config(bg="#292e2e", fg="#d6d6d6")
                l4.config(bg="#292e2e", fg="#d6d6d6")
                l5.config(bg="#292e2e", fg="#d6d6d6")
                l6.config(bg="#292e2e", fg="#d6d6d6")

                RHB.config(bg="#292e2e")
                self.app1.config(bg="#292e2e")
                self.app2.config(bg="#292e2e")
                self.app3.config(bg="#292e2e")
                self.app4.config(bg="#292e2e")
                self.app5.config(bg="#292e2e")
                self.app6.config(bg="#292e2e")
                self.app7.config(bg="#292e2e")
                self.app8.config(bg="#292e2e")
                self.app9.config(bg="#292e2e")
                self.app10.config(bg="#292e2e")
                self.apps.config(bg="#292e2e", fg="#d6d6d6")

                RHS.config(bg="#292e2e")
                system.config(bg="#292e2e", fg="#d6d6d6")
                lbl.config(bg="#292e2e", fg="#d6d6d6")
                lbl_plug.config(bg="#292e2e", fg="#d6d6d6")
                lbl_time.config(bg="#292e2e", fg="#d6d6d6")
                lbl_speaker.config(bg="#292e2e", fg="#d6d6d6")
                lbl_brightness.config(bg="#292e2e", fg="#d6d6d6")
                battery_label.config(bg="#292e2e", fg="#d6d6d6")

                self.button_mode = False

            else:
                self.LHS.config(bg="#f4f5f5")
                self.my_image.config(bg="#f4f5f5")

                l1.config(bg="#f4f5f5", fg="#292e2e")
                l2.config(bg="#f4f5f5", fg="#292e2e")
                l3.config(bg="#f4f5f5", fg="#292e2e")
                l4.config(bg="#f4f5f5", fg="#292e2e")
                l5.config(bg="#f4f5f5", fg="#292e2e")
                l6.config(bg="#f4f5f5", fg="#292e2e")

                RHB.config(bg="#f4f5f5")
                self.app1.config(bg="#f4f5f5")
                self.app2.config(bg="#f4f5f5")
                self.app3.config(bg="#f4f5f5")
                self.app4.config(bg="#f4f5f5")
                self.app5.config(bg="#f4f5f5")
                self.app6.config(bg="#f4f5f5")
                self.app7.config(bg="#f4f5f5")
                self.app8.config(bg="#f4f5f5")
                self.app9.config(bg="#f4f5f5")
                self.app10.config(bg="#f4f5f5")
                self.apps.config(bg="#f4f5f5", fg="#292e2e")

                RHS.config(bg="#f4f5f5")
                system.config(bg="#f4f5f5", fg="#292e2e")
                lbl.config(bg="#f4f5f5", fg="#292e2e")
                lbl_plug.config(bg="#f4f5f5", fg="#292e2e")
                lbl_time.config(bg="#f4f5f5", fg="#292e2e")
                lbl_speaker.config(bg="#f4f5f5", fg="#292e2e")
                lbl_brightness.config(bg="#f4f5f5", fg="#292e2e")
                battery_label.config(bg="#f4f5f5")

                self.button_mode = True

        def folder():
            subprocess.Popen(r'explorer /select, "C:\path\of\foler\file"')

        def google():
            wb.register('chrome', None)
            wb.open('https://www.google.com/')

        def github():
            wb.register('chrome', None)
            wb.open('https://github.com/mahaddinnagiyev')

        def web():
            wb.register('chrome', None)
            wb.open('https://mahaddinnagiyev.netlify.app/')

        def close_app():
            self.destroy()

        def screenshot():
            self.iconify()

            my_screenshot = pyautogui.screenshot()
            file_path = filedialog.asksaveasfilename(defaultextension=".png", filetypes=[("PNG", "*.png")])
            my_screenshot.save(file_path)

        self.apps = Label(RHB, text="Apps", font=("Acumin Variable Concept" ,15), bg="#f4f5f5")
        self.apps.place(x=10, y=10)

        self.app1_image_path = "images/weather.png"
        self.app1_resize_image = Image.open(self.app1_image_path).resize((70, 70), Image.Resampling.LANCZOS)
        self.app1_image = ImageTk.PhotoImage(self.app1_resize_image)
        self.app1 = Button(RHB, image=self.app1_image, bd=0, command=weather, cursor="hand2", background="#f4f5f5")
        self.app1.place(x=15, y=65)

        self.app2_image_path = "images/icons8-clock-128.png"
        self.app2_resize_image = Image.open(self.app2_image_path).resize((70, 70), Image.Resampling.LANCZOS)
        self.app2_image = ImageTk.PhotoImage(self.app2_resize_image)
        self.app2 = Button(RHB, image=self.app2_image, bd=0, cursor="hand2", background="#f4f5f5", command=clock)
        self.app2.place(x=115, y=65)

        self.app3_image_path = "images/pngwing.com.png"
        self.app3_resize_image = Image.open(self.app3_image_path).resize((70, 70), Image.Resampling.LANCZOS)
        self.app3_image = ImageTk.PhotoImage(self.app3_resize_image)
        self.app3 = Button(RHB, image=self.app3_image, bd=0, cursor="hand2", background="#f4f5f5", command=calendar)
        self.app3.place(x=215, y=65)

        self.app4_image_path = "images/change-theme.png"
        self.app4_resize_image = Image.open(self.app4_image_path).resize((70, 70), Image.Resampling.LANCZOS)
        self.app4_image = ImageTk.PhotoImage(self.app4_resize_image)
        self.app4 = Button(RHB, image=self.app4_image, bd=0, cursor="hand2", background="#f4f5f5", command=mode)
        self.app4.place(x=313, y=65)

        self.app5_image_path = "images/camera.png"
        self.app5_resize_image = Image.open(self.app5_image_path).resize((70, 70), Image.Resampling.LANCZOS)
        self.app5_image = ImageTk.PhotoImage(self.app5_resize_image)
        self.app5 = Button(RHB, image=self.app5_image, bd=0, cursor="hand2", background="#f4f5f5", command=screenshot)
        self.app5.place(x=414, y=65)

        self.app6_image_path = "images/folder.png"
        self.app6_resize_image = Image.open(self.app6_image_path).resize((70, 70), Image.Resampling.LANCZOS)
        self.app6_image = ImageTk.PhotoImage(self.app6_resize_image)
        self.app6 = Button(RHB, image=self.app6_image, bd=0, cursor="hand2", background="#f4f5f5", command=folder)
        self.app6.place(x=15, y=160)

        self.app7_image_path = "images/google.png"
        self.app7_resize_image = Image.open(self.app7_image_path).resize((70, 70), Image.Resampling.LANCZOS)
        self.app7_image = ImageTk.PhotoImage(self.app7_resize_image)
        self.app7 = Button(RHB, image=self.app7_image, bd=0, cursor="hand2", background="#f4f5f5", command=google)
        self.app7.place(x=115, y=160)

        self.app8_image_path = "images/github.png"
        self.app8_resize_image = Image.open(self.app8_image_path).resize((70, 70), Image.Resampling.LANCZOS)
        self.app8_image = ImageTk.PhotoImage(self.app8_resize_image)
        self.app8 = Button(RHB, image=self.app8_image, bd=0, cursor="hand2", background="#f4f5f5", command=github)
        self.app8.place(x=215, y=160)

        self.app9_image_path = "images/web.png"
        self.app9_resize_image = Image.open(self.app9_image_path).resize((70, 70), Image.Resampling.LANCZOS)
        self.app9_image = ImageTk.PhotoImage(self.app9_resize_image)
        self.app9 = Button(RHB, image=self.app9_image, bd=0, cursor="hand2", background="#f4f5f5", command=web)
        self.app9.place(x=313, y=160)

        self.app10_image_path = "images/power.png"
        self.app10_resize_image = Image.open(self.app10_image_path).resize((70, 70), Image.Resampling.LANCZOS)
        self.app10_image = ImageTk.PhotoImage(self.app10_resize_image)
        self.app10 = Button(RHB, image=self.app10_image, bd=0, cursor="hand2", background="#f4f5f5", command=close_app)
        self.app10.place(x=414, y=160)

        ##########################################################################

app = App()
app.mainloop()
