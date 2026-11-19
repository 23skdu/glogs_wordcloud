# Architecture

- `src/glogs_wordcloud/cli.py`: argument parsing and orchestration.
- `src/glogs_wordcloud/config.py`: validation and escaping.
- `src/glogs_wordcloud/gcp_logging.py`: Google Cloud Logging client.
- `src/glogs_wordcloud/analysis.py`: text cleaning and frequency counters.
- `src/glogs_wordcloud/visualization.py`: word cloud rendering.

Infrastructure under `infra/terraform` provisions a read-only service account.