# Future Assistant v1.0
A screen-reading, self-improving AI assistant powered by Groq, Whisper vibes, and agentic innovation.

## Vision
Compensate, innovate, adapt, adopt, learn, grow! Clean code (< 400 lines/file), open-source, unstoppable vibes. Now with pro-grade trading logic, a self-learning loop for stocks/crypto/futures (tracking TSLA swings, market sentiment), and a colorful, interactive twist to make it epic and fun!

## Setup
1. Clone: `git clone https://github.com/q-killer/b0t.git`
2. Setup Env: `cd b0t && python3 -m venv myenv && source myenv/bin/activate`
3. Install: `pip3 install -r requirements.txt`
4. Install TTS: `sudo apt-get install espeak`
5. Install GUI (optional): `pip3 install tkinter` (for voice selection dashboard)
6. Set `.env`: `GROQ_API_KEY=your_key`
7. Run: `./test_groq.py` or `./test_bot.sh`

## Status
- **Groq Integration**: Audio input → Whisper (`medium.en`) → Groq response → TTS (`pyttsx3`).
- **Voice**: `arecord` recording, `faster-whisper` with VAD tweaks, voice selection via dashboard.
- **TTS**: Fast local playback via `pyttsx3` with sentence splitting and fun phrases.
- **News**: Real-time headlines from Google News RSS.
- **Trading**: Ross Cameron-inspired momentum logic—stocks (Yahoo Finance), crypto (Binance), sentiment analysis, low-risk trades (TSLA, BTC, etc.).
- **Learning**: `learning.json` tracks trades, optimizes logic locally based on outcomes.
- **Interface**: Colorful terminal output (blue welcomes, green prompts, red errors) + ASCII art.

## Structure
- `test_groq.py`: Core script (Groq + audio I/O + trading + learning).
- `test_bot.sh`: Test runner with correct env.
- `test_tts.py`: TTS speed tester.
- `voice.py`: Voice input prototype.
- `dashboard.py`: Tkinter GUI for voice selection (optional).
- `.env`: API keys (gitignored).
- `learning.json`: Trade log and learning data (local, updated per run).
- `requirements.txt`: Dependencies.
- `myenv/`: Dedicated virtual env (gitignored).

## Trading Logic
- **Sources**: Yahoo Finance (stocks), Binance (crypto), news sentiment.
- **Strategy**: Buy on volume breakouts + positive sentiment, sell on RSI overbought or profit targets, tight stops (1%).
- **Goals**: Maximize profit, minimize risk—day trades, swing trades, crypto swings.

## Learning Loop
- **Storage**: `learning.json` logs trades (ticker, change, volume, RSI, advice, outcome).
- **Optimization**: Analyzes past trades, adjusts thresholds for better wins—local and efficient.

## Interface Enhancements
- **Colors**: Blue = welcome, Green = prompts, Red = errors, Yellow = info, Cyan = trades, Magenta = learning updates.
- **ASCII Art**: Startup logo, trade win graphics (e.g., profit rocket), learning brain icon.
- **Voice Selection**: Dashboard drop-down lists `pyttsx3` voices—pick your vibe!

## Example Output
```
  ____        _        
 / ___| _ __ | |_ _   _ 
 \___ \| '_ \| __| | | |
  ___) | | | | |_| |_| |
 |____/|_| |_|___|\__, |
                  |___/ 
[1;32mYo, what’s next? Pick an option (1-3):[0m
1. Ask a question
2. Check stock data
3. Exit
```

## Contributing
See `CONTRIBUTING.md` for how to jump in and make this bot even more epic!

## Bash Snippet Policy
- Copy-paste executable, expert-level, works first time.
- Updates files intelligently with error checking.
- **Why**: Ensures rapid optimization with minimal steps—turbocharges development and keeps the bot unstoppable!

## Notes for Future Devs
- **File Updates**: Heredocs with `cat` failed; use `> file` to clear and `>> file` to append directly—faster and reliable.
