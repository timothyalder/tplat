from __future__ import annotations

from atlas.schema import LintIssue, SystemModel


def lint_model(model: SystemModel) -> list[LintIssue]:
    issues: list[LintIssue] = []

    nodes_by_id = {n.id: n for n in model.nodes}

    for node in model.nodes:
        if not node.trust_zone:
            issues.append(
                LintIssue(
                    code="NODE_TRUST_ZONE_REQUIRED",
                    message="Node trust_zone is required",
                    where=f"node:{node.id}",
                )
            )

    for edge in model.edges:
        where = f"edge:{edge.id}"

        if edge.from_node not in nodes_by_id:
            issues.append(
                LintIssue(
                    code="EDGE_FROM_UNKNOWN",
                    message=f"Edge from references unknown node id: {edge.from_node}",
                    where=where,
                )
            )
            continue

        if edge.to_node not in nodes_by_id:
            issues.append(
                LintIssue(
                    code="EDGE_TO_UNKNOWN",
                    message=f"Edge to references unknown node id: {edge.to_node}",
                    where=where,
                )
            )
            continue

        # Required fields (spec v0.1)
        if edge.security.transport_encryption is None:
            issues.append(
                LintIssue(
                    code="EDGE_TRANSPORT_ENCRYPTION_REQUIRED",
                    message="Edge.security.transport_encryption is required",
                    where=where,
                )
            )
        if edge.invocation.authenticated is None:
            issues.append(
                LintIssue(
                    code="EDGE_AUTHENTICATED_REQUIRED",
                    message="Edge.invocation.authenticated is required",
                    where=where,
                )
            )

        from_node = nodes_by_id[edge.from_node]
        to_node = nodes_by_id[edge.to_node]
        derived_crosses = from_node.trust_zone != to_node.trust_zone
        if derived_crosses and not edge.trust_boundary_crossed:
            issues.append(
                LintIssue(
                    code="EDGE_TRUST_BOUNDARY_INCONSISTENT",
                    message=(
                        "Edge crosses trust zones but trust_boundary_crossed is false; "
                        "set trust_boundary_crossed=true"
                    ),
                    where=where,
                )
            )
        if (not derived_crosses) and edge.trust_boundary_crossed:
            issues.append(
                LintIssue(
                    code="EDGE_TRUST_BOUNDARY_INCONSISTENT",
                    message=(
                        "Edge does not cross trust zones but trust_boundary_crossed is true; "
                        "set trust_boundary_crossed=false"
                    ),
                    where=where,
                )
            )

    for asset in model.assets:
        if asset.owner not in nodes_by_id:
            issues.append(
                LintIssue(
                    code="ASSET_OWNER_UNKNOWN",
                    message=f"Asset owner references unknown node id: {asset.owner}",
                    where=f"asset:{asset.id}",
                )
            )

    return issues

