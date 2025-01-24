import os
import tempfile
import zipfile
import streamlit as st
from PIL import Image, ImageDraw
import random
import time
from genwallpaper.generator import generate_wallpapers, ColorPalette

st.set_page_config(page_title="Wallpaper Generator", layout="wide")

st.title("Wallpaper Generator")
st.write("Generate beautiful wallpapers with repeated text patterns")

# Initialize session state
if 'generated_images' not in st.session_state:
    st.session_state.generated_images = []
if 'processing' not in st.session_state:
    st.session_state.processing = False
if 'temp_dir' not in st.session_state:
    st.session_state.temp_dir = None
if 'current_palette_index' not in st.session_state:
    st.session_state.current_palette_index = 0
if 'shuffled_palettes' not in st.session_state:
    st.session_state.shuffled_palettes = []

# Input parameters
text_input = st.text_input("Enter text for wallpaper", value="Hello")
texts = [text.strip() for text in text_input.split(",") if text.strip()]

col1, col2 = st.columns(2)
with col1:
    width = st.number_input("Width (pixels)", min_value=800, max_value=3840, value=1920)
with col2:
    height = st.number_input("Height (pixels)", min_value=600, max_value=2160, value=1080)

def generate_single_wallpaper(text: str, palette: dict, temp_dir: str, width: int, height: int) -> str:
    """Generate a single wallpaper with specified palette and return its path"""
    # Create a temporary subdirectory for this specific wallpaper
    wallpaper_dir = os.path.join(temp_dir, str(time.time()))
    os.makedirs(wallpaper_dir, exist_ok=True)
    
    # Override the random palette selection in generate_wallpapers
    original_get_random_palette = ColorPalette.get_random_palette
    ColorPalette.get_random_palette = lambda: palette
    
    try:
        # Generate the wallpaper
        generate_wallpapers([text], wallpaper_dir, width, height)
        output_path = os.path.join(wallpaper_dir, f"{text}.png")
        
        # Move the file to the main temp directory with a unique name
        final_path = os.path.join(temp_dir, f"{text}_{palette['description']}.png")
        os.rename(output_path, final_path)
        return final_path
    finally:
        # Restore the original method
        ColorPalette.get_random_palette = original_get_random_palette
        # Clean up the temporary subdirectory
        if os.path.exists(wallpaper_dir):
            os.rmdir(wallpaper_dir)

def create_preview_grid():
    """Create a grid of generated images"""
    if not st.session_state.generated_images:
        return
    
    # Create columns for the grid (3 images per row)
    cols = st.columns(3)
    
    # Display images in the grid
    for idx, img_path in enumerate(st.session_state.generated_images):
        with cols[idx % 3]:
            if os.path.exists(img_path):
                img = Image.open(img_path)
                # Extract palette description from filename
                filename = os.path.basename(img_path)
                palette_name = filename.split('_', 1)[1].rsplit('.', 1)[0]
                st.image(img, caption=f"Palette: {palette_name}", use_container_width=True)
                
                # Download button for individual image
                with open(img_path, "rb") as file:
                    st.download_button(
                        label=f"Download {filename}",
                        data=file,
                        file_name=filename,
                        mime="image/png"
                    )

# Generate button
if st.button("Generate All Variations"):
    if texts:
        # Clear previous state
        st.session_state.generated_images = []
        if st.session_state.temp_dir:
            import shutil
            shutil.rmtree(st.session_state.temp_dir, ignore_errors=True)
        
        # Create new temporary directory
        st.session_state.temp_dir = tempfile.mkdtemp()
        st.session_state.processing = True
        
        # Reset palette index and create new shuffled palette list
        st.session_state.current_palette_index = 0
        st.session_state.shuffled_palettes = ColorPalette.PALETTES.copy()
        random.shuffle(st.session_state.shuffled_palettes)
    else:
        st.error("Please enter at least one text string")

def process_next_palette():
    """Process the next palette in the queue"""
    if not st.session_state.processing or not texts:
        return

    total_palettes = len(ColorPalette.PALETTES)
    
    # Check if we still have palettes to process
    if st.session_state.current_palette_index < len(st.session_state.shuffled_palettes):
        # Get current palette
        palette = st.session_state.shuffled_palettes[st.session_state.current_palette_index]
        
        try:
            # Generate wallpapers for current palette
            for text in texts:
                img_path = generate_single_wallpaper(
                    text, 
                    {"bg": palette["bg"], "fg": palette["fg"], "description": palette["description"]},
                    st.session_state.temp_dir,
                    width,
                    height
                )
                if img_path and os.path.exists(img_path):
                    st.session_state.generated_images.append(img_path)
            
            # Move to next palette
            st.session_state.current_palette_index += 1
            
            # Schedule next update if there are more palettes
            if st.session_state.current_palette_index < len(st.session_state.shuffled_palettes):
                st.query_params.update = str(time.time())
        except Exception as e:
            st.error(f"Error generating wallpaper: {str(e)}")
            st.session_state.processing = False
    else:
        # All palettes processed
        st.session_state.processing = False

# Display progress and process next palette
if st.session_state.processing:
    total_palettes = len(ColorPalette.PALETTES)
    current = st.session_state.current_palette_index
    progress = current / total_palettes
    
    # Progress indicators
    col1, col2 = st.columns([3, 1])
    with col1:
        st.progress(progress)
    with col2:
        st.write(f"{current}/{total_palettes}")
    
    # Process next palette with auto-rerun
    process_next_palette()
    if st.session_state.processing:
        time.sleep(0.1)  # Small delay to prevent too rapid updates
        st.rerun()

# Display generated images
if st.session_state.generated_images:
    st.subheader("Generated Wallpapers")
    create_preview_grid()
    
    # Create ZIP file containing all wallpapers
    if len(st.session_state.generated_images) > 1:
        zip_path = os.path.join(st.session_state.temp_dir, "wallpapers.zip")
        with zipfile.ZipFile(zip_path, "w") as zipf:
            for img_path in st.session_state.generated_images:
                if os.path.exists(img_path):
                    zipf.write(img_path, os.path.basename(img_path))
        
        # Download button for ZIP file
        with open(zip_path, "rb") as file:
            st.download_button(
                label="Download All Wallpapers (ZIP)",
                data=file,
                file_name="wallpapers.zip",
                mime="application/zip"
            )

# Display processing message
if st.session_state.processing:
    st.info("Generating wallpapers... New variations will appear as they are generated.")

# Display color palette examples
st.subheader("Available Color Palettes")
cols = st.columns(4)
for idx, palette in enumerate(ColorPalette.PALETTES):
    with cols[idx % 4]:
        # Create a small preview of the color palette
        preview = Image.new("RGB", (100, 50), palette["bg"])
        draw = ImageDraw.Draw(preview)
        draw.rectangle([40, 10, 60, 40], fill=palette["fg"])
        st.image(preview, caption=palette["description"])
