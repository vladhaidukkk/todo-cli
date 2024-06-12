from datetime import date, datetime

import pytest

from todo.main import parse_str_to_date

now = datetime.now()


@pytest.mark.parametrize(
    "value, expected",
    [
        ("2024-02-03", date(2024, 2, 3)),
        ("02-03", date(now.year, 2, 3)),
        ("03", date(now.year, now.month, 3)),
    ],
)
def test_valid_input_with_default_formats_returns_date(
    value: str, expected: date
) -> None:
    result = parse_str_to_date(value)
    assert result == expected


def test_valid_input_with_custom_format_returns_date() -> None:
    result = parse_str_to_date("2024-02-03", formats=["%Y-%m-%d"])
    assert result == date(2024, 2, 3)


@pytest.mark.parametrize(
    "value, expected",
    [
        ("02/03/2024", date(2024, 2, 3)),
        ("02/03", date(now.year, 2, 3)),
        ("03", date(now.year, now.month, 3)),
    ],
)
def test_valid_input_with_custom_formats_returns_date(
    value: str, expected: date
) -> None:
    result = parse_str_to_date(value, formats=["%m/%d/%Y", "%m/%d", "%d"])
    assert result == expected


@pytest.mark.parametrize(
    "value, expected",
    [
        ("2024-02-03", date(2024, 2, 3)),
        ("02-03", date(now.year, 2, 3)),
        ("03", date(now.year, now.month, 3)),
    ],
)
def test_valid_input_with_empty_formats_uses_default_formats(
    value: str, expected: date
) -> None:
    result = parse_str_to_date(value, formats=[])
    assert result == expected


def test_invalid_input_raises_invalid_format_exception() -> None:
    with pytest.raises(ValueError) as exc_info:
        parse_str_to_date("02/03/2024")

    assert "02/03/2024" in str(exc_info.value)
    for fmt in ["%Y-%m-%d", "%m-%d", "%d"]:
        assert fmt in str(exc_info.value)


@pytest.mark.parametrize(
    "value",
    [
        # invalid format
        "02/03/2024",
        "02/03",
        # invalid date
        "2024-00-03",
        "2024-13-03",
        "2024-02-00",
        "2024-02-32",
    ],
)
def test_invalid_input_raises_exception(value: str) -> None:
    with pytest.raises(ValueError) as exc_info:
        parse_str_to_date(value)

    assert value in str(exc_info.value)
    for fmt in ["%Y-%m-%d", "%m-%d", "%d"]:
        assert fmt in str(exc_info.value)
