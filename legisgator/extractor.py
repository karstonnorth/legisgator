import json
from openai import AsyncOpenAI, OpenAIError
from pathlib import Path
from .config import get_settings
import diskcache as dc


_cfg = get_settings()
client = AsyncOpenAI(api_key=_cfg.OPENAI_API_KEY)
_cache = dc.Cache(_cfg.CACHE_PATH)


async def _llm_call(text: str) -> list[dict]:
    prompt_path = Path(__file__).with_name("prompts").joinpath("extractor.txt")
    system_prompt = prompt_path.read_text()

    try:
        resp = await client.chat.completions.create(
            model=_cfg.MODEL,
            response_format={"type": "json_object"},
            messages=[
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": text},
            ],
            temperature=0.0,
        )
        return resp.model_dump()
    except OpenAIError as e:
        raise RuntimeError(f"LLM extract failed: {str(e)}")

async def extract_props(text: str) -> list[dict]:
    key = f"extract:{hash(text)}"
    if (hit := _cache.get(key)):
        return hit

    props = await _llm_call(text)
    _cache.set(key, props, expire=_cfg.CACHE_TTL_HOURS * 3600)   # TTL now env‑driven
    log.info("props_cached", key=key, ttl=_cfg.CACHE_TTL_HOURS, hits=len(props))
    return props
