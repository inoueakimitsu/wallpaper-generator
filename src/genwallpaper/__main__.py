"""
Command-line interface for the wallpaper generator.

This module provides the command-line interface for generating wallpapers.
It handles argument parsing and directory creation for the output files.

Usage:
    python -m genwallpaper -o images --resolution fhd Work Personal Project
    python -m genwallpaper -o images --resolution 1920x1080 Work Personal Project
"""

import argparse
import os
import re

from .generator import generate_wallpapers

# Common resolution aliases and their actual dimensions
RESOLUTION_ALIASES = {
    "hd": (1280, 720),
    "fhd": (1920, 1080),
    "2k": (2560, 1440),
    "4k": (3840, 2160),
    "uhd": (3840, 2160),
}

def parse_resolution(resolution_str: str) -> tuple[int, int]:
    """
    Parse resolution string and return width and height as a tuple.

    Args:
        resolution_str: Resolution string, e.g., "1920x1080", "fhd", "4k"

    Returns:
        Tuple[int, int]: A tuple of (width, height)

    Raises:
        ValueError: If an invalid resolution string is provided
    """
    # Check for aliases (case-insensitive)
    resolution_lower = resolution_str.lower()
    if resolution_lower in RESOLUTION_ALIASES:
        return RESOLUTION_ALIASES[resolution_lower]

    # Parse WxH format (e.g., 1920x1080)
    match = re.match(r'^(\d+)x(\d+)$', resolution_str)
    if match:
        width, height = map(int, match.groups())
        return width, height

    raise ValueError(
        f"Invalid resolution format: {resolution_str}. "
        f"Use either WxH format (e.g., 1920x1080) or "
        f"one of the aliases: {', '.join(RESOLUTION_ALIASES.keys())}"
    )

def main():
    parser = argparse.ArgumentParser(
        description='Generate wallpapers for multi-desktop environments',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Resolution can be specified in the following formats:
  - Dimensions: 1920x1080
  - Aliases: hd (1280x720), fhd (1920x1080), 2k (2560x1440), 4k/uhd (3840x2160)
"""
    )
    parser.add_argument('texts', nargs='+', help='Text strings to use in wallpapers')
    parser.add_argument(
        '-o', '--output',
        default='images',
        help='Output directory for wallpapers'
    )
    parser.add_argument(
        '--resolution',
        default='fhd',
        help='Resolution in WxH format (e.g., 1920x1080) or alias (e.g., fhd, 4k)'
    )

    args = parser.parse_args()

    try:
        width, height = parse_resolution(args.resolution)
    except ValueError as e:
        parser.error(str(e))

    # Create output directory if it doesn't exist
    os.makedirs(args.output, exist_ok=True)

    # Generate wallpapers
    generate_wallpapers(
        texts=args.texts,
        output_dir=args.output,
        width=width,
        height=height
    )

if __name__ == '__main__':
    main()
