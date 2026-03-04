#!/usr/bin/env python3
"""
Check for duplicate vocabulary words across existing generated files.

Usage:
    python3 check_duplicates.py <output_directory>

Reads all existing vocabulary markdown files in the output directory,
extracts words from the word list tables, and prints them for
deduplication purposes.
"""

import os
import re
import sys
from pathlib import Path


def extract_words_from_file(filepath: str) -> list[dict]:
    """Extract vocabulary words from a generated markdown file."""
    words = []
    in_word_table = False

    with open(filepath, "r", encoding="utf-8") as f:
        for line in f:
            stripped = line.strip()

            # Detect the word list table header
            if "| # | Word |" in stripped:
                in_word_table = True
                continue

            # Skip the separator row
            if in_word_table and stripped.startswith("|---"):
                continue

            # Parse word table rows
            if in_word_table and stripped.startswith("|"):
                parts = [p.strip() for p in stripped.split("|")]
                # parts[0] is empty (before first |), parts[1] is #, parts[2] is word
                if len(parts) >= 5 and parts[1].isdigit():
                    word = parts[2].strip()
                    pos = parts[3].strip()
                    if word and word != "{{WORD}}":
                        words.append({"word": word.lower(), "pos": pos})
                else:
                    in_word_table = False
            elif in_word_table and not stripped.startswith("|"):
                in_word_table = False

    return words


def main():
    if len(sys.argv) < 2:
        print("Usage: python3 check_duplicates.py <output_directory>")
        sys.exit(1)

    output_dir = sys.argv[1]
    output_path = Path(output_dir)

    if not output_path.exists():
        print("No output directory found. No duplicates to check.")
        sys.exit(0)

    all_words: dict[str, list[str]] = {}
    file_count = 0

    for vocab_file in sorted(output_path.glob("*-vocabulary.md")):
        file_count += 1
        words = extract_words_from_file(str(vocab_file))
        date = vocab_file.stem.replace("-vocabulary", "")

        for entry in words:
            word = entry["word"]
            if word not in all_words:
                all_words[word] = []
            all_words[word].append(date)

    if not all_words:
        print(f"Scanned {file_count} file(s). No existing words found.")
        sys.exit(0)

    print(f"Scanned {file_count} file(s). Found {len(all_words)} unique word(s).\n")

    # Print all known words for the agent to reference
    print("=== Known Words (do NOT reuse) ===")
    for word in sorted(all_words.keys()):
        sources = all_words[word]
        print(f"  - {word} (from: {', '.join(sources)})")

    # Flag words that appeared in multiple files
    duplicates = {w: s for w, s in all_words.items() if len(s) > 1}
    if duplicates:
        print(f"\n=== WARNING: {len(duplicates)} word(s) already duplicated ===")
        for word, sources in sorted(duplicates.items()):
            print(f"  - '{word}' appears in: {', '.join(sources)}")


if __name__ == "__main__":
    main()
