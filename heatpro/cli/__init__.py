# my_cli_tool/cli.py
import click


CONTEXT_SETTINGS = dict(help_option_names=["-h", "--help"])


@click.group(context_settings=CONTEXT_SETTINGS)
def cli():
    """HeatPro"""
    pass


if __name__ == "__main__":
    cli()
