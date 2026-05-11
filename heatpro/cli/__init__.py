import logging
from pathlib import Path

import click
from rich.logging import RichHandler

from .cold import cold_cli, import_weather, ColdConfig
from .. import SET_TEMPERATURE_COLD

CONTEXT_SETTINGS = dict(help_option_names=["-h", "--help"])


@click.group(context_settings=CONTEXT_SETTINGS)
def cli():
    """HeatPro"""
    pass


@cli.command()
@click.argument("weather_csv", type=click.Path(exists=True))
@click.argument("year_energy_reference", type=click.FLOAT)
@click.option(
    "--set_temperature",
    type=click.FLOAT,
    default=SET_TEMPERATURE_COLD,
    help="Default set temperature",
)
@click.option("-v", "--verbose", is_flag=True, help="Enable debug logging")
def cold(weather_csv, year_energy_reference, set_temperature, verbose):
    logging.basicConfig(
        level=logging.DEBUG if verbose else logging.INFO,
        format="%(message)s",
        handlers=[RichHandler(rich_tracebacks=True)],
    )
    weather = import_weather(Path(weather_csv))
    cold_config = ColdConfig(set_temperature=set_temperature)

    logging.debug(f"Cold consummption configuration: {cold_config}")

    cold_cli(weather, year_energy_reference, cold_config)


if __name__ == "__main__":
    cli()
