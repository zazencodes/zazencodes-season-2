# Travel Itinerary Generator

## Project Overview

A dark-mode web application that allows users to select locations on an interactive world map and generate personalized 3-day travel itineraries using AI. Built with vanilla HTML/CSS/JavaScript, Google Maps API, and Youware AI SDK.

## Architecture

### Core Components
- **Interactive Map**: Google Maps with dark theme styling and click-to-select functionality
- **AI Integration**: Youware AI SDK for intelligent itinerary generation with GPT-4o model
- **Location Services**: Google Geocoding API for address resolution and place details
- **Dark UI**: Custom CSS with dark color scheme optimized for travel planning

### Key Files
- `index.html`: Main application with embedded JavaScript and styling
- `yw_manifest.json`: AI configuration for travel planning model and system prompts
- Map integration uses Google Maps API key: `[GOOGLE_MAPS_API_KEY]`

### AI Configuration
The `travel_planner` scene in `yw_manifest.json` uses:
- Model: `openai-gpt-4o` for comprehensive travel knowledge
- Temperature: 0.7 for creative yet reliable suggestions
- Max tokens: 3000 for detailed 3-day itineraries
- Dynamic system prompt with interpolated variables (destination, travel style, budget)

### Map Implementation
- Dark-themed Google Maps with custom styling
- Click-to-select location functionality with visual markers
- Real-time geocoding for address resolution and place details
- Responsive design supporting both desktop and mobile

### User Flow
1. User clicks anywhere on the world map
2. Marker appears and location is geocoded to readable address
3. User selects travel preferences (style, interests, budget)
4. AI generates comprehensive 3-day itinerary with local insights
5. Results displayed with formatted headings and structured content

## Development Notes

### Required MCP Tools
- **Google Maps**: Essential for interactive mapping and geocoding services
- **AI SDK**: Required for intelligent itinerary generation

### Error Handling
- All AI-related errors include "API Error -" prefix for system monitoring
- Comprehensive logging for debugging map initialization and API calls
- User-friendly error messages with visual status indicators

### Performance Considerations
- Images and map tiles load asynchronously
- AI generation includes loading states and progress indicators
- Responsive grid layout adapts to mobile screens
