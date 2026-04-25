from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any, Literal


NodeType = Literal[
    "service",
    "client",
    "datastore",
    "queue",
    "identity",
    "external",
    "human",
]
Exposure = Literal["public", "internal", "restricted"]
Privileges = Literal["none", "user", "admin", "system"]
Authn = Literal["none", "password", "token", "mfa", "mutual_tls"]
Authz = Literal["none", "role_based", "attribute_based"]

Protocol = Literal["http", "https", "grpc", "tcp", "udp", "file", "internal_api", "unknown"]
Directionality = Literal["request", "response", "bidirectional"]
Classification = Literal["public", "internal", "confidential", "secret"]
TransportEncryption = Literal["none", "tls", "mutual_tls"]

TrustBoundaryType = Literal["network", "privilege", "process", "physical"]
AssetType = Literal["data", "credential", "key", "service_availability", "infrastructure"]
Sensitivity = Literal["low", "medium", "high", "critical"]

ThreatCategory = Literal["spoofing", "tampering", "repudiation", "disclosure", "dos", "elevation"]
AppliesTo = Literal["node", "edge", "asset"]
Phase = Literal["recon", "exploit", "persist", "exfiltrate"]
Action = Literal["intercept", "modify", "inject", "replay", "exhaust", "escalate"]

NetworkPosition = Literal["none", "adjacent", "on_path"]
UserInteraction = Literal["none", "required"]
Sophistication = Literal["low", "medium", "high"]

ThreatStatus = Literal["unmitigated", "mitigated", "accepted", "not_applicable"]


@dataclass(frozen=True)
class NodeDataHandling:
    stores_sensitive: bool
    processes_sensitive: bool


@dataclass(frozen=True)
class Node:
    id: str
    type: NodeType
    trust_zone: str
    exposure: Exposure
    privileges: Privileges
    authn: Authn
    authz: Authz
    data_handling: NodeDataHandling


@dataclass(frozen=True)
class EdgeData:
    classification: Classification
    includes_credentials: bool


@dataclass(frozen=True)
class EdgeSecurity:
    transport_encryption: TransportEncryption
    integrity_protection: bool


@dataclass(frozen=True)
class EdgeInvocation:
    authenticated: bool
    user_initiated: bool


@dataclass(frozen=True)
class Edge:
    id: str
    from_node: str
    to_node: str
    protocol: Protocol
    directionality: Directionality
    data: EdgeData
    security: EdgeSecurity
    invocation: EdgeInvocation
    trust_boundary_crossed: bool


@dataclass(frozen=True)
class TrustBoundary:
    id: str
    from_zone: str
    to_zone: str
    type: TrustBoundaryType


@dataclass(frozen=True)
class AssetProperties:
    confidentiality: bool
    integrity: bool
    availability: bool


@dataclass(frozen=True)
class Asset:
    id: str
    owner: str
    type: AssetType
    sensitivity: Sensitivity
    properties: AssetProperties


@dataclass(frozen=True)
class SystemModel:
    nodes: list[Node]
    edges: list[Edge]
    trust_boundaries: list[TrustBoundary]
    assets: list[Asset]


@dataclass(frozen=True)
class ThreatMechanism:
    phase: Phase
    actions: list[Action] = field(default_factory=list)


@dataclass(frozen=True)
class RequiredCapabilities:
    network_position: NetworkPosition | None = None
    privileges: Privileges | None = None
    user_interaction: UserInteraction | None = None
    physical_access: bool | None = None
    sophistication: Sophistication | None = None


@dataclass(frozen=True)
class ThreatImpact:
    confidentiality: bool = False
    integrity: bool = False
    availability: bool = False


@dataclass(frozen=True)
class ThreatTemplate:
    id: str
    category: ThreatCategory
    applies_to: AppliesTo
    conditions: list[str]
    parameters: list[str] = field(default_factory=list)
    mechanism: ThreatMechanism | None = None
    required_capabilities: RequiredCapabilities | None = None
    impact: ThreatImpact | None = None


@dataclass(frozen=True)
class ThreatInstance:
    id: str
    template_id: str
    bound_element: str
    parameter_values: dict[str, Any]
    risk_score: float
    status: ThreatStatus = "unmitigated"


@dataclass(frozen=True)
class Metrics:
    total_threats: int
    acknowledged_threats: int
    coverage: float
    total_risk: float
    mitigated_risk: float
    risk_weighted_coverage: float
    exposure: float
    drift: int | None = None


@dataclass(frozen=True)
class LintIssue:
    code: str
    message: str
    where: str | None = None


@dataclass(frozen=True)
class ThreatReport:
    instances: list[ThreatInstance]
    metrics: Metrics
    lint: list[LintIssue]
    template_ids: list[str]

