import typer

app = typer.Typer()


@app.command()
def test():
    print("It works!")


if __name__ == "__main__":
    app()
