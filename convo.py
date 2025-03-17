#!/usr/bin/env python3
"""convo.py - Voice conversation with LLM and Piper TTS in myenv"""

import subprocess
import sys
import os
import speech_recognition as sr

def get_voice_input(device_index=1):
    """Capture voice input from the microphone."""
    r = sr.Recognizer()
    try:
        with sr.Microphone(device_index=device_index) as source:
            print("Say something! (or 'exit' to quit)")
            audio = r.listen(source, timeout=5)
            text = r.recognize_google(audio)
            print(f"You said: {text}")
            return text.lower()
    except sr.UnknownValueError:
        print("Sorry, I couldn’t understand that.")
        return None
    except sr.RequestError as e:
        print(f"Error with recognition service: {e}")
        return None
    except Exception as e:
        print(f"Microphone error: {e}")
        return None

def play_tts(text, voice_model="en_GB-vctk-medium.onnx", speaker_id="42"):
    """Generate and play TTS with Piper."""
    script_dir = os.path.dirname(os.path.realpath(__file__))
    piper_dir = os.path.join(script_dir, "piper")
    voice_model_path = os.path.join(piper_dir, voice_model)
    sink = "alsa_output.pci-0000_04_00.6.analog-stereo"

    # Verify paths
    if not os.path.exists(piper_dir) or not os.path.exists(voice_model_path):
        print(f"Error: Piper or voice model not found at {voice_model_path}")
        return

    # Generate TTS
    piper_cmd = [os.path.join(piper_dir, "piper"), "--model", voice_model_path]
    if speaker_id:
        piper_cmd.extend(["--speaker", speaker_id])
    piper_cmd.extend(["--output_file", "output.wav"])
    try:
        subprocess.run(piper_cmd, input=text, text=True, cwd=piper_dir, env={"LD_LIBRARY_PATH": piper_dir}, check=True)
    except subprocess.CalledProcessError as e:
        print(f"Error generating TTS: {e}")
        return

    # Convert with sox
    sox_cmd = ["sox", "output.wav", "-r", "48000", "-c", "2", "-e", "signed-integer", "-b", "32", "output_converted.wav"]
    try:
        subprocess.run(sox_cmd, cwd=piper_dir, check=True)
    except subprocess.CalledProcessError as e:
        print(f"Error converting audio: {e}")
        return

    # Play with paplay
    print("Liza says...")
    paplay_cmd = ["paplay", "--device", sink, "output_converted.wav"]
    try:
        subprocess.run(paplay_cmd, cwd=piper_dir, check=True)
    except subprocess.CalledProcessError as e:
        print(f"Error playing audio: {e}")
        return

    # Clean up
    for f in ["output.wav", "output_converted.wav"]:
        os.remove(os.path.join(piper_dir, f))

def run_llm(prompt):
    """Run LLM and return response."""
    script_dir = os.path.dirname(os.path.realpath(__file__))
    llm_dir = os.path.join(script_dir, "llama.cpp/build/bin")
    model_path = os.path.join(script_dir, "models/qwen2.5-0.5b-instruct-q4_k_m.gguf")

    if not os.path.exists(llm_dir) or not os.path.exists(model_path):
        print(f"Error: LLM or model not found at {model_path}")
        return None

    llm_cmd = [os.path.join(llm_dir, "llama-cli"), "-m", model_path, "-p", prompt, "-n", "128", "--no-conversation"]
    try:
        output = subprocess.check_output(llm_cmd, text=True, stderr=subprocess.DEVNULL)
        if not output.strip():
            print("Error: LLM output is empty")
            return None
        return output.strip()
    except subprocess.CalledProcessError as e:
        print(f"Error running LLM: {e}")
        return None

def main():
    """Main conversation loop."""
    # Check dependencies
    for cmd in ["paplay", "sox"]:
        if subprocess.call(["which", cmd], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL) != 0:
            print(f"Error: {cmd} not found. Install it (e.g., sudo apt install {cmd if cmd != 'paplay' else 'pulseaudio-utils'})")
            sys.exit(1)

    print("Starting conversation with Liza (say 'exit' or 'quit' to stop)...")
    while True:
        # Get voice input
        prompt = get_voice_input()
        if not prompt:
            continue
        if prompt in ["exit", "quit"]:
            play_tts("Goodbye!", speaker_id="42")
            break

        # Process voice commands
        voice_model = "en_GB-vctk-medium.onnx"
        speaker_id = "42"  # Liza default
        voices = {
            "mia": "8", "liza": "42", "luna": "45", "sophie": "46", "ava": "48",
            "tiffany": "56", "olivia": "58", "ellie": "77"
        }
        if "switch voice to" in prompt:
            for name in voices:
                if f"switch voice to {name}" in prompt:
                    speaker_id = voices[name]
                    print(f"Switching to {name}")
                    play_tts(f"Switched to {name}", voice_model, speaker_id)
                    continue
            if "switch voice to southern" in prompt:
                voice_model = "en_GB-southern_english_female-low.onnx"
                speaker_id = None
                print("Switching to Southern")
                play_tts("Switched to Southern", voice_model, None)
                continue
            if "switch voice to vctk" in prompt:
                try:
                    vctk_id = int(prompt.split("switch voice to vctk ")[1].split()[0])
                    if 0 <= vctk_id <= 108:
                        speaker_id = str(vctk_id)
                        print(f"Switching to VCTK {vctk_id}")
                        play_tts(f"Switched to VCTK {vctk_id}", voice_model, speaker_id)
                        continue
                    else:
                        raise ValueError
                except (IndexError, ValueError):
                    play_tts("Invalid VCTK ID, staying with Liza", voice_model, "42")
                    continue

        # Get LLM response
        response = run_llm(prompt)
        if response:
            play_tts(response, voice_model, speaker_id)

if __name__ == "__main__":
    main()
