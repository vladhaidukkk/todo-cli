from typing import Annotated

from typer import Argument, run


def main(name: Annotated[str, Argument()] = "World"):
    print(f"Hello {name}")


if __name__ == "__main__":
    run(main)
