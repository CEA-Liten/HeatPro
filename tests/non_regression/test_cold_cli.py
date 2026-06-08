import pytest
import pandas as pd
from pathlib import Path


@pytest.mark.cli
def test_cold_command_1e8_year_energy_reference():
    from heatpro.cli import cli
    from click.testing import CliRunner

    # Define the input and output file paths
    weather_csv = "./tests/non_regression/data/weather_for_cold_cli.csv"
    output_csv = "./tests/non_regression/data/output.csv"
    output_to_imitate_csv = "./tests/non_regression/data/results_for_cold_cli_energy_to_1e8.csv"
    year_energy_reference = "100_000_000"
    default_loss = 0.02

    # Run the cold command
    runner = CliRunner()
    result = runner.invoke(cli, ["cold", weather_csv, output_csv, year_energy_reference])

    # Check if the command ran successfully
    assert result.exit_code == 0

    # Read the output and reference files
    output_df = pd.read_csv(output_csv, sep=";", decimal=",", index_col=0)
    output_to_imitate_df = pd.read_csv(output_to_imitate_csv, sep=";", decimal=",", index_col=0)

    # Compare the dataframes
    pd.testing.assert_frame_equal(output_df, output_to_imitate_df, rtol=1e-2, atol=1e-2)

    output_df.index = pd.to_datetime(output_df.index, unit="s")
    assert output_df["total_consumption_power"].resample("YS").sum().mean() == pytest.approx(
        1e8 * (1 + default_loss), rel=1e-4
    )

    # Clean up the output file
    Path(output_csv).unlink()


@pytest.mark.cli
def test_cold_command_H1_year_energy_reference():
    from heatpro.cli import cli
    from heatpro.cli.helpers import ReferenceCold
    from click.testing import CliRunner

    # Define the input and output file paths
    weather_csv = "./tests/non_regression/data/weather_for_cold_cli.csv"
    output_csv = "./tests/non_regression/data/output.csv"
    output_to_imitate_csv = "./tests/non_regression/data/results_for_cold_cli_energy_to_H1.csv"
    year_energy_reference = "H1"
    default_loss = 0.02

    # Run the cold command
    runner = CliRunner()
    result = runner.invoke(cli, ["cold", weather_csv, output_csv, year_energy_reference])

    # Check if the command ran successfully
    assert result.exit_code == 0

    # Read the output and reference files
    output_df = pd.read_csv(output_csv, sep=";", decimal=",", index_col=0)
    output_to_imitate_df = pd.read_csv(output_to_imitate_csv, sep=";", decimal=",", index_col=0)

    # Compare the dataframes
    pd.testing.assert_frame_equal(output_df, output_to_imitate_df, rtol=1e-2, atol=1e-2)

    output_df.index = pd.to_datetime(output_df.index, unit="s")
    assert output_df["total_consumption_power"].resample("YS").sum().mean() == pytest.approx(
        ReferenceCold.H1.value * (1 + default_loss), rel=1e-4
    )

    # Clean up the output file
    Path(output_csv).unlink()
