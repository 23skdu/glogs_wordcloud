# Usage

## Install

```bash
make setup
# or
uv sync --extra dev
```

## Run

```bash
uv run glogs-wordcloud PROJECT_ID LOG_NAME --num-entries 500 --output-file out.png
```

### Examples

Analyze all logs:

```bash
uv run glogs-wordcloud my-project global --num-entries 1000
```

Filter errors only:

```bash
uv run glogs-wordcloud my-project "projects/my-project/logs/app" \
  --filter 'severity>=ERROR' --output-file errors.png
```

Phrase (n-gram) analysis:

```bash
uv run glogs-wordcloud my-project global --analyze-phrases --ngram-size 3
```

## Docker

```bash
make docker-build
docker run --rm -v "$PWD:/data" -e GOOGLE_APPLICATION_CREDENTIALS=/data/sa.json \
  glogs-wordcloud:local my-project global --output-file /data/out.png
```