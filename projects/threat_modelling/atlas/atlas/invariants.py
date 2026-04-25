from __future__ import annotations

from atlas.schema import SystemModel, ThreatReport


def assert_all_boundary_crossing_edges_have_threats(model: SystemModel, report: ThreatReport) -> None:
    edge_ids_requiring = {e.id for e in model.edges if e.trust_boundary_crossed}
    if not edge_ids_requiring:
        return

    threatened_edges = {i.bound_element for i in report.instances if i.bound_element in edge_ids_requiring}
    missing = sorted(edge_ids_requiring - threatened_edges)
    if missing:
        raise AssertionError(f"boundary-crossing edges without any threats: {missing}")


def assert_all_threats_acknowledged(report: ThreatReport) -> None:
    bad = [i.id for i in report.instances if i.status not in ("mitigated", "accepted", "not_applicable")]
    if bad:
        raise AssertionError(f"unacknowledged threat instances: {bad[:20]}")


def assert_high_risk_mitigated(report: ThreatReport, *, threshold: float) -> None:
    bad = [
        i.id
        for i in report.instances
        if i.status != "not_applicable" and i.risk_score > threshold and i.status != "mitigated"
    ]
    if bad:
        raise AssertionError(f"high-risk instances not mitigated: {bad[:20]}")


def assert_exposure_not_increased(current: ThreatReport, prior: ThreatReport) -> None:
    if current.metrics.exposure > prior.metrics.exposure:
        raise AssertionError(
            f"exposure increased: prior={prior.metrics.exposure:.3f} current={current.metrics.exposure:.3f}"
        )

