"""Utility functions for the plant helper MCP server."""

from typing import Any


def validate_plant_name(name: str) -> None:
    """Validate that a plant name is provided and not empty."""
    if not isinstance(name, str):
        raise TypeError("Plant name must be a string")
    if not name.strip():
        raise ValueError("Plant name cannot be empty")


def validate_positive_number(value: int | float, name: str) -> None:
    """Validate that a value is a positive number."""
    if not isinstance(value, (int, float)):
        raise TypeError(f"{name} must be a number, got {type(value).__name__}")
    if value <= 0:
        raise ValueError(f"{name} must be positive, got {value}")


def validate_percentage(value: int | float, name: str) -> None:
    """Validate that a value is a valid percentage (0-100)."""
    if not isinstance(value, (int, float)):
        raise TypeError(f"{name} must be a number, got {type(value).__name__}")
    if not 0 <= value <= 100:
        raise ValueError(f"{name} must be between 0 and 100, got {value}")


def validate_light_level(level: str) -> None:
    """Validate that the light level is one of the accepted values."""
    valid_levels = ["low", "medium", "bright", "direct"]
    if not isinstance(level, str):
        raise TypeError("Light level must be a string")
    if level.lower() not in valid_levels:
        raise ValueError(f"Light level must be one of {valid_levels}, got '{level}'")


def validate_season(season: str) -> None:
    """Validate that the season is one of the accepted values."""
    valid_seasons = ["spring", "summer", "fall", "winter", "autumn"]
    if not isinstance(season, str):
        raise TypeError("Season must be a string")
    if season.lower() not in valid_seasons:
        raise ValueError(f"Season must be one of {valid_seasons}, got '{season}'")


def validate_problem_type(problem_type: str) -> None:
    """Validate that the problem type is one of the accepted values."""
    valid_types = [
        "yellowing", "browning", "wilting", "pests", "fungal", "overwatering", 
        "underwatering", "nutrient_deficiency", "light_stress", "other"
    ]
    if not isinstance(problem_type, str):
        raise TypeError("Problem type must be a string")
    if problem_type.lower() not in valid_types:
        raise ValueError(f"Problem type must be one of {valid_types}, got '{problem_type}'")


def calculate_watering_frequency(
    plant_type: str, 
    season: str, 
    humidity: float, 
    temperature: float
) -> int:
    """Calculate watering frequency in days based on plant and environmental factors."""
    # Base frequencies for different plant types (in days)
    base_frequencies = {
        "succulent": 10,
        "cactus": 14,
        "tropical": 5,
        "fern": 3,
        "herb": 4,
        "flowering": 6,
        "foliage": 7,
        "vine": 6,
        "tree": 8,
        "grass": 3
    }
    
    # Get base frequency or default to 7 days
    base_freq = base_frequencies.get(plant_type.lower(), 7)
    
    # Adjust for season
    season_multipliers = {
        "spring": 1.0,
        "summer": 0.8,  # More frequent watering
        "fall": 1.2,    # Less frequent
        "autumn": 1.2,  # Less frequent  
        "winter": 1.5   # Much less frequent
    }
    
    freq = base_freq * season_multipliers.get(season.lower(), 1.0)
    
    # Adjust for humidity (lower humidity = more frequent watering)
    if humidity < 30:
        freq *= 0.8
    elif humidity > 70:
        freq *= 1.2
    
    # Adjust for temperature (higher temp = more frequent watering)
    if temperature > 75:
        freq *= 0.9
    elif temperature < 65:
        freq *= 1.1
    
    return max(1, int(round(freq)))


def get_light_requirements(light_level: str) -> dict[str, Any]:
    """Get detailed light requirements for a given light level."""
    requirements = {
        "low": {
            "description": "Bright indirect light, can tolerate shade",
            "hours_per_day": "4-6 hours",
            "distance_from_window": "6-10 feet from bright window",
            "suitable_locations": ["North-facing windows", "Interior rooms", "Offices with fluorescent lighting"]
        },
        "medium": {
            "description": "Bright indirect light, some morning sun okay",
            "hours_per_day": "6-8 hours", 
            "distance_from_window": "3-6 feet from bright window",
            "suitable_locations": ["East-facing windows", "A few feet from south/west windows", "Bright bathrooms"]
        },
        "bright": {
            "description": "Bright indirect light, no direct sun",
            "hours_per_day": "8-10 hours",
            "distance_from_window": "1-3 feet from bright window",
            "suitable_locations": ["Near south/west windows with sheer curtains", "Bright rooms", "Sunrooms"]
        },
        "direct": {
            "description": "Direct sunlight for several hours",
            "hours_per_day": "6+ hours direct sun",
            "distance_from_window": "On windowsill or directly in front",
            "suitable_locations": ["South-facing windowsills", "Outdoor patios", "Greenhouse"]
        }
    }
    
    return requirements.get(light_level.lower(), requirements["medium"])