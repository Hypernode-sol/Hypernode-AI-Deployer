import os, httpx

VLLM_BASE_URL = os.getenv("VLLM_BASE_URL", "http://vllm:8000/v1")

async def chat(messages, model: str, **kwargs):
    payload = {"model": model, "messages": messages}
    payload.update(kwargs or {})
    async with httpx.AsyncClient(timeout=120) as client:
        r = await client.post(f"{VLLM_BASE_URL}/chat/completions", json=payload)
        r.raise_for_status()
        return r.json()
