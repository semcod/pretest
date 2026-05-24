"""Generate service contract test stubs."""

from __future__ import annotations

from pretest.collect.endpoint_inventory import ServiceInfo

_CONTRACT_TEMPLATE = '''\
"""Service contract tests for {module}."""
import pytest


class Test{class_name}Contract:
    """Contract tests: verify behaviour under dependency failure."""

    def test_timeout(self, monkeypatch):
        """Service should handle upstream timeouts gracefully."""
        # TODO: monkeypatch the HTTP client to raise a TimeoutError
        pass

    def test_dependency_unavailable(self, monkeypatch):
        """Service should degrade gracefully when dependency is down."""
        # TODO: monkeypatch to simulate connection refused
        pass

    def test_unexpected_response(self, monkeypatch):
        """Service should not crash on unexpected upstream response schema."""
        pass
'''


def render_service_test(service: ServiceInfo) -> str:
    """Return a service contract test template."""
    short = service.module.split(".")[-1]
    class_name = "".join(part.capitalize() for part in short.split("_"))
    return _CONTRACT_TEMPLATE.format(module=service.module, class_name=class_name)
