#!/usr/bin/env python3
"""screen_task.py - Screen reading and dashboard for Future Assistant"""

import os
import subprocess
import tkinter as tk
from PIL import Image
import pytesseract
import json
from datetime import datetime

def read_clipboard():
    """Read clipboard content using xclip."""
    try:
        text = subprocess.check_output(["xclip", "-o", "-selection", "clipboard"]).decode().strip()
        return text if text else None
    except Exception as e:
        print(f"Error reading clipboard: {e}")
        return None

def capture_screen():
    """Capture screen and OCR it."""
    try:
        subprocess.run(["scrot", "screen.png"], check=True)
        text = pytesseract.image_to_string(Image.open("screen.png"))
        os.remove("screen.png")
        return text if text.strip() else None
    except Exception as e:
        print(f"Error capturing screen: {e}")
        return None

def update_dashboard(root, text_widget, trades_widget):
    """Update dashboard with clipboard/screen data and trades."""
    clipboard = read_clipboard() or "No clipboard data"
    screen = capture_screen() or "No screen data"
    text_widget.delete(1.0, tk.END)
    text_widget.insert(tk.END, f"Clipboard: {clipboard}\n\nScreen OCR: {screen}")
    
    try:
        with open("learning.json", "r") as f:
            trades = json.load(f)
        trades_text = "\n".join([f"{t['timestamp']}: {t['ticker']} - {t['advice']}" for t in trades[-5:]])
        trades_widget.delete(1.0, tk.END)
        trades_widget.insert(tk.END, trades_text)
    except Exception as e:
        trades_widget.delete(1.0, tk.END)
        trades_widget.insert(tk.END, f"Error loading trades: {e}")
    
    root.after(5000, lambda: update_dashboard(root, text_widget, trades_widget))

def main():
    """Main function for screen reading and dashboard."""
    root = tk.Tk()
    root.title("Future Assistant Dashboard")
    root.geometry("800x600")

    text_widget = tk.Text(root, height=20, width=80)
    text_widget.pack(pady=10)

    trades_widget = tk.Text(root, height=10, width=80)
    trades_widget.pack(pady=10)

    update_dashboard(root, text_widget, trades_widget)
    root.mainloop()

if __name__ == "__main__":
    main()
