import asyncio, hashlib
from .extractor import extract_props
from .logic_engine import detect_contradictions
from .weakness import score_props
from structlog import get_logger

log = get_logger()

async def analyze(text: str) -> dict:
    text_hash = hashlib.sha256(text.encode()).hexdigest()         # safe trace
    props = await extract_props(text)
    contradictions, scores = await asyncio.gather(
        detect_contradictions(props),
        score_props(props),
    )
    weakest = sorted(scores, key=lambda x: x["score"])[:3]
    log.debug("analysis_complete", doc=text_hash,
              contradictions=len(contradictions), props=len(props))
    return {"props": props, "contradictions": contradictions, "weakest": weakest}
