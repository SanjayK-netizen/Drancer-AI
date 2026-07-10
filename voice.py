import whisper
import pyttsx3
import sounddevice as sd
from brain import ask

model = whisper.load_model("base")
engine = pyttsx3.init()
conversation_history = []

def record_audio(duration=5, fs=16000):
    print("Listening...")
    audio = sd.rec(int(duration * fs), samplerate=fs, channels=1, dtype='float32')
    sd.wait()
    return audio.flatten()

def transcribe(audio):
    result = model.transcribe(audio, fp16=False)
    return result["text"].strip()

while True:
    audio = record_audio()
    user_text = transcribe(audio)

    if not user_text:
        continue

    print(f"You: {user_text}")

    reply = ask(user_text, history=conversation_history)
    print(f"Drancer: {reply}")

    conversation_history.append({"role": "user", "content": user_text})
    conversation_history.append({"role": "assistant", "content": reply})

    engine.say(reply)
    engine.runAndWait()