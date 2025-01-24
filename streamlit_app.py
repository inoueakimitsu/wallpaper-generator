import os
import sys
import streamlit.web.cli as stcli

def main():
    # Get the absolute path to the Streamlit app
    current_dir = os.path.dirname(os.path.abspath(__file__))
    app_path = os.path.join(current_dir, "src", "genwallpaper", "streamlit_app.py")
    
    # Set up sys.argv for streamlit
    sys.argv = ["streamlit", "run", app_path]
    
    # Run the streamlit app
    sys.exit(stcli.main())

if __name__ == "__main__":
    main()
