from __future__ import annotations

import json
import os
from pathlib import Path
from typing import Any

from atlas.schema import (
    Asset,
    AssetProperties,
    Edge,
    EdgeData,
    EdgeInvocation,
    EdgeSecurity,
    Node,
    NodeDataHandling,
    RequiredCapabilities,
    SystemModel,
    ThreatImpact,
    ThreatMechanism,
    ThreatTemplate,
    TrustBoundary,
)


def _read_json(path: str) -> Any:
    resolved = _resolve_input_path(path)
    with open(resolved, "r", encoding="utf-8") as file:
        return json.load(file)


def _resolve_input_path(path: str) -> str:
    p = Path(path)
    if p.exists():
        return str(p)

    # When running under Bazel, user-provided workspace-relative paths often need
    # to be resolved inside the runfiles tree.
    if not p.is_absolute():
        workspace = os.environ.get("TEST_WORKSPACE") or "_main"
        bases = [os.environ.get("RUNFILES_DIR"), os.environ.get("TEST_SRCDIR")]
        for base in [b for b in bases if b]:
            for prefix in ("", workspace, "_main"):
                candidate = Path(base) / prefix / p
                if candidate.exists():
                    return str(candidate)

        manifest = os.environ.get("RUNFILES_MANIFEST_FILE")
        if manifest:
            keys = [str(p), f"{workspace}/{p}", f"_main/{p}"]
            try:
                with open(manifest, "r", encoding="utf-8") as file:
                    for line in file:
                        line = line.rstrip("\n")
                        if not line:
                            continue
                        try:
                            k, v = line.split(" ", 1)
                        except ValueError:
                            continue
                        if k in keys and v:
                            vp = Path(v)
                            if vp.exists():
                                return str(vp)
            except OSError:
                pass

        # Last resort: resolve relative to this module's location inside runfiles.
        # e.g. <...>.runfiles/_main/<workspace relative path>
        try:
            here = Path(__file__).resolve()
            for parent in here.parents:
                if parent.name in (workspace, "_main"):
                    candidate = parent / p
                    if candidate.exists():
                        return str(candidate)
        except OSError:
            pass

    return path


def load_system_model(path: str) -> SystemModel:
    raw = _read_json(path)

    nodes = []
    for n in raw.get("nodes", []):
        nodes.append(
            Node(
                id=n["id"],
                type=n["type"],
                trust_zone=n["trust_zone"],
                exposure=n["exposure"],
                privileges=n["privileges"],
                authn=n["authn"],
                authz=n["authz"],
                data_handling=NodeDataHandling(
                    stores_sensitive=bool(n["data_handling"]["stores_sensitive"]),
                    processes_sensitive=bool(n["data_handling"]["processes_sensitive"]),
                ),
            )
        )

    edges = []
    for e in raw.get("edges", []):
        edges.append(
            Edge(
                id=e["id"],
                from_node=e["from"],
                to_node=e["to"],
                protocol=e["protocol"],
                directionality=e["directionality"],
                data=EdgeData(
                    classification=e["data"]["classification"],
                    includes_credentials=bool(e["data"]["includes_credentials"]),
                ),
                security=EdgeSecurity(
                    transport_encryption=e["security"]["transport_encryption"],
                    integrity_protection=bool(e["security"]["integrity_protection"]),
                ),
                invocation=EdgeInvocation(
                    authenticated=bool(e["invocation"]["authenticated"]),
                    user_initiated=bool(e["invocation"]["user_initiated"]),
                ),
                trust_boundary_crossed=bool(e["trust_boundary_crossed"]),
            )
        )

    trust_boundaries = []
    for b in raw.get("trust_boundaries", []):
        trust_boundaries.append(
            TrustBoundary(
                id=b["id"],
                from_zone=b["from_zone"],
                to_zone=b["to_zone"],
                type=b["type"],
            )
        )

    assets = []
    for a in raw.get("assets", []):
        assets.append(
            Asset(
                id=a["id"],
                owner=a["owner"],
                type=a["type"],
                sensitivity=a["sensitivity"],
                properties=AssetProperties(
                    confidentiality=bool(a["properties"]["confidentiality"]),
                    integrity=bool(a["properties"]["integrity"]),
                    availability=bool(a["properties"]["availability"]),
                ),
            )
        )

    return SystemModel(
        nodes=nodes,
        edges=edges,
        trust_boundaries=trust_boundaries,
        assets=assets,
    )


def load_templates(path: str) -> list[ThreatTemplate]:
    raw = _read_json(path)
    if not isinstance(raw, list):
        raise ValueError(f"templates JSON must be a list, got {type(raw).__name__}")

    templates: list[ThreatTemplate] = []
    for t in raw:
        mechanism = None
        if "mechanism" in t and t["mechanism"] is not None:
            mechanism = ThreatMechanism(
                phase=t["mechanism"]["phase"],
                actions=list(t["mechanism"].get("actions", [])),
            )

        required = None
        if "required_capabilities" in t and t["required_capabilities"] is not None:
            rc = t["required_capabilities"]
            required = RequiredCapabilities(
                network_position=rc.get("network_position"),
                privileges=rc.get("privileges"),
                user_interaction=rc.get("user_interaction"),
                physical_access=rc.get("physical_access"),
                sophistication=rc.get("sophistication"),
            )

        impact = None
        if "impact" in t and t["impact"] is not None:
            impact = ThreatImpact(
                confidentiality=bool(t["impact"].get("confidentiality", False)),
                integrity=bool(t["impact"].get("integrity", False)),
                availability=bool(t["impact"].get("availability", False)),
            )

        templates.append(
            ThreatTemplate(
                id=t["id"],
                category=t["category"],
                applies_to=t["applies_to"],
                conditions=list(t.get("conditions", [])),
                parameters=list(t.get("parameters", [])),
                mechanism=mechanism,
                required_capabilities=required,
                impact=impact,
            )
        )

    return templates


def load_statuses(path: str | None) -> dict[str, str] | None:
    if path is None:
        return None
    raw = _read_json(path)
    if not isinstance(raw, dict):
        raise ValueError("statuses JSON must be an object mapping instance_id -> status")
    statuses: dict[str, str] = {}
    for key, value in raw.items():
        if not isinstance(key, str) or not isinstance(value, str):
            raise ValueError("statuses must map strings to strings")
        statuses[key] = value
    return statuses


def ensure_parent_dir(path: str) -> None:
    Path(path).expanduser().resolve().parent.mkdir(parents=True, exist_ok=True)
