from fastmcp import FastMCP
import json
from datetime import datetime

# Create the MCP server instance
mcp = FastMCP("Tutorial MCP Server")


@mcp.tool()
def greet(name: str) -> str:
    """Greet a person by name."""
    return f"Hello, {name}! Welcome to FastMCP 2.0!"


@mcp.tool()
def add_numbers(a: int, b: int) -> int:
    """Add two numbers together."""
    return a + b


@mcp.tool()
def get_server_info() -> str:
    """Get information about this MCP server."""
    return "This is a tutorial MCP server built with FastMCP 2.0. It provides tools, resources, and prompts for demonstration purposes."


# RESOURCES
@mcp.resource("resource://server-status")
def get_server_status() -> dict:
    """Get current server status information."""
    return {
        "status": "running",
        "timestamp": datetime.now().isoformat(),
        "version": "2.5.1",
        "features": ["tools", "resources", "prompts"]
    }


@mcp.resource("resource://greeting")
def get_greeting_resource() -> str:
    """Get a friendly greeting message."""
    return "Hello from FastMCP Resources! This is a static resource that provides information."


@mcp.resource("config://{section}")
def get_config_section(section: str) -> dict:
    """Get configuration for a specific section."""
    configs = {
        "server": {
            "name": "Tutorial MCP Server",
            "version": "1.0.0",
            "max_connections": 100
        },
        "features": {
            "tools_enabled": True,
            "resources_enabled": True,
            "prompts_enabled": True
        },
        "logging": {
            "level": "INFO",
            "format": "json",
            "output": "stdout"
        }
    }
    return configs.get(section, {"error": f"Configuration section '{section}' not found"})


@mcp.resource("data://user/{user_id}/profile")
def get_user_profile(user_id: str) -> dict:
    """Get user profile data by user ID."""
    # Mock user data
    mock_users = {
        "123": {
            "id": "123",
            "name": "Alice Smith",
            "email": "alice@example.com",
            "role": "developer",
            "created_at": "2024-01-15T10:30:00Z"
        },
        "456": {
            "id": "456",
            "name": "Bob Johnson",
            "email": "bob@example.com",
            "role": "designer",
            "created_at": "2024-02-20T14:45:00Z"
        }
    }
    return mock_users.get(user_id, {"error": f"User {user_id} not found"})


# PROMPTS
@mcp.prompt()
def code_review_prompt(language: str, code: str) -> str:
    """Generate a code review prompt for the given language and code."""
    return f"""Please review this {language} code and provide feedback:

```{language}
{code}
```

Focus on:
- Code quality and best practices
- Potential bugs or issues
- Performance considerations
- Readability and maintainability
- Security concerns (if applicable)

Provide specific suggestions for improvement."""


@mcp.prompt()
def documentation_prompt(function_name: str, parameters: str, description: str = "") -> str:
    """Generate a documentation writing prompt."""
    base_prompt = f"""Write comprehensive documentation for the function '{function_name}' with parameters: {parameters}.

The documentation should include:
- A clear description of what the function does
- Parameter descriptions with types
- Return value description
- Usage examples
- Any important notes or warnings"""
    
    if description:
        base_prompt += f"\n\nAdditional context: {description}"
    
    return base_prompt


@mcp.prompt()
def explain_concept_prompt(concept: str, audience: str = "general") -> str:
    """Generate a prompt to explain a technical concept to a specific audience."""
    audience_instructions = {
        "beginner": "Use simple language, avoid jargon, and provide relatable analogies",
        "intermediate": "Use technical terms but explain them, provide examples",
        "expert": "Use precise technical language and focus on nuances",
        "general": "Use accessible language with some technical detail"
    }
    
    instruction = audience_instructions.get(audience, audience_instructions["general"])
    
    return f"""Explain the concept of '{concept}' to a {audience} audience.

Guidelines: {instruction}

Structure your explanation with:
1. A brief overview
2. Key components or aspects
3. Practical examples or use cases
4. Common misconceptions (if any)
5. Further learning resources"""


@mcp.prompt()
def debugging_assistant_prompt(error_message: str, context: str = "") -> str:
    """Generate a debugging assistance prompt."""
    prompt = f"""Help me debug this error:

Error Message:
{error_message}

Please provide:
1. Possible causes of this error
2. Step-by-step debugging approach
3. Common solutions
4. How to prevent this error in the future"""
    
    if context:
        prompt += f"\n\nAdditional Context:\n{context}"
    
    return prompt


if __name__ == "__main__":
    mcp.run()
