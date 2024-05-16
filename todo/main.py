from typing import Annotated

from typer import Argument, Typer

app = Typer()


@app.command()
def main(name: Annotated[str, Argument()] = "World"):
    print(f"Hello {name}")
