"""
SautiCare Native East African Swahili Neural TTS Service
Generates authentic Kenyan and Tanzanian Swahili speech with boosted volume (+40%)
and elder-friendly pacing (-8%) using East African Neural Voices.
Cleans emojis, abbreviations, and symbols so speech sounds 100% natural and fluid.
"""

import os
import re
import hashlib
import asyncio
import logging
import urllib.request
import urllib.parse
from pathlib import Path
from typing import Dict, Any, Optional

logger = logging.getLogger(__name__)

# Pan-African Authentic Neural Voices across 4 African Regions
PAN_AFRICAN_VOICES = {
    # 🇰🇪 🇹🇿 East Africa (Kiswahili)
    "sw-ke-zuri": {"voice": "sw-KE-ZuriNeural", "region": "East Africa", "lang": "Kiswahili (Kenya)", "gender": "Female", "flag": "🇰🇪"},
    "sw-ke-rafiki": {"voice": "sw-KE-RafikiNeural", "region": "East Africa", "lang": "Kiswahili (Kenya)", "gender": "Male", "flag": "🇰🇪"},
    "sw-tz-daudi": {"voice": "sw-TZ-DaudiNeural", "region": "East Africa", "lang": "Kiswahili (Tanzania)", "gender": "Male", "flag": "🇹🇿"},
    "sw-tz-rehema": {"voice": "sw-TZ-RehemaNeural", "region": "East Africa", "lang": "Kiswahili (Tanzania)", "gender": "Female", "flag": "🇹🇿"},

    # 🇳🇬 West Africa (Nigerian Pidgin & Dialect)
    "ng-ezinne": {"voice": "en-NG-EzinneNeural", "region": "West Africa", "lang": "Nigerian Pidgin (Nigeria)", "gender": "Female", "flag": "🇳🇬"},
    "ng-abeo": {"voice": "en-NG-AbeoNeural", "region": "West Africa", "lang": "Nigerian Pidgin (Nigeria)", "gender": "Male", "flag": "🇳🇬"},

    # 🇿🇦 Southern Africa (isiZulu)
    "zu-thando": {"voice": "zu-ZA-ThandoNeural", "region": "Southern Africa", "lang": "isiZulu (South Africa)", "gender": "Female", "flag": "🇿🇦"},
    "zu-themba": {"voice": "zu-ZA-ThembaNeural", "region": "Southern Africa", "lang": "isiZulu (South Africa)", "gender": "Male", "flag": "🇿🇦"},

    # 🇪🇹 Horn of Africa (Amharic)
    "am-mekdes": {"voice": "am-ET-MekdesNeural", "region": "Horn of Africa", "lang": "Amharic / አማርኛ (Ethiopia)", "gender": "Female", "flag": "🇪🇹"},
    "am-ameha": {"voice": "am-ET-AmehaNeural", "region": "Horn of Africa", "lang": "Amharic / አማርኛ (Ethiopia)", "gender": "Male", "flag": "🇪🇹"},
}

# Backward compatibility alias
EAST_AFRICAN_VOICES = {k: v["voice"] for k, v in PAN_AFRICAN_VOICES.items()}

def clean_text_for_swahili_tts(text: str) -> str:
    """
    Cleans up emojis, English technical acronyms, and symbols
    so the East African TTS voice pronounces everything naturally in Swahili.
    """
    t = text

    # Remove all emojis
    t = re.sub(r'[\U00010000-\U0010ffff]', '', t)
    t = re.sub(r'[^\w\s.,!?:;\'"–-]', ' ', t)

    # Phonetic replacements for symbols & acronyms to prevent English phonetic butcher
    replacements = [
        (r'\bM-Pesa\b', 'Mpesa'),
        (r'\bMpesa\b', 'Em-pesa'),
        (r'\bWhatsApp\b', 'Watsapu'),
        (r'\bYouTube\b', 'Yutubu'),
        (r'\bSMS\b', 'ujumbe'),
        (r'\bPIN\b', 'namba ya siri'),
        (r'\bUSSD\b', 'huduma ya simu'),
        (r'\bWi-Fi\b', 'wayafai'),
        (r'\bWiFi\b', 'wayafai'),
        (r'\bBluetooth\b', 'blututhi'),
        (r'\bCamera\b', 'kamera'),
        (r'\bGallery\b', 'albamu'),
        (r'\*334#', 'nyota tatu tatu nne reli'),
        (r'\*144#', 'nyota moja nne nne reli'),
        (r'\*544#', 'nyota tano nne nne reli'),
        (r'\*100#', 'nyota mia moja reli'),
        (r'85%', 'asilimia themanini na tano'),
        (r'100%', 'asilimia mia moja'),
        (r'\(.*?\)', ''), # Remove text inside brackets like (85%)
    ]

    for pattern, repl in replacements:
        t = re.sub(pattern, repl, t, flags=re.IGNORECASE)

    # Clean multiple spaces
    t = re.sub(r'\s+', ' ', t).strip()
    return t

class TTSService:
    def __init__(self, cache_dir: Optional[Path] = None):
        self.default_voice_key = "sw-ke-zuri"
        self.default_voice = EAST_AFRICAN_VOICES[self.default_voice_key]
        # Loudness boosted for older ears: +40% volume
        self.volume = "+40%"
        # Slightly slower cadence for elder comprehension: -8% speed
        self.rate = "-8%"
        
        self.cache_dir = cache_dir or (Path(__file__).parent.parent / "static" / "audio_cache")
        self.cache_dir.mkdir(parents=True, exist_ok=True)

    async def get_or_generate_audio(self, text: str, voice_key: str = "sw-ke-zuri") -> str:
        """
        Synthesizes authentic Swahili audio and returns the URL path to the cached MP3 file.
        """
        clean_text = clean_text_for_swahili_tts(text)
        if not clean_text:
            return ""

        voice = EAST_AFRICAN_VOICES.get(voice_key, voice_key if "Neural" in str(voice_key) else self.default_voice)
        
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
