import pytest
from main import calculate_availability


def test_all_success():
    events = [{"status_code": 200}, {"status_code": 201}, {"status_code": 204}]
    assert calculate_availability(events) == 1.0


def test_all_failure():
    events = [{"status_code": 500}, {"status_code": 503}]
    assert calculate_availability(events) == 0.0


def test_mixed():
    events = [{"status_code": 200}, {"status_code": 500}]
    assert calculate_availability(events) == 0.5


def test_fixture_sample():
    # 200, 204, 500, 302, 503, 200, 200, 404, 200, 201 -> 7 successes / 10 total
    events = [
        {"status_code": 200}, {"status_code": 204}, {"status_code": 500},
        {"status_code": 302}, {"status_code": 503}, {"status_code": 200},
        {"status_code": 200}, {"status_code": 404}, {"status_code": 200},
        {"status_code": 201},
    ]
    assert calculate_availability(events) == 0.7


def test_boundary_399():
    events = [{"status_code": 399}, {"status_code": 400}]
    assert calculate_availability(events) == 0.5


def test_result_is_rounded_to_4_decimals():
    events = [{"status_code": 200}] * 3 + [{"status_code": 500}] * 10
    result = calculate_availability(events)
    assert result == round(3 / 13, 4)
