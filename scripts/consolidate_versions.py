#!/usr/bin/env python3
"""
Gemini Gems Version Consolidation Tool
Scans a prompt directory for versioned files (e.g., hpc-expert-v2.md, hpc-expert-v4.md),
promotes the highest version to the canonical filename (hpc-expert.md), updates YAML frontmatter,
and moves historical snapshots into an archive/ folder.
"""

import os
import re
import shutil
import argparse
from collections import defaultdict

def parse_version_info(filename: str):
    """
    Extracts the base name and version number from filenames like:
    'hpc-expert-v4.md', 'cyber-security-v1.md', 'prompt-engineer-2.md'
    Returns (base_name, version_float, original_filename)
    """
    name, ext = os.path.splitext(filename)
    if ext != '.md':
        return None

    # Match patterns like -v4, -v2.1, or -2 at the end of the filename
    match = re.search(r'[-_]v?(\d+(?:\.\d+)?)$', name, flags=re.IGNORECASE)
    if match:
        version_num = float(match.group(1))
        base_name = name[:match.start()].strip('-_.')
        return (base_name, version_num, filename)
    else:
        # File has no explicit version tag (treat as v1.0)
        return (name, 1.0, filename)

def update_yaml_version(filepath: str, new_version: str):
    """Updates or injects the version key inside YAML Frontmatter."""
    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()

    # Check if YAML frontmatter exists
    if content.startswith('---'):
        parts = content.split('---', 2)
        if len(parts) >= 3:
            frontmatter = parts[1]
            body = parts[2]
            
            # Replace version if exists, otherwise inject it
            if re.search(r'^version:\s*".*"', frontmatter, flags=re.MULTILINE):
                frontmatter = re.sub(r'^version:\s*".*"', f'version: "{new_version}"', frontmatter, flags=re.MULTILINE)
            else:
                frontmatter = f"{frontmatter.rstrip()}\nversion: \"{new_version}\"\n"
            
            new_content = f"---{frontmatter}---{body}"
            with open(filepath, 'w', encoding='utf-8') as f:
                f.write(new_content)

def safe_archive_move(orig_path: str, archive_dir: str, ver_str: str) -> str:
    """Safely moves a file to the archive directory without overwriting collisions."""
    os.makedirs(archive_dir, exist_ok=True)
    dest_path = os.path.join(archive_dir, f"v{ver_str}.md")
    counter = 1
    while os.path.exists(dest_path):
        dest_path = os.path.join(archive_dir, f"v{ver_str}-{counter}.md")
        counter += 1
    shutil.move(orig_path, dest_path)
    return dest_path

def consolidate_directory(target_dir: str):
    archive_base = os.path.join(target_dir, "archive")
    files = [f for f in os.listdir(target_dir) if os.path.isfile(os.path.join(target_dir, f)) and f.endswith('.md')]
    
    # Group files by their base name
    groups = defaultdict(list)
    for f in files:
        parsed = parse_version_info(f)
        if parsed:
            base_name, ver, orig = parsed
            groups[base_name].append((ver, orig))

    processed_groups = 0
    for base_name, versions in groups.items():
        # If there are multiple versions or a single file explicitly marked as -vX
        if len(versions) > 1 or any(orig != f"{base_name}.md" for ver, orig in versions):
            # Sort by version number descending
            versions.sort(key=lambda x: x[0], reverse=True)
            highest_ver, highest_file = versions[0]
            canonical_path = os.path.join(target_dir, f"{base_name}.md")
            highest_path = os.path.join(target_dir, highest_file)

            ver_str = f"{int(highest_ver) if highest_ver.is_integer() else highest_ver}.0.0"

            # 1. Promote highest version to canonical filename
            if highest_path != canonical_path:
                if os.path.exists(canonical_path):
                    # Existing canonical file might be an older unversioned snapshot; move to archive
                    archive_dir = os.path.join(archive_base, base_name)
                    archived = safe_archive_move(canonical_path, archive_dir, "1.0.0")
                    print(f"  ├── [ARCHIVED OLD CANONICAL] {canonical_path} -> {archived}")
                
                shutil.move(highest_path, canonical_path)
                print(f"[PROMOTED] {highest_file} -> {base_name}.md (Canonical v{ver_str})")

            # Update YAML frontmatter of canonical file
            update_yaml_version(canonical_path, ver_str)

            # 2. Archive older versions
            for ver, orig_file in versions[1:]:
                orig_path = os.path.join(target_dir, orig_file)
                if os.path.exists(orig_path):
                    archive_dir = os.path.join(archive_base, base_name)
                    v_sub_str = f"{int(ver) if ver.is_integer() else ver}.0.0"
                    archived = safe_archive_move(orig_path, archive_dir, v_sub_str)
                    print(f"  ├── [ARCHIVED] {orig_file} -> {archived}")
            
            processed_groups += 1

    print(f"\nConsolidation complete! Cleaned up and organized {processed_groups} prompt groups.")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Consolidate versioned Gemini Gems.")
    parser.add_argument("--dir", default="models/gemini-gems", help="Target directory to clean up")
    args = parser.parse_args()
    
    consolidate_directory(args.dir)
