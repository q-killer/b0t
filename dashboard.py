import tkinter as tk
from tkinter import ttk
import pyttsx3

class BotDashboard:
    def __init__(self):
        self.root = tk.Tk()
        self.root.title('Future Assistant Dashboard')
        self.engine = pyttsx3.init()
        self.voices = self.engine.getProperty('voices')
        self.voice_names = [voice.name for voice in self.voices]
        self.selected_voice = tk.StringVar(value=self.voice_names[0] if self.voice_names else 'Default')
        tk.Label(self.root, text='Choose Your Voice:').pack(pady=5)
        self.voice_dropdown = ttk.Combobox(self.root, textvariable=self.selected_voice, values=self.voice_names)
        self.voice_dropdown.pack(pady=5)
        self.voice_dropdown.bind('<<ComboboxSelected>>', self.set_voice)
        tk.Button(self.root, text='Test Voice', command=self.test_voice).pack(pady=5)

    def set_voice(self, event):
        selected_name = self.selected_voice.get()
        for voice in self.voices:
            if voice.name == selected_name:
                self.engine.setProperty('voice', voice.id)
                print(f'\033[1;32mVoice set to: {selected_name}\033[0m')
                break

    def test_voice(self):
        self.engine.runAndWait()

    def run(self):
        self.root.mainloop()

if __name__ == '__main__':
    dashboard = BotDashboard()
    dashboard.run()
