<<<<<<< HEAD
# b0t
text to speech and voice to text groq llm enabled learning bot
=======
# Future Assistant
A screen-reading, self-improving AI assistant powered by Groq, Whisper vibes, and agentic innovation.

## Vision
Compensate, innovate, adapt, adopt, learn, grow! Clean code (< 400 lines/file), open-source, unstoppable vibes.

## Setup
1. Clone: `git clone https://github.com/q-killer/b0t.git`
2. Install: `pip3 install -r requirements.txt`
3. Set `.env`: `GROQ_API_KEY=your_key`
4. Run: `./test_groq.py`

## Status
- **Groq Integration**: Audio input → transcription → Groq response → TTS output.
- **Voice**: Local recording (`arecord`) and transcription (`speechrecognition`).
- **Whisper**: WIP—adding `faster-whisper` for tighter voice input.
- **Learning**: `learning.json` planned for feedback loop.

## Structure
- `test_groq.py`: Core script (Groq + audio I/O).
- `voice.py`: Voice input prototype.
- `.env`: API keys (gitignored).
- `learning.json`: Feedback storage (WIP).
- `requirements.txt`: Dependencies.

## Contributing
Fork, branch, PR—keep it concise, documented, and epic!

## Bash Snippet Policy
- Copy-paste executable, expert-level, works first time.
- Updates files intelligently with error checking.
>>>>>>> 3b01c42 (Initial commit: Groq-powered assistant with audio I/O)
