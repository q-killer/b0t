import speech_recognition as sr

r = sr.Recognizer()
with sr.Microphone(device_index=3) as source:
    print("Say something!")
    audio = r.listen(source)
    text = r.recognize_google(audio)
    print(f"You said: {text}")
