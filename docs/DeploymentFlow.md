# DeploymentFlow.md

## Overview
The AI Deployment Flow describes the technical pipeline from the moment a user uploads a dataset to when the fine-tuned model is deployed as a live endpoint.

---

## 1. Model Selection
- Users can select a pre-configured model (e.g., LLaMA, Mistral, Stable Diffusion).
- The `/api/list_models` endpoint fetches all compatible base models listed in `/configs/models.yaml`.
- Each model entry includes its HuggingFace or Ollama reference, architecture type, and GPU requirements.

---

## 2. Dataset Upload
- Datasets are uploaded through the web dashboard or API.
- Data is encrypted using AES-256 and stored temporarily in distributed storage (IPFS/S3 hybrid).
- Metadata (hashes, size, structure) is logged for reproducibility.

---

## 3. Job Scheduling
- The `job_scheduler.py` analyzes available GPU nodes using telemetry from the network.
- It selects nodes based on VRAM, bandwidth, latency, and current load.
- Training jobs are chunked into smaller tasks and distributed across nodes.

---

## 4. Distributed Training
- The `training_orchestrator.py` runs fine-tuning via **Ray**, **Horovod**, or **DeepSpeed**.
- Gradients are synchronized via RPC, ensuring convergence.
- Checkpoints are generated every `N` steps and mirrored across nodes.

---

## 5. Telemetry and Performance Reporting
- Each node reports:
  - GPU utilization (%)
  - Power draw (W)
  - Memory consumption
  - Training step speed (tokens/s)
- These values are collected by the `telemetry_collector.py` and fed to the Reward Distribution system.

---

## 6. Model Packaging and Deployment
- Once the job completes:
  - Final model weights are verified via checksum.
  - The model is containerized using Docker or OCI.
  - Deployment occurs automatically via `/api/deploy_model`.
  - An endpoint (REST or WebSocket) is created for inference.

---

## 7. Reward Distribution
- Training job metadata is sent to the `reward_manager_adapter.py`.
- GPU-time and performance metrics are converted into **$HYPER** tokens.
- Nodes receive payouts proportional to their contribution.

---

## 8. Monitoring and Logs
- Users can check training progress and logs via `/api/get_job_status`.
- Dashboard visualizes:
  - GPU node map
  - Training progress bar
  - Estimated completion time
  - Token cost in real-time
