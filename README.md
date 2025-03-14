# Future Assistant
A screen-reading, self-improving AI assistant powered by Groq, Whisper vibes, and agentic innovation.

## Vision
Compensate, innovate, adapt, adopt, learn, grow! Clean code (< 400 lines/file), open-source, unstoppable vibes.

## Setup
1. Clone: `git clone https://github.com/q-killer/b0t.git`
2. Setup Env: `cd b0t && python3 -m venv myenv && source myenv/bin/activate`
3. Install: `pip3 install -r requirements.txt`
4. Set `.env`: `GROQ_API_KEY=your_key`
5. Run: `./test_groq.py` or `./test_bot.sh`

## Status
- **Groq Integration**: Audio input → Whisper (`medium.en`) → Groq response → TTS (`gTTS` + `pygame`).
- **Voice**: `arecord` recording, `faster-whisper` with VAD tweaks.
- **TTS**: Fast playback via `pygame.mixer`.
- **Learning**: `learning.json` planned for feedback loop.

## Structure
- `test_groq.py`: Core script (Groq + audio I/O).
- `test_bot.sh`: Test runner with correct env.
- `test_tts.py`: TTS speed tester.
- `voice.py`: Voice input prototype.
- `.env`: API keys (gitignored).
- `learning.json`: Feedback storage (WIP).
- `requirements.txt`: Dependencies.
- `myenv/`: Dedicated virtual env (gitignored).

## Contributing
Fork, branch, PR—keep it concise, documented, and epic!

## Bash Snippet Policy
- Copy-paste executable, expert-level, works first time.
- Updates files intelligently with error checking.
