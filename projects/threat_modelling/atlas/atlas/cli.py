from __future__ import annotations

import argparse
import json
import sys

from atlas.engine import evaluate
from atlas.lint import lint_model
from atlas.loader import load_statuses, load_system_model, load_templates
from atlas.report import load_report, write_report


def _cmd_lint(args: argparse.Namespace) -> int:
    model = load_system_model(args.model)
    issues = lint_model(model)
    if not issues:
        print("lint: ok")
        return 0
    for issue in issues:
        where = f" ({issue.where})" if issue.where else ""
        print(f"lint: {issue.code}{where}: {issue.message}", file=sys.stderr)
    return 2


def _cmd_eval(args: argparse.Namespace) -> int:
    model = load_system_model(args.model)
    templates = load_templates(args.templates)
    statuses = load_statuses(args.statuses)

    prior_ids = None
    if args.prior_report:
        prior = load_report(args.prior_report)
        prior_ids = {i.id for i in prior.instances}

    report = evaluate(model, templates, statuses=statuses, prior_instance_ids=prior_ids)
    write_report(report, path=args.out)

    print(f"instances: {len(report.instances)}")
    print(f"coverage: {report.metrics.coverage:.3f}")
    print(f"exposure: {report.metrics.exposure:.3f}")
    if report.metrics.drift is not None:
        print(f"drift: {report.metrics.drift}")
    if report.lint:
        print(f"lint_issues: {len(report.lint)}", file=sys.stderr)
        return 2
    return 0


def _cmd_metrics(args: argparse.Namespace) -> int:
    report = load_report(args.report)
    payload = {
        "total_threats": report.metrics.total_threats,
        "acknowledged_threats": report.metrics.acknowledged_threats,
        "coverage": report.metrics.coverage,
        "total_risk": report.metrics.total_risk,
        "mitigated_risk": report.metrics.mitigated_risk,
        "risk_weighted_coverage": report.metrics.risk_weighted_coverage,
        "exposure": report.metrics.exposure,
        "drift": report.metrics.drift,
    }
    print(json.dumps(payload, indent=2, sort_keys=True))
    return 0


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(prog="atlas")
    sub = parser.add_subparsers(dest="cmd", required=True)

    lint_p = sub.add_parser("lint", help="Lint a system model")
    lint_p.add_argument("--model", required=True)
    lint_p.set_defaults(func=_cmd_lint)

    eval_p = sub.add_parser("eval", help="Evaluate templates against a system model")
    eval_p.add_argument("--model", required=True)
    eval_p.add_argument("--templates", required=True)
    eval_p.add_argument("--statuses", required=False, default=None)
    eval_p.add_argument("--prior-report", required=False, default=None)
    eval_p.add_argument("--out", required=True)
    eval_p.set_defaults(func=_cmd_eval)

    metrics_p = sub.add_parser("metrics", help="Print metrics from a report")
    metrics_p.add_argument("--report", required=True)
    metrics_p.set_defaults(func=_cmd_metrics)

    args = parser.parse_args(argv)
    return int(args.func(args))


if __name__ == "__main__":
    raise SystemExit(main())

