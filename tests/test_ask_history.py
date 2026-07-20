import os
import sys

# Ensure repository root is on sys.path when running from tests/ directory.
ROOT_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), os.pardir))
if ROOT_DIR not in sys.path:
    sys.path.insert(0, ROOT_DIR)

import brain


def test_ask_history_does_not_leak():
    assert brain.ask.__defaults__[0] is None

    calls = []

    class DummyOllama:
        @staticmethod
        def chat(model, messages, stream, options):
            calls.append(messages)
            return {"message": {"content": "Test reply"}}

    brain.ollama = DummyOllama()

    first_response = brain.ask("Hello Drancer")
    second_response = brain.ask("Hello again")

    assert first_response == "Test reply"
    assert second_response == "Test reply"
    assert brain.ask.__defaults__[0] is None

    # First call should contain only system prompt + current user message
    assert len(calls[0]) == 2
    assert calls[0][-1]["content"] == "Hello Drancer"

    # Second call should not include the previous call's user message
    assert len(calls[1]) == 2
    assert calls[1][-1]["content"] == "Hello again"


if __name__ == "__main__":
    test_ask_history_does_not_leak()
    print("test_ask_history_does_not_leak passed")
