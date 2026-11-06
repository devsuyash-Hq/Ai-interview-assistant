"""
Voice Engine
============
Handles text-to-speech (the assistant asking questions aloud) and
speech-to-text (listening to the candidate's spoken answer).

Falls back gracefully to typed input if no microphone/speaker is
available, so the assistant never crashes mid-interview.
"""

import pyttsx3
import speech_recognition as sr


class VoiceEngine:
    def __init__(self, rate: int = 175):
        try:
            self.engine = pyttsx3.init()
            self.engine.setProperty("rate", rate)
            self.tts_available = True
        except Exception:
            self.tts_available = False

        self.recognizer = sr.Recognizer()
        try:
            self.microphone = sr.Microphone()
            self.mic_available = True
        except Exception:
            self.mic_available = False

    def speak(self, text: str):
        """Speak text aloud (if TTS available) and always print it."""
        print(f"\n🎤 Interviewer: {text}")
        if self.tts_available:
            self.engine.say(text)
            self.engine.runAndWait()

    def listen(self) -> str:
        """
        Record from the microphone and transcribe via Google's speech
        recognition API. Falls back to typed input on any failure.
        """
        if not self.mic_available:
            return input("Your answer (type — no mic detected): ").strip()

        with self.microphone as source:
            print("🎙️  Listening... (speak now)")
            self.recognizer.adjust_for_ambient_noise(source, duration=0.5)
            try:
                audio = self.recognizer.listen(source, timeout=8, phrase_time_limit=90)
            except sr.WaitTimeoutError:
                print("No speech detected.")
                return input("Your answer (type instead): ").strip()

        try:
            text = self.recognizer.recognize_google(audio)
            print(f"You said: {text}")
            return text
        except (sr.UnknownValueError, sr.RequestError):
            print("Couldn't understand the audio.")
            return input("Your answer (type instead): ").strip()
