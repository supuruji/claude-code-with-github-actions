#!/usr/bin/env python3
"""
Check for duplicate headlines across existing digest files.

Usage:
    python3 check_duplicates.py <output_directory>

Reads all existing digest markdown files in the output directory,
extracts headlines, and prints them for deduplication purposes.
"""

import os
import re
import sys
from pathlib import Path


def extract_headlines_from_digest(filepath: str) -> list[str]:
    """Extract headline text from a digest markdown file."""
    headlines = []
    with open(filepath, "r", encoding="utf-8") as f:
        for line in f:
            # Match table rows with headlines: | # | Headline | Source | Link |
            match = re.match(
                r"\|\s*\d+\s*\|\s*(.+?)\s*\|\s*.+?\s*\|\s*\[Read\]",
                line.strip(),
            )
            if match:
                headline = match.group(1).strip()
                if headline and headline != "{{HEADLINE}}":
                    headlines.append(headline)
    return headlines


def normalize_headline(headline: str) -> str:
    """Normalize a headline for fuzzy comparison."""
    # Lowercase, strip punctuation, collapse whitespace
    text = headline.lower()
    text = re.sub(r"[^\w\s]", "", text)
    text = re.sub(r"\s+", " ", text).strip()
    return text


def find_duplicates(output_dir: str) -> dict[str, list[str]]:
    """Find all existing headlines grouped by normalized form."""
    output_path = Path(output_dir)
    if not output_path.exists():
        return {}

    headline_sources: dict[str, list[str]] = {}

    for digest_file in sorted(output_path.glob("*-digest.md")):
        headlines = extract_headlines_from_digest(str(digest_file))
        date = digest_file.stem.replace("-digest", "")
        for headline in headlines:
            normalized = normalize_headline(headline)
            if normalized not in headline_sources:
                headline_sources[normalized] = []
            headline_sources[normalized].append(f"{date}: {headline}")

    return headline_sources


def main():
    if len(sys.argv) < 2:
        print("Usage: python3 check_duplicates.py <output_directory>")
        sys.exit(1)

    output_dir = sys.argv[1]
    headline_sources = find_duplicates(output_dir)

    if not headline_sources:
        print("No existing digests found. No duplicates to check.")
        sys.exit(0)

    print(f"Found {len(headline_sources)} unique headlines across existing digests.\n")

    # Print all known headlines for the agent to reference
    print("=== Known Headlines (avoid duplicates) ===")
    for normalized, sources in sorted(headline_sources.items()):
        print(f"  - {sources[0]}")

    # Flag actual duplicates (same headline in multiple digests)
    duplicates = {k: v for k, v in headline_sources.items() if len(v) > 1}
    if duplicates:
        print(f"\n=== WARNING: {len(duplicates)} duplicate(s) found across digests ===")
        for normalized, sources in duplicates.items():
            print(f"\n  Duplicate headline:")
            for source in sources:
                print(f"    - {source}")


if __name__ == "__main__":
    main()
