from __future__ import annotations

import hashlib
from typing import Any, Literal

from atlas.lint import lint_model
from atlas.metrics import compute_metrics
from atlas.predicate import PredicateError, evaluate_predicate, parse_predicate
from atlas.schema import (
    Asset,
    Edge,
    Node,
    RequiredCapabilities,
    SystemModel,
    ThreatImpact,
    ThreatInstance,
    ThreatReport,
    ThreatStatus,
    ThreatTemplate,
)


class EvaluationError(ValueError):
    pass


def evaluate(
    model: SystemModel,
    templates: list[ThreatTemplate],
    *,
    statuses: dict[str, str] | None = None,
    prior_instance_ids: set[str] | None = None,
) -> ThreatReport:
    lint = lint_model(model)

    parsed_templates: list[tuple[ThreatTemplate, list[Any]]] = []
    for template in templates:
        try:
            preds = [parse_predicate(expr) for expr in template.conditions]
        except PredicateError as exc:
            raise EvaluationError(f"template {template.id}: {exc}") from exc
        parsed_templates.append((template, preds))

    instances: list[ThreatInstance] = []
    for template, predicates in parsed_templates:
        if template.applies_to == "node":
            for node in model.nodes:
                if _match_all(predicates, model=model, element_type="node", element=node):
                    instances.append(_instantiate(template, model=model, element_type="node", element=node))
        elif template.applies_to == "edge":
            for edge in model.edges:
                if _match_all(predicates, model=model, element_type="edge", element=edge):
                    instances.append(_instantiate(template, model=model, element_type="edge", element=edge))
        elif template.applies_to == "asset":
            for asset in model.assets:
                if _match_all(predicates, model=model, element_type="asset", element=asset):
                    instances.append(_instantiate(template, model=model, element_type="asset", element=asset))
        else:
            raise EvaluationError(f"template {template.id}: unknown applies_to {template.applies_to!r}")

    instances.sort(key=lambda i: i.id)

    if statuses:
        instances = _apply_statuses(instances, statuses=statuses)

    metrics = compute_metrics(instances, prior_instance_ids=prior_instance_ids)
    return ThreatReport(
        instances=instances,
        metrics=metrics,
        lint=lint,
        template_ids=sorted({t.id for t in templates}),
    )


def _match_all(
    predicates: list[Any],
    *,
    model: SystemModel,
    element_type: Literal["node", "edge", "asset"],
    element: Node | Edge | Asset,
) -> bool:
    for predicate in predicates:
        if not evaluate_predicate(predicate, model=model, element_type=element_type, element=element):
            return False
    return True


def _instantiate(
    template: ThreatTemplate,
    *,
    model: SystemModel,
    element_type: Literal["node", "edge", "asset"],
    element: Node | Edge | Asset,
) -> ThreatInstance:
    bound_id = _element_id(element_type, element)
    instance_id = _stable_instance_id(template.id, element_type, bound_id)
    params = _extract_parameters(template.parameters, model=model, element_type=element_type, element=element)
    risk = _risk_score(template.impact, template.required_capabilities)
    return ThreatInstance(
        id=instance_id,
        template_id=template.id,
        bound_element=bound_id,
        parameter_values=params,
        risk_score=risk,
        status="unmitigated",
    )


def _element_id(element_type: str, element: Node | Edge | Asset) -> str:
    if element_type == "node":
        return element.id  # type: ignore[return-value]
    if element_type == "edge":
        return element.id  # type: ignore[return-value]
    if element_type == "asset":
        return element.id  # type: ignore[return-value]
    raise EvaluationError(f"unknown element_type {element_type!r}")


def _stable_instance_id(template_id: str, applies_to: str, bound_id: str) -> str:
    # Deterministic and human-readable, but avoid pathologically long ids.
    raw = f"{template_id}:{applies_to}:{bound_id}".encode("utf-8")
    suffix = hashlib.sha256(raw).hexdigest()[:10]
    return f"{template_id}:{applies_to}:{bound_id}:{suffix}"


def _extract_parameters(
    parameters: list[str],
    *,
    model: SystemModel,
    element_type: Literal["node", "edge", "asset"],
    element: Node | Edge | Asset,
) -> dict[str, Any]:
    from atlas.predicate import resolve_lhs

    out: dict[str, Any] = {}
    for name in parameters:
        out[name] = resolve_lhs(name, model=model, element_type=element_type, element=element)
    return out


def _apply_statuses(instances: list[ThreatInstance], *, statuses: dict[str, str]) -> list[ThreatInstance]:
    allowed: set[str] = {"unmitigated", "mitigated", "accepted", "not_applicable"}
    remapped: list[ThreatInstance] = []
    for inst in instances:
        status = statuses.get(inst.id)
        if status is None:
            remapped.append(inst)
            continue
        if status not in allowed:
            raise EvaluationError(f"invalid status {status!r} for instance id {inst.id}")
        remapped.append(
            ThreatInstance(
                id=inst.id,
                template_id=inst.template_id,
                bound_element=inst.bound_element,
                parameter_values=inst.parameter_values,
                risk_score=inst.risk_score,
                status=status,  # type: ignore[arg-type]
            )
        )
    return remapped


def _risk_score(impact: ThreatImpact | None, required: RequiredCapabilities | None) -> float:
    if impact is None:
        return 0.0
    impact_points = 0.0
    if impact.confidentiality:
        impact_points += 1.0
    if impact.integrity:
        impact_points += 1.0
    if impact.availability:
        impact_points += 1.0
    if impact_points == 0.0:
        return 0.0

    # v0.1 heuristic: lower required capability => higher likelihood => higher risk.
    factor = 1.0
    if required is None:
        return impact_points * 1.2

    network = required.network_position
    if network == "none":
        factor *= 1.6
    elif network == "adjacent":
        factor *= 1.3
    elif network == "on_path":
        factor *= 1.1

    priv = required.privileges
    if priv == "none":
        factor *= 1.6
    elif priv == "user":
        factor *= 1.3
    elif priv == "admin":
        factor *= 1.1
    elif priv == "system":
        factor *= 0.9

    ui = required.user_interaction
    if ui == "none":
        factor *= 1.3
    elif ui == "required":
        factor *= 1.0

    phys = required.physical_access
    if phys is True:
        factor *= 0.9
    elif phys is False:
        factor *= 1.1

    soph = required.sophistication
    if soph == "low":
        factor *= 1.4
    elif soph == "medium":
        factor *= 1.2
    elif soph == "high":
        factor *= 1.0

    return float(impact_points * factor)

