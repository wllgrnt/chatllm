"""Console script for chatllm."""


import click


@click.command()
def main():
    """Main entrypoint."""
    click.echo("chatllm")
    click.echo("=" * len("chatllm"))
    click.echo("Barebones locally run ChatGPT with BYO keys and local storage")


if __name__ == "__main__":
    main()
    
