import os, httpx

OLLAMA_BASE_URL = os.getenv("OLLAMA_BASE_URL", "http://ollama:11434")

async def chat(prompt: str, model: str, **kwargs):
    payload = {"model": model, "prompt": prompt}
    payload.update(kwargs or {})
    async with httpx.AsyncClient(timeout=120) as client:
        r = await client.post(f"{OLLAMA_BASE_URL}/api/generate", json=payload)
        r.raise_for_status()
        return r.json()
