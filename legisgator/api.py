from fastapi import FastAPI, UploadFile, HTTPException
from starlette.responses import JSONResponse
import asyncio, uvicorn
from .engine import analyze
from .config import get_settings
from structlog import get_logger

app = FastAPI(title="LegisGator", version="0.0.4")
log = get_logger()
cfg = get_settings()

@app.post("/analyze")
async def analyze_doc(file: UploadFile):
    data = await file.read()
    if len(data) > cfg.MAX_PAYLOAD_KB * 1024:
        raise HTTPException(413, "Payload too large.")
    text = data.decode()
    try:
        result = await asyncio.wait_for(analyze(text), timeout=cfg.GPT_TIMEOUT + 5)
    except asyncio.TimeoutError:
        raise HTTPException(504, "Analysis timeout.")
    return JSONResponse(result)

@app.get("/health")
async def health():  # simple liveness
    return {"status": "ok"}

def _run():
    uvicorn.run(
        "legisgator.api:app",
        host="0.0.0.0",
        port=8000,
        http="auto",          # HTTP/2 if client supports
        workers=2,
        log_level=cfg.LOG_LEVEL.lower(),
    )
