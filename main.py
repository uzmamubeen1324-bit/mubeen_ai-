import os
import sys
import time
import socket
import threading
import urllib.request
import math
import tkinter as tk
from tkinter import ttk
import pyautogui
import speech_recognition as sr
import pyttsx3

GITHUB_RAW_URL = "https://githubusercontent.com"

class AnimatedMubeenUI:
    def __init__(self, root, engine_bridge):
        self.root = root
        self.bridge = engine_bridge
        self.root.title("Mubeen AI Operator")
        
        # Window Canvas Config
        self.root.geometry("320x460+50+50")
        self.root.overrideredirect(True)
        self.root.attributes("-topmost", True)
        self.root.config(bg="#0d1117")
        self.root.wm_attributes("-alpha", 0.95)
        
        # Custom Title Bar
        self.title_bar = tk.Frame(self.root, bg="#161b22", relief="raised", height=30)
        self.title_bar.pack(side="top", fill="x")
        self.title_bar.bind("<Button-1>", self.start_drag)
        self.title_bar.bind("<B1-Motion>", self.drag_window)
        
        title_label = tk.Label(self.title_bar, text="🤖 MUBEEN AI (GLOBE SYNC)", fg="#58a6ff", bg="#161b22", font=("Consolas", 10, "bold"))
        title_label.pack(side="left", padx=10)
        
        close_btn = tk.Button(self.title_bar, text="×", fg="#f85149", bg="#161b22", borderwidth=0, font=("Arial", 12, "bold"), command=self.root.quit)
        close_btn.pack(side="right", padx=10)

        # Main Interface Canvas
        self.canvas = tk.Canvas(self.root, width=300, height=340, bg="#0d1117", highlightthickness=0)
        self.canvas.pack(pady=10)
        
        # Cyber Robot face structures
        self.bot_glow = self.canvas.create_oval(70, 20, 230, 180, fill="", outline="#1f6feb", width=2)
        self.bot_head = self.canvas.create_oval(80, 30, 220, 170, fill="#161b22", outline="#58a6ff", width=4)
        self.eye_left = self.canvas.create_oval(110, 80, 135, 105, fill="#58a6ff", outline="")
        self.eye_right = self.canvas.create_oval(165, 80, 190, 105, fill="#58a6ff", outline="")
        self.visor_line = self.canvas.create_line(120, 130, 180, 130, fill="#58a6ff", width=3)
        
        # --- NEW FEAT: CYBER VOICE TYPE GLOBE ICON ---
        # Base Audio Globe Circle Base (Hologram Outer Shell)
        self.globe_base = self.canvas.create_oval(115, 210, 185, 280, fill="#161b22", outline="#8b949e", width=1, dash=(4,4))
        self.globe_core = self.canvas.create_oval(125, 220, 175, 270, fill="#0d1117", outline="#58a6ff", width=2)
        
        # Audio Wave Bars inside the Voice Globe Ring
        self.wave_bars = []
        for i in range(5):
            bar = self.canvas.create_line(135 + (i*7), 245, 135 + (i*7), 245, fill="#58a6ff", width=3)
            self.wave_bars.append(bar)
            
        self.status_text = tk.Label(self.root, text="System Online", fg="#8b949e", bg="#0d1117", font=("Consolas", 11))
        self.status_text.pack(pady=5)
        
        self.pulse_dir = 1
        self.pulse_val = 0
        self.wave_time = 0
        self._x = 0
        self._y = 0
        self.animate_loop()

    def start_drag(self, event):
        self._x = event.x
        self._y = event.y

    def drag_window(self, event):
        deltax = event.x - self._x
        deltay = event.y - self._y
        x = self.root.winfo_x() + deltax
        y = self.root.winfo_y() + deltay
        self.root.geometry(f"+{x}+{y}")

    def update_status(self, text, color="#58a6ff"):
        self.status_text.config(text=text, fg=color)

    def animate_loop(self):
        try:
            self.pulse_val += self.pulse_dir * 2
            if self.pulse_val > 20 or self.pulse_val < 0:
                self.pulse_dir *= -1
                
            self.canvas.coords(self.bot_glow, 70 - self.pulse_val//2, 20 - self.pulse_val//2, 230 + self.pulse_val//2, 180 + self.pulse_val//2)
            
            # Simulated blinking loop
            if time.time() % 4 < 0.15:
                self.canvas.itemconfig(self.eye_left, fill="#161b22")
                self.canvas.itemconfig(self.eye_right, fill="#161b22")
            else:
                if self.bridge.listening:
                    self.canvas.itemconfig(self.eye_left, fill="#238636")
                    self.canvas.itemconfig(self.eye_right, fill="#238636")
                else:
                    self.canvas.itemconfig(self.eye_left, fill="#58a6ff")
                    self.canvas.itemconfig(self.eye_right, fill="#58a6ff")

            # --- DYNAMIC VOICE GLOBE WAVE ANIMATION ---
            self.wave_time += 0.4
            if self.bridge.listening:
                # Active Animation: Globe expands and audio frequencies bounce violently
                self.canvas.itemconfig(self.globe_core, outline="#238636", width=3)
                self.canvas.itemconfig(self.globe_base, outline="#238636")
                for i, bar in enumerate(self.wave_bars):
                    amplitude = abs(math.sin(self.wave_time + i)) * 18 + 4
                    self.canvas.coords(bar, 136 + (i*7), 245 - amplitude, 136 + (i*7), 245 + amplitude)
                    self.canvas.itemconfig(bar, fill="#34d058")
            else:
                # Standby State: Wave node drops to micro pulsations
                self.canvas.itemconfig(self.globe_core, outline="#58a6ff", width=2)
                self.canvas.itemconfig(self.globe_base, outline="#8b949e")
                for i, bar in enumerate(self.wave_bars):
                    amplitude = abs(math.sin(self.wave_time * 0.3 + i)) * 4 + 2
                    self.canvas.coords(bar, 136 + (i*7), 245 - amplitude, 136 + (i*7), 245 + amplitude)
                    self.canvas.itemconfig(bar, fill="#58a6ff")
                    
            self.root.after(50, self.animate_loop)
        except:
            pass

class MubeenEngineBridge:
    def __init__(self):
        self.listening = False
        self.ui = None
        self.tts = pyttsx3.init()
        self.tts.setProperty('rate', 175)
        self.recognizer = sr.Recognizer()
        self.recognizer.dynamic_energy_threshold = True

    def speak(self, text):
        if self.ui:
            self.ui.update_status("Speaking...", "#388bfd")
        try:
            self.tts.say(text)
            self.tts.runAndWait()
        except:
            pass
        if self.ui:
            self.ui.update_status("Listening...", "#58a6ff")

    def run_command(self, user_intent):
        intent = user_intent.lower()
        if self.ui:
            self.ui.update_status("Running Action...", "#ff7b72")
            
        if "photoshop" in intent:
            if "create" in intent or "canvas" in intent:
                self.speak("Opening Photoshop and setting up workspace canvases.")
                pyautogui.hotkey('ctrl', 'n')
                time.sleep(1)
                pyautogui.write('1080')
                pyautogui.press('tab')
                pyautogui.write('1350')
                pyautogui.press('enter')
            elif "save" in intent:
                pyautogui.hotkey('ctrl', 's')
                self.speak("Project assets saved.")
            elif "export" in intent:
                pyautogui.hotkey('ctrl', 'alt', 'shift', 'w')
                self.speak("Export sequences processed successfully.")
                
        elif "chrome" in intent or "search" in intent:
            self.speak("Launching web configurations.")
            os.system("start chrome")
            if "search for" in intent:
                query = intent.split("search for")[-1].strip()
                time.sleep(1.5)
                pyautogui.write(f"https://google.com{query}")
                pyautogui.press('enter')
                
        elif "notepad" in intent:
            self.speak("Opening target text pad frame.")
            os.system("start notepad")
        elif "office" in intent:
            self.speak("Opening Microsoft Office hub interface.")
            os.system("start ms-officeapp:")
        else:
            self.speak("Automation sequence applied.")

def auto_update_worker(ui):
    while True:
        try:
            time.sleep(60)
            if not sys.argv[0].endswith(".exe"):
                continue
            with urllib.request.urlopen(GITHUB_RAW_URL) as response:
                cloud_code = response.read().decode('utf-8')
            with open("main.py", "r", encoding="utf-8") as local_file:
                local_code = local_file.read()
                
            if cloud_code.strip() != local_code.strip():
                ui.update_status("Syncing Update...", "#ffb86c")
                with open("main.py", "w", encoding="utf-8") as local_file:
                    local_file.write(cloud_code)
                ui.update_status("Restarting...", "#238636")
                time.sleep(2)
                os.execv(sys.executable, ['python'] + sys.argv)
        except:
            pass

def start_network_bridge(bridge):
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    try:
        server.bind(('0.0.0.0', 9999))
        server.listen(5)
        while True:
            conn, addr = server.accept()
            command = conn.recv(1024).decode('utf-8')
            if command:
                bridge.run_command(command)
            conn.close()
    except:
        pass

def local_voice_loop(bridge):
    try:
        with sr.Microphone() as source:
            bridge.recognizer.adjust_for_ambient_noise(source, duration=0.5)
    except:
        pass

    time.sleep(1.5)
    bridge.speak("Mubeen A.I. stands ready.")
    
    while True:
        try:
            with sr.Microphone() as source:
                bridge.listening = False
                audio = bridge.recognizer.listen(source, timeout=4, phrase_time_limit=3)
                phrase = bridge.recognizer.recognize_google(audio).lower()
                
                if "mubeen" in phrase:
                    bridge.listening = True
