#!/usr/bin/env python3
"""run_llm.py - Run LLM and Piper TTS in myenv"""

import subprocess
import sys
import os

def run_llm(prompt):
    """Run LLM and play TTS output."""
    script_dir = os.path.dirname(os.path.realpath(__file__))
    llm_dir = os.path.join(script_dir, "llama.cpp/build/bin")
    piper_dir = os.path.join(script_dir, "piper")
    model_path = os.path.join(script_dir, "models/qwen2.5-0.5b-instruct-q4_k_m.gguf")
    voice_model = "en_GB-vctk-medium.onnx"
    voice_model_path = os.path.join(piper_dir, voice_model)
    sink = "alsa_output.pci-0000_04_00.6.analog-stereo"
    speaker_id = "42"  # Liza

    # Verify paths
    for path in [llm_dir, piper_dir, model_path, voice_model_path]:
        if not os.path.exists(path):
            print(f"Error: {path} not found")
            sys.exit(1)

    # Run LLM
    print("Running LLM...")
    llm_cmd = [os.path.join(llm_dir, "llama-cli"), "-m", model_path, "-p", prompt, "-n", "128", "--no-conversation"]
    output = subprocess.check_output(llm_cmd, text=True, stderr=subprocess.DEVNULL)
    if not output.strip():
        print("Error: LLM output is empty")
        sys.exit(1)
    print(f"LLM Output: {output.strip()}")

    # Generate TTS with Piper
    piper_cmd = [os.path.join(piper_dir, "piper"), "--model", voice_model_path, "--speaker", speaker_id, "--output_file", "output.wav"]
    subprocess.run(piper_cmd, input=output, text=True, cwd=piper_dir, env={"LD_LIBRARY_PATH": piper_dir}, check=True)

    # Convert with sox
    sox_cmd = ["sox", "output.wav", "-r", "48000", "-c", "2", "-e", "signed-integer", "-b", "32", "output_converted.wav"]
    subprocess.run(sox_cmd, cwd=piper_dir, check=True)

    # Play with paplay
    print("Playing audio...")
    paplay_cmd = ["paplay", "--device", sink, "output_converted.wav"]
    subprocess.run(paplay_cmd, cwd=piper_dir, check=True)

    # Clean up
    for f in ["output.wav", "output_converted.wav"]:
        os.remove(os.path.join(piper_dir, f))

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python run_llm.py \"your prompt here\"")
        sys.exit(1)
    run_llm(sys.argv[1])
