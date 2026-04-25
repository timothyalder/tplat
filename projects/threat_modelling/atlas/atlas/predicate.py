from __future__ import annotations

import re
from dataclasses import dataclass
from typing import Any, Literal

from atlas.schema import Asset, Edge, Node, SystemModel


Op = Literal["==", "!=", "in"]


@dataclass(frozen=True)
class Predicate:
    lhs: str
    op: Op
    rhs: Any


_EXPR_RE = re.compile(r"^\s*(?P<lhs>[^!=\s]+(?:\s*\[[^\]]+\])?(?:\.[^!=\s]+)*)\s*(?P<op>==|!=|in)\s*(?P<rhs>.+?)\s*$")
_LHS_CLEAN = re.compile(r"\s+")


class PredicateError(ValueError):
    pass


def parse_predicate(expr: str) -> Predicate:
    match = _EXPR_RE.match(expr)
    if not match:
        raise PredicateError(f"unsupported predicate expression: {expr!r}")

    lhs = _LHS_CLEAN.sub("", match.group("lhs"))
    op: Op = match.group("op")  # type: ignore[assignment]
    rhs_text = match.group("rhs").strip()
    rhs = _parse_rhs(rhs_text)
    return Predicate(lhs=lhs, op=op, rhs=rhs)


def _parse_rhs(text: str) -> Any:
    if text in ("true", "false"):
        return text == "true"

    # Numeric (risk thresholds etc.)
    if re.fullmatch(r"-?\d+", text):
        return int(text)
    if re.fullmatch(r"-?\d+\.\d+", text):
        return float(text)

    # List: [a, b]
    if text.startswith("[") and text.endswith("]"):
        inner = text[1:-1].strip()
        if not inner:
            return []
        return [_parse_rhs(part.strip()) for part in inner.split(",")]

    # Set-ish: {a, b}
    if text.startswith("{") and text.endswith("}"):
        inner = text[1:-1].strip()
        if not inner:
            return set()
        return set(_parse_rhs(part.strip()) for part in inner.split(","))

    # String identifiers: treat as raw token without quotes.
    # (We intentionally do not support quoted strings in v0.1.)
    return text


def evaluate_predicate(
    predicate: Predicate,
    *,
    model: SystemModel,
    element_type: Literal["node", "edge", "asset"],
    element: Node | Edge | Asset,
) -> bool:
    lhs_value = resolve_lhs(
        predicate.lhs,
        model=model,
        element_type=element_type,
        element=element,
    )
    rhs_value = predicate.rhs

    if predicate.op == "==":
        return lhs_value == rhs_value
    if predicate.op == "!=":
        return lhs_value != rhs_value
    if predicate.op == "in":
        if isinstance(rhs_value, set):
            return lhs_value in rhs_value
        if isinstance(rhs_value, list):
            return lhs_value in rhs_value
        raise PredicateError(f"rhs for 'in' must be a list or set, got {type(rhs_value).__name__}")

    raise PredicateError(f"unsupported operator: {predicate.op}")


def resolve_lhs(
    lhs: str,
    *,
    model: SystemModel,
    element_type: Literal["node", "edge", "asset"],
    element: Node | Edge | Asset,
) -> Any:
    nodes_by_id = {n.id: n for n in model.nodes}

    if lhs.startswith("edge.") or lhs.startswith("node.") or lhs.startswith("asset."):
        root, path = lhs.split(".", 1)
    elif lhs.startswith("node["):
        root = "node"
        path = lhs[len("node") :]
    else:
        root = element_type
        path = lhs

    if root == "edge":
        if not isinstance(element, Edge):
            raise PredicateError(f"lhs {lhs!r} requires edge context")
        return _resolve_edge_path(path, model=model, edge=element, nodes_by_id=nodes_by_id)

    if root == "node":
        if isinstance(element, Edge):
            # Support node[from] and node[to] when evaluating edges.
            return _resolve_node_from_edge(path, edge=element, nodes_by_id=nodes_by_id)
        if not isinstance(element, Node):
            raise PredicateError(f"lhs {lhs!r} requires node context")
        return _resolve_obj_path(element, path)

    if root == "asset":
        if not isinstance(element, Asset):
            raise PredicateError(f"lhs {lhs!r} requires asset context")
        return _resolve_obj_path(element, path)

    raise PredicateError(f"unknown root in lhs: {lhs!r}")


def _resolve_edge_path(path: str, *, model: SystemModel, edge: Edge, nodes_by_id: dict[str, Node]) -> Any:
    # Derived properties (spec v0.1)
    if path == "crosses_trust_boundary":
        from_node = nodes_by_id[edge.from_node]
        to_node = nodes_by_id[edge.to_node]
        return from_node.trust_zone != to_node.trust_zone
    if path == "exposes_sensitive_data":
        return edge.data.classification in ("confidential", "secret")

    # Normalized field aliases matching spec names.
    if path.startswith("from"):
        if path == "from":
            return edge.from_node
        # e.g. edge.from.trust_zone isn't supported; use node[from].trust_zone
    if path.startswith("to"):
        if path == "to":
            return edge.to_node

    # Schema uses from_node/to_node; spec uses from/to.
    if path.startswith("from_node"):
        path = path.replace("from_node", "from", 1)
    if path.startswith("to_node"):
        path = path.replace("to_node", "to", 1)

    # Map edge.<spec field> to dataclass fields.
    if path == "id":
        return edge.id
    if path == "from":
        return edge.from_node
    if path == "to":
        return edge.to_node

    # Nested fields.
    if path.startswith("data."):
        return _resolve_obj_path(edge.data, path[len("data.") :])
    if path.startswith("security."):
        return _resolve_obj_path(edge.security, path[len("security.") :])
    if path.startswith("invocation."):
        return _resolve_obj_path(edge.invocation, path[len("invocation.") :])

    if path in ("protocol", "directionality", "trust_boundary_crossed"):
        return _resolve_obj_path(edge, path)

    raise PredicateError(f"unknown edge path: edge.{path}")


def _resolve_node_from_edge(path: str, *, edge: Edge, nodes_by_id: dict[str, Node]) -> Any:
    # Syntax: node[to].privileges, node[from].trust_zone
    bracket_start = path.find("[")
    bracket_end = path.find("]")
    if bracket_start == -1 or bracket_end == -1 or bracket_end < bracket_start:
        raise PredicateError(
            f"node[...] reference required in edge context, got node.{path!r}. Use node[to] or node[from]."
        )
    selector = path[bracket_start + 1 : bracket_end].strip()
    remainder = path[bracket_end + 1 :]
    if remainder.startswith("."):
        remainder = remainder[1:]

    if selector == "to":
        node_id = edge.to_node
    elif selector == "from":
        node_id = edge.from_node
    else:
        raise PredicateError(f"unsupported node[...] selector: {selector!r}")

    if node_id not in nodes_by_id:
        raise PredicateError(f"edge references unknown node id: {node_id}")
    return _resolve_obj_path(nodes_by_id[node_id], remainder)


def _resolve_obj_path(obj: Any, path: str) -> Any:
    current = obj
    if not path:
        return current
    for part in path.split("."):
        if not hasattr(current, part):
            raise PredicateError(f"unknown attribute {part!r} on {type(current).__name__}")
        current = getattr(current, part)
    return current
