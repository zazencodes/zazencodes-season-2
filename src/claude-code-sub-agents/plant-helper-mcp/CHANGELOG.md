# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [Unreleased]

## [0.1.0] - 2025-07-27

### Added
- Initial release of plant-helper-mcp
- FastMCP v2.0 server implementation
- Six comprehensive plant care tools:
  - `get_plant_info` - Detailed care information for 8+ common houseplants
  - `calculate_watering_schedule` - Environment-based watering recommendations
  - `get_light_recommendations` - Light requirement guidance and placement tips
  - `diagnose_plant_problem` - Problem diagnosis with 9+ categories and solutions
  - `get_seasonal_care_tips` - Season-specific care adjustments and plant types
  - `monitor_plant_health` - Health assessment and care history tracking
- Comprehensive plant database with detailed care information
- Intelligent problem diagnosis system covering leaf, environmental, and biological issues
- Seasonal care guidance with month-by-month recommendations
- Environmental condition calculations for watering frequency
- Input validation and comprehensive error handling
- Type hints throughout the codebase
- Complete project structure with pyproject.toml
- Comprehensive documentation and usage examples
- PyPI packaging with uv build system
- MIT License

### Features
- JSON-RPC 2.0 transport over STDIO
- Support for Python 3.10+
- Plant database covering easy to moderate care houseplants
- Environmental factor integration (humidity, temperature, season)
- Problem diagnosis with urgency assessment
- Health monitoring with scoring system
- Extensible architecture for adding new plants and problems
- Full MCP protocol compliance

### Plant Database
- Snake Plant (Sansevieria trifasciata) - Easy care, low light
- Pothos (Epipremnum aureum) - Fast growing vine
- Monstera (Monstera deliciosa) - Popular tropical plant
- Spider Plant (Chlorophytum comosum) - Pet safe, prolific
- Rubber Plant (Ficus elastica) - Tree-like houseplant
- Peace Lily (Spathiphyllum wallisii) - Flowering plant
- Aloe Vera (Aloe barbadensis miller) - Medicinal succulent
- ZZ Plant (Zamioculcas zamiifolia) - Low maintenance

### Problem Categories
- Yellowing leaves (overwatering, aging, nutrients)
- Browning leaves/tips (humidity, water quality)
- Wilting (watering issues, root problems)
- Pest infestations (spider mites, aphids, scale)
- Fungal infections (humidity, air circulation)
- Overwatering (most common plant killer)
- Underwatering (scheduling and care neglect)
- Nutrient deficiency (fertilizer and soil issues)
- Light stress (too much or too little light)

### Developer Experience
- Modern Python packaging with pyproject.toml
- Code quality tools (ruff, mypy)
- Comprehensive input validation
- Detailed error messages and type safety
- Developer documentation with setup instructions
- MCP Inspector integration for testing