#!/usr/bin/env python3
"""test_tts.py - Quick TTS test"""
from gtts import gTTS
import pygame.mixer
tts = gTTS(text="Hello, this is a fast test!", lang="en")
tts.save("test.mp3")
pygame.mixer.init()
pygame.mixer.music.load("test.mp3")
pygame.mixer.music.play()
while pygame.mixer.music.get_busy():
    pygame.time.Clock().tick(10)
