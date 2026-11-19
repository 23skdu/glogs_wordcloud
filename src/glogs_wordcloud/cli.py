"""Command line interface for glogs-wordcloud."""

from __future__ import annotations

import argparse
import logging
from collections.abc import Sequence

from .analysis import analyze_phrase_frequency, analyze_word_frequency
from .config import (
    ConfigurationError,
    safe_output_path,
    validate_entries,
    validate_log_name,
    validate_ngram_size,
    validate_project_id,
)
from .gcp_logging import fetch_log_messages, validate_connection
from .visualization import generate_wordcloud

logger = logging.getLogger("glogs_wordcloud")


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        prog="glogs-wordcloud",
        description="Analyze Google Cloud Logging data and generate a word cloud.",
    )
    parser.add_argument("project_id", help="Google Cloud project ID.")
    parser.add_argument(
        "log_name",
        help="Log name to analyze (e.g. 'projects/PROJECT/logs/LOG'). Use 'global' for all logs.",
    )
    parser.add_argument(
        "--num-entries", type=int, default=1000, help="Number of log entries to fetch."
    )
    parser.add_argument("--output-file", default="wordcloud.png", help="Output image path.")
    parser.add_argument(
        "--credentials-path",
        default=None,
        help="Path to a service account JSON key (optional; ADC used otherwise).",
    )
    parser.add_argument(
        "--filter",
        dest="filter_string",
        default=None,
        help="Optional Cloud Logging filter.",
    )
    parser.add_argument(
        "--analyze-phrases",
        action="store_true",
        help="Analyze phrases (n-grams) instead of words.",
    )
    parser.add_argument(
        "--ngram-size", type=int, default=2, help="N-gram size for phrase analysis."
    )
    parser.add_argument("--verbose", action="store_true", help="Enable verbose logging.")
    return parser


def main(argv: Sequence[str] | None = None) -> int:
    parser = build_parser()
    args = parser.parse_args(argv)

    logging.basicConfig(
        level=logging.DEBUG if args.verbose else logging.INFO,
        format="%(asctime)s %(levelname)s %(name)s: %(message)s",
    )

    try:
        project_id = validate_project_id(args.project_id)
        log_name = validate_log_name(args.log_name)
        num_entries = validate_entries(args.num_entries)
        ngram_size = validate_ngram_size(args.ngram_size)
        output_path = safe_output_path(args.output_file)
    except ConfigurationError as exc:
        logger.error("Invalid configuration: %s", exc)
        return 2

    try:
        validate_connection(project_id, args.credentials_path)
        logger.info("Successfully connected to Google Cloud Logging.")
    except Exception as exc:
        logger.error("Failed to connect to Google Cloud Logging: %s", exc)
        logger.error("Check your project ID and credentials.")
        return 1

    try:
        messages = fetch_log_messages(
            project_id=project_id,
            log_name=log_name,
            num_entries=num_entries,
            filter_string=args.filter_string,
            credentials_path=args.credentials_path,
        )
    except Exception as exc:
        logger.error("Failed to fetch logs: %s", exc)
        return 1

    if not messages:
        logger.warning("No log entries found.")
        return 0

    try:
        if args.analyze_phrases:
            counts = analyze_phrase_frequency(messages, n=ngram_size)
        else:
            counts = analyze_word_frequency(messages)
    except ValueError as exc:
        logger.error("Analysis failed: %s", exc)
        return 2

    if not counts:
        logger.warning("No tokens found after filtering; nothing to render.")
        return 0

    try:
        result = generate_wordcloud(counts, output_path)
        logger.info("Word cloud saved to %s", result)
    except Exception as exc:
        logger.error("Failed to generate word cloud: %s", exc)
        return 1

    return 0


if __name__ == "__main__":  # pragma: no cover
    raise SystemExit(main())
