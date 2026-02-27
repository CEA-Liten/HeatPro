from dataclasses import dataclass


@dataclass
class Threshold:
    min: float
    max: float


@dataclass
class TemperatureThreshold:
    heating_season: Threshold
    non_heating_season: Threshold
    outside_mid: float
    outside_min: float
