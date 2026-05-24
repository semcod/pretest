"""Generate TestQL integration suggestions for SQL-heavy services."""

from __future__ import annotations

from testless.collect.endpoint_inventory import ServiceInfo

_TESTQL_TEMPLATE = '''\
"""TestQL-style source-level tests for {module}.

These tests validate SQL queries and edge-cases without full provisioning.
See: https://github.com/ThugPigeon653/testQL-source
"""
import pytest


class Test{class_name}SQL:
    """Source-level SQL contract tests."""

    def test_query_returns_expected_columns(self, db_session):
        """Verify that the primary query returns expected columns."""
        # TODO: call the function under test and assert on result keys
        pass

    def test_empty_result_handled(self, db_session):
        """Service handles empty result set without raising."""
        pass

    def test_sql_injection_rejected(self, db_session):
        """Parameterised queries must not be vulnerable to injection."""
        # TODO: pass a payload like "'; DROP TABLE users; --" as input
        pass

    def test_large_result_set_pagination(self, db_session):
        """Service must paginate large result sets correctly."""
        pass
'''


def render_testql_stub(service: ServiceInfo) -> str:
    """Return a TestQL test stub for a SQL-heavy service."""
    short = service.module.split(".")[-1]
    class_name = "".join(part.capitalize() for part in short.split("_"))
    return _TESTQL_TEMPLATE.format(module=service.module, class_name=class_name)
