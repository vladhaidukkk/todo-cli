from typing import Annotated

from typer import Argument


def main(name: Annotated[str, Argument()] = "World"):
    print(f"Hello {name}")
