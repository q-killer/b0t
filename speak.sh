source ~/bot/piper_env/bin/activate
VOICE=${1:-'Mia'}
case $VOICE in
  'Mia') MODEL='en_GB-vctk-medium.onnx' SPEAKER='8';;
  'Southern') MODEL='en_GB-southern_english_female-low.onnx' SPEAKER='';;
  *) echo 'Voice not found'; exit 1;;
esac
echo "$TEXT" | ~/bot/piper/piper --model ~/bot/piper/$MODEL --speaker $SPEAKER --output_file out.wav
paplay out.wav && rm out.wav
