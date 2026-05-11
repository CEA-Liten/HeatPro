import logging
from pathlib import Path

import click
from rich.logging import RichHandler

from .cold import cold_cli, import_weather, ColdConfig
from .helpers import ReferenceCold
from .. import SET_TEMPERATURE_COLD

CONTEXT_SETTINGS = dict(help_option_names=["-h", "--help"])


@click.group(context_settings=CONTEXT_SETTINGS)
def cli():
    """HeatPro"""
    pass


@cli.command()
@click.argument("weather_csv", type=click.Path(exists=True))
@click.argument("output_csv", type=click.Path())
@click.argument("year_energy_reference")
@click.option(
    "--set_temperature",
    type=click.FLOAT,
    default=SET_TEMPERATURE_COLD,
    help="Default set temperature",
)
@click.option("-v", "--verbose", is_flag=True, help="Enable debug logging")
def cold(weather_csv, output_csv, year_energy_reference, set_temperature, verbose):
    logging.basicConfig(
        level=logging.DEBUG if verbose else logging.INFO,
        format="%(message)s",
        handlers=[RichHandler(rich_tracebacks=True)],
    )
    weather = import_weather(Path(weather_csv))
    cold_config = ColdConfig(set_temperature=set_temperature)
    try:
        year_energy_reference = float(year_energy_reference)
    except ValueError:
        match year_energy_reference:
            case ReferenceCold.H1.name:
                year_energy_reference = ReferenceCold.H1.value
            case ReferenceCold.H2.name:
                year_energy_reference = ReferenceCold.H2.value
            case ReferenceCold.H3.name:
                year_energy_reference = ReferenceCold.H3.value
            case _:
                logging.error(f"year_energy_reference must be numeric or one of ReferenceCold names: H1, H2, H3. You gave {year_energy_reference=}")
                exit()

    logging.debug(f"Cold consummption configuration: {cold_config}")

    result = cold_cli(weather, year_energy_reference, cold_config)
    result.to_csv(Path(output_csv), sep=";", float_format="%.2f")


if __name__ == "__main__":
    cli()
