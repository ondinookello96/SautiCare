"""
SautiCare Main Application Server
FastAPI Web and WebSocket server powering the Swahili Voice Agent for African Elders.
Integrates AssemblyAI Realtime Streaming STT, Swahili Agent Engine, Native East African TTS, and Offline Resilience.
"""

import os
import json
import logging
from pathlib import Path
from dotenv import load_dotenv
from fastapi import FastAPI, WebSocket, WebSocketDisconnect, Request, Query
from fastapi.responses import HTMLResponse, JSONResponse, FileResponse
from fastapi.staticfiles import StaticFiles
from pydantic import BaseModel

from services.assemblyai_service import AssemblyAIService
from services.agent_engine import AgentEngine
from services.tts_service import TTSService, EAST_AFRICAN_VOICES, PAN_AFRICAN_VOICES

# Configure logging
logging.basicConfig(level=logging.INFO, format="%(asctime)s [%(levelname)s] %(message)s")
logger = logging.getLogger("sauticare")

# Load environment variables
load_dotenv()

app = FastAPI(
    title="SautiCare",
    description="Pan-African Voice Assistant & Smartphone Navigator for Elderly Users",
    version="1.0.0"
)

# Initialize Core Services
agent_engine = AgentEngine()
tts_service = TTSService()
assemblyai_key = os.getenv("ASSEMBLYAI_API_KEY", "")

# Mount static folder
static_dir = Path(__file__).parent / "static"
static_dir.mkdir(exist_ok=True)
(static_dir / "audio_cache").mkdir(exist_ok=True)
app.mount("/static", StaticFiles(directory=str(static_dir)), name="static")

class TextQueryRequest(BaseModel):
    text: str
    voice: str = "sw-ke-zuri"
    lang: str = "sw"

@app.get("/")
async def get_index():
    index_file = static_dir / "index.html"
    if index_file.exists():
        with open(index_file, "r", encoding="utf-8") as f:
            return HTMLResponse(f.read())
    return HTMLResponse("<h1>SautiCare Server Running</h1><p>Static UI not yet loaded.</p>")

@app.get("/manifest.json")
async def get_manifest():
    manifest_file = static_dir / "manifest.json"
    if manifest_file.exists():
        return FileResponse(manifest_file, media_type="application/manifest+json")
    return JSONResponse(status_code=404, content={"detail": "Manifest not found"})

@app.get("/sw.js")
async def get_service_worker():
    sw_file = static_dir / "sw.js"
    if sw_file.exists():
        return FileResponse(sw_file, media_type="application/javascript")
    return JSONResponse(status_code=404, content={"detail": "Service Worker not found"})

@app.get("/api/health")
async def health_check():
    has_aai_key = bool(assemblyai_key and assemblyai_key != "your_assemblyai_api_key_here")
    return {
        "status": "healthy",
        "service": "SautiCare Swahili Voice Agent",
        "pan_african_regions": ["East Africa", "West Africa", "Southern Africa", "Horn of Africa"],
        "assemblyai_configured": has_aai_key,
        "offline_support": True,
        "language": "Kiswahili (East Africa)",
        "available_voices": list(PAN_AFRICAN_VOICES.keys())
    }

@app.get("/api/voices")
async def get_voices():
    voices_list = []
    for vid, meta in PAN_AFRICAN_VOICES.items():
        vcode = meta["voice"].split("-")[2].replace("Neural", "")
        lang_prefix = vid.split("-")[0] if vid.split("-")[0] in ["sw", "ng", "zu", "am"] else "sw"
        voices_list.append({
            "id": vid,
            "name": f"{meta['flag']} {vcode} ({meta['lang']})",
            "gender": meta["gender"],
            "region": meta["region"],
            "lang_code": lang_prefix
        })
    return {"voices": voices_list}

@app.get("/api/tts")
async def get_tts_audio(text: str = Query(..., description="Text to synthesize"), voice: str = "sw-ke-zuri"):
    """
    Synthesize authentic African regional speech with boosted volume and return audio file.
    """
    audio_url = await tts_service.get_or_generate_audio(text, voice)
    if audio_url:
        file_path = static_dir / "audio_cache" / Path(audio_url).name
        if file_path.exists():
            return FileResponse(file_path, media_type="audio/mpeg")
    return JSONResponse({"error": "Failed to synthesize speech audio"}, status_code=500)

@app.post("/api/tts")
async def post_tts_audio(req: TextQueryRequest):
    """
    Synthesize authentic African speech for JSON POST requests and return audio URL.
    """
    audio_url = await tts_service.get_or_generate_audio(req.text, req.voice)
    if audio_url:
        return {"audio_url": audio_url, "text": req.text, "voice": req.voice}
    return JSONResponse({"error": "Failed to synthesize audio"}, status_code=500)

@app.post("/api/process-text")
async def process_text_query(req: TextQueryRequest):
    """
    Process text and return structured tool decision with regional audio URL.
    """
    result = agent_engine.process_intent(req.text, lang=req.lang)
    spoken_reply = result.get("swahili_response", "")
    
    # Generate authentic regional audio
    audio_url = await tts_service.get_or_generate_audio(spoken_reply, req.voice)
    result["audio_url"] = audio_url
    return JSONResponse(result)

@app.post("/api/emergency/sos")
async def trigger_emergency(voice: str = "sw-ke-zuri", lang: str = "sw"):
    """
    Direct SOS trigger endpoint supporting Pan-African languages.
    """
    result = agent_engine.tool_trigger_emergency_sos(
        lang_key=lang,
        distress_type="Dharura ya Moja kwa Moja (Instant SOS)",
        details="Kitufe cha dharura kimebonyezwa moja kwa moja"
    )
    spoken_reply = result["swahili_response"]
    audio_url = await tts_service.get_or_generate_audio(spoken_reply, voice)
    result["audio_url"] = audio_url
    return JSONResponse(result)

@app.post("/api/transcribe-audio")
async def transcribe_audio_endpoint(
    request: Request,
    voice: str = Query("sw-ke-zuri"),
    lang: str = Query("sw")
):
    """
    Accepts raw audio bytes recorded from user microphone,
    transcribes it with AssemblyAI, runs the Pan-African intent engine,
    and returns the decision with authentic regional speech.
    """
    audio_bytes = await request.body()
    if not audio_bytes:
        return JSONResponse({"error": "No audio received"}, status_code=400)

    aai_service = AssemblyAIService(api_key=assemblyai_key)
    transcript = aai_service.transcribe_audio_bytes(audio_bytes, lang=lang)

    if not transcript:
        defaults = {
            "sw": "Nisaidie",
            "ng": "Help me abeg",
            "zu": "Ngifuna usizo",
            "am": "እባክዎን እርዳኝ"
        }
        transcript = defaults.get(lang, "Nisaidie")

    decision = agent_engine.process_intent(transcript, lang=lang)
    audio_url = await tts_service.get_or_generate_audio(decision["swahili_response"], voice)
    decision["audio_url"] = audio_url
    decision["transcript"] = transcript

    return JSONResponse(decision)

@app.websocket("/ws/voice")
async def websocket_voice_endpoint(
    websocket: WebSocket,
    voice: str = "sw-ke-zuri",
    lang: str = "sw"
):
    """
    Bidirectional WebSocket endpoint for streaming speech audio to AssemblyAI
    and returning live transcripts and native Pan-African audio.
    """
    await websocket.accept()
    logger.info("Client connected to SautiCare Voice WebSocket.")

    state = {"lang": lang, "voice": voice}
    aai_service = AssemblyAIService(api_key=assemblyai_key)

    def handle_transcript(transcript: str, is_final: bool):
        import asyncio
        asyncio.create_task(_send_transcript_update(websocket, transcript, is_final))

    async def _send_transcript_update(ws: WebSocket, text: str, is_final: bool):
        try:
            payload = {
                "type": "transcript",
                "text": text,
                "is_final": is_final
            }
            if is_final:
                decision = agent_engine.process_intent(text, lang=state["lang"])
                audio_url = await tts_service.get_or_generate_audio(decision["swahili_response"], state["voice"])
                decision["audio_url"] = audio_url
                payload["decision"] = decision

            await ws.send_text(json.dumps(payload))
        except Exception as e:
            logger.error(f"Error sending transcript update: {e}")

    # Connect to AssemblyAI Realtime STT
    if aai_service.api_key and aai_service.api_key != "your_assemblyai_api_key_here":
        await aai_service.connect(handle_transcript)

    try:
        while True:
            data = await websocket.receive()
            if "bytes" in data and data["bytes"]:
                await aai_service.send_audio_chunk(data["bytes"])
            elif "text" in data and data["text"]:
                msg = json.loads(data["text"])
                if msg.get("action") == "set_language":
                    state["lang"] = msg.get("lang", state["lang"])
                    state["voice"] = msg.get("voice", state["voice"])
                elif msg.get("action") == "process_text":
                    text_input = msg.get("text", "")
                    voice_pref = msg.get("voice", state["voice"])
                    lang_pref = msg.get("lang", state["lang"])
                    decision = agent_engine.process_intent(text_input, lang=lang_pref)
                    audio_url = await tts_service.get_or_generate_audio(decision["swahili_response"], voice_pref)
                    decision["audio_url"] = audio_url
                    await websocket.send_text(json.dumps({
                        "type": "agent_response",
                        "text": text_input,
                        "decision": decision
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
