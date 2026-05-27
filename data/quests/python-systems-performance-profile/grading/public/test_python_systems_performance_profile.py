import pytest
from main import most_common_tokens


def test_basic_counts():
    # "ok ok ERROR error warn error" -> error=3, ok=2, warn=1
    result = most_common_tokens("ok ok ERROR error warn error", 3)
    assert result == [("error", 3), ("ok", 2), ("warn", 1)]


def test_k_limits_results():
    result = most_common_tokens("a b c d e", 2)
    assert len(result) == 2


def test_case_insensitive():
    result = most_common_tokens("Foo foo FOO", 1)
    assert result == [("foo", 3)]


def test_sort_by_count_desc_then_token_asc():
    # "apple banana apple banana cherry" -> apple=2, banana=2, cherry=1
    # tie: apple before banana (alphabetical)
    result = most_common_tokens("apple banana apple banana cherry", 2)
    assert result == [("apple", 2), ("banana", 2)]


def test_empty_string():
    assert most_common_tokens("", 5) == []


def test_non_alpha_ignored():
    # digits are excluded; only alphabetic runs are tokens
    result = most_common_tokens("hello123world", 5)
    tokens = [t for t, _ in result]
    assert "hello" in tokens
    assert "world" in tokens
    # digits should not appear as tokens
    assert all(t.isalpha() for t in tokens)
