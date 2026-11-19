"""Text cleaning and frequency analysis for log messages."""

from __future__ import annotations

import re
from collections import Counter
from collections.abc import Iterable

from wordcloud import STOPWORDS

__all__ = ["analyze_phrase_frequency", "analyze_word_frequency", "clean_text"]

# Pre-compiled patterns for performance and clarity.
_PUNCTUATION_RE = re.compile(r"[^\w\s]", re.UNICODE)
_DIGITS_RE = re.compile(r"\d+", re.UNICODE)
_WHITESPACE_RE = re.compile(r"\s+")


def clean_text(text: str) -> str:
    """Lower-case text, strip punctuation and digits, and normalise whitespace."""
    if not isinstance(text, str):
        text = str(text)
    text = _PUNCTUATION_RE.sub(" ", text)
    text = _DIGITS_RE.sub(" ", text)
    text = text.lower()
    text = _WHITESPACE_RE.sub(" ", text).strip()
    return text


def _tokenize(message: str, stop_words: set[str]) -> list[str]:
    cleaned = clean_text(message)
    return [w for w in cleaned.split() if w not in stop_words and len(w) > 2]


def analyze_word_frequency(
    log_messages: Iterable[str], stop_words: set[str] | None = None
) -> Counter[str]:
    """Return a frequency counter of words across the provided log messages."""
    if stop_words is None:
        stop_words = set(STOPWORDS)
    word_counts: Counter[str] = Counter()
    for message in log_messages:
        word_counts.update(_tokenize(str(message), stop_words))
    return word_counts


def analyze_phrase_frequency(
    log_messages: Iterable[str], n: int = 2, stop_words: set[str] | None = None
) -> Counter[str]:
    """Return a frequency counter of n-gram phrases across the provided log messages."""
    if n < 1:
        raise ValueError("n must be a positive integer.")
    if stop_words is None:
        stop_words = set(STOPWORDS)
    phrase_counts: Counter[str] = Counter()
    for message in log_messages:
        words = _tokenize(str(message), stop_words)
        if len(words) < n:
            continue
        phrases = (" ".join(words[i : i + n]) for i in range(len(words) - n + 1))
        phrase_counts.update(phrases)
    return phrase_counts
