# Future Assistant
A screen-reading, self-improving AI assistant powered by Groq, Whisper vibes, and agentic innovation.

## Vision
Compensate, innovate, adapt, adopt, learn, grow! Clean code (< 400 lines/file), open-source, unstoppable vibes. Now with pro-grade trading logic and a self-learning loop for stocks, crypto, futures—tracking TSLA swings, market sentiment, and more.

## Setup
1. Clone: `git clone https://github.com/q-killer/b0t.git`
2. Setup Env: `cd b0t && python3 -m venv myenv && source myenv/bin/activate`
3. Install: `pip3 install -r requirements.txt`
4. Install TTS: `sudo apt-get install espeak`
5. Set `.env`: `GROQ_API_KEY=your_key`
6. Run: `./test_groq.py` or `./test_bot.sh`

## Status
- **Groq Integration**: Audio input → Whisper (`medium.en`) → Groq response → TTS (`pyttsx3`).
- **Voice**: `arecord` recording, `faster-whisper` with VAD tweaks.
- **TTS**: Fast local playback via `pyttsx3` with sentence splitting.
- **News**: Real-time headlines from Google News RSS.
- **Trading**: Ross Cameron-inspired momentum logic—stocks (Yahoo Finance), crypto (Binance), sentiment analysis, low-risk trades (TSLA, BTC, etc.).
- **Learning**: `learning.json` tracks trades, optimizes logic locally based on outcomes.

## Structure
- `test_groq.py`: Core script (Groq + audio I/O + trading + learning).
- `test_bot.sh`: Test runner with correct env.
- `test_tts.py`: TTS speed tester.
- `voice.py`: Voice input prototype.
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

## Contributing
Fork, branch, PR—keep it concise, documented, and epic!

## Bash Snippet Policy
- Copy-paste executable, expert-level, works first time.
- Updates files intelligently with error checking.
