"""
AssemblyAI Streaming & Transcription Service for SautiCare
Handles real-time audio streaming to AssemblyAI, session lifecycle,
and event handling for sub-second speech recognition.
"""

import os
import json
import logging
import asyncio
from typing import Callable, Optional
import websockets

logger = logging.getLogger(__name__)

class AssemblyAIService:
    def __init__(self, api_key: Optional[str] = None):
        self.api_key = api_key or os.getenv("ASSEMBLYAI_API_KEY", "")
        self.sample_rate = 16000
        self.ws_url = f"wss://api.assemblyai.com/v2/realtime/ws?sample_rate={self.sample_rate}"
        self.ws = None
        self.is_connected = False

    async def connect(self, on_transcript_callback: Callable[[str, bool], None]):
        """
        Connect to AssemblyAI Realtime WebSocket API and listen for streaming transcripts.
        """
        if not self.api_key or self.api_key == "your_assemblyai_api_key_here":
            logger.warning("No valid ASSEMBLYAI_API_KEY found. Running in simulation/fallback mode.")
            return

        headers = {
            "Authorization": self.api_key
        }

        try:
            self.ws = await websockets.connect(self.ws_url, additional_headers=headers)
            self.is_connected = True
            logger.info("Connected to AssemblyAI Realtime STT WebSocket.")

            # Start background listener loop
            asyncio.create_task(self._listen_transcripts(on_transcript_callback))
        except Exception as e:
            logger.error(f"Failed to connect to AssemblyAI WebSocket: {e}")
            self.is_connected = False

    async def _listen_transcripts(self, callback: Callable[[str, bool], None]):
        """
        Listen for incoming transcription messages from AssemblyAI.
        """
        try:
            async for message in self.ws:
                data = json.loads(message)
                msg_type = data.get("message_type")
                text = data.get("text", "")

                if msg_type == "SessionBegins":
                    logger.info("AssemblyAI Session started: %s", data.get("session_id"))
                elif msg_type == "PartialTranscript":
                    if text:
                        callback(text, False)
                elif msg_type == "FinalTranscript":
                    if text:
                        callback(text, True)
                elif msg_type == "SessionTerminated":
                    logger.info("AssemblyAI Session terminated.")
                    break
        except websockets.exceptions.ConnectionClosed:
            logger.info("AssemblyAI WebSocket connection closed.")
        except Exception as e:
            logger.error(f"Error reading AssemblyAI stream: {e}")
        finally:
            self.is_connected = False

    async def send_audio_chunk(self, audio_data: bytes):
        """
        Send raw PCM audio bytes to AssemblyAI streaming endpoint.
        """
        if self.ws and self.is_connected:
            try:
                await self.ws.send(audio_data)
            except Exception as e:
                logger.error(f"Error sending audio chunk to AssemblyAI: {e}")

    async def close(self):
        """
        Close the streaming session.
        """
        if self.ws and self.is_connected:
            try:
                terminate_msg = json.dumps({"terminate_session": True})
                await self.ws.send(terminate_msg)
                await self.ws.close()
            except Exception:
                pass
            finally:
                self.is_connected = False
