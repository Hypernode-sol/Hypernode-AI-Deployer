from __future__ import annotations
from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from typing import List

from ...core.job_scheduler import JobScheduler, JobStatus
from ...core.model_registry import ModelRegistry

router = APIRouter(tags=["status"])

_registry = ModelRegistry()
_scheduler = JobScheduler(_registry)


class JobStatusDTO(BaseModel):
    job_id: str
    status: str
    progress: float
    message: str
    checkpoints: List[str]

    @classmethod
    def from_model(cls, m: JobStatus) -> "JobStatusDTO":
        return cls(
            job_id=m.job_id,
            status=m.status,
            progress=m.progress,
            message=m.message,
            checkpoints=m.checkpoints,
        )


@router.get("/get_job_status/{job_id}", response_model=JobStatusDTO)
def get_job_status(job_id: str) -> JobStatusDTO:
    """Return current job status and progress."""
    status = _scheduler.store.get(job_id)
    if not status:
        raise HTTPException(status_code=404, detail="Job not found.")
    return JobStatusDTO.from_model(status)
