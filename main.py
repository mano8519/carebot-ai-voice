import os
import tempfile
from fastapi import FastAPI, HTTPException
from fastapi.responses import FileResponse
from pydantic import BaseModel
from openai import OpenAI

app = FastAPI(title="CareBot AI Voice")
client = OpenAI(api_key=os.environ.get("OPENAI_API_KEY"))

class SpeakRequest(BaseModel):
    text: str

@app.get("/health")
def health():
    return {"ok": True}

@app.post("/speak")
def speak(req: SpeakRequest):
    if not os.environ.get("OPENAI_API_KEY"):
        raise HTTPException(status_code=500, detail="OPENAI_API_KEY is not configured")
    if not req.text.strip():
        raise HTTPException(status_code=400, detail="text is required")

    tmp = tempfile.NamedTemporaryFile(delete=False, suffix=".mp3")
    tmp.close()

    with client.audio.speech.with_streaming_response.create(
        model="gpt-4o-mini-tts",
        voice="coral",
        input=req.text,
        instructions=(
            "Speak like a warm, natural conversational assistant for an older adult. "
            "Use a comfortable normal pace, clear pronunciation, short pauses, and a friendly tone. "
            "Do not sound robotic or overly slow."
        ),
        response_format="mp3",
    ) as response:
        response.stream_to_file(tmp.name)

    return FileResponse(
        tmp.name,
        media_type="audio/mpeg",
        filename="carebot_voice.mp3",
        background=None
    )
