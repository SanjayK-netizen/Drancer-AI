import whisper
import pyttsx3
import sounddevice as sd
from brain import ask

model = whisper.load_model("base")
engine = pyttsx3.init()
conversation_history = []

# Configure engine for better voice output
engine.setProperty('rate', 150)  # Slightly slower for clarity

def record_audio(duration=5, fs=16000):
    """Record audio from microphone."""
    print("Listening...")
    audio = sd.rec(int(duration * fs), samplerate=fs, channels=1, dtype='float32')
    sd.wait()
    return audio.flatten()

def speak(text):
    """Speak text out loud."""
    engine = pyttsx3.init()
    engine.setProperty('rate', 150)
    engine.say(text)
    engine.runAndWait()
    engine.stop()

def transcribe(audio):
    """Transcribe audio to text using Whisper."""
    result = model.transcribe(audio, fp16=False)
    return result["text"].strip()

# Main conversation loop
try:
    print("Drancer is online. Say something...")
    while True:
        audio = record_audio()
        user_text = transcribe(audio)

        if not user_text:
            print("(No speech detected, try again)")
            continue

        print(f"You: {user_text}")

        # Get response from brain with conversation history
        reply = ask(user_text, history=conversation_history)
        print(f"Drancer: {reply}")

        # Update conversation history
        conversation_history.append({"role": "user", "content": user_text})
        conversation_history.append({"role": "assistant", "content": reply})

        # Speak the response
        speak(reply)

except KeyboardInterrupt:
    print("\nDrancer shutting down. Goodbye!")