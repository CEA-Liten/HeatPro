"""Module for defining climatic zones."""

from enum import Enum


class ClimaticZone(Enum):
    """Enumeration of different climatic zones.

    This enum defines various climatic zones based on the French climate classification system.
    Each zone represents a specific climate type that can be used in energy management systems.

    Attributes:
        H1A: Represents a cold climate zone (H1a).
        H1B: Represents a cold climate zone (H1b).
        H1C: Represents a cold climate zone (H1c).
        H2A: Represents a temperate climate zone (H2a).
        H2B: Represents a temperate climate zone (H2b).
        H2C: Represents a temperate climate zone (H2c).
        H2D: Represents a temperate climate zone (H2d).
        H3: Represents a hot climate zone (H3).
    """

    H1A = "H1a"
    H1B = "H1b"
    H1C = "H1c"
    H2A = "H2a"
    H2B = "H2b"
    H2C = "H2c"
    H2D = "H2d"
    H3 = "H3"
