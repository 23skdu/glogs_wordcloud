"""Tests for configuration validation."""

from __future__ import annotations

import pytest

from glogs_wordcloud.config import (
    ConfigurationError,
    escape_filter_value,
    validate_entries,
    validate_project_id,
)


def test_validate_project_id_ok() -> None:
    assert validate_project_id("my-project-123") == "my-project-123"


def test_validate_project_id_bad() -> None:
    with pytest.raises(ConfigurationError):
        validate_project_id("UPPER")


def test_validate_entries_bounds() -> None:
    assert validate_entries(5) == 5
    with pytest.raises(ConfigurationError):
        validate_entries(0)
    with pytest.raises(ConfigurationError):
        validate_entries(True)


def test_escape_filter_value() -> None:
    assert escape_filter_value('a"b\\c') == 'a\\"b\\\\c'
