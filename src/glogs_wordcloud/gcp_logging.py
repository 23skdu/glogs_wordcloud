"""Google Cloud Logging access helpers."""

from __future__ import annotations

import logging
from pathlib import Path

from google.cloud import logging as gcp_logging
from google.oauth2 import service_account

from .config import escape_filter_value, validate_log_name

logger = logging.getLogger(__name__)


def _build_credentials(credentials_path: str | None) -> service_account.Credentials | None:
    if credentials_path is None:
        return None
    path = Path(credentials_path).expanduser()
    if not path.is_file():
        raise FileNotFoundError(f"Credentials file not found: {path}")
    # Restrict to a regular file; reject symlinks that escape? Keep simple but safe.
    creds = service_account.Credentials.from_service_account_file(str(path))
    return creds


def fetch_log_messages(
    project_id: str,
    log_name: str,
    num_entries: int,
    *,
    filter_string: str | None = None,
    credentials_path: str | None = None,
    order: str = "timestamp desc",
) -> list[str]:
    """Fetch up to ``num_entries`` log messages from Google Cloud Logging."""
    log_name = validate_log_name(log_name)
    credentials = _build_credentials(credentials_path)
    client = gcp_logging.Client(project=project_id, credentials=credentials)

    # Lightweight connectivity check.
    try:
        next(client.list_entries(page_size=1), None)
    except Exception as exc:  # pragma: no cover - network dependent
        logger.error("Failed to connect to Google Cloud Logging: %s", exc)
        raise

    filters: list[str] = []
    if log_name.lower() != "global":
        filters.append(f'logName="{escape_filter_value(log_name)}"')
    if filter_string:
        filters.append(f"({filter_string})")
    log_filter = " AND ".join(filters) if filters else None

    logger.info("Fetching up to %d log entries (filter=%s)", num_entries, log_filter)
    entries = client.list_entries(
        page_size=num_entries,
        filter_=log_filter,
        order_by=order,
    )

    messages: list[str] = []
    for entry in entries:
        if len(messages) >= num_entries:
            break
        payload = entry.payload
        try:
            if isinstance(payload, str):
                messages.append(payload)
            elif isinstance(payload, dict):
                message = payload.get("message")
                messages.append(message if isinstance(message, str) else str(payload))
            else:
                messages.append(str(payload))
        except Exception as exc:  # defensive
            logger.warning("Skipping unprocessable log entry: %s", exc)
    return messages


def validate_connection(project_id: str, credentials_path: str | None = None) -> None:
    credentials = _build_credentials(credentials_path)
    client = gcp_logging.Client(project=project_id, credentials=credentials)
    next(client.list_entries(page_size=1), None)
