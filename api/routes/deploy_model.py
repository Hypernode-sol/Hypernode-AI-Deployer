from __future__ import annotations
from fastapi import APIRouter, HTTPException
from pydantic import BaseModel, conint, confloat
from typing import Optional

from ..auth import auth_required
from ..state import registry as _registry, scheduler as _scheduler
from ...core.job_scheduler import JobSpec

router = APIRouter(tags=["deploy"])



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
from fastapi import Depends

def deploy_model(req: DeployRequest, principal: str = Depends(auth_required)) -> DeployResponse:
    """Validate and submit a training job to the scheduler."""
    try:
        status = _scheduler.submit(JobSpec(**req.dict()))
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))

    return DeployResponse(job_id=status.job_id, status=status.status, message=status.message)
