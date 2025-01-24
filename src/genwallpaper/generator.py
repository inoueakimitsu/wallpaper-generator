"""
Wallpaper generation module.

This module handles the actual generation of wallpaper images with repeated text
patterns. It includes functionality for color palette selection and text placement
in a diagonal pattern.
"""

import os
import random
from typing import ClassVar

from PIL import Image, ImageDraw, ImageFont

# Color type alias for RGB tuples
RGB = tuple[int, int, int]


class ColorPalette:
    """
    Manages color palettes for wallpaper generation.
    Each palette consists of a background color and a foreground color
    that are designed to work well together while maintaining readability.
    """

    # Queue for shuffled palettes
    _palette_queue: ClassVar[list[dict[str, RGB]]] = []

    # Curated color palettes with carefully selected combinations
    PALETTES: ClassVar[list[dict[str, RGB]]] = [
        # Dark themes - Sophisticated and easy on the eyes
        {"bg": (30, 30, 35), "fg": (200, 200, 210), "description": "Neutral dark"},
        {"bg": (25, 35, 45), "fg": (180, 200, 220), "description": "Ocean dark"},
        {"bg": (40, 30, 45), "fg": (220, 200, 230), "description": "Purple haze"},
        {"bg": (35, 40, 35), "fg": (200, 220, 200), "description": "Forest dark"},
        # Light themes - Clean and professional
        {"bg": (240, 240, 245), "fg": (60, 60, 70), "description": "Neutral light"},
        {"bg": (235, 240, 245), "fg": (40, 50, 60), "description": "Sky light"},
        {"bg": (245, 235, 240), "fg": (50, 40, 55), "description": "Rose light"},
        {"bg": (240, 245, 240), "fg": (45, 55, 45), "description": "Mint light"},
        # New color themes
        {"bg": (139, 58, 74), "fg": (176, 196, 222), "description": "Stiletto"},
        {"bg": (245, 247, 220), "fg": (95, 158, 160), "description": "Mint Julep"},
        {"bg": (187, 229, 211), "fg": (180, 76, 67), "description": "Surf"},
        {"bg": (46, 75, 143), "fg": (181, 184, 227), "description": "Sapphire"},
        {"bg": (75, 0, 130), "fg": (255, 182, 193), "description": "Blue Gem"},
        {"bg": (74, 103, 65), "fg": (255, 69, 0), "description": "Shadow Green"},
        {"bg": (227, 38, 54), "fg": (255, 215, 0), "description": "Alizarin Crimson"},
        {"bg": (102, 205, 170), "fg": (139, 69, 19), "description": "Monte Carlo"},
    ]

    @classmethod
    def get_random_palette(cls) -> dict[str, RGB]:
        """
        Select a color palette from the shuffled queue.
        When the queue is empty, reshuffles all palettes.

        Returns:
            Dict[str, RGB]: A dictionary containing background ('bg') and
                foreground ('fg') colors
        """
        if not cls._palette_queue:
            # Create a new copy of PALETTES and shuffle it
            cls._palette_queue = cls.PALETTES.copy()
            random.shuffle(cls._palette_queue)
        
        # Get the next palette from the queue
        palette = cls._palette_queue.pop(0)
        return {"bg": palette["bg"], "fg": palette["fg"]}


def _load_font(height: int) -> tuple[ImageFont.FreeTypeFont | ImageFont.ImageFont, int]:
    """Load and return the font and font size."""
    font_size = height // 5
    
    # Try different system fonts in order of preference
    font_names = [
        "DejaVuSans-Bold.ttf",
        "Arial Bold.ttf",
        "Helvetica Bold.ttf",
        "OpenSans-Bold.ttf",
    ]
    
    try:
        for font_name in font_names:
            try:
                return ImageFont.truetype(font_name, font_size), font_size
            except OSError:
                continue
        
        # If no system fonts are available, use default
        return ImageFont.load_default(), height // 10
    except Exception:
        return ImageFont.load_default(), height // 10

def _create_rotated_text_template(
    text: str,
    font: ImageFont.FreeTypeFont | ImageFont.ImageFont,
    text_width: int,
    text_height: int,
    fg_color: RGB,
) -> Image.Image:
    """Create and return a rotated text template."""
    # Create a transparent image for the text
    text_img = Image.new('RGBA', (text_width * 2, text_height * 2), (0, 0, 0, 0))
    text_draw = ImageDraw.Draw(text_img)
    
    # Draw text at the center of the transparent image
    text_draw.text(
        (text_width // 2, text_height // 2),
        text,
        fill=fg_color + (255,),  # Add alpha channel
        font=font,
        anchor="mm"  # Center the text
    )
    
    # Rotate the text image
    return text_img.rotate(45, expand=True, resample=Image.Resampling.BICUBIC)

def generate_wallpapers(
    texts: list[str], output_dir: str, width: int = 1920, height: int = 1080
) -> None:
    """
    Generate wallpapers for each provided text string.

    Args:
        texts: List of text strings to use in wallpapers
        output_dir: Directory where the generated wallpapers will be saved
        width: Width of the wallpaper in pixels
        height: Height of the wallpaper in pixels

    Each wallpaper will have:
    - A unique color palette selected from predefined combinations
    - Text repeated in a diagonal pattern
    - Large, bold text that's easily readable
    """
    # Load font once for all wallpapers
    font, font_size = _load_font(height)
    
    for text in texts:
        # Select a color palette
        palette = ColorPalette.get_random_palette()

        # Create new image with background color
        image = Image.new("RGB", (width, height), palette["bg"])
        draw = ImageDraw.Draw(image)

        # Get text dimensions for layout calculations
        bbox = draw.textbbox((0, 0), text, font=font)
        text_width = bbox[2] - bbox[0]
        text_height = bbox[3] - bbox[1]

        # Calculate spacing for 45-degree pattern
        diagonal_spacing = (text_width + text_height) / 2  # Base diagonal spacing
        
        # Calculate grid parameters
        spacing = diagonal_spacing * 1.2  # Add some space between texts
        offset = spacing * 0.5  # Offset for creating diagonal pattern
        
        # Create rotated text template once
        rotated_text = _create_rotated_text_template(
            text, font, text_width, text_height, palette["fg"]
        )
        
        # Calculate visible area bounds with some margin
        margin = max(text_width, text_height)
        min_row = max(-3, int((-margin) / spacing))
        max_row = min(int((height + margin) / spacing) + 3, int(height / spacing) + 3)
        min_col = max(-3, int((-margin) / spacing))
        max_col = min(int((width + margin) / spacing) + 3, int(width / spacing) + 3)
        
        # Draw text in diagonal pattern (only in visible area)
        for row in range(min_row, max_row):
            for col in range(min_col, max_col):
                # Calculate base position with diagonal offset
                x = col * spacing + (row * offset)
                y = row * spacing
                
                # Calculate paste position
                paste_x = int(x - rotated_text.width // 2)
                paste_y = int(y - rotated_text.height // 2)
                
                # Skip if completely outside the image bounds
                if (paste_x + rotated_text.width < 0 or paste_x >= width or
                    paste_y + rotated_text.height < 0 or paste_y >= height):
                    continue
                
                # Paste the rotated text onto the main image
                image.paste(rotated_text, (paste_x, paste_y), rotated_text)

        # Save the generated wallpaper
        output_path = os.path.join(output_dir, f"{text}.png")
        image.save(output_path)
