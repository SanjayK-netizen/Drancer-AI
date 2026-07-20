import importlib
import sys
import unittest
from unittest import mock


class VoiceFallbackTests(unittest.TestCase):
    def test_voice_module_imports_without_whisper(self):
        sys.modules.pop("voice", None)
        sys.modules.pop("brain", None)

        voice = importlib.import_module("voice")

        self.assertEqual(voice.transcribe(None, "auto"), ("", ""))

    def test_speak_handles_tts_engine_initialization_failure(self):
        sys.modules.pop("voice", None)
        sys.modules.pop("brain", None)
        voice = importlib.import_module("voice")

        class FailingTtsModule:
            def init(self):
                raise RuntimeError("engine startup failed")

        with mock.patch.object(voice, "pyttsx3", FailingTtsModule()):
            voice.speak("hello", language_code="en")


if __name__ == "__main__":
    unittest.main()
