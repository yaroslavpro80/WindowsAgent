from __future__ import annotations


class VoicePipeline:
    """Minimal placeholder for wake-word, STT and TTS adapters."""

    def __init__(self, wake_word: str = "assistant") -> None:
        self.wake_word = wake_word

    def listen_once(self) -> str:
        return ""

    def speak(self, text: str) -> None:
        print(f"[TTS] {text}")
