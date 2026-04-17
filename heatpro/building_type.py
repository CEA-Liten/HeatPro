"""Module for defining building types."""

from enum import Enum


class BuildingType(Enum):
    """Enumeration of different building types.

    This enum defines various types of buildings that can be used in energy management systems.
    Each building type is associated with a French label that can be used for display purposes.

    Attributes:
        OFFICE: Represents office buildings (Bureaux).
        CAFE: Represents cafes (Café).
        RETAIL: Represents retail stores (Commerces).
        EHPAD: Represents elderly care facilities (EHPAD).
        SCHOOL: Represents schools (Écoles).
        HOTEL: Represents hotels (Hôtel).
        RESIDENTIAL: Represents residential buildings (Résidentiel).
        HEALTHCARE: Represents healthcare facilities (Santé).
        SPORTS: Represents sports facilities (Sport).
    """

    OFFICE = "Bureaux"
    CAFE = "Café"
    RETAIL = "Commerces"
    EHPAD = "EHPAD"
    SCHOOL = "Écoles"
    HOTEL = "Hôtel"
    RESIDENTIAL = "Résidentiel"
    HEALTHCARE = "Santé"
    SPORTS = "Sport"
