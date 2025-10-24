"""
Reward Manager Adapter.

Maps telemetry into a normalized summary the Reward Distribution Manager can
consume. This module does not perform token transfers; it returns an aggregate
structure that the on-chain logic (or a separate service) will execute.
"""
from __future__ import annotations
from dataclasses import dataclass
from typing import Dict, List
from collections import defaultdict

from .telemetry_collector import TelemetryCollector, TelemetryRecord


@dataclass
class RewardShare:
    node_id: str
    weight: float  # normalized share 0..1


class RewardManagerAdapter:
    def __init__(self, telemetry: TelemetryCollector) -> None:
        self.telemetry = telemetry

    def summarize_job(self, job_id: str) -> List[RewardShare]:
        records: List[TelemetryRecord] = self.telemetry.list_for_job(job_id)
        if not records:
            return []

        # Very naive weighting: proportional to tokens_per_second * gpu_utilization
        raw: Dict[str, float] = defaultdict(float)
        for r in records:
            raw[r.node_id] += max(0.0, r.tokens_per_second) * max(0.0, r.gpu_utilization)

        denom = sum(raw.values()) or 1.0
        return [RewardShare(node_id=n, weight=v / denom) for n, v in raw.items()]
