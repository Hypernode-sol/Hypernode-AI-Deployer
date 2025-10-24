from __future__ import annotations
from fastapi import APIRouter
from pydantic import BaseModel
from typing import List

from ...core.model_registry import ModelRegistry, ModelSpec

router = APIRouter(tags=["models"])
_registry = ModelRegistry()


class ModelDTO(BaseModel):
    name: str
    provider: str
    reference: str
    task: str
    min_vram_gb: int
    quantization: str | None = None
    notes: str | None = None

    @classmethod
    def from_spec(cls, spec: ModelSpec) -> "ModelDTO":
        return cls(**spec.__dict__)


@router.get("/list_models", response_model=List[ModelDTO])
def list_models() -> List[ModelDTO]:
    """Return all available base models from the registry."""
    return [ModelDTO.from_spec(m) for m in _registry.list_models()]
