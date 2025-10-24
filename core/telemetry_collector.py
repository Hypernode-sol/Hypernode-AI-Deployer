"""
Telemetry Collector module.

Receives metrics from GPU nodes and exposes a simple API for the Reward Manager.
In production, prefer a push-based design (Prometheus remote-write, OpenTelemetry)
or a message bus (NATS/Kafka). This module validates payload schema and buffers.
"""
from __future__ import annotations
from dataclasses import dataclass
from typing import Dict, List
from datetime import datetime, timezone


@dataclass
class TelemetryRecord:
    node_id: str
    job_id: str
    gpu_utilization: float
    power_watts: float
    vram_used_gb: float
    tokens_per_second: float
    timestamp: datetime


class TelemetryCollector:
    def __init__(self) -> None:
        self._records: List[TelemetryRecord] = []

    def submit(self, payload: Dict) -> TelemetryRecord:
        record = TelemetryRecord(
            node_id=str(payload["node_id"]),
            job_id=str(payload["job_id"]),
            gpu_utilization=float(payload.get("gpu_utilization", 0.0)),
            power_watts=float(payload.get("power_watts", 0.0)),
            vram_used_gb=float(payload.get("vram_used_gb", 0.0)),
            tokens_per_second=float(payload.get("tokens_per_second", 0.0)),
            timestamp=datetime.now(timezone.utc),
        )
        self._records.append(record)
        return record

    def list_for_job(self, job_id: str) -> List[TelemetryRecord]:
        return [r for r in self._records if r.job_id == job_id]
