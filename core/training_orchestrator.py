"""
Training Orchestrator module.

Consumes scheduled jobs and coordinates distributed fine-tuning across GPU nodes.
In this reference implementation, we only simulate state transitions. Integrate
with Ray/Horovod/DeepSpeed and a network resource manager in production.
"""
from __future__ import annotations
from typing import Optional
import time
from threading import Thread, Event

from .job_scheduler import InMemoryJobStore, JobStatus


class TrainingOrchestrator:
    """Background loop that simulates job execution and progress updates."""
    def __init__(self, store: InMemoryJobStore) -> None:
        self.store = store
        self._stop = Event()
        self._thread: Optional[Thread] = None

    def start(self) -> None:
        if self._thread and self._thread.is_alive():
            return
        self._stop.clear()
        self._thread = Thread(target=self._run, daemon=True)
        self._thread.start()

    def stop(self) -> None:
        self._stop.set()
        if self._thread:
            self._thread.join(timeout=2.0)

    def _run(self) -> None:
        while not self._stop.is_set():
            for job in list(self.store.list()):
                if job.status == "queued":
                    self.store.update(job.job_id, status="running", message="Distributed training started.")
                elif job.status == "running":
                    new_prog = min(1.0, job.progress + 0.10)
                    msg = "Training in progress." if new_prog < 1.0 else "Training complete. Packaging model..."
                    self.store.update(job.job_id, progress=new_prog, message=msg)
                    if new_prog >= 1.0:
                        self.store.update(job.job_id, status="completed", message="Deployed inference endpoint.")
                # terminal states are ignored
            time.sleep(1.0)
