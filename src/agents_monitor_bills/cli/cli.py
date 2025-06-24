import typer

from agents_monitor_bills import main

app = typer.Typer(no_args_is_help=True)


@app.command()
def hello():
    """Say hello for debug purposes."""
    print("Hello from CLI!")


@app.command("start")
def start():
    """Run the bill monitoring agent."""
    main.main()


if __name__ == "__main__":
    app()
