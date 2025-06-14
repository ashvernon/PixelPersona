import os

# I/O
OUTPUT_DIR = "output_sprites"
os.makedirs(OUTPUT_DIR, exist_ok=True)

SPRITE_SIZE = 32  
OUTLINE     = (0, 0, 0)


# Sprite geometry
HEAD_WIDTH   = 10
HEAD_HEIGHT  = 11
HEAD_Y       = 0
BODY_WIDTH   = 12
BODY_HEIGHT  = 10
LEG_WIDTH    = 3

# UI scales
PREVIEW_SCALE = 6
EDIT_SCALE    = 20
CANVAS_SIZE   = SPRITE_SIZE * PREVIEW_SCALE

# Animation
FRAME_DELAY = 250  # ms
