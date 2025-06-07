# FastMCP Tutorial Server

A tutorial MCP (Model Context Protocol) server built with FastMCP 2.0, providing example tools for demonstration purposes.

## Features

### 🔧 Tools
- **Greet Tool**: Greets users by name
- **Add Numbers Tool**: Performs basic arithmetic addition
- **Server Info Tool**: Provides information about the server

### 📚 Resources
- **Server Status**: Real-time server status and configuration (`resource://server-status`)
- **Greeting Resource**: Static greeting message (`resource://greeting`)
- **Config Sections**: Parameterized configuration data (`config://{section}`)
- **User Profiles**: Mock user profile data (`data://user/{user_id}/profile`)

### 💬 Prompts
- **Code Review Prompt**: Generates code review prompts for different languages
- **Documentation Prompt**: Creates documentation writing prompts for functions
- **Explain Concept Prompt**: Generates explanation prompts for different audiences
- **Debugging Assistant Prompt**: Creates debugging assistance prompts

## Installation

### Option 1: Install from PyPI (Recommended)

> #### THIS WILL NOT WORK.
>
> Use option 2 instead.
>
> This section is for demonstration purposes only. i.e. It's how you would want
> to write your README if you actually published the server to PyPI.

The easiest way to install and use this MCP server:

#### Prerequisites
- **Python 3.12 or higher** - Download from [python.org](https://www.python.org/downloads/)
- **Claude Desktop** - Download from [claude.ai/download](https://claude.ai/download)

#### Install the Package

> The code below will not work. I have not actually deployed this to PyPi.
> You can clone the repo and run it with uv to test it out!

```bash
# Install with pip
pip install fastmcp-tutorial

# Or with pipx (recommended for CLI tools)
pipx install fastmcp-tutorial
```

#### Test the Installation

```bash
# Test the server
fastmcp-tutorial-test

# Start the server
fastmcp-tutorial
```

### Option 2: Install from Source

For development or customization:

#### Prerequisites

1. **Python 3.12 or higher**
   - Download from [python.org](https://www.python.org/downloads/)
   - Verify installation: `python --version` or `python3 --version`

2. **uv package manager** (optional but recommended)
   - Install with: `curl -LsSf https://astral.sh/uv/install.sh | sh` (macOS/Linux)
   - Or: `powershell -ExecutionPolicy ByPass -c "irm https://astral.sh/uv/install.ps1 | iex"` (Windows)
   - More options: [uv installation guide](https://docs.astral.sh/uv/getting-started/installation/)
   - Verify installation: `uv --version`

3. **Git** (for cloning)
   - Download from [git-scm.com](https://git-scm.com/downloads)
   - Or download ZIP directly from GitHub (no Git required)

#### Setup from Source

1. **Clone the repository:**
   ```bash
   git clone <repository-url>
   cd fastmcp-tutorial
   ```

2. **Install dependencies:**
   ```bash
   # With uv (recommended)
   uv sync

   # Or with pip
   pip install -e .
   ```

3. **Test the installation:**
   ```bash
   # With uv
   uv run fastmcp-tutorial-test

   # Or direct
   fastmcp-tutorial-test
   ```

## Usage

### Running the Server

#### From PyPI Installation
```bash
# Start the server
fastmcp-tutorial

# Test the server
fastmcp-tutorial-test
```

#### From Source Installation
```bash
# With uv
uv run fastmcp-tutorial

# Or direct
fastmcp-tutorial
```

### Testing the Server

```bash
# Test all functionality
fastmcp-tutorial-test
```

## Connecting to Claude Desktop

To use this MCP server with Claude Desktop, follow these steps:

### 1. Install Claude Desktop

Download and install Claude Desktop from [Anthropic's website](https://claude.ai/download).

### 2. Configure the MCP Server

1. Open Claude Desktop
2. Go to Claude menu ? Settings ? Developer
3. Click "Edit Config" to open the configuration file

### 3. Add Server Configuration

#### For PyPI Installation (Recommended)

Add the following configuration to your `claude_desktop_config.json`:

```json
{
  "mcpServers": {
    "fastmcp-tutorial": {
      "command": "fastmcp-tutorial"
    }
  }
}
```

#### For Source Installation

Add the following configuration to your `claude_desktop_config.json`:

```json
{
  "mcpServers": {
    "fastmcp-tutorial": {
      "command": "uv",
      "args": [
        "run",
        "fastmcp-tutorial"
      ],
      "cwd": "/absolute/path/to/fastmcp-tutorial"
    }
  }
}
```

**Important**: Replace `/absolute/path/to/fastmcp-tutorial` with the actual absolute path to where you cloned/downloaded this project.

### 4. Restart Claude Desktop

After saving the configuration file, restart Claude Desktop completely.

### 5. Verify Connection

Once restarted, you should see:
- A = connector icon in the bottom left of the input box
- A =( hammer icon indicating available tools

Click the connector icon to see your connected MCP servers and available tools.

## Configuration File Locations

The Claude Desktop configuration file is located at:

- **macOS**: `~/Library/Application Support/Claude/claude_desktop_config.json`
- **Windows**: `%APPDATA%\\Claude\\claude_desktop_config.json`

## Troubleshooting

### Server Not Appearing in Claude Desktop

1. **Check the configuration file**: Ensure the JSON syntax is valid and the path is correct
2. **Verify the path**: Make sure the `cwd` path points to the actual project directory
3. **Check logs**: Enable Developer Mode in Claude Desktop and check the MCP logs:
   - **macOS**: `~/Library/Logs/Claude/mcp.log`
   - **Windows**: `%APPDATA%\\Claude\\Logs\\mcp.log`

### Testing Server Manually

You can test if the server works by running it manually:
```bash
cd /path/to/fastmcp-tutorial
uv run python main.py
```

### Finding Your Absolute Path

If you're not sure of the absolute path to your project:

**macOS/Linux:**
```bash
cd fastmcp-tutorial
pwd
```

**Windows Command Prompt:**
```cmd
cd fastmcp-tutorial
cd
```

**Windows PowerShell:**
```powershell
cd fastmcp-tutorial
Get-Location
```

Copy the output and use it as your `cwd` value in the configuration.

### Common Issues

#### Installation Problems
- **Python not found**: Make sure Python 3.12+ is installed and in your PATH
- **uv not found**: Restart your terminal after installing uv, or add it to your PATH manually
- **Permission errors**: On Windows, try running commands as Administrator

#### Claude Desktop Connection Issues
- **Path not found**: Ensure you're using absolute paths, not relative paths
- **Server not starting**: Check that all dependencies are installed with `uv run python test_server.py`
- **JSON syntax errors**: Validate your configuration file with a JSON validator
- **Permission errors**: Ensure Claude Desktop has permission to access the project directory

#### Getting Help
- Check the MCP logs in Claude Desktop (Developer → View Logs)
- Test the server manually: `uv run python test_server.py`
- Verify your configuration path is correct

## Development

### Project Structure

```
fastmcp-tutorial/
    main.py              # Main MCP server implementation
    test_server.py       # Test script for server functionality
    pyproject.toml       # Project dependencies
    uv.lock             # Dependency lock file
    README.md           # This file
```

### Adding New Features

#### Adding Tools
Add functions with the `@mcp.tool()` decorator in `src/fastmcp_tutorial/server.py` (or `main.py` for source installs):

```python
@mcp.tool()
def your_new_tool(param: str) -> str:
    """Description of what your tool does."""
    return f"Result: {param}"
```

#### Adding Resources
Add functions with the `@mcp.resource()` decorator:

```python
@mcp.resource("custom://your-resource")
def your_resource() -> dict:
    """Your resource description."""
    return {"data": "your resource data"}

# Parameterized resources
@mcp.resource("api://{endpoint}")
def api_resource(endpoint: str) -> dict:
    """Access different API endpoints."""
    return {"endpoint": endpoint, "data": "mock data"}
```

#### Adding Prompts
Add functions with the `@mcp.prompt()` decorator:

```python
@mcp.prompt()
def your_prompt(topic: str, style: str = "formal") -> str:
    """Generate a prompt for the given topic."""
    return f"Write about {topic} in a {style} style."
```

## Example Usage in Claude Desktop

Once connected to Claude Desktop, you can:

### Use Tools
- "Please greet John" → Uses the greet tool
- "Add 15 and 27" → Uses the add_numbers tool
- "What's the server info?" → Uses get_server_info tool

### Access Resources
- Resources appear as available data sources
- Access server status with `resource://server-status`
- Get user profiles with `data://user/123/profile`
- Retrieve config sections with `config://server`

### Generate Prompts
- Request code review prompts for specific languages
- Generate documentation templates
- Create explanation prompts for different audiences
- Get debugging assistance prompts

## Server Statistics

The extended server now provides:
- **3 Tools**: Interactive functionality
- **4 Resources**: Static and dynamic data access
- **4 Prompts**: Template generators for various use cases

## Package Information

This package is available on PyPI as `fastmcp-tutorial`:
- **PyPI**: [https://pypi.org/project/fastmcp-tutorial/](https://pypi.org/project/fastmcp-tutorial/)
- **Source**: [GitHub Repository](https://github.com/yourusername/fastmcp-tutorial)

### CLI Commands

After installation, you get these commands:
- `fastmcp-tutorial`: Start the MCP server
- `fastmcp-tutorial-test`: Run comprehensive tests

### Resources

- [FastMCP Documentation](https://gofastmcp.com/)
- [FastMCP Resources Guide](https://gofastmcp.com/servers/resources.md)
- [FastMCP Prompts Guide](https://gofastmcp.com/servers/prompts.md)
- [Model Context Protocol Specification](https://modelcontextprotocol.io/)
- [Claude Desktop MCP Guide](https://modelcontextprotocol.io/quickstart/user)
