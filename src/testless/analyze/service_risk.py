"""Assess service risk based on missing tests and critical characteristics."""

from __future__ import annotations

from testless.collect.endpoint_inventory import ServiceInfo
from testless.models.findings import MissingTestFinding


def score_service_risk(
    service: ServiceInfo,
    missing: list[MissingTestFinding],
) -> dict[str, object]:
    """
    Return a risk assessment dict for a service.

    Higher score = higher risk of undetected failures.
    """
    risk_score = 0.0
    reasons: list[str] = []

    # Missing tests for this service
    service_missing = [m for m in missing if m.target == service.module]
    if service_missing:
        risk_score += 0.4 * len(service_missing)
        reasons.append(f"{len(service_missing)} missing test type(s)")

    if service.has_sql:
        risk_score += 0.3
        reasons.append("uses SQL without verified query tests")
    if service.has_http_client:
        risk_score += 0.2
        reasons.append("makes external HTTP calls")
    if service.has_retry:
        risk_score += 0.1
        reasons.append("uses retry/backoff logic")

    return {
        "module": service.module,
        "risk_score": round(min(risk_score, 1.0), 2),
        "reasons": reasons,
    }
