from datetime import date, datetime

import pytest

from todo.main import target_date_parser

now = datetime.now()


@pytest.mark.parametrize(
    "value, expected",
    [
        ("2024-02-03", date(2024, 2, 3)),
        ("02-03", date(now.year, 2, 3)),
        ("03", date(now.year, now.month, 3)),
    ],
)
def test_target_date_parser(value, expected):
    result = target_date_parser(value)
    assert result == expected
