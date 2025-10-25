#!/usr/bin/env bash
set -euo pipefail
CFG="configs/axolotl/qwen1_5b_lora.yaml"
echo "[Axolotl] Training with ${CFG} ..."
docker run --gpus all --rm -v $PWD:/workspace -e HF_TOKEN winglian/axolotl:main-cuda12.1 axolotl train ${CFG}
echo "[Axolotl] Done. Checkpoints in ./checkpoints"
