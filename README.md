# 🧠 Hypernode AI Deployer  
> Distributed AI Model Deployer — serving, fine-tuning, and managing LLMs across GPU nodes.


## 🚀 Overview

**Hypernode AI Deployer** is the orchestration layer for deploying, fine-tuning, and managing AI models across the **Hypernode Network** — a distributed GPU compute marketplace powered by Solana.  

It supports **inference, fine-tuning, and distributed training** for major open-source LLMs like **DeepSeek**, **Qwen**, **Mistral**, and **LLaMA**, with integration layers for **vLLM**, **Ollama**, and **Axolotl (QLoRA/PEFT)**.

---

## 🧩 Core Capabilities

| Feature | Description |
|----------|--------------|
| 🔁 **Distributed Inference** | Run LLMs via **vLLM** (OpenAI-compatible endpoint) or **Ollama** (GGUF runtime). |
| 🧮 **Fine-tuning Pipeline** | Integrated **Axolotl** runner for PEFT/QLoRA training on local or distributed GPUs. |
| 💾 **Checkpoint Management** | Automatic upload/download of models via **MinIO/S3**. |
| ⚙️ **API Layer** | REST endpoints for deployment, job tracking, and telemetry. |
| 🧠 **LLM Registry** | Declarative configs for DeepSeek, Qwen, and other models. |
| 🛰️ **Reward Integration** | Hooks for reward distribution and telemetry collection from the Hypernode core network. |

---

## 📦 Components

```
├── api/
│   └── main.py                # FastAPI service (deploy/list/status)
├── core/
│   ├── backends/
│   │   ├── vllm_backend.py    # Inference backend for DeepSeek/Qwen (vLLM)
│   │   └── ollama_backend.py  # GGUF runtime (Ollama)
│   ├── trainers/
│   │   └── axolotl_runner.py  # Fine-tuning orchestrator (QLoRA)
│   ├── checkpoint_store.py    # MinIO/S3 upload utilities
│   └── model_registry.py      # Default model configs
├── configs/
│   ├── models/                # Model configuration files
│   ├── axolotl/               # Fine-tuning configs
│   └── datasets/              # Example training data
├── docker/
│   ├── docker-compose.yaml    # vLLM, Ollama, API, MinIO stack
│   ├── api.Dockerfile
│   ├── ollama/Modelfile       # Ollama model definition
│   └── vllm.Dockerfile
└── scripts/
    └── train_qwen1_5b.sh      # Axolotl training helper
```

---

## ⚙️ Setup & Deployment

### 1️⃣ Clone the repository
```bash
git clone https://github.com/Hypernode-sol/Hypernode-AI-Deployer.git
cd Hypernode-AI-Deployer
```

### 2️⃣ Environment configuration
Create your `.env` file:
```bash
cp .env.example .env
```
Edit and fill with your credentials:
```bash
HF_TOKEN=your_huggingface_token_here
S3_ENDPOINT=http://minio:9000
S3_BUCKET=hypernode-checkpoints
S3_ACCESS_KEY=minioadmin
S3_SECRET_KEY=minioadmin
S3_USE_SSL=false
API_PORT=8080
```

### 3️⃣ Launch stack
Run all containers (vLLM, Ollama, FastAPI, MinIO):
```bash
docker compose -f docker/docker-compose.yaml --env-file .env up -d --build
```

---

## 🧠 Inference Examples

### DeepSeek-R1-Distill (vLLM)
```bash
curl http://localhost:8000/v1/chat/completions   -H "Content-Type: application/json"   -d '{
    "model": "deepseek-ai/DeepSeek-R1-Distill-Qwen-7B",
    "messages": [{"role":"user","content":"Explain Hypernode in one line."}]
  }'
```

### Qwen via Ollama
```bash
docker exec -it ollama ollama create qwen2.5-7b-instruct -f /workspace/docker/ollama/Modelfile
docker exec -it ollama ollama run qwen2.5-7b-instruct
```

---

## 🔧 Fine-tuning (QLoRA / PEFT)

Train Qwen 1.5B using Axolotl:
```bash
bash scripts/train_qwen1_5b.sh
```

Modify the config:
```yaml
# configs/axolotl/qwen1_5b_lora.yaml
base_model: Qwen/Qwen1.5-1.8B
load_in_4bit: true
adapter: lora
lora_r: 16
lora_alpha: 32
lora_dropout: 0.05
seq_len: 4096
dataset: configs/datasets/sample.jsonl
output_dir: /workspace/checkpoints/qwen1_5b_lora
```

Resulting adapters are stored in:
```
./checkpoints/qwen1_5b_lora/
```
You can attach these LoRAs to Ollama models by editing:
```dockerfile
# docker/ollama/Modelfile
ADAPTER ./checkpoints/qwen1_5b_lora.gguf
```

---

## 🌐 API Endpoints

| Method | Endpoint | Description |
|--------|-----------|--------------|
| `GET` | `/api/list_models` | Lists available models from vLLM and Ollama. |
| `POST` | `/api/deploy_model` | Deploys or warms up a model. |
| `GET` | `/api/get_job_status?job_id=` | Returns training/deployment job status. |

Example:
```bash
curl -X POST http://localhost:8080/api/deploy_model   -H "Content-Type: application/json"   -d '{
    "base_model": "deepseek-ai/DeepSeek-R1-Distill-Qwen-7B",
    "backend": "vllm"
  }'
```

---

## 🖥️ Monitoring & Storage

- **MinIO Dashboard:**  
  → http://localhost:9001 (user: `minioadmin`, pass: `minioadmin`)

- **vLLM Endpoint:**  
  → http://localhost:8000/v1

- **Ollama Endpoint:**  
  → http://localhost:11434

- **API Service:**  
  → http://localhost:8080/docs (Swagger UI)

---

## 🧩 Architecture Diagram

```text
               ┌──────────────────────────────┐
               │        User / Client         │
               │     (API / Dashboard UI)     │
               └─────────────┬────────────────┘
                             │
               ┌─────────────┴────────────────┐
               │     Hypernode API Layer      │
               │  deploy_model / list_models  │
               └─────────────┬────────────────┘
                             │
           ┌─────────────────┼──────────────────────┐
           │                 │                      │
   ┌───────▼──────┐   ┌──────▼──────┐      ┌────────▼────────┐
   │   vLLM        │   │   Ollama    │      │  Axolotl/PEFT   │
   │ DeepSeek/Qwen │   │ GGUF models │      │ Fine-tune jobs  │
   └───────┬───────┘   └──────┬──────┘      └────────┬────────┘
           │                  │                     │
           └───────────────┬──┴─────────────────────┘
                           │
                     ┌─────▼─────┐
                     │  MinIO/S3 │
                     │ Checkpoints│
                     └────────────┘
```

---

## 🔐 License

This project is licensed under the **MIT License**.  
Models such as **DeepSeek R1 Distill** and **Qwen** follow their respective open-source licenses (MIT / Apache 2.0).

---

## 🌍 About Hypernode

Hypernode is a **distributed GPU compute network** that connects idle compute power with AI workloads through tokenized incentives and intelligent orchestration layers.  
Learn more at **[hypernodesolana.org](https://hypernodesolana.org)**.

---

### 🤝 Contributors
- Core Engineering: **Hypernode Labs**
- AI Infrastructure: **Hypernode Network Team**
- Systems Integration: **Hypernode Compute Layer**

---

**Hypernode © 2025 — Building the distributed intelligence network of tomorrow.**

