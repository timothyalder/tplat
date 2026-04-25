from __future__ import annotations

import json
from dataclasses import asdict
from typing import Any

from atlas.loader import ensure_parent_dir
from atlas.schema import Metrics, ThreatInstance, ThreatReport


def report_to_dict(report: ThreatReport) -> dict[str, Any]:
    # dataclasses.asdict is fine here; we post-process ordering when dumping JSON.
    return asdict(report)


def write_report(report: ThreatReport, *, path: str) -> None:
    ensure_parent_dir(path)
    payload = report_to_dict(report)
    with open(path, "w", encoding="utf-8") as file:
        json.dump(payload, file, indent=2, sort_keys=True)
        file.write("\n")


def load_report(path: str) -> ThreatReport:
    with open(path, "r", encoding="utf-8") as file:
        raw = json.load(file)
    if not isinstance(raw, dict):
        raise ValueError("report JSON must be an object")
    return _report_from_dict(raw)


def _report_from_dict(raw: dict[str, Any]) -> ThreatReport:
    instances = [
        ThreatInstance(
            id=i["id"],
            template_id=i["template_id"],
            bound_element=i["bound_element"],
            parameter_values=dict(i.get("parameter_values", {})),
            risk_score=float(i["risk_score"]),
            status=i.get("status", "unmitigated"),
        )
        for i in raw.get("instances", [])
    ]
    m = raw.get("metrics", {})
    metrics = Metrics(
        total_threats=int(m["total_threats"]),
        acknowledged_threats=int(m["acknowledged_threats"]),
        coverage=float(m["coverage"]),
        total_risk=float(m["total_risk"]),
        mitigated_risk=float(m["mitigated_risk"]),
        risk_weighted_coverage=float(m["risk_weighted_coverage"]),
        exposure=float(m["exposure"]),
        drift=(int(m["drift"]) if m.get("drift") is not None else None),
    )
    lint = raw.get("lint", [])
    template_ids = list(raw.get("template_ids", []))
    from atlas.schema import LintIssue

    lint_issues = [LintIssue(code=i["code"], message=i["message"], where=i.get("where")) for i in lint]
    return ThreatReport(instances=instances, metrics=metrics, lint=lint_issues, template_ids=template_ids)
