"""
Wallpaper Generator for Multi-Desktop Environments

This package provides functionality to generate wallpapers for multi-desktop
environments. Each wallpaper contains repeated text in a diagonal pattern with
carefully selected color combinations.

Example:
    >>> from genwallpaper import generate_wallpapers
    >>> generate_wallpapers(['Work', 'Personal'], output_dir='images')
"""

from .generator import generate_wallpapers

__all__ = ["generate_wallpapers"]
