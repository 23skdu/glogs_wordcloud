"""Configuration helpers and validation for glogs-wordcloud."""

from __future__ import annotations

import re
from pathlib import Path

# Google Cloud project IDs: 6-30 chars, lowercase letters, digits, hyphens.
_PROJECT_ID_RE = re.compile(r"^[a-z][a-z0-9-]{4,28}[a-z0-9]$")

# Sensible upper bound to avoid unbounded memory consumption.
MAX_ENTRIES = 50_000
MIN_ENTRIES = 1


class ConfigurationError(ValueError):
    """Raised when user supplied configuration is invalid."""


def validate_project_id(project_id: str) -> str:
    if not isinstance(project_id, str) or not _PROJECT_ID_RE.fullmatch(project_id):
        raise ConfigurationError(
            "project_id must be a valid Google Cloud project ID "
            "(6-30 chars, lowercase letters, digits, hyphens)."
        )
    return project_id


def validate_log_name(log_name: str) -> str:
    if not isinstance(log_name, str) or not log_name.strip():
        raise ConfigurationError("log_name must be a non-empty string.")
    # Reject control characters that could corrupt the filter expression.
    if any(ch in log_name for ch in ("\n", "\r", "\x00")):
        raise ConfigurationError("log_name contains invalid control characters.")
    return log_name.strip()


def validate_entries(num_entries: int) -> int:
    if not isinstance(num_entries, int) or isinstance(num_entries, bool):
        raise ConfigurationError("num_entries must be an integer.")
    if num_entries < MIN_ENTRIES or num_entries > MAX_ENTRIES:
        raise ConfigurationError(f"num_entries must be between {MIN_ENTRIES} and {MAX_ENTRIES}.")
    return num_entries


def validate_ngram_size(n: int) -> int:
    if not isinstance(n, int) or isinstance(n, bool) or n < 1 or n > 5:
        raise ConfigurationError("ngram_size must be an integer between 1 and 5.")
    return n


def escape_filter_value(value: str) -> str:
    """Escape a value for use inside a double-quoted Cloud Logging filter string."""
    return value.replace("\\", "\\\\").replace('"', '\\"')


def safe_output_path(output_file: str) -> Path:
    if not isinstance(output_file, str) or not output_file.strip():
        raise ConfigurationError("output_file must be a non-empty path.")
    path = Path(output_file).expanduser()
    if path.is_absolute() is False:
        path = Path.cwd() / path
    # Prevent writing into obviously dangerous locations is left to the OS/permissions.
    return path.resolve(strict=False)
