import os
import random
from PIL import Image, ImageDraw, ImageTk
import tkinter as tk
from tkinter import colorchooser, messagebox

# Configuration
SPRITE_SIZE = 32  # final sprite size in pixels
OUTPUT_DIR = "output_sprites"
os.makedirs(OUTPUT_DIR, exist_ok=True)

# Head dimensions
HEAD_WIDTH = 10
HEAD_HEIGHT = 11  # increased to fit 9px face plus outline
HEAD_Y = 0         # draw head starting at y=0

# Save index (for incremental filenames)
SAVE_INDEX = 1

# Editor dimensions
FACE_WIDTH = 8
FACE_HEIGHT = 9     # allow 9px tall faces

# Color palettes
def hex_palette(hex_list):
    return [tuple(int(h[i:i+2], 16) for i in (0, 2, 4)) for h in hex_list]

SKIN_TONES = hex_palette(["FFE0BD", "F1C27D", "E0AC69", "C68642", "8D5524"])
HAIR_COLORS = hex_palette(["000000", "5E3C27", "C27754", "FFE066", "C8C8C8"])
CLOTHES_COLORS = hex_palette(["E6194B", "3CB44B", "0082C8", "F58230", "911EB4", "D2F53C"])
PANTS_COLORS = hex_palette(["323232", "1E90FF", "228B22", "800080"])
OUTLINE = (0, 0, 0)
WHITE = (255, 255, 255)
EYE_COLORS = [(0, 0, 0), (0, 0, 100), (100, 0, 0), (0, 100, 0)]
SHIRT_STYLES = ["tshirt", "shirt_tie", "lab_coat", "dress"]

# Drawing helpers

def draw_eyes(draw, x, y):
    for ox in (-2, 1):
        ex, ey = x + ox, y
        draw.rectangle([ex, ey, ex+1, ey+1], fill=WHITE, outline=OUTLINE)
        draw.point((ex, ey), fill=random.choice(EYE_COLORS))


def draw_hair(draw, x, y, color):
    style = hair_var.get()
    if style == "flat":
        draw.rectangle([x, y, x+HEAD_WIDTH-1, y+2], fill=color, outline=OUTLINE)
    elif style == "side_part":
        draw.rectangle([x, y, x+HEAD_WIDTH-2, y+2], fill=color, outline=OUTLINE)
    else:
        draw.rectangle([x, y, x+HEAD_WIDTH-1, y+3], fill=color, outline=OUTLINE)


def draw_body(draw, x, y, clothes):
    w, h = 12, 10
    draw.rectangle([x, y, x+w-1, y+h-1], fill=clothes, outline=OUTLINE)
    style = shirt_var.get()
    if style == 'shirt_tie':
        cx = x + w//2
        draw.line([(cx, y), (cx, y+3)], fill=WHITE)
        draw.rectangle([cx-1, y+3, cx+1, y+4], fill=WHITE)
    elif style == 'lab_coat':
        draw.line([(x+2, y+2), (x+2, y+h-2)], fill=WHITE)
        draw.line([(x+w-3, y+2), (x+w-3, y+h-2)], fill=WHITE)
    elif style == 'dress':
        draw.polygon([(x, y+h), (x+w//2, y+h-4), (x+w, y+h)], fill=clothes, outline=OUTLINE)


def draw_arms(draw, x, y, skin, clothes):
    # Left arm moved 2px closer (3px width) with hand
    draw.rectangle([x-3, y,   x-1, y+6], fill=clothes, outline=OUTLINE)
    draw.rectangle([x-3, y+7, x-1, y+9], fill=skin,    outline=OUTLINE)
    # Right arm (3px width) with hand
    rx = x + 12
    draw.rectangle([rx,   y,   rx+2, y+6], fill=clothes, outline=OUTLINE)
    draw.rectangle([rx,   y+7, rx+2, y+9], fill=skin,    outline=OUTLINE)

def draw_legs(draw, x, y, skin, pants):
    # Widened legs to 3px and better centered
    leg_w = 3  # width of each leg
    # left leg
    left_x = x + 1  # move in from body edge
    draw.rectangle([left_x, y, left_x + leg_w - 1, y + 8], fill=pants, outline=OUTLINE)
    draw.rectangle([left_x, y + 9, left_x + leg_w - 1, y + 9], fill=skin, outline=OUTLINE)
    # right leg
    right_x = x + 12 - leg_w - 1  # align from body right edge
    draw.rectangle([right_x, y, right_x + leg_w - 1, y + 8], fill=pants, outline=OUTLINE)
    draw.rectangle([right_x, y + 9, right_x + leg_w - 1, y + 9], fill=skin, outline=OUTLINE)

# UI helpers

def to_hex(col):
    return f"#{col[0]:02X}{col[1]:02X}{col[2]:02X}"

# Tkinter setup
root = tk.Tk()
root.title("Sprite Face Designer")

PREVIEW_SCALE = 6  # for full sprite preview
EDIT_SCALE = 20    # for face editor grid
CANVAS_SIZE = SPRITE_SIZE * PREVIEW_SCALE

# Variables
skin_var = tk.StringVar(value=to_hex(SKIN_TONES[0]))
hair_var = tk.StringVar(value="flat")
hair_color_var = tk.StringVar(value=to_hex(HAIR_COLORS[0]))
shirt_var = tk.StringVar(value=SHIRT_STYLES[0])
face_color_var = tk.StringVar(value="#000000")

# Face template (9 rows tall)
face_template = [[None]*FACE_WIDTH for _ in range(FACE_HEIGHT)]

# Layout
ctrl = tk.Frame(root)
ctrl.pack(side=tk.LEFT, padx=10, pady=10)
canvas = tk.Canvas(root, width=CANVAS_SIZE, height=CANVAS_SIZE)
canvas.pack(side=tk.RIGHT, padx=10, pady=10)

# Controls
# Skin
tk.Label(ctrl, text="Skin Tone:").grid(row=0, column=0)
skin_menu = tk.OptionMenu(ctrl, skin_var, *[to_hex(c) for c in SKIN_TONES])
skin_menu.grid(row=0, column=1)
# Hair style
tk.Label(ctrl, text="Hair Style:").grid(row=1, column=0)
hair_menu = tk.OptionMenu(ctrl, hair_var, *["flat","side_part","messy"])
hair_menu.grid(row=1, column=1)
# Hair color
tk.Label(ctrl, text="Hair Color:").grid(row=2, column=0)
hc_menu = tk.OptionMenu(ctrl, hair_color_var, *[to_hex(c) for c in HAIR_COLORS])
hc_menu.grid(row=2, column=1)
# Face color picker
tk.Label(ctrl, text="Face Pixel Color:").grid(row=3, column=0)
clr_entry = tk.Entry(ctrl, textvariable=face_color_var, width=10)
clr_entry.grid(row=3, column=1)
pick_btn = tk.Button(ctrl, text="Pick...", command=lambda: face_color_var.set(colorchooser.askcolor()[1]))
pick_btn.grid(row=3, column=2)

# Face editor grid
tk.Label(ctrl, text=f"Paint Face ({FACE_WIDTH}×{FACE_HEIGHT}):").grid(row=4, column=0, columnspan=3)
ed_cr = tk.Canvas(ctrl, width=FACE_WIDTH*EDIT_SCALE, height=FACE_HEIGHT*EDIT_SCALE, bg="#333")
ed_cr.grid(row=5, column=0, columnspan=3)
for r in range(FACE_HEIGHT):
    for c in range(FACE_WIDTH):
        ed_cr.create_rectangle(c*EDIT_SCALE, r*EDIT_SCALE,
                                (c+1)*EDIT_SCALE, (r+1)*EDIT_SCALE,
                                outline="#555", fill="#333")

def on_edit(event):
    col = event.x // EDIT_SCALE
    row = event.y // EDIT_SCALE
    hx = face_color_var.get()
    if hx.startswith('#') and len(hx)==7:
        face_template[row][col] = hx
        ed_cr.create_rectangle(col*EDIT_SCALE, row*EDIT_SCALE,
                               (col+1)*EDIT_SCALE, (row+1)*EDIT_SCALE,
                               outline=to_hex(OUTLINE), fill=hx)
    update_preview()
ed_cr.bind("<Button-1>", on_edit)

# Right-click to clear single cell
def on_clear(event):
    col=event.x//EDIT_SCALE;row=event.y//EDIT_SCALE
    face_template[row][col]=None
    ed_cr.create_rectangle(col*EDIT_SCALE,row*EDIT_SCALE,(col+1)*EDIT_SCALE,(row+1)*EDIT_SCALE,outline="#555",fill="#333")
    update_preview()

d_ed=ed_cr.bind
ed_cr.bind("<Button-1>",on_edit)
ed_cr.bind("<Button-3>",on_clear)

# Clear All button
def clear_all():
    for r in range(FACE_HEIGHT):
        for c in range(FACE_WIDTH): face_template[r][c]=None
    ed_cr.delete("all")
    for r in range(FACE_HEIGHT):
        for c in range(FACE_WIDTH):
            ed_cr.create_rectangle(c*EDIT_SCALE,r*EDIT_SCALE,(c+1)*EDIT_SCALE,(r+1)*EDIT_SCALE,outline="#555",fill="#333")
    update_preview()

btn_clear=tk.Button(ctrl,text="Clear Face",command=clear_all)
btn_clear.grid(row=6,column=0,columnspan=3,pady=5)



# Preview update
def update_preview(*args):
    canvas.delete("all")
    img = Image.new("RGBA", (SPRITE_SIZE, SPRITE_SIZE), (0,0,0,0))
    draw = ImageDraw.Draw(img)
    # Skin & hair
    skin = tuple(int(skin_var.get()[i:i+2],16) for i in (1,3,5))
    hair = tuple(int(hair_color_var.get()[i:i+2],16) for i in (1,3,5))
    # Draw head
    head_x = (SPRITE_SIZE - HEAD_WIDTH)//2
    draw.rectangle([head_x, HEAD_Y, head_x+HEAD_WIDTH-1, HEAD_Y+HEAD_HEIGHT-1], fill=skin, outline=OUTLINE)
    draw_hair(draw, head_x, HEAD_Y, hair)
    # Draw custom face pixels
    for r in range(FACE_HEIGHT):
        for c in range(FACE_WIDTH):
            px = face_template[r][c]
            if px:
                col = tuple(int(px[i:i+2],16) for i in (1,3,5))
                draw.point((head_x+1+c, HEAD_Y+1+r), fill=col)
    # Draw body
    body_x = (SPRITE_SIZE - 12)//2
    body_y = HEAD_Y + HEAD_HEIGHT
    clothes = random.choice(CLOTHES_COLORS)
    pants = random.choice(PANTS_COLORS)
    draw_body(draw, body_x, body_y, clothes)
    draw_arms(draw, body_x, body_y+2, skin, clothes)
    draw_legs(draw, body_x, body_y+10, skin, pants)
    # Scale and render
    preview = img.resize((CANVAS_SIZE, CANVAS_SIZE), Image.NEAREST)
    tk_img = ImageTk.PhotoImage(preview)
    canvas.image = tk_img
    canvas.create_image(0,0,anchor=tk.NW,image=tk_img)

# Generate & Save with incremental filenames
def generate():
    global SAVE_INDEX
    update_preview()
    img = Image.new("RGBA", (SPRITE_SIZE, SPRITE_SIZE), (0,0,0,0))
    d = ImageDraw.Draw(img)
    # Draw head, face, body, arms, legs (reuse existing draw calls)
    skin = tuple(int(skin_var.get()[i:i+2],16) for i in (1,3,5))
    hair = tuple(int(hair_color_var.get()[i:i+2],16) for i in (1,3,5))
    head_x = (SPRITE_SIZE - HEAD_WIDTH)//2
    d.rectangle([head_x, HEAD_Y, head_x+HEAD_WIDTH-1, HEAD_Y+HEAD_HEIGHT-1], fill=skin, outline=OUTLINE)
    draw_hair(d, head_x, HEAD_Y, hair)
    for r in range(FACE_HEIGHT):
        for c in range(FACE_WIDTH):
            px = face_template[r][c]
            if px:
                col = tuple(int(px[i:i+2],16) for i in (1,3,5))
                d.point((head_x+1+c, HEAD_Y+1+r), fill=col)
    bx, by = head_x-1, HEAD_Y+HEAD_HEIGHT
    clothes = random.choice(CLOTHES_COLORS)
    legs = random.choice(PANTS_COLORS)
    draw_body(d, bx, by, clothes)
    draw_arms(d, bx, by+2, skin, clothes)
    draw_legs(d, bx, by+10, skin, legs)
    # Save with incremental index
    filename = f"custom_sprite_{SAVE_INDEX:03d}.png"
    path = os.path.join(OUTPUT_DIR, filename)
    img.save(path)
    messagebox.showinfo("Saved", f"Sprite saved to {path}")
    SAVE_INDEX += 1

# Bind events
for var in (skin_var, hair_var, hair_color_var, face_color_var):
    var.trace_add("write", update_preview)
update_preview()
btn = tk.Button(ctrl, text="Generate Sprite", command=generate)
btn.grid(row=6, column=0, columnspan=3, pady=10)
root.mainloop()
