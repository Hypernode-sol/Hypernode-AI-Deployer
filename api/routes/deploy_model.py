from __future__ import annotations
from fastapi import APIRouter, HTTPException
from pydantic import BaseModel, conint, confloat
from typing import Optional

from ...core.model_registry import ModelRegistry
from ...core.job_scheduler import JobScheduler, JobSpec
from ...core.training_orchestrator import TrainingOrchestrator
from ...core.telemetry_collector import TelemetryCollector
from ...core.reward_manager_adapter import RewardManagerAdapter

router = APIRouter(tags=["deploy"])

_registry = ModelRegistry()
_scheduler = JobScheduler(_registry)
_orchestrator = TrainingOrchestrator(_scheduler.store)
_orchestrator.start()
_telemetry = TelemetryCollector()
_reward_adapter = RewardManagerAdapter(_telemetry)


class DeployRequest(BaseModel):
    model_name: str
    dataset_uri: str
    epochs: conint(ge=1) = 1
    learning_rate: confloat(gt=0) = 5e-5
    batch_size: conint(ge=1) = 1
    seed: Optional[int] = 42
    user_id: Optional[str] = None


class DeployResponse(BaseModel):
    job_id: str
    status: str
    message: str


@router.post("/deploy_model", response_model=DeployResponse)
def deploy_model(req: DeployRequest) -> DeployResponse:
    """Validate and submit a training job to the scheduler."""
    try:
        status = _scheduler.submit(JobSpec(**req.dict()))
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))

    return DeployResponse(job_id=status.job_id, status=status.status, message=status.message)
