import os
import sys
import time
import socket
import threading
import pyautogui
import win32gui
import win32con
import speech_recognition as sr
import pyttsx3
from PIL import ImageGrab

# Core Automation Settings
pyautogui.FAILSAFE = True
pyautogui.PAUSE = 0.3

class MubeenEngine:
    def __init__(self):
        self.tts = pyttsx3.init()
        self.tts.setProperty('rate', 175)
        self.recognizer = sr.Recognizer()
        self.recognizer.dynamic_energy_threshold = True

    def speak(self, text):
        print(f"[Mubeen AI]: {text}")
        try:
            self.tts.say(text)
            self.tts.runAndWait()
        except:
            pass

    def run_command(self, user_intent):
        intent = user_intent.lower()
        
        # 🪟 Photoshop Actions
        if "photoshop" in intent:
            if "create" in intent or "canvas" in intent:
                self.speak("Opening Photoshop and creating canvas.")
                pyautogui.hotkey('ctrl', 'n')
                time.sleep(1)
                pyautogui.write('1080')
                pyautogui.press('tab')
                pyautogui.write('1350')
                pyautogui.press('enter')
            elif "save" in intent:
                pyautogui.hotkey('ctrl', 's')
                self.speak("Saving project.")
            elif "export" in intent:
                pyautogui.hotkey('ctrl', 'alt', 'shift', 'w')
                self.speak("Exporting PNG.")
                
        # 🌐 Chrome Actions
        elif "chrome" in intent or "search" in intent:
            self.speak("Opening Chrome Browser.")
            os.system("start chrome")
            if "search for" in intent:
                query = intent.split("search for")[-1].strip()
                time.sleep(1.5)
                pyautogui.write(f"https://google.com{query}")
                pyautogui.press('enter')
                
        # 📝 Notepad / Generic
        elif "notepad" in intent:
            self.speak("Opening Notepad.")
            os.system("start notepad")
            
        else:
            self.speak(f"Executing standard Windows pipeline for: {user_intent}")

# Android App Network Bridge
def start_mobile_bridge(engine):
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    try:
        server.bind(('0.0.0.0', 9999))
        server.listen(5)
        while True:
            conn, addr = server.accept()
            command = conn.recv(1024).decode('utf-8')
            if command:
                engine.run_command(command)
            conn.close()
    except:
        pass

def main():
    engine = MubeenEngine()
    engine.speak("Mubeen A.I. stands ready.")
    
    # Start Network listening for Mobile APK triggers
    threading.Thread(target=start_mobile_bridge, args=(engine,), daemon=True).start()
    
    # Local Windows Mic Listening Loop
    while True:
        with sr.Microphone() as source:
            try:
                audio = self.recognizer.listen(source, timeout=5, phrase_time_limit=3)
                phrase = self.recognizer.recognize_google(audio).lower()
                if "mubeen" in phrase:
                    engine.speak("Yes?")
                    audio_cmd = self.recognizer.listen(source, timeout=7, phrase_time_limit=8)
                    cmd = self.recognizer.recognize_google(audio_cmd)
                    engine.run_command(cmd)
            except:
                pass
        time.sleep(0.1)

if __name__ == "__main__":
    main()
