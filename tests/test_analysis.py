"""Tests for text analysis helpers."""

from __future__ import annotations

from collections import Counter

from glogs_wordcloud.analysis import (
    analyze_phrase_frequency,
    analyze_word_frequency,
    clean_text,
)


def test_clean_text_removes_punctuation_and_numbers() -> None:
    assert clean_text("Hello, World! 123") == "hello world"


def test_analyze_word_frequency_counts_tokens() -> None:
    messages = ["error timeout error", "warning timeout"]
    counts = analyze_word_frequency(messages)
    assert counts == Counter({"timeout": 2, "error": 2, "warning": 1})


def test_analyze_word_frequency_respects_stopwords() -> None:
    counts = analyze_word_frequency(["the the a an"], stop_words={"the", "a", "an"})
    assert counts == Counter()


def test_analyze_phrase_frequency_bigrams() -> None:
    messages = ["connection refused error", "connection timeout error"]
    counts = analyze_phrase_frequency(messages, n=2)
    assert counts["connection refused"] == 1
    assert counts["connection timeout"] == 1


def test_analyze_phrase_frequency_invalid_n() -> None:
    import pytest

    with pytest.raises(ValueError):
        analyze_phrase_frequency(["a b c"], n=0)
