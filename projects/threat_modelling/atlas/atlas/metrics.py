from __future__ import annotations

from atlas.schema import Metrics, ThreatInstance


def compute_metrics(
    instances: list[ThreatInstance],
    *,
    prior_instance_ids: set[str] | None = None,
) -> Metrics:
    total = len(instances)
    acknowledged_statuses = {"mitigated", "accepted"}

    acknowledged = sum(1 for i in instances if i.status in acknowledged_statuses)

    applicable = [i for i in instances if i.status != "not_applicable"]
    total_risk = sum(float(i.risk_score) for i in applicable)
    mitigated_risk = sum(float(i.risk_score) for i in applicable if i.status in acknowledged_statuses)
    exposure = sum(float(i.risk_score) for i in applicable if i.status == "unmitigated")

    coverage = (acknowledged / total) if total else 1.0
    risk_weighted = (mitigated_risk / total_risk) if total_risk else 1.0

    drift = None
    if prior_instance_ids is not None:
        current_ids = {i.id for i in instances}
        drift = len(current_ids - prior_instance_ids)

    return Metrics(
        total_threats=total,
        acknowledged_threats=acknowledged,
        coverage=float(coverage),
        total_risk=float(total_risk),
        mitigated_risk=float(mitigated_risk),
        risk_weighted_coverage=float(risk_weighted),
        exposure=float(exposure),
        drift=drift,
    )

