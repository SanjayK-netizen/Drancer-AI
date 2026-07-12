import os
import whisper
import pyttsx3
import sounddevice as sd
from brain import ask

model = whisper.load_model("base")
conversation_history = []

LANGUAGE_CODE_MAP = {
    "auto": "auto",
    "english": "en",
    "en": "en",
    "hindi": "hi",
    "hi": "hi",
    "tamil": "ta",
    "ta": "ta",
    "telugu": "te",
    "te": "te",
}

LANGUAGE_NAME_MAP = {
    "en": "English",
    "hi": "Hindi",
    "ta": "Tamil",
    "te": "Telugu",
    "auto": "auto-detected language",
}


def normalize_language_code(language):
    if not language:
        return "auto"
    language = language.strip().lower()
    return LANGUAGE_CODE_MAP.get(language, language)


def language_name(code):
    return LANGUAGE_NAME_MAP.get(code, code)


def get_language_selection():
    env_lang = os.getenv("DRANCER_LANGUAGE")
    if env_lang:
        selected = normalize_language_code(env_lang)
        print(f"Using DRANCER_LANGUAGE={selected}")
        return selected

    prompt = (
        "Enter recognition language code or name "
        "(auto, en, hi, ta, te) [auto]: "
    )
    selected = input(prompt).strip()
    if not selected:
        return "auto"
    return normalize_language_code(selected)


def record_audio(duration=5, fs=16000):
    """Record audio from microphone."""
    print("Listening...")
    audio = sd.rec(int(duration * fs), samplerate=fs, channels=1, dtype="float32")
    sd.wait()
    return audio.flatten()


def select_tts_voice(engine, language_code="auto"):
    if not language_code or language_code == "auto":
        return None
    search = language_code.lower()
    for voice in engine.getProperty("voices"):
        voice_id = getattr(voice, "id", "").lower()
        voice_name = getattr(voice, "name", "").lower()
        if search in voice_id or search in voice_name:
            return voice
        languages = getattr(voice, "languages", [])
        if isinstance(languages, (list, tuple)):
            for lang in languages:
                if isinstance(lang, bytes):
                    lang = lang.decode(errors="ignore")
                if search in str(lang).lower():
                    return voice
    return None


def speak(text, language_code="auto"):
    """Speak text out loud, choosing a voice if available."""
    engine = pyttsx3.init()
    engine.setProperty("rate", 150)
    voice = select_tts_voice(engine, language_code)
    if voice:
        engine.setProperty("voice", voice.id)
    elif language_code != "auto":
        print(
            f"(No matching TTS voice found for {language_name(language_code)}; using default voice.)"
        )
    engine.say(text)
    engine.runAndWait()
    engine.stop()


def transcribe(audio, language_code="auto"):
    """Transcribe audio to text using Whisper."""
    decode_language = None if language_code == "auto" else language_code
    result = model.transcribe(audio, fp16=False, language=decode_language)
    text = result["text"].strip()
    detected = result.get("language", "unknown")
    return text, detected


def main():
    selected_language = get_language_selection()
    print(f"Speech recognition language: {language_name(selected_language)}")
    if selected_language == "auto":
        print("Whisper will attempt automatic language detection.")

    try:
        print("Drancer is online. Press Enter to start talking...")
        while True:
            input("Press Enter to talk to Drancer...")

            audio = record_audio()
            user_text, detected_lang = transcribe(audio, selected_language)
            if not user_text:
                print("(No speech detected, try again)")
                continue

            effective_language = (
                detected_lang if selected_language == "auto" and detected_lang != "unknown" else selected_language
            )
            lang_label = language_name(effective_language)
            print(f"You ({lang_label}): {user_text}")
            if selected_language == "auto":
                print(f"(Detected language: {lang_label})")

            reply = ask(user_text, history=conversation_history, language=effective_language)
            print(f"Drancer ({lang_label}): {reply}")

            conversation_history.append({"role": "user", "content": user_text})
            conversation_history.append({"role": "assistant", "content": reply})

            speak(reply, language_code=effective_language)

    except KeyboardInterrupt:
        print("\nDrancer shutting down. Goodbye!")


if __name__ == "__main__":
    main()
