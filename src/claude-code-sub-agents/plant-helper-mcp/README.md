# Plant Helper MCP

Comprehensive plant care assistant utilities exposed via Model Context Protocol, helping plant owners provide optimal care through intelligent recommendations, problem diagnosis, and health monitoring.

## 🌱 Tools

| Tool                          | Purpose                                         | Key Features                              |
| ----------------------------- | ----------------------------------------------- | ----------------------------------------- |
| `get_plant_info`             | Get comprehensive plant care information       | Care guides for 8+ common houseplants    |
| `calculate_watering_schedule` | Calculate personalized watering schedules      | Environment-based recommendations         |
| `get_light_recommendations`   | Get detailed light requirement guidance        | Placement tips and problem identification |
| `diagnose_plant_problem`      | Diagnose issues and provide treatment solutions| 9+ problem categories with solutions     |
| `get_seasonal_care_tips`      | Get season-specific care adjustments          | Monthly care guidance and plant types    |
| `monitor_plant_health`        | Assess plant health and track care history    | Health scoring and priority actions      |

## 🔧 Setup

### Claude Desktop

Add this to your Claude Desktop configuration file:

**macOS**: `~/Library/Application Support/Claude/claude_desktop_config.json`   
**Windows**: `%APPDATA%/Claude/claude_desktop_config.json`

```json
{
  "mcpServers": {
    "plant-helper": {
      "command": "uvx",
      "args": ["plant-helper-mcp"]
    }
  }
}
```

## 📋 Tool Reference

### `get_plant_info`

Get comprehensive care information for a specific plant from our database of common houseplants.

**Parameters:**
- `plant_name` (str): Name of the plant to get information for

**Supported Plants:**
- Snake Plant, Pothos, Monstera, Spider Plant, Rubber Plant, Peace Lily, Aloe Vera, ZZ Plant

**Example:**
```json
{
  "name": "get_plant_info",
  "arguments": {
    "plant_name": "snake plant"
  }
}
```

**Returns:**
- Scientific name and plant type
- Light, watering, and humidity requirements
- Temperature and soil preferences
- Fertilizer schedule and common problems
- Care difficulty, pet safety, and growth characteristics

### `calculate_watering_schedule`

Calculate a personalized watering schedule based on plant type, season, and environmental conditions.

**Parameters:**
- `plant_name` (str): Name of the plant
- `current_season` (str): Current season (spring, summer, fall, autumn, winter)
- `humidity_level` (float): Current humidity percentage (0-100)
- `temperature` (float): Current temperature in Fahrenheit

**Example:**
```json
{
  "name": "calculate_watering_schedule",
  "arguments": {
    "plant_name": "monstera",
    "current_season": "summer",
    "humidity_level": 45.0,
    "temperature": 78.0
  }
}
```

**Returns:**
- Calculated watering frequency in days
- Environmental condition adjustments
- Season-specific recommendations
- Plant-type specific watering tips

### `get_light_recommendations`

Get detailed recommendations for plants requiring specific light levels.

**Parameters:**
- `light_level` (str): Required light level (low, medium, bright, direct)

**Example:**
```json
{
  "name": "get_light_recommendations",
  "arguments": {
    "light_level": "bright"
  }
}
```

**Returns:**
- Detailed light requirements and suitable locations
- Hours per day and distance from windows
- Signs of inadequate or excessive light
- Practical placement and care tips

### `diagnose_plant_problem`

Diagnose plant problems and provide comprehensive treatment solutions based on symptoms.

**Parameters:**
- `plant_name` (str): Name of the plant with problems
- `symptoms` (list[str]): List of observed symptoms
- `problem_type` (str): Type of problem (yellowing, browning, wilting, pests, fungal, overwatering, underwatering, nutrient_deficiency, light_stress, other)

**Supported Problem Types:**
- `yellowing` - Yellow leaves (overwatering, aging, nutrients)
- `browning` - Brown leaves/tips (humidity, water quality, sun burn)
- `wilting` - Drooping plants (watering issues, root problems)
- `pests` - Insect infestations (spider mites, aphids, scale)
- `fungal` - Fungal infections (humidity, air circulation)
- `overwatering` - Too much water (drainage, frequency)
- `underwatering` - Not enough water (scheduling, root bound)
- `nutrient_deficiency` - Lack of nutrients (fertilizer, soil)
- `light_stress` - Light-related problems (too much/little light)
- `other` - General problems and stress

**Example:**
```json
{
  "name": "diagnose_plant_problem",
  "arguments": {
    "plant_name": "pothos",
    "symptoms": ["yellow leaves", "soft stems", "musty smell"],
    "problem_type": "overwatering"
  }
}
```

**Returns:**
- Detailed diagnosis with common causes
- Step-by-step treatment solutions
- Prevention strategies for future care
- Urgency level and follow-up recommendations

### `get_seasonal_care_tips`

Get season-specific care tips and adjustments for optimal plant health throughout the year.

**Parameters:**
- `season` (str): Current season (spring, summer, fall, autumn, winter)
- `plant_type` (str, optional): Type of plant for specific advice (defaults to "general")

**Supported Plant Types:**
- `general` - Universal seasonal care tips
- `succulent` - Drought-tolerant plants (aloe, snake plant)
- `tropical` - High-humidity plants (monstera, pothos)
- `flowering` - Blooming plants (peace lily, orchids)

**Example:**
```json
{
  "name": "get_seasonal_care_tips",
  "arguments": {
    "season": "winter",
    "plant_type": "tropical"
  }
}
```

**Returns:**
- General seasonal care adjustments
- Specific tasks for the season
- Plant-type specific recommendations
- Month-by-month care guidance

### `monitor_plant_health`

Monitor and assess plant health based on care history and current condition to provide actionable recommendations.

**Parameters:**
- `plant_name` (str): Name of the plant being monitored
- `current_condition` (str): Current condition (excellent, good, fair, poor, critical)
- `days_since_last_water` (int): Number of days since last watering
- `days_since_last_fertilizer` (int): Number of days since last fertilizing

**Example:**
```json
{
  "name": "monitor_plant_health",
  "arguments": {
    "plant_name": "rubber plant",
    "current_condition": "fair",
    "days_since_last_water": 5,
    "days_since_last_fertilizer": 45
  }
}
```

**Returns:**
- Overall health assessment with scoring
- Care status evaluation (watering, fertilizing)
- Priority actions requiring immediate attention
- Recommendations for improvement
- Plant-specific care guidance

## 🌿 Plant Database

Our comprehensive database includes detailed care information for:

### Easy Care Plants
- **Snake Plant** - Extremely drought tolerant, low light
- **ZZ Plant** - Very forgiving, low maintenance
- **Pothos** - Fast growing, adaptable vine
- **Spider Plant** - Pet safe, produces plantlets

### Moderate Care Plants  
- **Monstera** - Popular tropical, needs support
- **Rubber Plant** - Tree-like growth, glossy leaves
- **Peace Lily** - Flowering plant, humidity loving

### Specialty Plants
- **Aloe Vera** - Medicinal succulent, bright light

Each plant entry includes:
- Scientific name and classification
- Detailed care requirements (light, water, humidity, temperature)
- Soil and fertilizer preferences
- Common problems and solutions
- Pet safety information
- Growth characteristics and mature size

## 🔍 Problem Diagnosis System

Our intelligent diagnosis system covers:

### Leaf Problems
- **Yellowing** - Most common issue, usually overwatering
- **Browning** - Often humidity or water quality related
- **Wilting** - Watering schedule or root health issues

### Environmental Issues
- **Light Stress** - Too much or too little light exposure
- **Nutrient Deficiency** - Fertilizer and soil-related problems

### Biological Problems  
- **Pests** - Spider mites, aphids, scale, mealybugs
- **Fungal** - Mold, mildew, root rot issues

### Care-Related Issues
- **Overwatering** - Most common cause of plant death
- **Underwatering** - Neglect and scheduling problems

Each diagnosis includes:
- Common causes and identification
- Step-by-step treatment solutions
- Prevention strategies
- Urgency assessment
- Follow-up care recommendations

## 📅 Seasonal Care System

### Spring (Growing Season Begins)
- Increase watering and begin fertilizing
- Best time for repotting and propagation
- Pruning and cleaning tasks
- Pest prevention measures

### Summer (Peak Growing Season)
- Maximum watering and fertilizer needs
- Heat and humidity management
- Light protection from intense sun
- Outdoor transition planning

### Fall/Autumn (Transition to Dormancy)
- Gradually reduce watering and fertilizing
- Prepare for reduced light conditions
- Bring outdoor plants inside
- Pest inspection before indoor transition

### Winter (Dormant Season)
- Minimal watering and no fertilizing
- Maximize available light
- Humidity management with heating systems
- Temperature protection measures

## 🛠️ Development

### Prerequisites

- Python 3.10+
- [uv](https://docs.astral.sh/uv/) package manager

### Setup

```bash
# Clone the repository
git clone https://github.com/example/plant-helper-mcp
cd plant-helper-mcp

# Install dependencies
uv sync --dev

# Run tests
uv run pytest

# Run linting
uv run ruff check --fix
uv run ruff format

# Type checking
uv run mypy src/
```

### MCP Client Config

```json
{
  "mcpServers": {
    "plant-helper-dev": {
      "command": "uv",
      "args": [
        "--directory",
        "<path_to_your_repo>/plant-helper-mcp",
        "run",
        "plant-helper-mcp"
      ]
    }
  }
}
```

**Note:** Replace `<path_to_your_repo>/plant-helper-mcp` with the absolute path to your cloned repository.

### Building

```bash
# Build package
uv build

# Test installation
uv run --with dist/*.whl plant-helper-mcp
```

### Release Checklist

1. **Update Version:**
   - Increment the `version` number in `pyproject.toml` and `src/__init__.py`.

2. **Update Changelog:**
   - Add a new entry in `CHANGELOG.md` for the release.
   - Draft notes with coding agent using `git diff` context.

   ```
   Update the @CHANGELOG.md for the latest release.
   List all significant changes, bug fixes, and new features.
   Here's the git diff:
   [GIT_DIFF]
   ```
   
   - Commit along with any other pending changes.

3. **Create GitHub Release:**
   - Draft a new release on the GitHub UI.
   - Tag release using UI.
   - The GitHub workflow will automatically build and publish the package to PyPI.

## Testing with MCP Inspector

For exploring and/or developing this server, use the MCP Inspector npm utility:

```bash
# Install MCP Inspector
npm install -g @modelcontextprotocol/inspector

# Run local development server with the inspector
npx @modelcontextprotocol/inspector uv run plant-helper-mcp

# Run PyPI production server with the inspector
npx @modelcontextprotocol/inspector uvx plant-helper-mcp
```

## 🌿 Usage Examples

### Getting Plant Information
```json
{
  "name": "get_plant_info",
  "arguments": {
    "plant_name": "monstera"
  }
}
```

### Creating a Watering Schedule
```json
{
  "name": "calculate_watering_schedule", 
  "arguments": {
    "plant_name": "snake plant",
    "current_season": "winter",
    "humidity_level": 35.0,
    "temperature": 68.0
  }
}
```

### Diagnosing Plant Problems
```json
{
  "name": "diagnose_plant_problem",
  "arguments": {
    "plant_name": "peace lily",
    "symptoms": ["brown leaf tips", "drooping leaves"], 
    "problem_type": "browning"
  }
}
```

### Monitoring Plant Health
```json
{
  "name": "monitor_plant_health",
  "arguments": {
    "plant_name": "pothos",
    "current_condition": "good",
    "days_since_last_water": 3,
    "days_since_last_fertilizer": 20
  }
}
```

## 📝 License

MIT License - see [LICENSE](LICENSE) file for details.

## 🤝 Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

Areas for contribution:
- Additional plants in the database
- More problem diagnosis categories
- Seasonal care improvements
- Regional climate adjustments
- Integration with plant identification APIs

## 📚 Links

- [Model Context Protocol](https://modelcontextprotocol.io/)
- [FastMCP Documentation](https://github.com/jlowin/fastmcp)
- [Plant Care Resources](https://www.houseplantjournal.com/)
- [Plant Problem Identification](https://www.extension.iastate.edu/plantpath/)