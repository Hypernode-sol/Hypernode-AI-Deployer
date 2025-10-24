"""
Job Scheduler module.

Responsible for validating incoming training jobs, selecting eligible GPU nodes,
and placing jobs into the orchestrator queue. This simplified reference uses an
in-memory store. Replace with a durable queue (e.g., Redis, NATS, Kafka) in prod.
"""
from __future__ import annotations
from dataclasses import dataclass, field
from typing import Dict, List, Optional
from uuid import uuid4
from datetime import datetime, timezone

from .model_registry import ModelRegistry, ModelSpec


@dataclass
class JobSpec:
    """User-submitted job specification."""
    model_name: str
    dataset_uri: str  # e.g., ipfs://..., s3://..., file://...
    epochs: int = 1
    learning_rate: float = 5e-5
    batch_size: int = 1
    seed: int = 42
    user_id: Optional[str] = None


@dataclass
class JobStatus:
    job_id: str
    status: str  # queued | running | completed | failed | cancelled
    created_at: datetime
    updated_at: datetime
    progress: float = 0.0  # 0..1
    message: str = ""
    checkpoints: List[str] = field(default_factory=list)


class InMemoryJobStore:
    """Naive in-memory job store. Replace with a persistent backend in prod."""
    def __init__(self) -> None:
        self.jobs: Dict[str, JobStatus] = {}

    def create(self, status: JobStatus) -> None:
        self.jobs[status.job_id] = status

    def get(self, job_id: str) -> Optional[JobStatus]:
        return self.jobs.get(job_id)

    def update(self, job_id: str, **kwargs) -> Optional[JobStatus]:
        job = self.jobs.get(job_id)
        if not job:
            return None
        for k, v in kwargs.items():
            setattr(job, k, v)
        job.updated_at = datetime.now(timezone.utc)
        return job

    def list(self) -> List[JobStatus]:
        return list(self.jobs.values())


class JobScheduler:
    """Validate jobs against ModelRegistry and enqueue for orchestration."""
    def __init__(self, registry: ModelRegistry, store: Optional[InMemoryJobStore] = None) -> None:
        self.registry = registry
        self.store = store or InMemoryJobStore()

    def submit(self, spec: JobSpec) -> JobStatus:
        model: ModelSpec = self.registry.get(spec.model_name)
        if not model:
            raise ValueError(f"Unknown model '{spec.model_name}'. Call /api/list_models to discover.")

        job_id = str(uuid4())
        now = datetime.now(timezone.utc)
        status = JobStatus(
            job_id=job_id,
            status="queued",
            created_at=now,
            updated_at=now,
            progress=0.0,
            message="Job accepted and queued for orchestration.",
        )
        self.store.create(status)
        return status
