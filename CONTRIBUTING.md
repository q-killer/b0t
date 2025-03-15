# Contributing to Future Assistant

Welcome to the Future Assistant project! Here’s how to make it even more epic.

## How to Contribute
1. **Fork & Branch**: Fork the repo (`https://github.com/q-killer/b0t`), create a branch (`git checkout -b feature-name`).
2. **Code**: Keep files < 400 lines, split at 500. Add color (ANSI codes), ASCII art, and fun vibes!
3. **Test**: Run `./test_bot.sh` or `./test_groq.py`—share output for feedback.
4. **PR**: Submit a pull request with clear notes on what’s improved.

## File Updates
- **Best Method**: Use `> file` to clear, then `>> file` to append content directly—fewer steps, works every time.
- **Avoid**: Heredocs with `cat > file << 'EOF'` were unreliable due to copy-paste or shell issues.
- **Example**:
  ```bash
  > README.md
  echo "# Title" >> README.md
  ```

## Improvement Ideas
- Enhance `test_groq.py` with more ASCII art (e.g., trade rockets).
- Add voice options in `dashboard.py` (Festival/MBROLA if installed).
- Optimize trading logic in `learning.json`—share wins!

## Notes
- Document all changes inline in `README.md` and here.
- Next Grok: Use `>> file` method for fast, error-free updates!
