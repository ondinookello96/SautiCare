"""
SautiCare Main Application Server
FastAPI Web and WebSocket server powering the Swahili Voice Agent for African Elders.
Integrates AssemblyAI Realtime Streaming STT, Swahili Agent Engine, and Offline Resilience.
"""

import os
import json
import logging
from pathlib import Path
from dotenv import load_dotenv
from fastapi import FastAPI, WebSocket, WebSocketDisconnect, Request
from fastapi.responses import HTMLResponse, JSONResponse
from fastapi.staticfiles import StaticFiles
from pydantic import BaseModel

from services.assemblyai_service import AssemblyAIService
from services.agent_engine import AgentEngine
from services.tts_service import TTSService

# Configure logging
logging.basicConfig(level=logging.INFO, format="%(asctime)s [%(levelname)s] %(message)s")
logger = logging.getLogger("sauticare")

# Load environment variables
load_dotenv()

app = FastAPI(
    title="SautiCare",
    description="Swahili Voice Assistant for Elderly Smartphone Users across Africa",
    version="1.0.0"
)

# Initialize Core Services
agent_engine = AgentEngine()
tts_service = TTSService()
assemblyai_key = os.getenv("ASSEMBLYAI_API_KEY", "")

# Mount static folder
static_dir = Path(__file__).parent / "static"
static_dir.mkdir(exist_ok=True)
app.mount("/static", StaticFiles(directory=str(static_dir)), name="static")

class TextQueryRequest(BaseModel):
    text: str

@app.get("/")
async def get_index():
    index_file = static_dir / "index.html"
    if index_file.exists():
        with open(index_file, "r", encoding="utf-8") as f:
            return HTMLResponse(f.read())
    return HTMLResponse("<h1>SautiCare Server Running</h1><p>Static UI not yet loaded.</p>")

@app.get("/api/health")
async def health_check():
    has_aai_key = bool(assemblyai_key and assemblyai_key != "your_assemblyai_api_key_here")
    return {
        "status": "healthy",
        "service": "SautiCare Swahili Voice Agent",
        "assemblyai_configured": has_aai_key,
        "offline_support": True,
        "language": "Kiswahili (East Africa)"
    }

@app.post("/api/process-text")
async def process_text_query(req: TextQueryRequest):
    """
    Process Swahili text directly (useful for testing and instant keyboard fallback).
    """
    result = agent_engine.process_swahili_intent(req.text)
    tts_payload = tts_service.format_speech_payload(
        text=result.get("swahili_response", ""),
        emotion="emergency" if result.get("is_emergency") else "calm"
    )
    result["tts"] = tts_payload
    return JSONResponse(result)

@app.post("/api/emergency/sos")
async def trigger_emergency():
    """
    Direct SOS trigger endpoint.
    """
    result = agent_engine.tool_trigger_emergency_sos(
        distress_type="Dharura ya Moja kwa Moja (Instant SOS)",
        details="Kitufe cha dharura kimebonyezwa moja kwa moja"
    )
    result["tts"] = tts_service.format_speech_payload(
        text=result["swahili_response"],
        emotion="emergency"
    )
    return JSONResponse(result)

@app.websocket("/ws/voice")
async def websocket_voice_endpoint(websocket: WebSocket):
    """
    Bidirectional WebSocket endpoint for streaming speech audio to AssemblyAI
    and returning live Swahili transcripts and agent tool actions.
    """
    await websocket.accept()
    logger.info("Client connected to SautiCare Voice WebSocket.")

    aai_service = AssemblyAIService(api_key=assemblyai_key)

    def handle_transcript(transcript: str, is_final: bool):
        # Callback from AssemblyAI stream
        asyncio_task = asyncio.create_task(
            _send_transcript_update(websocket, transcript, is_final)
        )

    async def _send_transcript_update(ws: WebSocket, text: str, is_final: bool):
        try:
            payload = {
                "type": "transcript",
                "text": text,
                "is_final": is_final
            }
            if is_final:
                # Run Swahili intent and tool execution
                decision = agent_engine.process_swahili_intent(text)
                tts_info = tts_service.format_speech_payload(
                    text=decision["swahili_response"],
                    emotion="emergency" if decision.get("is_emergency") else "calm"
                )
                payload["decision"] = decision
                payload["tts"] = tts_info

            await ws.send_text(json.dumps(payload))
        except Exception as e:
            logger.error(f"Error sending transcript update: {e}")

    # Connect to AssemblyAI Realtime STT
    import asyncio
    if aai_service.api_key and aai_service.api_key != "your_assemblyai_api_key_here":
        await aai_service.connect(handle_transcript)

    try:
        while True:
            data = await websocket.receive()
            if "bytes" in data and data["bytes"]:
                # Stream raw audio chunk to AssemblyAI
                await aai_service.send_audio_chunk(data["bytes"])
            elif "text" in data and data["text"]:
                msg = json.loads(data["text"])
                if msg.get("action") == "process_text":
                    # Direct text query through WebSocket
                    text_input = msg.get("text", "")
                    decision = agent_engine.process_swahili_intent(text_input)
                    tts_info = tts_service.format_speech_payload(
                        text=decision["swahili_response"],
                        emotion="emergency" if decision.get("is_emergency") else "calm"
                    )
                    await websocket.send_text(json.dumps({
                        "type": "agent_response",
                        "text": text_input,
                        "decision": decision,
                        "tts": tts_info
                    }))
    except WebSocketDisconnect:
        logger.info("Voice WebSocket disconnected.")
    except Exception as e:
        logger.error(f"Voice WebSocket error: {e}")
    finally:
        await aai_service.close()

if __name__ == "__main__":
    import uvicorn
    port = int(os.getenv("PORT", 8000))
    host = os.getenv("HOST", "0.0.0.0")
    logger.info(f"Starting SautiCare Server on http://{host}:{port}")
    uvicorn.run(app, host=host, port=port)
