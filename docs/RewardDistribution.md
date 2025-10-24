# RewardDistribution.md

## Overview
The Reward Distribution system ensures fair and transparent payment to GPU nodes participating in distributed AI training or inference.

---

## 1. Metrics Collected

| Metric | Description | Weight |
|--------|--------------|--------|
| GPU-Time | Total active computation time per node | 0.5 |
| Throughput | Samples/tokens processed per second | 0.25 |
| Uptime | Stability and availability during job | 0.15 |
| Latency | Response speed in synchronization | 0.10 |

Total reward weight = 1.0

---

## 2. Calculation Formula

Each node receives:
```
Reward(node) = JobTotalReward * (
   0.5 * GPU_Time(node) / ΣGPU_Time +
   0.25 * Throughput(node) / ΣThroughput +
   0.15 * Uptime(node) / ΣUptime +
   0.10 * (1 - Latency(node) / MaxLatency)
)
```

- All metrics are normalized per job scope.
- Final payouts are executed by the **Reward Distribution Manager** (already part of the main Hypernode Network).

---

## 3. Token Distribution Process

1. Each job generates a **Job Metadata Record (JMR)**.
2. The `telemetry_collector.py` submits GPU metrics to the **Reward Manager Adapter**.
3. The **Reward Manager** aggregates performance data from all nodes.
4. Rewards are transferred in **$HYPER** via Solana-based smart contracts.

---

## 4. Anti-Fraud & Validation

- Node signatures are verified cryptographically before accepting metrics.
- Double-reporting or fake workloads are rejected automatically.
- Nodes with high reliability and correct reports gain **Reputation Boost** (affects future job prioritization).

---

## 5. Audit & Transparency

- All reward transactions are stored in the **Hypernode Telemetry Ledger**.
- Jobs can be audited retrospectively for performance verification.
- Users can view reward logs in their dashboard with on-chain proof.

---

## 6. Future Enhancements

- ZK-Proof of GPU-Time (verifiable training without exposing model data)
- Dynamic weighting model (adapts reward factors by workload type)
- Integration with Hypernode Reputation System
