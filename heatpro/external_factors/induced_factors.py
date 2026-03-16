from dataclasses import dataclass, fields

import pandas as pd


@dataclass(frozen=True)
class InducedFactors:
    supply_temperature: pd.Series | None = None
    return_temperature: pd.Series | None = None
    soil_temperature: pd.Series | None = None
    closed_heating_season: pd.Series | None = None
    cold_water_temperature: pd.Series | None = None

    def __post_init__(self):
        non_none_series = [
            getattr(self, field.name)
            for field in fields(self)
            if getattr(self, field.name) is not None
        ]

        if not len(non_none_series) > 1:
            return None

        # Find the field name of the first series
        first_series_field = next(
            field.name for field in fields(self) if getattr(self, field.name) is non_none_series[0]
        )

        # Check if all indexes are identical
        first_index = non_none_series[0].index
        for series in non_none_series[1:]:
            if not series.index.equals(first_index):
                # Find the field name of the mismatched series
                mismatched_field = next(
                    field.name for field in fields(self) if getattr(self, field.name) is series
                )
                raise ValueError(
                    f"Index mismatch: '{mismatched_field}' series index "
                    f"does not match '{first_series_field}' series index"
                )
