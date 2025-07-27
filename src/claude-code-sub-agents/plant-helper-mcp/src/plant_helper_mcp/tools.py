"""Plant care tools for the MCP server."""

from typing import Any

from .utils import (
    calculate_watering_frequency,
    get_light_requirements,
    validate_light_level,
    validate_percentage,
    validate_plant_name,
    validate_positive_number,
    validate_problem_type,
    validate_season,
)


def get_plant_info(plant_name: str) -> dict[str, Any]:
    """Get comprehensive care information for a specific plant.

    Args:
        plant_name: Name of the plant to get information for

    Returns:
        Dictionary containing plant care information

    Raises:
        ValueError: If plant name is empty
        TypeError: If plant name is not a string
    """
    validate_plant_name(plant_name)
    
    # Comprehensive plant database
    plant_database = {
        "snake plant": {
            "scientific_name": "Sansevieria trifasciata",
            "type": "succulent",
            "light": "low to bright indirect",
            "water_frequency": "every 2-3 weeks",
            "humidity": "30-50%",
            "temperature": "65-75°F (18-24°C)",
            "soil": "well-draining potting mix",
            "fertilizer": "monthly during growing season",
            "common_problems": ["overwatering", "root rot"],
            "care_difficulty": "easy",
            "pet_safe": False,
            "growth_rate": "slow",
            "max_size": "3-4 feet tall"
        },
        "pothos": {
            "scientific_name": "Epipremnum aureum",
            "type": "vine",
            "light": "medium to bright indirect",
            "water_frequency": "when top inch of soil is dry",
            "humidity": "40-60%",
            "temperature": "65-85°F (18-29°C)",
            "soil": "well-draining potting mix",
            "fertilizer": "monthly during spring/summer",
            "common_problems": ["overwatering", "pests", "yellowing leaves"],
            "care_difficulty": "easy",
            "pet_safe": False,
            "growth_rate": "fast",
            "max_size": "6-10 feet long"
        },
        "monstera": {
            "scientific_name": "Monstera deliciosa",
            "type": "tropical",
            "light": "bright indirect",
            "water_frequency": "when top 2 inches of soil are dry",
            "humidity": "50-70%",
            "temperature": "65-80°F (18-27°C)",
            "soil": "well-draining, chunky potting mix",
            "fertilizer": "monthly during growing season",
            "common_problems": ["overwatering", "low humidity", "lack of support"],
            "care_difficulty": "moderate",
            "pet_safe": False,
            "growth_rate": "moderate to fast",
            "max_size": "6-8 feet indoors"
        },
        "spider plant": {
            "scientific_name": "Chlorophytum comosum",
            "type": "foliage",
            "light": "bright indirect",
            "water_frequency": "weekly or when soil surface is dry",
            "humidity": "40-60%",
            "temperature": "65-75°F (18-24°C)",
            "soil": "well-draining potting mix",
            "fertilizer": "bi-weekly during growing season",
            "common_problems": ["brown tips", "overwatering", "underwatering"],
            "care_difficulty": "easy",
            "pet_safe": True,
            "growth_rate": "fast",
            "max_size": "12-24 inches"
        },
        "rubber plant": {
            "scientific_name": "Ficus elastica",
            "type": "tree",
            "light": "bright indirect",
            "water_frequency": "when top inch of soil is dry",
            "humidity": "40-60%",
            "temperature": "65-80°F (18-27°C)",
            "soil": "well-draining potting mix",
            "fertilizer": "monthly during growing season",
            "common_problems": ["overwatering", "low light", "leaf drop"],
            "care_difficulty": "moderate",
            "pet_safe": False,
            "growth_rate": "moderate",
            "max_size": "6-10 feet indoors"
        },
        "peace lily": {
            "scientific_name": "Spathiphyllum wallisii",
            "type": "flowering",
            "light": "low to medium indirect",
            "water_frequency": "when soil surface feels dry",
            "humidity": "50-70%",
            "temperature": "65-80°F (18-27°C)",
            "soil": "well-draining, moisture-retaining mix",
            "fertilizer": "monthly during growing season",
            "common_problems": ["brown tips", "overwatering", "low humidity"],
            "care_difficulty": "moderate",
            "pet_safe": False,
            "growth_rate": "moderate",
            "max_size": "1-3 feet"
        },
        "aloe vera": {
            "scientific_name": "Aloe barbadensis miller",
            "type": "succulent",
            "light": "bright indirect to direct",
            "water_frequency": "every 2-3 weeks",
            "humidity": "30-50%",
            "temperature": "65-75°F (18-24°C)",
            "soil": "cactus/succulent potting mix",
            "fertilizer": "2-3 times during growing season",
            "common_problems": ["overwatering", "root rot", "sunburn"],
            "care_difficulty": "easy",
            "pet_safe": False,
            "growth_rate": "slow",
            "max_size": "1-2 feet"
        },
        "zz plant": {
            "scientific_name": "Zamioculcas zamiifolia",
            "type": "foliage",
            "light": "low to bright indirect",
            "water_frequency": "every 2-3 weeks",
            "humidity": "30-50%",
            "temperature": "65-75°F (18-24°C)",
            "soil": "well-draining potting mix",
            "fertilizer": "2-3 times during growing season",
            "common_problems": ["overwatering", "root rot"],
            "care_difficulty": "easy",
            "pet_safe": False,
            "growth_rate": "slow",
            "max_size": "2-3 feet"
        }
    }
    
    plant_key = plant_name.lower().strip()
    if plant_key in plant_database:
        return plant_database[plant_key]
    else:
        # Return generic care information if specific plant not in database
        return {
            "scientific_name": "Unknown",
            "type": "unknown",
            "light": "bright indirect light",
            "water_frequency": "when top inch of soil is dry",
            "humidity": "40-60%",
            "temperature": "65-75°F (18-24°C)",
            "soil": "well-draining potting mix",
            "fertilizer": "monthly during growing season",
            "common_problems": ["overwatering", "underwatering", "inadequate light"],
            "care_difficulty": "varies",
            "pet_safe": "unknown - check specific plant safety",
            "growth_rate": "varies",
            "max_size": "varies",
            "note": f"Specific information for '{plant_name}' not found. These are general care guidelines."
        }


def calculate_watering_schedule(
    plant_name: str,
    current_season: str,
    humidity_level: float,
    temperature: float
) -> dict[str, Any]:
    """Calculate a watering schedule for a specific plant based on environmental conditions.

    Args:
        plant_name: Name of the plant
        current_season: Current season (spring, summer, fall/autumn, winter)
        humidity_level: Current humidity percentage (0-100)
        temperature: Current temperature in Fahrenheit

    Returns:
        Dictionary containing watering schedule and recommendations

    Raises:
        ValueError: If inputs are invalid
        TypeError: If inputs are wrong type
    """
    validate_plant_name(plant_name)
    validate_season(current_season)
    validate_percentage(humidity_level, "humidity_level")
    validate_positive_number(temperature, "temperature")
    
    # Get plant info to determine type
    plant_info = get_plant_info(plant_name)
    plant_type = plant_info.get("type", "foliage")
    
    # Calculate watering frequency
    frequency_days = calculate_watering_frequency(
        plant_type, current_season, humidity_level, temperature
    )
    
    # Generate schedule
    schedule = {
        "plant_name": plant_name,
        "watering_frequency_days": frequency_days,
        "season": current_season,
        "environmental_conditions": {
            "humidity": f"{humidity_level}%",
            "temperature": f"{temperature}°F"
        },
        "next_watering": f"In {frequency_days} days",
        "recommendations": []
    }
    
    # Add specific recommendations based on conditions
    if humidity_level < 30:
        schedule["recommendations"].append("Consider using a humidifier or pebble tray to increase humidity")
    elif humidity_level > 70:
        schedule["recommendations"].append("Ensure good air circulation to prevent fungal issues")
    
    if temperature > 80:
        schedule["recommendations"].append("Monitor soil moisture more frequently in high temperatures")
    elif temperature < 60:
        schedule["recommendations"].append("Reduce watering frequency in cooler temperatures")
    
    if current_season.lower() in ["fall", "autumn", "winter"]:
        schedule["recommendations"].append("Reduce watering during dormant season")
    
    # Add plant-specific watering tips
    if plant_type in ["succulent", "cactus"]:
        schedule["recommendations"].append("Allow soil to dry completely between waterings")
    elif plant_type == "fern":
        schedule["recommendations"].append("Keep soil consistently moist but not waterlogged")
    elif plant_type == "tropical":
        schedule["recommendations"].append("Maintain consistent moisture levels")
    
    return schedule


def get_light_recommendations(light_level: str) -> dict[str, Any]:
    """Get detailed light recommendations for plants requiring specific light levels.

    Args:
        light_level: Light level requirement (low, medium, bright, direct)

    Returns:
        Dictionary containing light recommendations

    Raises:
        ValueError: If light level is invalid
        TypeError: If light level is not a string
    """
    validate_light_level(light_level)
    
    requirements = get_light_requirements(light_level)
    
    return {
        "light_level": light_level,
        "requirements": requirements,
        "signs_of_inadequate_light": [
            "Leggy or stretched growth",
            "Small, pale leaves",
            "Slow growth",
            "Loss of variegation in colorful plants"
        ],
        "signs_of_too_much_light": [
            "Scorched or brown leaf edges",
            "Wilting despite adequate water",
            "Faded or bleached appearance",
            "Crispy leaf texture"
        ],
        "tips": [
            "Rotate plant weekly for even growth",
            "Use sheer curtains to filter harsh direct sunlight",
            "Consider grow lights if natural light is insufficient",
            "Monitor plant response and adjust placement as needed"
        ]
    }


def diagnose_plant_problem(
    plant_name: str,
    symptoms: list[str],
    problem_type: str
) -> dict[str, Any]:
    """Diagnose plant problems and provide solutions based on symptoms.

    Args:
        plant_name: Name of the plant with problems
        symptoms: List of observed symptoms
        problem_type: Type of problem (yellowing, browning, wilting, etc.)

    Returns:
        Dictionary containing diagnosis and treatment recommendations

    Raises:
        ValueError: If inputs are invalid
        TypeError: If inputs are wrong type
    """
    validate_plant_name(plant_name)
    validate_problem_type(problem_type)
    
    if not isinstance(symptoms, list):
        raise TypeError("Symptoms must be a list of strings")
    
    if not symptoms:
        raise ValueError("At least one symptom must be provided")
    
    # Problem diagnosis database
    problem_solutions = {
        "yellowing": {
            "common_causes": [
                "Overwatering - most common cause",
                "Natural aging of older leaves",
                "Nutrient deficiency (especially nitrogen)",
                "Root bound condition",
                "Poor drainage"
            ],
            "solutions": [
                "Check soil moisture - allow to dry if soggy",
                "Improve drainage with better potting mix",
                "Remove yellow leaves to redirect energy",
                "Consider repotting if root bound",
                "Apply balanced fertilizer if nutrients are lacking"
            ],
            "prevention": [
                "Water only when top inch of soil is dry",
                "Ensure pots have drainage holes",
                "Use well-draining potting mix",
                "Maintain consistent watering schedule"
            ]
        },
        "browning": {
            "common_causes": [
                "Low humidity",
                "Fluoride or chlorine in water",
                "Over-fertilization",
                "Direct sunlight burning leaves",
                "Underwatering"
            ],
            "solutions": [
                "Increase humidity with pebble tray or humidifier",
                "Use filtered or distilled water",
                "Flush soil with water to remove excess salts",
                "Move away from direct sunlight",
                "Establish consistent watering routine"
            ],
            "prevention": [
                "Maintain appropriate humidity levels",
                "Use filtered water when possible",
                "Fertilize sparingly and dilute solutions",
                "Provide appropriate light conditions"
            ]
        },
        "wilting": {
            "common_causes": [
                "Underwatering",
                "Overwatering leading to root rot",
                "Root damage",
                "Extreme temperatures",
                "Transplant shock"
            ],
            "solutions": [
                "Check soil moisture and water if dry",
                "If soil is wet, improve drainage and reduce watering",
                "Inspect roots for rot - trim damaged parts",
                "Move to appropriate temperature range",
                "Reduce light temporarily if recently repotted"
            ],
            "prevention": [
                "Monitor soil moisture regularly",
                "Ensure proper drainage",
                "Maintain stable temperatures",
                "Handle roots gently during repotting"
            ]
        },
        "pests": {
            "common_causes": [
                "Spider mites (dry conditions)",
                "Aphids (new growth)",
                "Mealybugs (humid conditions)",
                "Scale insects",
                "Fungus gnats (overwatering)"
            ],
            "solutions": [
                "Isolate affected plant immediately",
                "Spray with insecticidal soap or neem oil",
                "Wipe leaves with damp cloth",
                "Use yellow sticky traps for flying pests",
                "Rinse plant with water to remove pests"
            ],
            "prevention": [
                "Inspect plants regularly",
                "Quarantine new plants",
                "Maintain appropriate humidity",
                "Avoid overwatering",
                "Clean leaves regularly"
            ]
        },
        "fungal": {
            "common_causes": [
                "High humidity with poor air circulation",
                "Overwatering",
                "Contaminated soil",
                "Overcrowding plants",
                "Water on leaves"
            ],
            "solutions": [
                "Improve air circulation around plant",
                "Reduce watering frequency",
                "Apply fungicide if severe",
                "Remove affected leaves immediately",
                "Repot in fresh, sterile soil"
            ],
            "prevention": [
                "Water at soil level, not on leaves",
                "Ensure good air circulation",
                "Avoid overcrowding plants",
                "Use sterile potting mix",
                "Remove dead plant material promptly"
            ]
        },
        "overwatering": {
            "common_causes": [
                "Watering too frequently",
                "Poor drainage",
                "Using wrong soil type",
                "Pot without drainage holes",
                "Cool, humid conditions"
            ],
            "solutions": [
                "Stop watering immediately",
                "Improve drainage",
                "Repot in well-draining soil if necessary",
                "Remove rotted roots",
                "Increase air circulation"
            ],
            "prevention": [
                "Check soil before watering",
                "Use pots with drainage holes",
                "Choose appropriate potting mix",
                "Adjust watering for season and conditions"
            ]
        },
        "underwatering": {
            "common_causes": [
                "Infrequent watering",
                "Very fast-draining soil",
                "High temperatures",
                "Low humidity",
                "Root bound condition"
            ],
            "solutions": [
                "Water thoroughly until water drains out",
                "Increase watering frequency",
                "Soak pot in water for 30 minutes if very dry",
                "Consider repotting if root bound",
                "Mulch soil surface to retain moisture"
            ],
            "prevention": [
                "Establish regular watering schedule",
                "Monitor soil moisture regularly",
                "Adjust watering for environmental conditions",
                "Repot when plant becomes root bound"
            ]
        },
        "nutrient_deficiency": {
            "common_causes": [
                "Depleted potting soil",
                "Infrequent fertilizing",
                "Wrong fertilizer type",
                "pH imbalance affecting nutrient uptake",
                "Excessive watering leaching nutrients"
            ],
            "solutions": [
                "Apply balanced liquid fertilizer",
                "Repot in fresh potting mix",
                "Test and adjust soil pH",
                "Use appropriate fertilizer for plant type",
                "Follow proper fertilizing schedule"
            ],
            "prevention": [
                "Fertilize regularly during growing season",
                "Use quality potting mix",
                "Monitor plant for early signs",
                "Repot annually or bi-annually"
            ]
        },
        "light_stress": {
            "common_causes": [
                "Too much direct sunlight",
                "Insufficient light",
                "Sudden change in light conditions",
                "Wrong light spectrum",
                "Inconsistent lighting"
            ],
            "solutions": [
                "Gradually adjust light exposure",
                "Move to appropriate light level",
                "Use sheer curtains to filter light",
                "Consider supplemental grow lights",
                "Rotate plant for even exposure"
            ],
            "prevention": [
                "Research plant's light requirements",
                "Make gradual light changes",
                "Monitor plant response to light",
                "Provide consistent lighting conditions"
            ]
        },
        "other": {
            "common_causes": [
                "Environmental stress",
                "Genetic factors",
                "Age-related changes",
                "Mechanical damage",
                "Chemical exposure"
            ],
            "solutions": [
                "Assess overall care conditions",
                "Consult plant care resources",
                "Consider consulting local nursery",
                "Document symptoms for tracking",
                "Maintain consistent care routine"
            ],
            "prevention": [
                "Provide optimal growing conditions",
                "Handle plants gently",
                "Keep plants away from chemicals",
                "Monitor for changes regularly"
            ]
        }
    }
    
    problem_key = problem_type.lower()
    diagnosis_info = problem_solutions.get(problem_key, problem_solutions["other"])
    
    # Get plant-specific information
    plant_info = get_plant_info(plant_name)
    
    return {
        "plant_name": plant_name,
        "problem_type": problem_type,
        "symptoms": symptoms,
        "diagnosis": diagnosis_info,
        "plant_specific_notes": {
            "plant_type": plant_info.get("type", "unknown"),
            "common_problems": plant_info.get("common_problems", []),
            "care_difficulty": plant_info.get("care_difficulty", "varies")
        },
        "urgency_level": "high" if problem_type in ["fungal", "pests", "overwatering"] else "medium",
        "follow_up": [
            "Monitor plant daily for changes",
            "Document treatment progress",
            "Adjust care routine based on response",
            "Consult professional if condition worsens"
        ]
    }


def get_seasonal_care_tips(season: str, plant_type: str = "general") -> dict[str, Any]:
    """Get seasonal care tips for plants based on the time of year.

    Args:
        season: Current season (spring, summer, fall/autumn, winter)
        plant_type: Type of plant (optional, defaults to general)

    Returns:
        Dictionary containing seasonal care recommendations

    Raises:
        ValueError: If season is invalid
        TypeError: If season is not a string
    """
    validate_season(season)
    
    seasonal_tips = {
        "spring": {
            "general": {
                "watering": "Increase watering frequency as plants enter growing season",
                "fertilizing": "Begin monthly fertilizing with balanced fertilizer",
                "repotting": "Best time for repotting most houseplants",
                "pruning": "Remove dead/damaged growth and shape plants",
                "light": "Gradually increase light exposure as days get longer",
                "humidity": "Monitor as heating systems are used less"
            },
            "specific_tasks": [
                "Check for pests that may have developed over winter",
                "Refresh top layer of potting soil",
                "Begin propagation projects",
                "Clean leaves to remove dust buildup",
                "Gradually move plants closer to windows"
            ]
        },
        "summer": {
            "general": {
                "watering": "Increase watering frequency, may need daily for some plants",
                "fertilizing": "Continue regular fertilizing schedule",
                "repotting": "Can repot if necessary but spring is preferred",
                "pruning": "Light pruning and deadheading flowers",
                "light": "Provide shade during intense afternoon sun",
                "humidity": "Increase humidity with air conditioning running"
            },
            "specific_tasks": [
                "Move plants away from hot windows",
                "Use humidity trays or humidifiers",
                "Monitor for spider mites (thrive in heat)",
                "Consider moving plants outdoors gradually",
                "Ensure adequate air circulation"
            ]
        },
        "fall": {
            "general": {
                "watering": "Begin reducing watering frequency",
                "fertilizing": "Reduce or stop fertilizing by late fall",
                "repotting": "Avoid repotting unless emergency",
                "pruning": "Light cleanup of dead/dying foliage",
                "light": "Supplement with grow lights as days shorten",
                "humidity": "Monitor as heating systems start up"
            },
            "specific_tasks": [
                "Bring outdoor plants inside before frost",
                "Quarantine outdoor plants before bringing inside",
                "Reduce fertilizing frequency",
                "Check for pests before bringing plants inside",
                "Clean windows to maximize available light"
            ]
        },
        "autumn": {
            "general": {
                "watering": "Begin reducing watering frequency",
                "fertilizing": "Reduce or stop fertilizing by late autumn",
                "repotting": "Avoid repotting unless emergency",
                "pruning": "Light cleanup of dead/dying foliage",
                "light": "Supplement with grow lights as days shorten",
                "humidity": "Monitor as heating systems start up"
            },
            "specific_tasks": [
                "Bring outdoor plants inside before frost",
                "Quarantine outdoor plants before bringing inside",
                "Reduce fertilizing frequency",
                "Check for pests before bringing plants inside",
                "Clean windows to maximize available light"
            ]
        },
        "winter": {
            "general": {
                "watering": "Reduce watering significantly - most plants are dormant",
                "fertilizing": "Stop fertilizing most plants",
                "repotting": "Avoid repotting - plants are dormant",
                "pruning": "Minimal pruning - only remove dead/damaged growth",
                "light": "Maximize available light, consider grow lights",
                "humidity": "Use humidifiers to combat dry indoor air"
            },
            "specific_tasks": [
                "Move plants away from cold windows and heat sources",
                "Reduce watering frequency significantly",
                "Use grow lights for light-loving plants",
                "Maintain humidity with humidifiers or pebble trays",
                "Monitor for pests (spider mites love dry, warm conditions)"
            ]
        }
    }
    
    season_key = season.lower()
    season_info = seasonal_tips.get(season_key, seasonal_tips["spring"])
    
    # Add plant-type specific tips if applicable
    type_specific_tips = {}
    if plant_type.lower() == "succulent":
        type_specific_tips = {
            "watering": "Reduce watering even more than other plants",
            "temperature": "Can tolerate cooler temperatures",
            "special_note": "Very drought tolerant, err on side of underwatering"
        }
    elif plant_type.lower() == "tropical":
        type_specific_tips = {
            "humidity": "Maintain higher humidity levels year-round",
            "temperature": "Keep above 60°F, prefer 65-80°F",
            "special_note": "May need extra humidity and warmth in winter"
        }
    elif plant_type.lower() == "flowering":
        type_specific_tips = {
            "deadheading": "Remove spent flowers to encourage more blooms",
            "fertilizing": "May benefit from bloom-boosting fertilizer",
            "special_note": "Flowering may reduce in shorter daylight hours"
        }
    
    return {
        "season": season,
        "plant_type": plant_type,
        "general_care": season_info["general"],
        "specific_tasks": season_info["specific_tasks"],
        "type_specific_tips": type_specific_tips,
        "month_by_month": {
            "early": f"Early {season} care adjustments",
            "mid": f"Mid-{season} maintenance focus", 
            "late": f"Late {season} preparation for next season"
        }
    }


def monitor_plant_health(
    plant_name: str,
    current_condition: str,
    days_since_last_water: int,
    days_since_last_fertilizer: int
) -> dict[str, Any]:
    """Monitor and assess plant health based on care history and current condition.

    Args:
        plant_name: Name of the plant being monitored
        current_condition: Current condition (excellent, good, fair, poor, critical)
        days_since_last_water: Number of days since last watering
        days_since_last_fertilizer: Number of days since last fertilizing

    Returns:
        Dictionary containing health assessment and recommendations

    Raises:
        ValueError: If inputs are invalid
        TypeError: If inputs are wrong type
    """
    validate_plant_name(plant_name)
    validate_positive_number(days_since_last_water, "days_since_last_water")
    validate_positive_number(days_since_last_fertilizer, "days_since_last_fertilizer")
    
    valid_conditions = ["excellent", "good", "fair", "poor", "critical"]
    if not isinstance(current_condition, str):
        raise TypeError("Current condition must be a string")
    if current_condition.lower() not in valid_conditions:
        raise ValueError(f"Current condition must be one of {valid_conditions}")
    
    # Get plant information
    plant_info = get_plant_info(plant_name)
    plant_type = plant_info.get("type", "foliage")
    
    # Determine watering status
    typical_watering_days = {
        "succulent": 14,
        "cactus": 21,
        "tropical": 7,
        "fern": 5,
        "foliage": 7,
        "flowering": 7,
        "vine": 7,
        "tree": 10
    }
    
    expected_watering = typical_watering_days.get(plant_type, 7)
    watering_status = "overdue" if days_since_last_water > expected_watering else "on_schedule"
    
    # Determine fertilizing status
    fertilizer_status = "overdue" if days_since_last_fertilizer > 30 else "on_schedule"
    
    # Generate health assessment
    condition_scores = {
        "excellent": 5,
        "good": 4,
        "fair": 3,
        "poor": 2,
        "critical": 1
    }
    
    condition_score = condition_scores.get(current_condition.lower(), 3)
    
    # Calculate overall health score
    health_factors = {
        "condition": condition_score,
        "watering": 5 if watering_status == "on_schedule" else 2,
        "fertilizing": 5 if fertilizer_status == "on_schedule" else 3
    }
    
    overall_score = sum(health_factors.values()) / len(health_factors)
    
    if overall_score >= 4.5:
        health_status = "excellent"
    elif overall_score >= 3.5:
        health_status = "good"
    elif overall_score >= 2.5:
        health_status = "fair"
    elif overall_score >= 1.5:
        health_status = "poor"
    else:
        health_status = "critical"
    
    # Generate recommendations
    recommendations = []
    priority_actions = []
    
    if watering_status == "overdue":
        priority_actions.append(f"Water immediately - {days_since_last_water} days since last watering")
    
    if fertilizer_status == "overdue" and days_since_last_fertilizer > 60:
        recommendations.append("Consider light fertilizing during growing season")
    
    if current_condition.lower() in ["poor", "critical"]:
        priority_actions.append("Inspect plant thoroughly for pests, disease, or environmental stress")
        priority_actions.append("Consider isolating plant if condition is declining rapidly")
    
    if current_condition.lower() == "fair":
        recommendations.append("Monitor daily for changes and adjust care routine")
        recommendations.append("Check light, water, and humidity conditions")
    
    # Add plant-specific recommendations
    common_problems = plant_info.get("common_problems", [])
    if common_problems:
        recommendations.append(f"Watch for common {plant_name} problems: {', '.join(common_problems)}")
    
    return {
        "plant_name": plant_name,
        "health_assessment": {
            "overall_status": health_status,
            "condition_score": f"{overall_score:.1f}/5.0",
            "current_condition": current_condition,
            "care_status": {
                "watering": watering_status,
                "fertilizing": fertilizer_status
            }
        },
        "care_history": {
            "days_since_last_water": days_since_last_water,
            "days_since_last_fertilizer": days_since_last_fertilizer,
            "expected_watering_interval": f"every {expected_watering} days"
        },
        "priority_actions": priority_actions,
        "recommendations": recommendations,
        "next_steps": [
            "Continue monitoring daily if condition is poor",
            "Take photos to track changes over time",
            "Keep care log to identify patterns",
            "Adjust care routine based on plant response"
        ],
        "plant_info": {
            "type": plant_type,
            "care_difficulty": plant_info.get("care_difficulty", "varies"),
            "common_problems": common_problems
        }
    }