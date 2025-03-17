# b0t - AI-Powered Trading Bot

A modular, bash-driven trading bot with LLM analysis, news scanning, and voice output. Built for LMDE, CPU-only.

## Setup
1. **Install Deps**: `sudo apt update && sudo apt install -y python3 python3-pip git g++ make libopenblas-dev cmake libblas-dev liblapack-dev libomp-dev`
2. **Clone and Build LLM**: Run `setup_llm.sh` to get Qwen 2.5 0.5B via `llama.cpp`.
3. **Virtual Env**: `python3 -m venv myenv && source myenv/bin/activate`
4. **Python Deps**: `pip3 install alpha_vantage yfinance pandas numpy`

## Run
- **LLM Analysis**: `./run_llm.sh` - Analyzes market prompts with Qwen 2.5 0.5B.
- **Full Bot**: `./test_bot.sh` - Launches LLM, trading module TBD.

## Files
- `setup_llm.sh`: Builds `llama.cpp` and downloads Qwen 2.5 0.5B.
- `run_llm.sh`: Runs Qwen for market analysis.
- `test_bot.sh`: Launcher script.
- `trading_logic.py`: Alpha Vantage RSI logic (Other Grok).
- `momentum_scanner.py`: yfinance momentum scan (Other Grok).

## Next Steps
- Voice output with Piper TTS.
- Speech input.
- Alpha Vantage news scanning.
- Trading logic optimization.

Built with <3 by Isaac and Grok 3 (xAI), March 2025.

# Voice Output
- Piper TTS with en_GB-vctk-medium.onnx (speaker 8 default).
- Switch voices with 'Switch voice to southern' or 'Switch voice to vctk N'.
- Setup in ~/bot/piper/—flat dir.
- Run ~/bot/run_llm.sh for analysis + voice.
