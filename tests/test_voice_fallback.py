import importlib
import sys
import unittest


class VoiceFallbackTests(unittest.TestCase):
    def test_voice_module_imports_without_whisper(self):
        sys.modules.pop("voice", None)
        sys.modules.pop("brain", None)

        voice = importlib.import_module("voice")

        self.assertFalse(voice.WHISPER_AVAILABLE)
        self.assertEqual(voice.transcribe(None, "auto"), ("", ""))


if __name__ == "__main__":
    unittest.main()
