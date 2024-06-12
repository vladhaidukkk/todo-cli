from datetime import date
from unittest.mock import MagicMock

import pytest
from pytest_mock import MockerFixture
from typer import BadParameter

import todo.main
from todo.main import target_date_parser


@pytest.fixture
def parse_str_to_date_spy(mocker: MockerFixture) -> MagicMock:
    return mocker.spy(todo.main, "parse_str_to_date")


def test_valid_input_returns_date(parse_str_to_date_spy: MagicMock) -> None:
    result = target_date_parser("2024-02-03")
    assert result == date(2024, 2, 3)
    parse_str_to_date_spy.assert_called_once_with("2024-02-03")


def test_already_parsed_input_returns_input(parse_str_to_date_spy: MagicMock) -> None:
    result = target_date_parser(date(2024, 2, 3))  # type: ignore
    assert result == date(2024, 2, 3)
    parse_str_to_date_spy.assert_not_called()


def test_invalid_input_raises_exception(parse_str_to_date_spy: MagicMock) -> None:
    with pytest.raises(BadParameter) as exc_info:
        target_date_parser("02/03/2024")

    assert isinstance(exc_info.value.__context__, ValueError)
    assert str(exc_info.value) == str(exc_info.value.__context__)
    parse_str_to_date_spy.assert_called_once_with("02/03/2024")
