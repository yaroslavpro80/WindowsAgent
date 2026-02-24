from __future__ import annotations

from dataclasses import dataclass
from typing import Any


@dataclass
class VoiceConfig:
    enabled: bool
    tts_enabled: bool
    stt_enabled: bool
    device_index: int
    ambient_adjust_seconds: float


class VoicePipeline:
    def __init__(self, wake_word: str = "assistant", config: dict[str, Any] | None = None) -> None:
        self.wake_word = wake_word
        c = config or {}
        self.config = VoiceConfig(
            enabled=bool(c.get("enabled", True)),
            tts_enabled=bool(c.get("tts_enabled", True)),
            stt_enabled=bool(c.get("stt_enabled", True)),
            device_index=int(c.get("device_index", -1)),
            ambient_adjust_seconds=float(c.get("ambient_adjust_seconds", 0.5)),
        )
        self._tts_engine = None
        self._recognizer = None
        self._microphone = None
        self._init_audio()

    def _init_audio(self) -> None:
        if not self.config.enabled:
            return
        if self.config.tts_enabled:
            try:
                import pyttsx3

                self._tts_engine = pyttsx3.init()
            except Exception:
                self._tts_engine = None
        if self.config.stt_enabled:
            try:
                import speech_recognition as sr

                self._recognizer = sr.Recognizer()
                mic_kwargs = {}
                if self.config.device_index >= 0:
                    mic_kwargs["device_index"] = self.config.device_index
                self._microphone = sr.Microphone(**mic_kwargs)
                with self._microphone as source:
                    self._recognizer.adjust_for_ambient_noise(
                        source, duration=self.config.ambient_adjust_seconds
                    )
            except Exception:
                self._recognizer = None
                self._microphone = None

    def listen_once(self) -> str:
        if not self.config.enabled or self._recognizer is None or self._microphone is None:
            return ""
        try:
            audio = None
            with self._microphone as source:
                audio = self._recognizer.listen(source, timeout=3, phrase_time_limit=8)
            if audio is None:
                return ""
            text = self._recognizer.recognize_google(audio, language="uk-UA")
            return text.strip()
        except Exception:
            return ""

    def is_wake_word(self, text: str) -> bool:
        return self.wake_word.lower() in text.lower()

    def speak(self, text: str) -> None:
        if self.config.enabled and self.config.tts_enabled and self._tts_engine is not None:
            try:
                self._tts_engine.say(text)
                self._tts_engine.runAndWait()
                return
            except Exception:
                pass
        print(f"[TTS] {text}")
