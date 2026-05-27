import pytest
from main import slugify, unique_sorted, run_tool_request


class TestSlugify:
    def test_basic_lowercase(self):
        assert slugify("Hello World") == "hello-world"

    def test_strips_whitespace(self):
        assert slugify("  hello  ") == "hello"

    def test_special_chars_removed(self):
        assert slugify("Hello, World!") == "hello-world"

    def test_consecutive_dashes_collapsed(self):
        assert slugify("hello---world") == "hello-world"

    def test_leading_trailing_dashes_stripped(self):
        assert slugify("--hello--") == "hello"

    def test_alphanumeric_preserved(self):
        assert slugify("abc123") == "abc123"

    def test_mixed_punctuation(self):
        result = slugify("  My Great Idea!  ")
        assert result == "my-great-idea"


class TestUniqueSorted:
    def test_deduplicates(self):
        assert unique_sorted(["b", "a", "a"]) == ["a", "b"]

    def test_sorted_alphabetically(self):
        assert unique_sorted(["c", "a", "b"]) == ["a", "b", "c"]

    def test_lowercases_items(self):
        assert unique_sorted(["B", "A"]) == ["a", "b"]

    def test_strips_whitespace(self):
        assert unique_sorted(["  hello  ", "hello"]) == ["hello"]

    def test_removes_empty_strings(self):
        assert unique_sorted(["", "a", "  "]) == ["a"]

    def test_empty_input(self):
        assert unique_sorted([]) == []


class TestRunToolRequest:
    def test_slugify_tool(self):
        result = run_tool_request({"tool": "slugify", "payload": {"text": "Hello World"}})
        assert result["ok"] is True
        assert result["result"] == "hello-world"
        assert result["error"] is None

    def test_unique_sorted_tool(self):
        result = run_tool_request({"tool": "unique_sorted", "payload": {"items": ["b", "a", "a"]}})
        assert result["ok"] is True
        assert result["result"] == ["a", "b"]

    def test_sum_tool(self):
        result = run_tool_request({"tool": "sum", "payload": {"numbers": [1, 2, 3]}})
        assert result["ok"] is True
        assert result["result"] == 6

    def test_unknown_tool_returns_error(self):
        result = run_tool_request({"tool": "nonexistent", "payload": {}})
        assert result["ok"] is False
        assert result["error"] == "EF_TOOL_UNKNOWN"

    def test_bad_input_missing_text(self):
        result = run_tool_request({"tool": "slugify", "payload": {}})
        assert result["ok"] is False
        assert result["error"] == "EF_TOOL_BAD_INPUT"

    def test_empty_tool_name(self):
        result = run_tool_request({"tool": "", "payload": {}})
        assert result["ok"] is False
        assert result["error"] == "EF_TOOL_BAD_INPUT"
