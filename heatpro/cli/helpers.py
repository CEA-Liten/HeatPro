from enum import Enum


class ReferenceCold(Enum):
    """Yearly cold energy consumption in kWh for different French cities.

    The values are categorized into three climate zones, with corresponding
    example cities and typical temperature ranges during the cooling season.
    These estimates are based on a total surface area of 144 hectares of
    tertiary buildings, evenly split between offices (50%) and commercial
    spaces (50%). The cooling temperature (TNC) is set to 22°C.

    - H1: Strasbourg (43,920,000 kWh) - Typical temperatures: 7-14°C
    - H2: Bordeaux (60,480,000 kWh) - Typical temperatures: 7-14°C
    - H3: Montpellier (80,640,000 kWh) - Typical temperatures: 7-14°C

    These climate zones represent different levels of cold energy demand based on
    geographical location and climate characteristics in France.

    Attributes:
        H1 (int): Yearly cold energy consumption for climate zone 1
            (example: Strasbourg, typical temperatures 7-14°C)
        H2 (int): Yearly cold energy consumption for climate zone 2
            (example: Bordeaux, typical temperatures 7-14°C)
        H3 (int): Yearly cold energy consumption for climate zone 3
            (example: Montpellier, typical temperatures 7-14°C)
    """

    H1 = 43_920_000
    H2 = 60_480_000
    H3 = 80_640_000
