import logging
from pathlib import Path

import click
from rich.console import Console
from rich.logging import RichHandler

from .cold import cold_pipeline, import_weather, ColdConfig, Repartition
from .helpers import ReferenceCold
from .plotting import cold_results
from .. import SET_TEMPERATURE_COLD

CONTEXT_SETTINGS = dict(help_option_names=["-h", "--help"])


@click.group(context_settings=CONTEXT_SETTINGS)
def cli():
    """HeatPro"""
    pass


def validate_float_between_0_and_1(ctx, param, value):
    """_summary_

    Args:
        ctx (_type_): _description_
        param (_type_): _description_
        value (_type_): _description_

    Raises:
        click.BadParameter: _description_

    Returns:
        _type_: _description_
    
    :meta private:
    """
    if value is None:
        return value
    if not (0 <= value <= 1):
        raise click.BadParameter("Value must be between 0 and 1")
    return value


@cli.command("cold")
@click.argument("weather_csv", type=click.Path(exists=True))
@click.argument("output_csv", type=click.Path())
@click.argument("year_energy_reference")
@click.option(
    "--set-temperature",
    type=click.FLOAT,
    default=SET_TEMPERATURE_COLD,
    help="Default set temperature",
)
@click.option(
    "--loss",
    type=click.FLOAT,
    default=0.02,
    help="Cold energy loss",
)
@click.option(
    "-fws",
    "--full-week-share",
    type=click.FLOAT,
    callback=validate_float_between_0_and_1,
    default=1 / 2,
    help="Share of cold energy consummed following a full week activity profile",
)
@click.option(
    "-fwts",
    "--full-week-temperature-sensitivity",
    type=click.FLOAT,
    callback=validate_float_between_0_and_1,
    default=1 / 2,
    help="Share of cold energy within consumption associated to full week profile consummed in a temperature sensitive manner",
)
@click.option(
    "-wets",
    "--week-end-temperature-sensitivity",
    type=click.FLOAT,
    callback=validate_float_between_0_and_1,
    default=1 / 2,
    help="Share of cold energy within consumption associated to low activity on weekend profile consummed in a temperature sensitive manner",
)
@click.option("-start", "--date-start", default=None, help="date start")
@click.option("-end", "--date-end", default=None, help="date end")
@click.option("-v", "--verbose", is_flag=True, help="Enable debug logging")
@click.option("-s", "--show", is_flag=True, help="Show graphs of the result")
def cold_cli(
    weather_csv,
    output_csv,
    year_energy_reference,
    loss,
    set_temperature,
    full_week_share,
    full_week_temperature_sensitivity,
    week_end_temperature_sensitivity,
    date_start,
    date_end,
    verbose,
    show,
):
    logging.basicConfig(
        level=logging.DEBUG if verbose else logging.INFO,
        format="%(message)s",
        handlers=[RichHandler(rich_tracebacks=True)],
    )
    console = Console()
    with console.status("[bold green]Importing weather csv data...", spinner="bouncingBall"):
        weather = import_weather(Path(weather_csv)).loc[date_start:date_end]
    logging.debug(weather.index.max())
    cold_config = ColdConfig(
        set_temperature,
        loss,
        Repartition(full_week_share, 1 - full_week_share),
        Repartition(full_week_temperature_sensitivity, week_end_temperature_sensitivity),
    )
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
                logging.error(
                    f"year_energy_reference must be numeric or one of ReferenceCold names: H1, H2, H3. You gave {year_energy_reference=}"
                )
                exit()

    logging.debug(f"Cold consummption configuration: {cold_config}")

    with console.status("[bold red]Calculating cold demand...", spinner="bouncingBall"):
        result = cold_pipeline(weather, year_energy_reference, cold_config)

    with console.status("[bold magenta]Exporting results...", spinner="bouncingBall"):
        result.to_csv(Path(output_csv), sep=";", float_format="%.2f")

        if show:
            cold_results(weather, result).show()


if __name__ == "__main__":
    cli()
