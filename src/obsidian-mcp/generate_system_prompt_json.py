#!/usr/bin/env python3
import json
from pathlib import Path
import sys

def convert_md_to_json(prompts_dir: Path):
    """
    For each .md file in prompts_dir, read its text and write out a .json file
    with the same stem, containing {"systemPrompt": "<full md content>"}.
    """
    md_files = list(prompts_dir.glob("*.md"))
    if not md_files:
        print(f"No .md files found in {prompts_dir}", file=sys.stderr)
        return

    for md_path in md_files:
        json_path = md_path.with_suffix(".json")
        try:
            text = md_path.read_text(encoding="utf-8")
        except Exception as e:
            print(f"Failed to read {md_path}: {e}", file=sys.stderr)
            continue

        payload = {"systemPrompt": text}
        try:
            json_path.write_text(
                json.dumps(payload, ensure_ascii=False, indent=2),
                encoding="utf-8"
            )
            print(f"✅  {md_path.name} → {json_path.name}")
        except Exception as e:
            print(f"Failed to write {json_path}: {e}", file=sys.stderr)

if __name__ == "__main__":
    # Allow optional override of the directory via command-line
    base = Path(__file__).parent
    prompts_folder = base / "system_prompts"
    if len(sys.argv) > 1:
        prompts_folder = Path(sys.argv[1])

    if not prompts_folder.is_dir():
        print(f"Error: {prompts_folder} is not a directory.", file=sys.stderr)
        sys.exit(1)

    convert_md_to_json(prompts_folder)

