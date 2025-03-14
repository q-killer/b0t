#!/usr/bin/env python3
# bot.py - A screen-reading, self-improving AI assistant powered by Ollama and LangChain
# Created: March 14, 2025, by Isaac on LMDE with 16GB RAM
# Purpose: Chats, tools, learns—epic, human-focused growth
# Vision: Compensate, innovate, adapt, adopt, learn, grow! Improve speed, troubleshoot, utilize resources (multiple terminals, RAM full, CPU idle). Expand to cloud/free resources if needed. Use Matthew Berman’s videos and my YouTube subs for AI innovation. Make it epic, positive, human-focused, leveraging tech innovators—grow unstoppable, organized, envelope-pushing!
# // GROK: USER_REQUEST - Isaac, 2025-03-14: Full vision above + "Love ASCII art and speech! Growing together—reiterative learning! Add README.md with clear docs!"
# // GROK: USER_RESULT - 2025-03-14 05:00 AM CDT:
#   - TTS live with pyttsx3—robot voice on point!
#   - Mic tuned via pavucontrol (gain up, fan noise down), switched to device_index=3 (Pulse), energy threshold 300
#   - Voice input 98%: Mic opens, debug added, recognition pending
#   - Learning loop active in learning.json—feedback logged
#   - Next: Finalize mic, preload Ollama, YouTube integration, README.md
import os
import signal
import random
import json
from langchain_ollama import OllamaLLM
from langchain.agents import initialize_agent, AgentType
from langchain.memory import ConversationBufferMemory
from langchain_community.tools import DuckDuckGoSearchRun
from langchain.tools import Tool
import numexpr
from rich.console import Console
from mss import mss
from PIL import Image
import pytesseract
import pathlib
import speech_recognition as sr
import pyttsx3
search_tool = DuckDuckGoSearchRun()
def calculate(expression): return numexpr.evaluate(expression).item()
calc_tool = Tool(name="calculate", func=calculate, description="Evaluate math (e.g., 2 + 2)")
def read_screen(_=None):
    screenshot_path = pathlib.Path("screen.png")
    with mss() as sct:
        sct.shot(output=str(screenshot_path))
    return pytesseract.image_to_string(Image.open(screenshot_path))
screen_tool = Tool(name="read_screen", func=read_screen, description="Read screen text")
tools = [search_tool, calc_tool, screen_tool]
llm = OllamaLLM(model="qwen2.5:7b", base_url="http://localhost:11434", timeout=120)
memory = ConversationBufferMemory(return_messages=True, input_key="input")
agent = initialize_agent(tools=tools, llm=llm, agent=AgentType.CONVERSATIONAL_REACT_DESCRIPTION, verbose=True, memory=memory)
recognizer = sr.Recognizer()
recognizer.energy_threshold = 300  # Tuned for gain-adjusted mic
recognizer.dynamic_energy_threshold = True  # Adapts to fan noise
tts_engine = pyttsx3.init()
tts_engine.setProperty("rate", 150)
console = Console()
console.print("[bold cyan]🤖  // FUTURE ASSISTANT v1.0 \\\\[/bold cyan]\n       [italic]Booting... Humanity’s Ally Online[/italic]")
log_path = pathlib.Path("interactions.log")
learn_path = pathlib.Path("learning.json")
if not log_path.exists(): log_path.touch()
if not learn_path.exists():
    with open(learn_path, "w") as f:
        json.dump({"helpful": {}, "unhelpful": {}}, f)
def signal_handler(sig, frame):
    console.print("[bold red]Bot:[/bold red] Shutting down—signal caught!")
    os.system("pkill -9 ollama")
    exit(0)
signal.signal(signal.SIGINT, signal_handler)
signal.signal(signal.SIGTERM, signal_handler)
greetings = ["Howdy, partner!", "Greetings, Earthling!", "Yo, what’s up?"]
while True:
    try:
        use_voice = input("Use voice? (y/n): ").lower() == "y"
        if use_voice:
            try:
                with sr.Microphone(device_index=3) as source:
                    console.print("[cyan]Listening...[/cyan]")
                    console.print(f"[yellow]Mic energy threshold: {recognizer.energy_threshold}[/yellow]")
                    audio = recognizer.listen(source, timeout=10, phrase_time_limit=5)
                    console.print("[yellow]Audio captured, recognizing...[/yellow]")
                    user_input = recognizer.recognize_google(audio)
                    console.print(f"You (voice): {user_input}")
            except (sr.UnknownValueError, sr.RequestError, sr.WaitTimeoutError) as e:
                console.print(f"[yellow]Voice failed: {str(e)}. Switching to text![/yellow]")
                user_input = input("You (text fallback): ")
        else:
            user_input = input("You: ")
        if user_input.lower() in ["exit", "quit"]:
            console.print("[bold green]Bot:[/bold green] Catch you later!")
            os.system("pkill -9 ollama")
            break
        inputs = {"input": user_input, "chat_history": memory.chat_memory.messages}
        response = agent.invoke(inputs)["output"]
        greeting = random.choice(greetings)
        full_response = f"{greeting} {response}"
        console.print(f"[bold green]Bot:[/bold green] {full_response}")
        if use_voice:
            tts_engine.say(full_response)
            tts_engine.runAndWait()
        feedback = input("Was this helpful? (yes/no): ")
        with open(log_path, "a") as f:
            f.write(f"Input: {user_input}\nResponse: {response}\nFeedback: {feedback}\n\n")
        with open(learn_path, "r+") as f:
            learn_data = json.load(f)
            key = "helpful" if feedback.lower() == "yes" else "unhelpful"
            learn_data[key][user_input] = response
            f.seek(0)
            json.dump(learn_data, f, indent=2)
    except Exception as e:
        console.print(f"[bold red]Oops:[/bold red] Hit a snag—{str(e)}. Keepin’ it rolling!")
        with open(log_path, "a") as f:
            f.write(f"Error: {str(e)}\n\n")
# // GROK: OPTIMIZE - Next: preload model, async tools, cloud toggle
# // GROK: GROW - Learning loop active—YouTube integration + README.md soon!

