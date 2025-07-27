"""Main MCP server using FastMCP to expose plant care utilities."""

from typing import Any

from fastmcp import FastMCP

from . import tools

# Create the FastMCP server instance
app: FastMCP = FastMCP("Plant Care Assistant")


@app.tool()
def get_plant_info(plant_name: str) -> dict[str, Any]:
    """Get comprehensive care information for a specific plant.

    Args:
        plant_name: Name of the plant to get information for

    Returns:
        Dictionary containing detailed plant care information including light requirements,
        watering frequency, humidity needs, temperature range, soil type, fertilizer needs,
        common problems, care difficulty, pet safety, and growth characteristics.
    """
    return tools.get_plant_info(plant_name)


@app.tool()
def calculate_watering_schedule(
    plant_name: str,
    current_season: str,
    humidity_level: float,
    temperature: float
) -> dict[str, Any]:
    """Calculate a personalized watering schedule for a plant based on environmental conditions.

    Args:
        plant_name: Name of the plant
        current_season: Current season (spring, summer, fall, autumn, winter)
        humidity_level: Current humidity percentage (0-100)
        temperature: Current temperature in Fahrenheit

    Returns:
        Dictionary containing watering frequency, schedule recommendations, and 
        environmental considerations tailored to the specific plant and conditions.
    """
    return tools.calculate_watering_schedule(
        plant_name, current_season, humidity_level, temperature
    )


@app.tool()
def get_light_recommendations(light_level: str) -> dict[str, Any]:
    """Get detailed light recommendations for plants requiring specific light levels.

    Args:
        light_level: Required light level (low, medium, bright, direct)

    Returns:
        Dictionary containing detailed light requirements, suitable locations,
        signs of inadequate or excessive light, and practical placement tips.
    """
    return tools.get_light_recommendations(light_level)


@app.tool()
def diagnose_plant_problem(
    plant_name: str,
    symptoms: list[str],
    problem_type: str
) -> dict[str, Any]:
    """Diagnose plant problems and provide comprehensive treatment solutions.

    Args:
        plant_name: Name of the plant with problems
        symptoms: List of observed symptoms (e.g., ["yellow leaves", "brown tips"])
        problem_type: Type of problem (yellowing, browning, wilting, pests, fungal, 
                     overwatering, underwatering, nutrient_deficiency, light_stress, other)

    Returns:
        Dictionary containing detailed diagnosis, common causes, treatment solutions,
        prevention strategies, urgency level, and follow-up recommendations.
    """
    return tools.diagnose_plant_problem(plant_name, symptoms, problem_type)


@app.tool()
def get_seasonal_care_tips(season: str, plant_type: str = "general") -> dict[str, Any]:
    """Get seasonal care tips and adjustments for optimal plant health throughout the year.

    Args:
        season: Current season (spring, summer, fall, autumn, winter)
        plant_type: Type of plant for specific advice (general, succulent, tropical, 
                   flowering, or any specific plant type)

    Returns:
        Dictionary containing seasonal care adjustments for watering, fertilizing,
        light, humidity, and specific tasks to perform during the season.
    """
    return tools.get_seasonal_care_tips(season, plant_type)


@app.tool()
def monitor_plant_health(
    plant_name: str,
    current_condition: str,
    days_since_last_water: int,
    days_since_last_fertilizer: int
) -> dict[str, Any]:
    """Monitor and assess plant health based on care history and current condition.

    Args:
        plant_name: Name of the plant being monitored
        current_condition: Current plant condition (excellent, good, fair, poor, critical)
        days_since_last_water: Number of days since the plant was last watered
        days_since_last_fertilizer: Number of days since the plant was last fertilized

    Returns:
        Dictionary containing comprehensive health assessment, care status evaluation,
        priority actions needed, recommendations for improvement, and tracking guidance.
    """
    return tools.monitor_plant_health(
        plant_name, current_condition, days_since_last_water, days_since_last_fertilizer
    )


def main() -> None:
    """Main entry point for the MCP server."""
    app.run()


if __name__ == "__main__":
    main()