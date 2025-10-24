"""
FastAPI entrypoint for Hypernode-AI-Deployer.

Exposes endpoints to list models, submit training jobs, check status, and render
a lightweight HTML dashboard. Replace in-memory stores with persistent services
for production. All comments are written in English by convention.
"""
from __future__ import annotations
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from .routes.list_models import router as list_models_router
from .routes.deploy_model import router as deploy_router
from .routes.get_job_status import router as status_router
from .routes.user_dashboard import router as dashboard_router

app = FastAPI(title="Hypernode AI Deployer", version="0.1.0")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(list_models_router, prefix="/api")
app.include_router(deploy_router, prefix="/api")
app.include_router(status_router, prefix="/api")
app.include_router(dashboard_router, prefix="/api")
