"""Word cloud rendering helpers."""

from __future__ import annotations

from collections import Counter
from pathlib import Path

# Use a non-interactive backend so rendering works in containers/CI.
import matplotlib

matplotlib.use("Agg")

import matplotlib.pyplot as plt
from wordcloud import STOPWORDS, WordCloud

__all__ = ["generate_wordcloud"]


def generate_wordcloud(
    word_counts: Counter[str],
    output_file: str | Path = "wordcloud.png",
    *,
    width: int = 800,
    height: int = 400,
    max_words: int = 200,
) -> Path:
    """Render ``word_counts`` to an image file and return the resolved path."""
    if not word_counts:
        raise ValueError("word_counts must not be empty.")

    output_path = Path(output_file).expanduser().resolve()
    output_path.parent.mkdir(parents=True, exist_ok=True)

    wordcloud = WordCloud(
        width=width,
        height=height,
        background_color="white",
        stopwords=STOPWORDS,
        max_words=max_words,
        contour_width=3,
        contour_color="steelblue",
    ).generate_from_frequencies(dict(word_counts))

    fig, ax = plt.subplots(figsize=(10, 5))
    ax.imshow(wordcloud, interpolation="bilinear")
    ax.axis("off")
    fig.tight_layout(pad=0)
    fig.savefig(output_path, dpi=150, bbox_inches="tight")
    plt.close(fig)

    return output_path
