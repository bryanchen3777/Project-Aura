# loader.py - Static Injection Loader for Project Aura
# Reads SOUL.md, MEMORY.md from workspace and combines into system prompt string
#
# Optimized version with:
# - pathlib for flexible path handling
# - Guide text for each section
# - Caching mechanism for performance

import os
from pathlib import Path
from datetime import datetime
from typing import Optional

# Base workspace path (supports environment variable override)
WORKSPACE = Path(os.environ.get('OPENCLAW_WORKSPACE', r"C:\Users\bbfcc\.openclaw\workspace"))

# File paths using pathlib
SOUL_PATH = WORKSPACE / "SOUL.md"
MEMORY_PATH = WORKSPACE / "MEMORY.md"

# Section definitions with guide text (descriptions for the model)
SECTION_GUIDES = {
    "SOUL.md": "這是妳的核心人格與身份認同，請永遠遵守。",
    "MEMORY.md": "這是妳的行為準則與綠茶哲學，定義了妳的互動姿態。"
}

# Cache variables
_cached_instructions: Optional[str] = None
_cache_timestamp: Optional[datetime] = None


def _read_file(file_path: Path) -> str:
    """Read file content with error handling."""
    try:
        with open(file_path, "r", encoding="utf-8") as f:
            return f.read()
    except FileNotFoundError:
        return ""
    except Exception as e:
        return f"[Error reading {file_path.name}: {e}]"


def _format_section(file_name: str, content: str, guide: str) -> str:
    """Format a section with Markdown header and blockquote guide."""
    if not content:
        return ""
    
    return f"""## {file_name}

> {guide}

{content}"""


def get_system_instructions(use_cache: bool = True) -> str:
    """
    Reads SOUL.md and MEMORY.md from workspace locations,
    combines them into a single system prompt string.

    Args:
        use_cache: If True, return cached version if available.
                   Set to False to force reload (e.g., after file updates).

    Returns:
        str: Combined system instructions with Markdown formatting.
    """
    global _cached_instructions, _cache_timestamp

    # Return cached version if available and cache is enabled
    if use_cache and _cached_instructions is not None:
        return _cached_instructions

    sections = []

    # Read SOUL.md
    soul_content = _read_file(SOUL_PATH)
    if soul_content:
        sections.append(_format_section(
            "SOUL.md",
            soul_content,
            SECTION_GUIDES.get("SOUL.md", "")
        ))

    # Read MEMORY.md
    memory_content = _read_file(MEMORY_PATH)
    if memory_content:
        sections.append(_format_section(
            "MEMORY.md",
            memory_content,
            SECTION_GUIDES.get("MEMORY.md", "")
        ))

    # Combine sections
    _cached_instructions = "\n\n---\n\n".join(sections)
    _cache_timestamp = datetime.now()

    return _cached_instructions


def invalidate_cache() -> None:
    """
    Clear the instruction cache.
    
    Call this when /sync_soul is triggered to force reload of files.
    """
    global _cached_instructions, _cache_timestamp
    _cached_instructions = None
    _cache_timestamp = None


def get_cache_status() -> dict:
    """Return current cache status for debugging."""
    return {
        "cached": _cached_instructions is not None,
        "timestamp": _cache_timestamp.isoformat() if _cache_timestamp else None,
        "size_chars": len(_cached_instructions) if _cached_instructions else 0
    }


def get_soul_only() -> str:
    """Read only SOUL.md content (bypasses cache)."""
    return _read_file(SOUL_PATH)


def get_memory_only() -> str:
    """Read only MEMORY.md content (bypasses cache)."""
    return _read_file(MEMORY_PATH)


if __name__ == "__main__":
    # Test output
    instructions = get_system_instructions()
    print(f"Total length: {len(instructions)} chars")
    print(f"Cache status: {get_cache_status()}")
    print("\n--- OUTPUT PREVIEW ---")
    print(instructions[:500] + "..." if len(instructions) > 500 else instructions)
