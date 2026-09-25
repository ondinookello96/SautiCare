"""
SautiCare TTS (Text-to-Speech) Service
Handles speech synthesis formatting for natural, elder-respectful cadence.
Supports both browser Web Speech (Swahili 'sw-TZ' / 'sw-KE') and audio generation parameters.
"""

from typing import Dict, Any

class TTSService:
    def __init__(self):
        # Default East African Swahili voice profile
        self.default_lang = "sw-KE"
        self.speech_rate = 0.85  # Slightly slower, gentle pace for elders
        self.pitch = 1.0

    def format_speech_payload(self, text: str, emotion: str = "calm") -> Dict[str, Any]:
        """
        Formats speech synthesis instructions for client playback.
        """
        rate = self.speech_rate
        if emotion == "emergency":
            rate = 0.90  # Clear and reassuring

        return {
            "text": text,
            "lang": self.default_lang,
            "rate": rate,
            "pitch": self.pitch,
            "emotion": emotion
        }
