# Configuration

## Authentication

glogs-wordcloud uses Google Application Default Credentials (ADC) by default.
Set one of:

- `GOOGLE_APPLICATION_CREDENTIALS` pointing to a service account JSON key.
- Run on GCP with an attached service account (recommended).
- Pass `--credentials-path /path/to/key.json`.

Prefer Workload Identity over long-lived keys.

## Environment variables

- `GOOGLE_CLOUD_PROJECT` (optional; project is also a CLI argument)
- `GOOGLE_APPLICATION_CREDENTIALS` (optional)

## Validation

CLI inputs are validated:

- Project ID format.
- Log name non-empty, no control characters.
- Entry count between 1 and 50,000.
- N-gram size between 1 and 5.