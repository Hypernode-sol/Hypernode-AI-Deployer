import os
import uuid
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
import httpx

VLLM_BASE_URL = os.getenv("VLLM_BASE_URL", "http://vllm:8000/v1")
OLLAMA_BASE_URL = os.getenv("OLLAMA_BASE_URL", "http://ollama:11434")
API_PORT = int(os.getenv("API_PORT", "8080"))

app = FastAPI(title="Hypernode AI Deployer API")

# --------- Schemas ---------
class DeployRequest(BaseModel):
    base_model: str
    backend: str  # "vllm" or "ollama"
    finetune_checkpoint: str | None = None  # s3://bucket/path or local path
    params: dict | None = None

# --------- Helpers ---------
async def vllm_list_models():
    # vLLM OpenAI-compatible: not all builds expose /models; fallback to using requested model names
    try:
        async with httpx.AsyncClient(timeout=30) as client:
            r = await client.get(f"{VLLM_BASE_URL}/models")
            if r.status_code == 200:
                return r.json()
    except Exception:
        pass
    return {"data": []}

async def ollama_list_models():
    async with httpx.AsyncClient(timeout=30) as client:
        r = await client.get(f"{OLLAMA_BASE_URL}/api/tags")
        r.raise_for_status()
        return r.json()

# --------- Routes ---------
@app.get("/api/list_models")
async def list_models():
    v = await vllm_list_models()
    try:
        o = await ollama_list_models()
    except Exception:
        o = {"models": []}
    return {"vllm": v, "ollama": o}

@app.post("/api/deploy_model")
async def deploy_model(req: DeployRequest):
    job_id = str(uuid.uuid4())
    if req.backend == "vllm":
        # vLLM "deployment" is typically already running; we can optionally warmup via a quick request
        payload = {
            "model": req.base_model,
            "messages": [{"role":"user","content":"ping"}],
            "max_tokens": 4
        }
        try:
            async with httpx.AsyncClient(timeout=60) as client:
                await client.post(f"{VLLM_BASE_URL}/chat/completions", json=payload)
        except Exception as e:
            raise HTTPException(status_code=500, detail=f"vLLM warmup failed: {e}")
        return {"job_id": job_id, "status": "deployed", "backend": "vllm", "model": req.base_model}

    elif req.backend == "ollama":
        # Ensure model exists (create via Modelfile if needed)
        try:
            async with httpx.AsyncClient(timeout=120) as client:
                # Try to pull base model (if FROM <model> in Modelfile already exists, this is a no‑op)
                await client.post(f"{OLLAMA_BASE_URL}/api/pull", json={"name": req.base_model})
        except Exception as e:
            raise HTTPException(status_code=500, detail=f"Ollama pull failed: {e}")
        return {"job_id": job_id, "status": "deployed", "backend": "ollama", "model": req.base_model}
    else:
        raise HTTPException(status_code=400, detail="backend must be 'vllm' or 'ollama'")

@app.get("/api/get_job_status")
async def get_job_status(job_id: str):
    # Minimal stub for now
    return {"job_id": job_id, "status": "ok"}
