import os
import sys
import time
import socket
import threading
import urllib.request
import tkinter as tk
from tkinter import ttk
import pyautogui
import speech_recognition as sr
import pyttsx3

# URL to check for live updates directly from your GitHub repository
# Replace 'uzmamubeen1324-bit' with your repository details if needed
GITHUB_RAW_URL = "https://githubusercontent.com"

class AnimatedMubeenUI:
    def __init__(self, root, engine_bridge):
        self.root = root
        self.bridge = engine_bridge
        self.root.title("Mubeen AI Operator")
        
        self.root.geometry("320x420+50+50")
        self.root.overrideredirect(True)
        self.root.attributes("-topmost", True)
        self.root.config(bg="#0d1117")
        self.root.wm_attributes("-alpha", 0.95)
        
        self.title_bar = tk.Frame(self.root, bg="#161b22", relief="raised", height=30)
        self.title_bar.pack(side="top", fill="x")
        self.title_bar.bind("<Button-1>", self.start_drag)
        self.title_bar.bind("<B1-Motion>", self.drag_window)
        
        title_label = tk.Label(self.title_bar, text="🤖 MUBEEN AI (LIVE)", fg="#58a6ff", bg="#161b22", font=("Consolas", 10, "bold"))
        title_label.pack(side="left", padx=10)
        
        close_btn = tk.Button(self.title_bar, text="×", fg="#f85149", bg="#161b22", borderwidth=0, font=("Arial", 12, "bold"), command=self.root.quit)
        close_btn.pack(side="right", padx=10)

        self.canvas = tk.Canvas(self.root, width=300, height=280, bg="#0d1117", highlightthickness=0)
        self.canvas.pack(pady=10)
        
        self.bot_glow = self.canvas.create_oval(70, 50, 230, 210, fill="", outline="#1f6feb", width=2)
        self.bot_head = self.canvas.create_oval(80, 60, 220, 200, fill="#161b22", outline="#58a6ff", width=4)
        self.eye_left = self.canvas.create_oval(110, 110, 135, 135, fill="#58a6ff", outline="")
        self.eye_right = self.canvas.create_oval(165, 110, 190, 135, fill="#58a6ff", outline="")
        self.visor_line = self.canvas.create_line(120, 160, 180, 160, fill="#58a6ff", width=3)
        
        self.status_text = tk.Label(self.root, text="Booting Cloud Matrix...", fg="#8b949e", bg="#0d1117", font=("Consolas", 11))
        self.status_text.pack(pady=5)
        
        self.pulse_dir = 1
        self.pulse_val = 0
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
                
            self.canvas.coords(self.bot_glow, 70 - self.pulse_val//2, 50 - self.pulse_val//2, 230 + self.pulse_val//2, 210 + self.pulse_val//2)
            
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
                    
            self.root.after(60, self.animate_loop)
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
    """Background listener that pulls fresh changes from GitHub without reinstalling."""
    while True:
        try:
            time.sleep(60) # Checks for code changes every 60 seconds
            current_file_path = sys.argv[0]
            if not current_file_path.endswith(".exe"):
                continue
                
            # Download fresh source string from GitHub
            with urllib.request.urlopen(GITHUB_RAW_URL) as response:
                cloud_code = response.read().decode('utf-8')
                
            # Read local code state
            with open("main.py", "r", encoding="utf-8") as local_file:
                local_code = local_file.read()
                
            # If GitHub code is updated, hot-swap the script framework safely
            if cloud_code.strip() != local_code.strip():
                ui.update_status("Syncing Update...", "#ffb86c")
                with open("main.py", "w", encoding="utf-8") as local_file:
                    local_file.write(cloud_code)
                ui.update_status("Update Complete! Restarting...", "#238636")
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
                    bridge.speak("Yes?")
                    audio_cmd = bridge.recognizer.listen(source, timeout=6, phrase_time_limit=7)
                    cmd = bridge.recognizer.recognize_google(audio_cmd)
                    bridge.run_command(cmd)
        except:
            pass
        time.sleep(0.1)

if __name__ == "__main__":
    root = tk.Tk()
    bridge = MubeenEngineBridge()
    ui = AnimatedMubeenUI(root, bridge)
    bridge.ui = ui
    
    threading.Thread(target=start_network_bridge, args=(bridge,), daemon=True).start()
    threading.Thread(target=local_voice_loop, args=(bridge,), daemon=True).start()
    threading.Thread(target=auto_update_worker, args=(ui,), daemon=True).start()
    
    root.mainloop()
