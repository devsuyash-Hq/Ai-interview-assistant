"""
Configuration management for AI Interview Assistant.
Loads environment variables from a .env file and exposes them
as a single, typed Config object used across the project.
"""

import os
from dotenv import load_dotenv

load_dotenv()


class Config:
    GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")
    GEMINI_MODEL = os.getenv("GEMINI_MODEL", "gemini-2.5-flash")
    VOICE_RATE = int(os.getenv("VOICE_RATE", "175"))
    DEFAULT_NUM_QUESTIONS = 5

    @classmethod
    def validate(cls):
        """Fail fast with a clear message if the API key is missing."""
        if not cls.GEMINI_API_KEY:
            raise EnvironmentError(
                "GEMINI_API_KEY not found.\n"
                "Create a file named '.env' in the project folder with:\n"
                "GEMINI_API_KEY=your_key_here\n"
                "(Get a free key at https://aistudio.google.com/apikey)"
            )
