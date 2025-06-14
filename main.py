import os
import random
from PIL import Image, ImageTk
import tkinter as tk
from tkinter import colorchooser, messagebox

from pixelpersona.sprite import (
    Sprite, SPRITE_SIZE, HEAD_WIDTH, HEAD_HEIGHT, HEAD_Y, OUTLINE
)
from pixelpersona.animator import SpriteAnimator

# Output directory and save index
OUTPUT_DIR = "output_sprites"
os.makedirs(OUTPUT_DIR, exist_ok=True)
SAVE_INDEX = 1

# Editor dimensions
FACE_WIDTH = 8
FACE_HEIGHT = 9

# Color palettes -----------------------------------------------------------

def hex_palette(hex_list):
    return [tuple(int(h[i:i+2], 16) for i in (0, 2, 4)) for h in hex_list]

SKIN_TONES = hex_palette(["FFE0BD", "F1C27D", "E0AC69", "C68642", "8D5524"])
HAIR_COLORS = hex_palette(["000000", "5E3C27", "C27754", "FFE066", "C8C8C8"])
CLOTHES_COLORS = hex_palette(["E6194B", "3CB44B", "0082C8", "F58230", "911EB4", "D2F53C"])
PANTS_COLORS = hex_palette(["323232", "1E90FF", "228B22", "800080"])
SHIRT_STYLES = ["tshirt", "shirt_tie", "lab_coat", "dress"]

# Tkinter setup -----------------------------------------------------------
root = tk.Tk()
root.title("Sprite Face Designer")

PREVIEW_SCALE = 6
EDIT_SCALE = 20
CANVAS_SIZE = SPRITE_SIZE * PREVIEW_SCALE

# Tkinter variables
skin_var = tk.StringVar(value=f"#{SKIN_TONES[0][0]:02X}{SKIN_TONES[0][1]:02X}{SKIN_TONES[0][2]:02X}")
hair_var = tk.StringVar(value="flat")
hair_color_var = tk.StringVar(value=f"#{HAIR_COLORS[0][0]:02X}{HAIR_COLORS[0][1]:02X}{HAIR_COLORS[0][2]:02X}")
shirt_var = tk.StringVar(value=SHIRT_STYLES[0])
face_color_var = tk.StringVar(value="#000000")

# Face template (9 rows tall)
face_template = [[None] * FACE_WIDTH for _ in range(FACE_HEIGHT)]

# Layout -----------------------------------------------------------------
ctrl = tk.Frame(root)
ctrl.pack(side=tk.LEFT, padx=10, pady=10)
canvas = tk.Canvas(root, width=CANVAS_SIZE, height=CANVAS_SIZE)
canvas.pack(side=tk.RIGHT, padx=10, pady=10)

# Controls ---------------------------------------------------------------
# Skin
tk.Label(ctrl, text="Skin Tone:").grid(row=0, column=0)
skin_menu = tk.OptionMenu(ctrl, skin_var, *[f"#{c[0]:02X}{c[1]:02X}{c[2]:02X}" for c in SKIN_TONES])
skin_menu.grid(row=0, column=1)
# Hair style
tk.Label(ctrl, text="Hair Style:").grid(row=1, column=0)
hair_menu = tk.OptionMenu(ctrl, hair_var, "flat", "side_part", "messy")
hair_menu.grid(row=1, column=1)
# Hair color
tk.Label(ctrl, text="Hair Color:").grid(row=2, column=0)
hc_menu = tk.OptionMenu(ctrl, hair_color_var, *[f"#{c[0]:02X}{c[1]:02X}{c[2]:02X}" for c in HAIR_COLORS])
hc_menu.grid(row=2, column=1)
# Face color picker
tk.Label(ctrl, text="Face Pixel Color:").grid(row=3, column=0)
clr_entry = tk.Entry(ctrl, textvariable=face_color_var, width=10)
clr_entry.grid(row=3, column=1)
pick_btn = tk.Button(ctrl, text="Pick...", command=lambda: face_color_var.set(colorchooser.askcolor()[1]))
pick_btn.grid(row=3, column=2)

# Face editor grid -------------------------------------------------------
tk.Label(ctrl, text=f"Paint Face ({FACE_WIDTH}×{FACE_HEIGHT}):").grid(row=4, column=0, columnspan=3)
ed_cr = tk.Canvas(ctrl, width=FACE_WIDTH * EDIT_SCALE, height=FACE_HEIGHT * EDIT_SCALE, bg="#333")
ed_cr.grid(row=5, column=0, columnspan=3)
for r in range(FACE_HEIGHT):
    for c in range(FACE_WIDTH):
        ed_cr.create_rectangle(c * EDIT_SCALE, r * EDIT_SCALE,
                               (c + 1) * EDIT_SCALE, (r + 1) * EDIT_SCALE,
                               outline="#555", fill="#333")


def on_edit(event):
    col = event.x // EDIT_SCALE
    row = event.y // EDIT_SCALE
    hx = face_color_var.get()
    if hx.startswith('#') and len(hx) == 7:
        face_template[row][col] = hx
        ed_cr.create_rectangle(col * EDIT_SCALE, row * EDIT_SCALE,
                               (col + 1) * EDIT_SCALE, (row + 1) * EDIT_SCALE,
                               outline=f"#{OUTLINE[0]:02X}{OUTLINE[1]:02X}{OUTLINE[2]:02X}", fill=hx)
    update_preview()


ed_cr.bind("<Button-1>", on_edit)

# Right-click to clear single cell

def on_clear(event):
    col = event.x // EDIT_SCALE
    row = event.y // EDIT_SCALE
    face_template[row][col] = None
    ed_cr.create_rectangle(col * EDIT_SCALE, row * EDIT_SCALE,
                           (col + 1) * EDIT_SCALE, (row + 1) * EDIT_SCALE,
                           outline="#555", fill="#333")
    update_preview()


ed_cr.bind("<Button-3>", on_clear)

# Clear All button -------------------------------------------------------

def clear_all():
    for r in range(FACE_HEIGHT):
        for c in range(FACE_WIDTH):
            face_template[r][c] = None
    ed_cr.delete("all")
    for r in range(FACE_HEIGHT):
        for c in range(FACE_WIDTH):
            ed_cr.create_rectangle(c * EDIT_SCALE, r * EDIT_SCALE,
                                   (c + 1) * EDIT_SCALE, (r + 1) * EDIT_SCALE,
                                   outline="#555", fill="#333")
    update_preview()


btn_clear = tk.Button(ctrl, text="Clear Face", command=clear_all)
btn_clear.grid(row=6, column=0, columnspan=3, pady=5)


# Sprite helpers ---------------------------------------------------------

def build_sprite():
    skin = tuple(int(skin_var.get()[i:i + 2], 16) for i in (1, 3, 5))
    hair = tuple(int(hair_color_var.get()[i:i + 2], 16) for i in (1, 3, 5))
    clothes = random.choice(CLOTHES_COLORS)
    pants = random.choice(PANTS_COLORS)
    return Sprite(face_template, skin, hair, hair_var.get(), shirt_var.get(), clothes, pants)


# Preview update ---------------------------------------------------------

def update_preview(*args):
    canvas.delete("all")
    img = build_sprite().image()
    preview = img.resize((CANVAS_SIZE, CANVAS_SIZE), Image.NEAREST)
    tk_img = ImageTk.PhotoImage(preview)
    canvas.image = tk_img
    canvas.create_image(0, 0, anchor=tk.NW, image=tk_img)


# Save sprite ------------------------------------------------------------

def generate():
    global SAVE_INDEX
    img = build_sprite().image()
    filename = f"custom_sprite_{SAVE_INDEX:03d}.png"
    path = os.path.join(OUTPUT_DIR, filename)
    img.save(path)
    messagebox.showinfo("Saved", f"Sprite saved to {path}")
    SAVE_INDEX += 1


# Simple animation demo --------------------------------------------------
animator = None

def start_animation():
    styles = ["flat", "side_part", "messy"]
    frames = []
    for style in styles:
        skin = tuple(int(skin_var.get()[i:i + 2], 16) for i in (1, 3, 5))
        hair = tuple(int(hair_color_var.get()[i:i + 2], 16) for i in (1, 3, 5))
        spr = Sprite(face_template, skin, hair, style, shirt_var.get(),
                     random.choice(CLOTHES_COLORS), random.choice(PANTS_COLORS))
        frames.append(spr.image())
    global animator
    animator = SpriteAnimator(canvas, frames, delay=300, scale=PREVIEW_SCALE)
    animator.start()


# Bind events ------------------------------------------------------------
for var in (skin_var, hair_var, hair_color_var, face_color_var):
    var.trace_add("write", update_preview)
update_preview()

btn = tk.Button(ctrl, text="Generate Sprite", command=generate)
btn.grid(row=7, column=0, columnspan=3, pady=10)

anim_btn = tk.Button(ctrl, text="Play Animation", command=start_animation)
anim_btn.grid(row=8, column=0, columnspan=3)

root.mainloop()
