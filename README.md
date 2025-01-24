# Wallpaper Generator

A command-line tool for generating wallpapers for multi-desktop environments. Each wallpaper contains repeated text in a diagonal pattern with carefully selected color combinations.

## Features

- Generate wallpapers with custom text
- Multiple predefined color schemes (both light and dark themes)
- Support for various resolutions (HD, FHD, 2K, 4K)
- Diagonal text pattern for visual distinction
- Easy-to-read text with carefully selected color combinations

## Installation

```bash
# Clone the repository
git clone https://github.com/yourusername/wallpaper-generator.git
cd wallpaper-generator

# Install using Poetry
poetry install
```

## Usage

```bash
# Basic usage
poetry run genwallpaper Work Personal Project

# Specify output directory
poetry run genwallpaper -o wallpapers Work Personal Project

# Specify resolution using predefined aliases
poetry run genwallpaper --resolution fhd Work Personal Project  # 1920x1080
poetry run genwallpaper --resolution 2k Work Personal Project   # 2560x1440
poetry run genwallpaper --resolution 4k Work Personal Project   # 3840x2160

# Specify custom resolution
poetry run genwallpaper --resolution 1920x1200 Work Personal Project
```

## Web Interface

The tool also provides a web interface powered by Streamlit, which allows you to:
- Generate wallpapers through an interactive interface
- Preview wallpapers before downloading
- Download individual wallpapers or all wallpapers as a ZIP file
- View all available color palettes

### Running the Web Interface

```bash
# Start the web interface
poetry run genwallpaper-web
```

This will launch a local web server and open the interface in your default browser. You can also deploy this interface to Streamlit Community Cloud for free.

### Using the Web Interface

1. Enter text for your wallpaper(s) - separate multiple texts with commas
2. Adjust the width and height as needed
3. Click "Generate Preview" to see your wallpapers
4. Download individual wallpapers or use the ZIP download option for multiple wallpapers
5. Browse through the available color palettes at the bottom of the page

### Available Resolution Aliases

- `hd`: 1280x720
- `fhd`: 1920x1080
- `2k`: 2560x1440
- `4k`/`uhd`: 3840x2160

## Output

The tool generates PNG images in the specified output directory (default: `images/`). Each image is named after the provided text (e.g., `Work.png`, `Personal.png`).

## Color Schemes

The tool includes several carefully selected color combinations for both light and dark themes:

### Dark Themes
- Neutral Dark: Sophisticated grayscale
- Ocean Dark: Cool blue tones
- Purple Haze: Elegant purple shades
- Forest Dark: Natural green tints

### Light Themes
- Neutral Light: Clean grayscale
- Sky Light: Subtle blue tones
- Rose Light: Gentle pink hues
- Mint Light: Fresh green tints

### Additional Color Themes
- Stiletto: Deep burgundy with pearl blue accents
- Mint Julep: Soft cream with seafoam green text
- Surf: Aqua mint with coral accents
- Sapphire: Royal blue with periwinkle text
- Blue Gem: Deep indigo with soft pink text
- Shadow Green: Forest green with vibrant orange text
- Alizarin Crimson: Bright red with golden text
- Monte Carlo: Turquoise with chocolate brown text

## License

MIT License - see LICENSE file for details.
