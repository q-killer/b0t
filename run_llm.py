#!/usr/bin/env python3
"""run_llm.py - Run LLM and Piper TTS in myenv with voice switching"""

import subprocess
import sys
import os

def run_llm(prompt):
    """Run LLM and play TTS output with specified voice."""
    script_dir = os.path.dirname(os.path.realpath(__file__))
    llm_dir = os.path.join(script_dir, "llama.cpp/build/bin")
    piper_dir = os.path.join(script_dir, "piper")
    model_path = os.path.join(script_dir, "models/qwen2.5-0.5b-instruct-q4_k_m.gguf")
    sink = "alsa_output.pci-0000_04_00.6.analog-stereo"

    # Voice defaults
    voice_model = "en_GB-vctk-medium.onnx"
    speaker_id = "8"  # Mia

    # Voice switching
    voices = {
        "Mia": "8", "Liza": "42", "Luna": "45", "Sophie": "46", "Ava": "48",
        "Tiffany": "56", "Olivia": "58", "Ellie": "77"
    }
    if "Switch voice to" in prompt:
        for name in voices:
            if f"Switch voice to {name}" in prompt:
                speaker_id = voices[name]
                print(f"Voice: {name}")
                prompt = f"Switched to {name}"
                break
        if "Switch voice to southern" in prompt:
            voice_model = "en_GB-southern_english_female-low.onnx"
            speaker_id = None
            print("Voice: Southern")
            prompt = "Switched to Southern"
        elif "Switch voice to vctk" in prompt:
            try:
                vctk_id = int(prompt.split("Switch voice to vctk ")[1].split()[0])
                if 0 <= vctk_id <= 108:
                    speaker_id = str(vctk_id)
                    print(f"Voice: VCTK {vctk_id}")
                    prompt = f"Switched to VCTK {vctk_id}"
                else:
                    raise ValueError
            except (IndexError, ValueError):
                speaker_id = "8"
                print("Invalid VCTK ID—defaulting to Mia (8)")
                prompt = "Switched to Mia"

    voice_model_path = os.path.join(piper_dir, voice_model)

    # Verify paths
    for path in [llm_dir, piper_dir, model_path, voice_model_path]:
        if not os.path.exists(path):
            print(f"Error: {path} not found")
            sys.exit(1)

    # Check dependencies
    for cmd in ["paplay", "sox"]:
        if subprocess.call(["which", cmd], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL) != 0:
            print(f"Error: {cmd} not found. Install it (e.g., sudo apt install {cmd if cmd != 'paplay' else 'pulseaudio-utils'})")
            sys.exit(1)

    # Run LLM
    print("Running LLM...")
    llm_cmd = [os.path.join(llm_dir, "llama-cli"), "-m", model_path, "-p", prompt, "-n", "128", "--no-conversation"]
    try:
        output = subprocess.check_output(llm_cmd, text=True, stderr=subprocess.DEVNULL)
        if not output.strip():
            print("Error: LLM output is empty")
            sys.exit(1)
        print(f"LLM Output: {output.strip()}")
    except subprocess.CalledProcessError as e:
        print(f"Error running LLM: {e}")
        sys.exit(1)

    # Generate TTS with Piper
    piper_cmd = [os.path.join(piper_dir, "piper"), "--model", voice_model_path]
    if speaker_id:
        piper_cmd.extend(["--speaker", speaker_id])
    piper_cmd.extend(["--output_file", "output.wav"])
    try:
        subprocess.run(piper_cmd, input=output, text=True, cwd=piper_dir, env={"LD_LIBRARY_PATH": piper_dir}, check=True)
    except subprocess.CalledProcessError as e:
        print(f"Error generating TTS: {e}")
        sys.exit(1)

    # Convert with sox
    sox_cmd = ["sox", "output.wav", "-r", "48000", "-c", "2", "-e", "signed-integer", "-b", "32", "output_converted.wav"]
    try:
        subprocess.run(sox_cmd, cwd=piper_dir, check=True)
    except subprocess.CalledProcessError as e:
        print(f"Error converting audio: {e}")
        sys.exit(1)

    # Play with paplay
    print("Playing audio...")
    paplay_cmd = ["paplay", "--device", sink, "output_converted.wav"]
    try:
        subprocess.run(paplay_cmd, cwd=piper_dir, check=True)
    except subprocess.CalledProcessError as e:
        print(f"Error playing audio: {e}")
        sys.exit(1)

    # Clean up
    for f in ["output.wav", "output_converted.wav"]:
        os.remove(os.path.join(piper_dir, f))

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python run_llm.py \"your prompt here\"")
        sys.exit(1)
    run_llm(sys.argv[1])
