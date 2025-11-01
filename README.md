# Hypernode LLM Deployer

**Deploy and Host LLMs on the Hypernode Network**

Deploy language models (Qwen, DeepSeek, Llama, Mistral) as always-online hosted services across the Hypernode GPU network.

![Python](https://img.shields.io/badge/Python-3.10+-blue)
![FastAPI](https://img.shields.io/badge/Framework-FastAPI-green)
![Ollama](https://img.shields.io/badge/Models-Ollama-orange)

---

## 🎯 Overview

Unlike one-off jobs, the LLM Deployer allows you to:
- Deploy a model that stays online 24/7
- Get a dedicated inference endpoint
- Load balance across multiple nodes
- Auto-scale based on demand
- Cache model weights for fast startup

---

## ✨ Features

- ✅ **Deploy Popular Models**: Qwen, DeepSeek R1, Llama 3, Mistral, GPT-J
- ✅ **REST API**: OpenAI-compatible endpoints
- ✅ **WebSocket Streaming**: Real-time token streaming
- ✅ **Load Balancing**: Distribute requests across nodes
- ✅ **Auto-scaling**: Spin up/down nodes based on load
- ✅ **Model Caching**: Fast model loading via IPFS/S3
- ✅ **Version Management**: Deploy multiple model versions
- ✅ **Cost Optimization**: Pay per token, not per hour

---

## 🚀 Quick Start

### Deploy a Model

```bash
# Install CLI
npm install -g @hypernode/llm-cli

# Login with wallet
hypernode login

# Deploy DeepSeek R1 Qwen 7B
hypernode deploy \
  --model deepseek-r1-qwen-7b \
  --nodes 3 \
  --min-vram 16 \
  --region us-east

# Get endpoint URL
# https://deepseek-abc123.hypernode.sol/v1/chat/completions
```

### Use the Endpoint

```python
import openai

client = openai.OpenAI(
    api_key="your_hyper_api_key",
    base_url="https://deepseek-abc123.hypernode.sol/v1"
)

response = client.chat.completions.create(
    model="deepseek-r1-qwen-7b",
    messages=[
        {"role": "user", "content": "Explain quantum computing"}
    ],
    stream=True
)

for chunk in response:
    print(chunk.choices[0].delta.content, end="")
```

---

## 📁 Supported Models

| Model | Size | Min VRAM | Speed | Cost/1M tokens |
|-------|------|----------|-------|----------------|
| Qwen 2.5 7B | 7B | 8GB | Fast | 0.5 HYPER |
| DeepSeek R1 Qwen 7B | 7B | 10GB | Fast | 0.6 HYPER |
| Llama 3.1 8B | 8B | 12GB | Fast | 0.7 HYPER |
| Mistral 7B | 7B | 8GB | Fast | 0.5 HYPER |
| Llama 3.1 70B | 70B | 80GB | Slow | 3.0 HYPER |
| DeepSeek R1 671B | 671B | 320GB | Very Slow | 15.0 HYPER |

---

## 🏗️ Architecture

```
User Request
    │
    ▼
┌─────────────────────────┐
│  Load Balancer (HAProxy)│
└────────┬────────────────┘
         │
    ┌────┴─────┬──────┐
    ▼          ▼      ▼
┌────────┐ ┌────────┐ ┌────────┐
│ Node 1 │ │ Node 2 │ │ Node 3 │
│ GPU A  │ │ GPU B  │ │ GPU C  │
│ (RTX   │ │ (RTX   │ │ (A100) │
│ 4090)  │ │ 3090)  │ │        │
└────────┘ └────────┘ └────────┘
```

---

## 💰 Pricing

### Pay Per Token
- No upfront costs
- No minimum usage
- Pay only for actual inference
- Competitive rates vs. OpenAI/Anthropic

### Example Costs
- 1M tokens Qwen 7B: 0.5 HYPER (~$5)
- 1M tokens Llama 70B: 3.0 HYPER (~$30)
- Compare: OpenAI GPT-4: $30/1M tokens

---

## 📚 API Reference

### OpenAI-Compatible

```typescript
POST /v1/chat/completions
POST /v1/completions
POST /v1/embeddings
GET  /v1/models
```

### Hypernode-Specific

```typescript
GET  /v1/deployment/status
POST /v1/deployment/scale
GET  /v1/deployment/metrics
```

---

## 🔧 CLI Commands

```bash
# Deploy model
hypernode deploy --model <model-name>

# List deployments
hypernode list

# Scale deployment
hypernode scale <deployment-id> --nodes 5

# Get logs
hypernode logs <deployment-id>

# Terminate deployment
hypernode terminate <deployment-id>
```

---

## 📄 License

MIT License

---

**Deploy your AI in minutes, not days! 🚀**
