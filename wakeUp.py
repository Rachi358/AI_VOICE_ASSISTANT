import os
import queue
import sounddevice as sd
import vosk
import sys
import json

# Model path
model_path = r"vosk\models\vosk-model-small-en-us-0.15"

# Check if model path exists
if not os.path.exists(model_path):
    print(f" Model path does NOT exist: {model_path}")
    sys.exit(1)

try:
    model = vosk.Model(model_path)
except Exception as e:
    print(f" Failed to load model: {e}")
    sys.exit(1)

# Set Vosk log level to suppress output
vosk.SetLogLevel(-1)

# Initialize queue and audio settings
q = queue.Queue()
samplerate = 16000
device = None

def callback(indata, frames, time, status):
    if status:
        print(f"[Audio Status] {status}", file=sys.stderr)
    q.put(bytes(indata))

def listen_for_wake_word(wake_words=None):
    if wake_words is None:
        wake_words = ["yara", "jarvis", "jimmy", "ara", "gimme"]

    print(" Listening for wake word...")
    try:
        with sd.RawInputStream(samplerate=samplerate, blocksize=8000, device=device,
                               dtype='int16', channels=1, callback=callback):
            rec = vosk.KaldiRecognizer(model, samplerate)
            while True:
                data = q.get()
                if rec.AcceptWaveform(data):
                    result = json.loads(rec.Result())
                    text = result.get("text", "").lower()
                    print(f" Heard: {text}")
                    for wake_word in wake_words:
                        if wake_word in text:
                            print(f" Wake Word Detected: {wake_word}")
                            return
    except KeyboardInterrupt:
        print("\n[INFO] Wake word listener stopped manually.")
    except Exception as e:
        print(f"[ERROR] Microphone stream error: {e}")
