import os
import tempfile
import zipfile
import streamlit as st
from PIL import Image, ImageDraw
from genwallpaper.generator import generate_wallpapers, ColorPalette

st.set_page_config(page_title="Wallpaper Generator", layout="wide")

st.title("Wallpaper Generator")
st.write("Generate beautiful wallpapers with repeated text patterns")

# Input parameters
text_input = st.text_input("Enter text for wallpaper", value="Hello")
texts = [text.strip() for text in text_input.split(",") if text.strip()]

col1, col2 = st.columns(2)
with col1:
    width = st.number_input("Width (pixels)", min_value=800, max_value=3840, value=1920)
with col2:
    height = st.number_input("Height (pixels)", min_value=600, max_value=2160, value=1080)

# Preview section
if st.button("Generate Preview"):
    if texts:
        # Create temporary directory for generated images
        with tempfile.TemporaryDirectory() as temp_dir:
            # Generate wallpapers
            generate_wallpapers(texts, temp_dir, width, height)
            
            # Display previews
            st.subheader("Generated Wallpapers")
            for text in texts:
                img_path = os.path.join(temp_dir, f"{text}.png")
                if os.path.exists(img_path):
                    img = Image.open(img_path)
                    st.image(img, caption=f"Wallpaper: {text}", use_container_width=True)
                    
                    # Create download button for individual image
                    with open(img_path, "rb") as file:
                        st.download_button(
                            label=f"Download {text}.png",
                            data=file,
                            file_name=f"{text}.png",
                            mime="image/png"
                        )
            
            # Create ZIP file containing all wallpapers
            if len(texts) > 1:
                zip_path = os.path.join(temp_dir, "wallpapers.zip")
                with zipfile.ZipFile(zip_path, "w") as zipf:
                    for text in texts:
                        img_path = os.path.join(temp_dir, f"{text}.png")
                        if os.path.exists(img_path):
                            zipf.write(img_path, f"{text}.png")
                
                # Download button for ZIP file
                with open(zip_path, "rb") as file:
                    st.download_button(
                        label="Download All Wallpapers (ZIP)",
                        data=file,
                        file_name="wallpapers.zip",
                        mime="application/zip"
                    )
    else:
        st.error("Please enter at least one text string")

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
