#!/usr/bin/env python3
"""
Example usage of the anime quote fetcher.
This demonstrates different ways to use the script programmatically.
"""

import subprocess
import sys
from pathlib import Path

def run_command(cmd):
    """Run a command and display the output."""
    print(f"\n🚀 Running: {' '.join(cmd)}")
    print("=" * 60)
    
    try:
        result = subprocess.run(cmd, capture_output=True, text=True, check=True)
        print(result.stdout)
        if result.stderr:
            print("STDERR:", result.stderr)
    except subprocess.CalledProcessError as e:
        print(f"Command failed with exit code {e.returncode}")
        print("STDOUT:", e.stdout)
        print("STDERR:", e.stderr)

def main():
    """Run example commands."""
    script_path = Path(__file__).parent / "anime_quotes.py"
    
    print("🎌 Anime Quote Fetcher - Example Usage")
    print("=" * 60)
    
    # Example 1: Fetch quotes for specific anime
    print("\n📝 Example 1: Fetch quotes for specific anime shows")
    run_command([
        sys.executable, str(script_path),
        "--anime", "One Punch Man", "Naruto"
    ])
    
    # Example 2: Use popular anime list
    print("\n📝 Example 2: Fetch quotes for popular anime")
    run_command([
        sys.executable, str(script_path),
        "--popular", "--output-only"
    ])
    
    # Example 3: Use JSON file input
    json_file = Path(__file__).parent / "example_anime_list.json"
    if json_file.exists():
        print("\n📝 Example 3: Fetch quotes from JSON file")
        run_command([
            sys.executable, str(script_path),
            "--file", str(json_file), "--no-save"
        ])

if __name__ == "__main__":
    main()