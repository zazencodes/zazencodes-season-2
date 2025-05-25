"""Test module for FastMCP Tutorial Server."""

import asyncio
import json
from fastmcp import Client
from .server import mcp


async def test_server():
    """Test the MCP server functionality including tools, resources, and prompts."""
    client = Client(mcp)
    
    async with client:
        print("=" * 60)
        print("TESTING FASTMCP TUTORIAL SERVER")
        print("=" * 60)
        
        # Test Tools
        print("\n🔧 TESTING TOOLS:")
        print("-" * 20)
        
        # Test greet tool
        result = await client.call_tool("greet", {"name": "World"})
        print(f"✓ Greet tool: {result}")
        
        # Test add_numbers tool
        result = await client.call_tool("add_numbers", {"a": 5, "b": 3})
        print(f"✓ Add numbers tool: {result}")
        
        # Test get_server_info tool
        result = await client.call_tool("get_server_info", {})
        print(f"✓ Server info tool: {result}")
        
        # Test Resources
        print("\n📚 TESTING RESOURCES:")
        print("-" * 20)
        
        # Test server status resource
        try:
            result = await client.read_resource("resource://server-status")
            print(f"✓ Server status resource: {result}")
        except Exception as e:
            print(f"✗ Server status resource error: {e}")
        
        # Test greeting resource
        try:
            result = await client.read_resource("resource://greeting")
            print(f"✓ Greeting resource: {result}")
        except Exception as e:
            print(f"✗ Greeting resource error: {e}")
        
        # Test config section resource (parameterized)
        try:
            result = await client.read_resource("config://server")
            print(f"✓ Config server resource: {result}")
        except Exception as e:
            print(f"✗ Config server resource error: {e}")
        
        try:
            result = await client.read_resource("config://features")
            print(f"✓ Config features resource: {result}")
        except Exception as e:
            print(f"✗ Config features resource error: {e}")
        
        # Test user profile resource (parameterized)
        try:
            result = await client.read_resource("data://user/123/profile")
            print(f"✓ User profile resource: {result}")
        except Exception as e:
            print(f"✗ User profile resource error: {e}")
        
        # Test Prompts
        print("\n💬 TESTING PROMPTS:")
        print("-" * 20)
        
        # Test code review prompt
        try:
            result = await client.get_prompt("code_review_prompt", {
                "language": "python",
                "code": "def hello():\n    print('Hello World')"
            })
            print(f"✓ Code review prompt: {result}")
        except Exception as e:
            print(f"✗ Code review prompt error: {e}")
        
        # Test documentation prompt
        try:
            result = await client.get_prompt("documentation_prompt", {
                "function_name": "calculate_area",
                "parameters": "radius: float",
                "description": "Calculates the area of a circle"
            })
            print(f"✓ Documentation prompt: {result}")
        except Exception as e:
            print(f"✗ Documentation prompt error: {e}")
        
        # Test explain concept prompt
        try:
            result = await client.get_prompt("explain_concept_prompt", {
                "concept": "machine learning",
                "audience": "beginner"
            })
            print(f"✓ Explain concept prompt: {result}")
        except Exception as e:
            print(f"✗ Explain concept prompt error: {e}")
        
        # Test debugging assistant prompt
        try:
            result = await client.get_prompt("debugging_assistant_prompt", {
                "error_message": "AttributeError: 'NoneType' object has no attribute 'strip'",
                "context": "Processing user input in a web form"
            })
            print(f"✓ Debugging assistant prompt: {result}")
        except Exception as e:
            print(f"✗ Debugging assistant prompt error: {e}")
        
        print("\n" + "=" * 60)
        print("✅ ALL TESTS COMPLETED!")
        print("=" * 60)


def run_tests():
    """CLI entry point for running tests."""
    asyncio.run(test_server())


if __name__ == "__main__":
    run_tests()