import time
from collections.abc import Generator

import pytest
from pytest import Config, FixtureRequest, Parser


def pytest_addoption(parser: Parser) -> None:
    parser.addoption(
        "--total-duration",
        action="store_true",
        default=False,
        help="Show total duration of tests execution at the end",
    )


def pytest_configure(config: Config) -> None:
    if config.getoption("--total-duration"):

        def show_total_duration(request: FixtureRequest) -> Generator[None, None, None]:
            start = time.perf_counter()
            yield
            elapsed = time.perf_counter() - start

            output = f"Total duration: {elapsed:.3f}s"
            divider = "=" * len(output)

            cap_manager = request.config.pluginmanager.getplugin("capturemanager")
            with cap_manager.global_and_fixture_disabled():  # type: ignore
                print(f"\n\n{divider}")
                print(output)
                print(divider, end="")

        globals()["show_total_duration"] = pytest.fixture(
            scope="session", autouse=True
        )(show_total_duration)
