#!/usr/bin/env python3
"""
Anime Quote Fetcher

A script to fetch anime quotes from the animechan.io API.
Supports fetching quotes for specific anime shows with proper error handling,
rate limiting, and formatted output.
"""

import argparse
import json
import os
import sys
import time
from datetime import datetime
from pathlib import Path
from typing import Dict, List, Optional
from urllib.parse import quote

import requests


class AnimeQuoteFetcher:
    """Client for fetching anime quotes from animechan.io API."""
    
    BASE_URL = "https://api.animechan.io/v1"
    
    def __init__(self, rate_limit: float = 1.0):
        """
        Initialize the quote fetcher.
        
        Args:
            rate_limit: Delay in seconds between API requests
        """
        self.rate_limit = rate_limit
        self.session = requests.Session()
        self.session.headers.update({
            'User-Agent': 'Anime-Quote-Fetcher/1.0'
        })
    
    def fetch_quotes(self, anime_name: str) -> Dict:
        """
        Fetch quotes for a specific anime.
        
        Args:
            anime_name: Name of the anime to fetch quotes for
            
        Returns:
            Dict containing the API response
            
        Raises:
            requests.RequestException: If the API request fails
        """
        # URL encode the anime name to handle spaces and special characters
        encoded_name = quote(anime_name)
        url = f"{self.BASE_URL}/quotes?anime={encoded_name}"
        
        try:
            response = self.session.get(url, timeout=10)
            response.raise_for_status()
            
            # Rate limiting
            time.sleep(self.rate_limit)
            
            return response.json()
            
        except requests.exceptions.RequestException as e:
            raise requests.RequestException(f"Failed to fetch quotes for '{anime_name}': {e}")
    
    def fetch_multiple_anime(self, anime_list: List[str]) -> Dict[str, Dict]:
        """
        Fetch quotes for multiple anime shows.
        
        Args:
            anime_list: List of anime names
            
        Returns:
            Dict mapping anime names to their quote data
        """
        results = {}
        
        for anime_name in anime_list:
            print(f"Fetching quotes for: {anime_name}")
            try:
                quotes_data = self.fetch_quotes(anime_name)
                results[anime_name] = quotes_data
                print(f"  ✓ Found {len(quotes_data.get('data', []))} quotes")
            except requests.RequestException as e:
                print(f"  ✗ Error: {e}")
                results[anime_name] = {"error": str(e)}
        
        return results


class QuoteFormatter:
    """Formats anime quotes for display and output."""
    
    @staticmethod
    def format_quote_display(quote_data: Dict) -> str:
        """
        Format a single quote for console display.
        
        Args:
            quote_data: Dictionary containing quote information
            
        Returns:
            Formatted string for display
        """
        character = quote_data.get('character', {}).get('name', 'Unknown')
        anime = quote_data.get('anime', {}).get('name', 'Unknown')
        quote_text = quote_data.get('content', 'No quote available')
        
        return f"""
╭─ {anime} ─╮
│ Character: {character}
│ Quote: "{quote_text}"
╰─{'─' * (len(anime) + 2)}─╯
"""
    
    @staticmethod
    def format_all_quotes(results: Dict[str, Dict]) -> str:
        """
        Format all quotes for display.
        
        Args:
            results: Dictionary mapping anime names to quote data
            
        Returns:
            Formatted string containing all quotes
        """
        output = []
        
        for anime_name, data in results.items():
            if "error" in data:
                output.append(f"\n❌ {anime_name}: {data['error']}")
                continue
            
            quotes = data.get('data', [])
            if not quotes:
                output.append(f"\n❌ {anime_name}: No quotes found")
                continue
            
            output.append(f"\n🎌 {anime_name.upper()} ({len(quotes)} quotes)")
            output.append("=" * 50)
            
            for quote in quotes:
                output.append(QuoteFormatter.format_quote_display(quote))
        
        return "\n".join(output)


class OutputManager:
    """Manages output files and directories."""
    
    def __init__(self, base_dir: str = "results"):
        """
        Initialize output manager.
        
        Args:
            base_dir: Base directory for output files
        """
        self.base_dir = Path(base_dir)
        self.base_dir.mkdir(exist_ok=True)
    
    def save_results(self, results: Dict, anime_list: List[str]) -> str:
        """
        Save results to a JSON file with date-based filename.
        
        Args:
            results: Dictionary containing all fetched data
            anime_list: List of anime names that were requested
            
        Returns:
            Path to the saved file
        """
        date_slug = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
        filename = f"{date_slug}_anime_quotes.json"
        filepath = self.base_dir / filename
        
        output_data = {
            "timestamp": datetime.now().isoformat(),
            "requested_anime": anime_list,
            "results": results,
            "summary": {
                "total_anime_requested": len(anime_list),
                "successful_fetches": len([r for r in results.values() if "error" not in r]),
                "failed_fetches": len([r for r in results.values() if "error" in r]),
                "total_quotes": sum(len(r.get("data", [])) for r in results.values() if "error" not in r)
            }
        }
        
        with open(filepath, 'w', encoding='utf-8') as f:
            json.dump(output_data, f, indent=2, ensure_ascii=False)
        
        return str(filepath)


def load_anime_list_from_file(filepath: str) -> List[str]:
    """
    Load anime list from a JSON file.
    
    Args:
        filepath: Path to JSON file containing anime list
        
    Returns:
        List of anime names
    """
    try:
        with open(filepath, 'r', encoding='utf-8') as f:
            data = json.load(f)
            
        # Handle different JSON structures
        if isinstance(data, list):
            return data
        elif isinstance(data, dict) and 'anime' in data:
            return data['anime']
        elif isinstance(data, dict) and 'anime_list' in data:
            return data['anime_list']
        else:
            raise ValueError("JSON file must contain a list or dict with 'anime' or 'anime_list' key")
            
    except (json.JSONDecodeError, FileNotFoundError, ValueError) as e:
        print(f"Error loading anime list from file: {e}")
        sys.exit(1)


def get_popular_anime_list() -> List[str]:
    """Return a list of popular anime shows."""
    return [
        "One Punch Man",
        "Naruto",
        "Attack on Titan",
        "Death Note",
        "Demon Slayer",
        "My Hero Academia",
        "Dragon Ball Z",
        "One Piece",
        "Fullmetal Alchemist",
        "Tokyo Ghoul",
        "Hunter x Hunter",
        "Cowboy Bebop"
    ]


def main():
    """Main function to run the anime quote fetcher."""
    parser = argparse.ArgumentParser(
        description="Fetch anime quotes from animechan.io API",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  %(prog)s --anime "One Punch Man" "Naruto"
  %(prog)s --file anime_list.json
  %(prog)s --popular
  %(prog)s --anime "Attack on Titan" --output-only
        """
    )
    
    # Input options (mutually exclusive)
    input_group = parser.add_mutually_exclusive_group(required=True)
    input_group.add_argument(
        '--anime', '-a',
        nargs='+',
        help='Anime names to fetch quotes for (space-separated)'
    )
    input_group.add_argument(
        '--file', '-f',
        help='JSON file containing list of anime names'
    )
    input_group.add_argument(
        '--popular', '-p',
        action='store_true',
        help='Fetch quotes for popular anime shows'
    )
    
    # Output options
    parser.add_argument(
        '--output-only', '-o',
        action='store_true',
        help='Only save to file, don\'t display quotes in console'
    )
    parser.add_argument(
        '--no-save',
        action='store_true',
        help='Don\'t save results to file, only display in console'
    )
    parser.add_argument(
        '--rate-limit', '-r',
        type=float,
        default=1.0,
        help='Delay between API requests in seconds (default: 1.0)'
    )
    
    args = parser.parse_args()
    
    # Determine anime list based on input option
    if args.anime:
        anime_list = args.anime
    elif args.file:
        anime_list = load_anime_list_from_file(args.file)
    elif args.popular:
        anime_list = get_popular_anime_list()
    else:
        # This shouldn't happen due to mutually exclusive group
        parser.error("No input method specified")
    
    print(f"Starting anime quote fetcher for {len(anime_list)} anime shows...")
    print("=" * 60)
    
    # Initialize components
    fetcher = AnimeQuoteFetcher(rate_limit=args.rate_limit)
    output_manager = OutputManager()
    
    try:
        # Fetch quotes
        results = fetcher.fetch_multiple_anime(anime_list)
        
        # Display results
        if not args.output_only:
            formatted_output = QuoteFormatter.format_all_quotes(results)
            print(formatted_output)
        
        # Save results
        if not args.no_save:
            saved_file = output_manager.save_results(results, anime_list)
            print(f"\n💾 Results saved to: {saved_file}")
        
        # Print summary
        successful = len([r for r in results.values() if "error" not in r])
        total_quotes = sum(len(r.get("data", [])) for r in results.values() if "error" not in r)
        
        print(f"\n📊 Summary:")
        print(f"  • Total anime requested: {len(anime_list)}")
        print(f"  • Successful fetches: {successful}")
        print(f"  • Failed fetches: {len(anime_list) - successful}")
        print(f"  • Total quotes retrieved: {total_quotes}")
        
    except KeyboardInterrupt:
        print("\n\n⚠️  Operation cancelled by user")
        sys.exit(1)
    except Exception as e:
        print(f"\n❌ Unexpected error: {e}")
        sys.exit(1)


if __name__ == "__main__":
    main()