"""
SautiCare Native East African Swahili Neural TTS Service
Generates authentic Kenyan and Tanzanian Swahili speech with boosted volume (+35%)
and elder-friendly pacing (-10%) using East African Neural Voices.
"""

import os
import hashlib
import asyncio
import logging
import urllib.request
import urllib.parse
from pathlib import Path
from typing import Dict, Any, Optional

logger = logging.getLogger(__name__)

# Available Authentic East African Voices
EAST_AFRICAN_VOICES = {
    "sw-ke-zuri": "sw-KE-ZuriNeural",      # Kenyan Female (Warm, elder-respectful, default)
    "sw-ke-rafiki": "sw-KE-RafikiNeural",  # Kenyan Male (Friendly, clear)
    "sw-tz-daudi": "sw-TZ-DaudiNeural",    # Tanzanian Male (Classic coastal Swahili)
    "sw-tz-rehema": "sw-TZ-RehemaNeural",  # Tanzanian Female (Clear, melodious)
}

class TTSService:
    def __init__(self, cache_dir: Optional[Path] = None):
        self.default_voice_key = "sw-ke-zuri"
        self.default_voice = EAST_AFRICAN_VOICES[self.default_voice_key]
        # Loudness boosted for older ears: +35% volume
        self.volume = "+35%"
        # Slightly slower cadence for elder comprehension: -10% speed
        self.rate = "-10%"
        
        self.cache_dir = cache_dir or (Path(__file__).parent.parent / "static" / "audio_cache")
        self.cache_dir.mkdir(parents=True, exist_ok=True)

    async def get_or_generate_audio(self, text: str, voice_key: str = "sw-ke-zuri") -> str:
        """
        Synthesizes authentic Swahili audio and returns the URL path to the cached MP3 file.
        """
        clean_text = text.strip()
        if not clean_text:
            return ""

        voice = EAST_AFRICAN_VOICES.get(voice_key, self.default_voice)
        
        # Unique hash based on text and voice
        text_hash = hashlib.md5(f"{voice}:{clean_text}".encode("utf-8")).hexdigest()
        file_name = f"{text_hash}.mp3"
        file_path = self.cache_dir / file_name

        # Return cached file if already generated
        if file_path.exists() and file_path.stat().st_size > 0:
            return f"/static/audio_cache/{file_name}"

        # 1. Primary: Edge Neural TTS (Real Kenyan/Tanzanian Voice Actors)
        success = await self._generate_edge_tts(clean_text, voice, file_path)
        if success:
            return f"/static/audio_cache/{file_name}"

        # 2. Fallback: Google Swahili TTS
        logger.warning("Edge-TTS unavailable, falling back to Google Swahili TTS.")
        success = self._generate_google_swahili_tts(clean_text, file_path)
        if success:
            return f"/static/audio_cache/{file_name}"

        return ""

    async def _generate_edge_tts(self, text: str, voice: str, output_path: Path) -> bool:
        try:
            import edge_tts
            communicate = edge_tts.Communicate(
                text=text,
                voice=voice,
                rate=self.rate,
                volume=self.volume
            )
            await communicate.save(str(output_path))
            return output_path.exists() and output_path.stat().st_size > 0
        except Exception as e:
            logger.error(f"Error in edge-tts generation: {e}")
            return False

    def _generate_google_swahili_tts(self, text: str, output_path: Path) -> bool:
        try:
            url = "https://translate.google.com/translate_tts?ie=UTF-8&tl=sw&client=tw-ob&q=" + urllib.parse.quote(text)
            req = urllib.request.Request(url, headers={"User-Agent": "Mozilla/5.0"})
            with urllib.request.urlopen(req, timeout=5) as response:
                data = response.read()
                with open(output_path, "wb") as f:
                    f.write(data)
            return True
        except Exception as e:
            logger.error(f"Error in Google Swahili fallback TTS: {e}")
            return False
