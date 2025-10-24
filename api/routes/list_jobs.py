from __future__ import annotations
from fastapi import APIRouter, Depends, Query
from pydantic import BaseModel
from typing import List, Optional

from ..auth import auth_required
from ..state import scheduler

router = APIRouter(tags=["jobs"])


class JobItem(BaseModel):
    job_id: str
    status: str
    progress: float
    message: str
    user_id: str | None = None


class JobListResponse(BaseModel):
    items: List[JobItem]
    page: int
    page_size: int
    total: int


@router.get("/list_jobs", response_model=JobListResponse)
def list_jobs(
    principal: str = Depends(auth_required),
    status: Optional[str] = Query(None, description="Filter by status"),
    user_id: Optional[str] = Query(None, description="Filter by user id"),
    page: int = Query(1, ge=1),
    page_size: int = Query(10, ge=1, le=100),
) -> JobListResponse:
    items = scheduler.store.list_filtered(status=status, user_id=user_id)
    total = len(items)
    start = (page - 1) * page_size
    end = start + page_size
    page_items = items[start:end]
    return JobListResponse(
        items=[JobItem(job_id=i.job_id, status=i.status, progress=i.progress, message=i.message, user_id=i.user_id) for i in page_items],
        page=page,
        page_size=page_size,
        total=total,
    )
