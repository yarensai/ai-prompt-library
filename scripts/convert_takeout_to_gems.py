#!/usr/bin/env python3
"""
Google Takeout Gemini Parser
Scans exported Takeout HTML and JSON files, extracts customized prompt configurations,
and generates standardized Markdown files with YAML frontmatter.
"""

import json
import html
import os
import re
from datetime import datetime
import argparse

def sanitize_filename(name: str) -> str:
    """Converts a prompt string into a clean, kebab-case filename."""
    name = re.sub(r'[^a-zA-Z0-9\s-]', '', name).strip().lower()
    return re.sub(r'[\s]+', '-', name) or "untitled-gem"

def create_markdown_gem(title: str, instructions: str, output_dir: str):
    """Formats and writes the Gem into a YAML + Markdown file."""
    base_filename = sanitize_filename(title)
    filename = f"{base_filename}.md"
    filepath = os.path.join(output_dir, filename)
    
    # Handle filename collisions
    counter = 1
    while os.path.exists(filepath):
        filename = f"{base_filename}-{counter}.md"
        filepath = os.path.join(output_dir, filename)
        counter += 1
    
    # Escape quotes and backslashes for valid YAML syntax
    safe_title = title.replace('\\', '\\\\').replace('"', '\\"')
    date_str = datetime.now().strftime('%Y-%m-%d')

    content = f"""---
name: "{safe_title}"
description: "Imported from Google Takeout"
version: "1.0.0"
date_imported: "{date_str}"
---

## System Instructions

{instructions.strip()}
"""
    
    with open(filepath, 'w', encoding='utf-8') as f:
        f.write(content)
    print(f"[+] Created: {filepath}")

def parse_html_gems(filepath: str, output_dir: str) -> int:
    """Parses Google Takeout HTML files (like gemini_gems_data.html)."""
    count = 0
    with open(filepath, 'r', encoding='utf-8') as f:
        raw_html = f.read()

    # Convert HTML line breaks to markdown newlines
    content = re.sub(r'<br\s*/?>', '\n', raw_html, flags=re.IGNORECASE)
    # Remove HTML structural tags
    content = re.sub(r'</?div[^>]*>', '', content, flags=re.IGNORECASE)
    # Decode HTML entities (e.g., &amp;, &#39;, &quot;)
    content = html.unescape(content)

    # Split into sections based on <b>Name:</b>
    sections = re.split(r'<b>Name:</b>', content, flags=re.IGNORECASE)
    for section in sections:
        section = section.strip()
        if not section:
            continue
        
        # Split section into name and instructions
        parts = re.split(r'\n?<b>Instructions:</b>\n?', section, maxsplit=1, flags=re.IGNORECASE)
        if len(parts) == 2:
            title = parts[0].strip()
            instructions = parts[1].strip()
            if title and instructions:
                create_markdown_gem(title, instructions, output_dir)
                count += 1
    return count

def parse_takeout_directory(takeout_path: str, output_dir: str):
    """Walks through the Takeout directory to find and extract prompt structures."""
    os.makedirs(output_dir, exist_ok=True)
    processed_count = 0

    for root, _, files in os.walk(takeout_path):
        for file in files:
            full_path = os.path.join(root, file)
            
            # 1. Parse HTML export files (Google Takeout default for Gems)
            if file.endswith('.html') and 'gemini_gems_data' in file:
                try:
                    count = parse_html_gems(full_path, output_dir)
                    processed_count += count
                except Exception as e:
                    print(f"[-] Error parsing HTML file {file}: {e}")
            
            # 2. Parse JSON export files (if present)
            elif file.endswith('.json'):
                try:
                    with open(full_path, 'r', encoding='utf-8') as f:
                        data = json.load(f)
                        items = data if isinstance(data, list) else [data]
                        for item in items:
                            title = item.get('title') or item.get('name') or "Exported Gem"
                            instructions = item.get('systemInstructions') or item.get('customInstructions') or item.get('promptText')
                            
                            if instructions:
                                create_markdown_gem(title, instructions, output_dir)
                                processed_count += 1
                except Exception as e:
                    print(f"[-] Error parsing JSON file {file}: {e}")

    print(f"\nExtraction complete! Processed {processed_count} Gems into '{output_dir}'.")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Convert Gemini Takeout exports to MD Gems.")
    parser.add_argument("--input", required=True, help="Path to extracted Google Takeout folder")
    parser.add_argument("--output", default="models/gemini-gems", help="Output folder for MD files")
    args = parser.parse_args()

    parse_takeout_directory(args.input, args.output)


