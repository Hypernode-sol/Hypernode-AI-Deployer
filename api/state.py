from __future__ import annotations
from . import auth  # noqa: F401 (ensures env vars are loaded)
from ..core.model_registry import ModelRegistry
from ..core.job_scheduler import JobScheduler
from ..core.training_orchestrator import TrainingOrchestrator
from ..core.telemetry_collector import TelemetryCollector
from ..core.reward_manager_adapter import RewardManagerAdapter

# Global singletons to keep in-memory state consistent across routes.
registry = ModelRegistry()
scheduler = JobScheduler(registry)
orchestrator = TrainingOrchestrator(scheduler.store)
orchestrator.start()
telemetry = TelemetryCollector()
reward_adapter = RewardManagerAdapter(telemetry)
