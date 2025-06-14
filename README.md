A simple Python/Tkinter application for generating 32×32 pixel-art sprites with editable 8×9 face templates.

## Screenshot

![PixelPersona Preview](docs/screenshot.png)

Features

Interactive face editor (8×9 grid) with color picker and clear functionality

Randomized body, arms, legs, hair, and clothing styles

Incremental save of custom_sprite_XXX.png files to avoid overwriting

Export sprites as PNGs in output_sprites/

Optional animation preview and GIF export

Installation

# Clone the repo
git clone https://github.com/your-username/spritegen.git
cd spritegen

# (Optional) Create & activate a virtual environment
python -m venv venv
source venv/bin/activate  # macOS/Linux
venv\Scripts\activate   # Windows

# Install dependencies
pip install pillow tk

Usage

# Launch the GUI
python main.py

Use the Skin Tone, Hair Style, and Hair Color menus to set base colors.

Click Pick... to open a color picker for face pixels.

Left-click on the 8×9 grid to paint a pixel; right-click to erase a single pixel; click Clear Face to reset the grid.

Press Generate Sprite to save a new PNG under output_sprites/custom_sprite_001.png, custom_sprite_002.png, etc.
Use the **Animate** button to preview walking frames. You can also export the animation as a GIF via **Export GIF**.
