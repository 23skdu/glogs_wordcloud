"""Allow ``python -m glogs_wordcloud``."""

from .cli import main

if __name__ == "__main__":
    raise SystemExit(main())
