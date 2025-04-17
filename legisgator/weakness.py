import asyncio, json
import diskcache as dc
from openai import AsyncOpenAI, OpenAIError
from structlog import get_logger
from .config import get_settings

_cfg = get_settings()
log = get_logger()
client = AsyncOpenAI(api_key=_cfg.OPENAI_API_KEY)
_cache = dc.Cache(_cfg.CACHE_PATH)

async def _score_call(props_json: str) -> list[dict]:
    try:
        resp = await asyncio.wait_for(
            client.chat.completions.create(
                model=_cfg.MODEL,
                response_format={"type": "json_object"},
                messages=[
                    {"role": "system", "content": open(__file__.replace("weakness.py", "prompts/scorer.txt")).read()},
                    {"role": "user", "content": props_json},
                ],
            ),
            timeout=_cfg.GPT_TIMEOUT,
        )
        return resp.model_dump()
    except (asyncio.TimeoutError, OpenAIError) as exc:
        log.error("LLM scorer failed", err=str(exc))
        raise

async def score_props(props: list[dict]) -> list[dict]:
    key = f"score:{hash(json.dumps(props, sort_keys=True))}"
    if (hit := _cache.get(key)):
        return hit
    scores = await _score_call(json.dumps(props))
    _cache.set(key, scores, expire=60 * 60 * 24)
    return scores
