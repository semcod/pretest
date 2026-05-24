"""Generate e2e test stubs for critical user journeys."""

from __future__ import annotations

from testless.collect.endpoint_inventory import EndpointInfo

_JOURNEY_PATHS = {"/login", "/logout", "/search", "/checkout", "/register"}

_E2E_TEMPLATE = '''\
"""End-to-end test for the {journey} user journey."""
import pytest


@pytest.mark.e2e
def test_{journey}_journey(client):
    """
    Verify the complete {journey} user journey.

    Steps:
      1. TODO: Set up required preconditions
      2. Perform the {journey} action via {method} {path}
      3. Verify the expected outcome
    """
    # Step 1 – preconditions
    # Step 2 – action
    response = client.{method_lower}("{path}")
    # Step 3 – assertions
    assert response.status_code == 200  # adjust as needed
'''


def render_e2e_test(endpoint: EndpointInfo) -> str | None:
    """Return an e2e test template for journey-critical endpoints, or None."""
    if endpoint.path not in _JOURNEY_PATHS:
        return None
    journey = endpoint.path.strip("/").replace("/", "_").replace("-", "_")
    return _E2E_TEMPLATE.format(
        journey=journey,
        method=endpoint.method,
        method_lower=endpoint.method.lower(),
        path=endpoint.path,
    )
