## Git Reset and Whisper Update - March 20, 2025
- Renamed future-assistant to bot, reset Git to remote main.
- Updated Whisper.cpp to use whisper-cli, fixed STT pipeline.
## Piper Relocation - March 20, 2025
- Moved Piper to ~/bot/piper for modularity.
- Updated speak.sh to new Piper path.
## LFS Cleanup and Live Mic - March 20, 2025
- Cleaned Git with LFS migration, removed unnecessary files.
- Fixed Piper with Python env, tested live mic STT.
- Added GLaDOS integration.
## Piper Fix and Git Cleanup - March 20, 2025
- Fixed Piper audio with fresh binary and env.
- Fully migrated Piper to Git LFS.
## GLaDOS Integration - March 20, 2025
- Added GLaDOS TTS from dnhkng/GLaDOS.
- Noted Piper env issue for later fix.
## Piper Fix and Live Mic - March 20, 2025
- Fixed speak.sh to match working Piper command.
- Tested live mic with Piper, GLaDOS optional.
## Piper Binary Fix - March 20, 2025
- Replaced corrupted Piper binary (ELF header error).
- Tested live mic with fixed speak.sh.
- Re-optimized repo with LFS.
## Piper Binary Fix - March 20, 2025
- Replaced corrupted Piper binary (ELF header error).
- Tested live mic with fixed speak.sh.
- Re-optimized repo with LFS.
## GLaDOS Focus - March 20, 2025
- Shifted to GLaDOS TTS due to Piper JSON errors.
- Installed GLaDOS deps, tested live mic integration.
## GLaDOS Setup Fix - March 20, 2025
- Fixed uv PATH issue for install.py.
- Tested GLaDOS TTS with live mic input.
## GLaDOS Simplified - March 20, 2025
- Used find for script search, ran GLaDOS via -m glados_tts.
- Leveraged demo.ipynb, tested live mic.
