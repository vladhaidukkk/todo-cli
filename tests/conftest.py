import time

import pytest
from pytest import FixtureRequest, Parser


def pytest_addoption(parser: Parser):
    parser.addoption(
        "--total-duration",
        action="store_true",
        default=False,
        help="Show total duration of tests execution at the end",
    )


@pytest.fixture(scope="session", autouse=True)
def show_total_duration(request: FixtureRequest):
    if not request.config.getoption("--total-duration"):
        yield
        return

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
