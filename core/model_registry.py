from dataclasses import dataclass

@dataclass
class ModelSpec:
    name: str
    backend: str  # "vllm" | "ollama"
    config_path: str | None = None

DEFAULT_MODELS = [
    ModelSpec(name="deepseek-ai/DeepSeek-R1-Distill-Qwen-7B", backend="vllm", config_path="configs/models/deepseek-r1-distill-qwen-7b.yaml"),
    ModelSpec(name="qwen2.5-7b-instruct", backend="ollama", config_path="configs/models/qwen-7b.yaml"),
]
