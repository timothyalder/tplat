from pathlib import Path

from atlas import evaluate, lint_model, load_system_model, load_templates
from atlas.invariants import assert_all_boundary_crossing_edges_have_threats


def test_end_to_end_eval_is_deterministic():
    root = Path(__file__).parent.parent
    model = load_system_model(str(root / "data/system_model_example.json"))
    templates = load_templates(str(root / "data/templates_v0_1.json"))

    lint = lint_model(model)
    assert lint == []

    report1 = evaluate(model, templates)
    report2 = evaluate(model, templates)

    assert [i.id for i in report1.instances] == [i.id for i in report2.instances]
    assert report1.metrics == report2.metrics

    assert len(report1.instances) > 0
    assert_all_boundary_crossing_edges_have_threats(model, report1)

    # Spot-check that key v0.1 templates match expected elements.
    by_template_edge = {(i.template_id, i.bound_element) for i in report1.instances}
    assert ("DISCLOSURE_MITM_READ", "e_client_web") in by_template_edge
    assert ("EOP_UNAUTHENTICATED_ACCESS", "e_client_web") in by_template_edge
    assert ("EOP_MISSING_AUTHZ", "db") in {(i.template_id, i.bound_element) for i in report1.instances}

