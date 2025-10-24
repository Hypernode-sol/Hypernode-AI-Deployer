"""
Model Registry module.

Provides a simple abstraction to list, register, and retrieve model blueprints
from external catalogs (e.g., Hugging Face, Ollama). In production, this module
should handle caching, compatibility checks (GPU/VRAM/quantization), and
container build templates.
"""
from __future__ import annotations
from dataclasses import dataclass
from typing import Dict, List, Optional
import yaml
from pathlib import Path

MODELS_YAML = Path(__file__).resolve().parents[1] / "configs" / "models.yaml"


@dataclass(frozen=True)
class ModelSpec:
    """Static description of a base model available to the network."""
    name: str
    provider: str  # e.g. huggingface, ollama
    reference: str # e.g. meta-llama/Llama-3-8B
    task: str      # e.g. text-generation, embeddings, image-generation
    min_vram_gb: int
    quantization: Optional[str] = None  # e.g. Q4_K_M, bitsandbytes-4bit
    notes: Optional[str] = None


class ModelRegistry:
    """Load and serve model specifications from configs/models.yaml."""

    def __init__(self, config_path: Path = MODELS_YAML) -> None:
        self.config_path = config_path
        self._models: Dict[str, ModelSpec] = {}
        self._load()

    def _load(self) -> None:
        if not self.config_path.exists():
            raise FileNotFoundError(f"models.yaml not found at {self.config_path}")
        data = yaml.safe_load(self.config_path.read_text(encoding="utf-8")) or {}
        registry = {}
        for item in data.get("models", []):
            spec = ModelSpec(**item)
            registry[spec.name] = spec
        self._models = registry

    def list_models(self) -> List[ModelSpec]:
        return list(self._models.values())

    def get(self, name: str) -> Optional[ModelSpec]:
        return self._models.get(name)

    def refresh(self) -> None:
        """Reload from disk. Useful when updating models.yaml at runtime."""
        self._load()
