import os, random
import tkinter as tk
from tkinter import colorchooser, messagebox
from PIL import Image, ImageTk
from .constants import *  # OUTPUT_DIR, CANVAS_SIZE, EDIT_SCALE
from .utils import hex_palette, to_hex
from .sprite_builder import SpriteBuilder
from .animator import SpriteAnimator

# Color palettes
SKIN_TONES = hex_palette(["FFE0BD", "F1C27D", "E0AC69", "C68642", "8D5524"])
HAIR_COLORS = hex_palette(["000000", "5E3C27", "C27754", "FFE066", "C8C8C8"])
CLOTHES_COLORS = hex_palette(["E6194B", "3CB44B", "0082C8", "F58230", "911EB4", "D2F53C"])
PANTS_COLORS = hex_palette(["323232", "1E90FF", "228B22", "800080"])
SHIRT_STYLES = ["tshirt", "shirt_tie", "lab_coat", "dress"]

# Face editor dimensions
FACE_WIDTH = 8
FACE_HEIGHT = 9

class SpriteFaceDesigner:
    def __init__(self):
        # 1) Create window
        self.root = tk.Tk()
        self.root.title("Sprite Face Designer")

        # 2) Variables
        self._make_variables()

        # 3) Animator ready before layout
        self.animator = SpriteAnimator(self._on_frame)

        # 4) Build UI (uses self.animator)
        self._build_layout()

        # 5) Initial preview
        self.update_preview()

    def _make_variables(self):
        self.skin_var = tk.StringVar(value=to_hex(SKIN_TONES[0]))
        self.hair_var = tk.StringVar(value="flat")
        self.hair_color_var = tk.StringVar(value=to_hex(HAIR_COLORS[0]))
        self.shirt_var = tk.StringVar(value=SHIRT_STYLES[0])
        self.face_color_var = tk.StringVar(value="#000000")
        self.face_template = [[None] * FACE_WIDTH for _ in range(FACE_HEIGHT)]
        self.save_idx = 1
        for var in (self.skin_var, self.hair_var, self.hair_color_var,
                    self.shirt_var, self.face_color_var):
            var.trace_add("write", lambda *a: self.update_preview())

    def _build_layout(self):
        ctrl = tk.Frame(self.root)
        ctrl.pack(side=tk.LEFT, padx=10, pady=10)

        # Skin tone
        tk.Label(ctrl, text="Skin Tone:").grid(row=0, column=0)
        tk.OptionMenu(ctrl, self.skin_var, *[to_hex(c) for c in SKIN_TONES]).grid(row=0, column=1)

        # Hair style
        tk.Label(ctrl, text="Hair Style:").grid(row=1, column=0)
        tk.OptionMenu(ctrl, self.hair_var, "flat", "side_part", "messy").grid(row=1, column=1)

        # Hair color
        tk.Label(ctrl, text="Hair Color:").grid(row=2, column=0)
        tk.OptionMenu(ctrl, self.hair_color_var, *[to_hex(c) for c in HAIR_COLORS]).grid(row=2, column=1)

        # Shirt style
        tk.Label(ctrl, text="Shirt Style:").grid(row=3, column=0)
        tk.OptionMenu(ctrl, self.shirt_var, *SHIRT_STYLES).grid(row=3, column=1)

        # Face pixel color
        tk.Label(ctrl, text="Face Color:").grid(row=4, column=0)
        tk.Entry(ctrl, textvariable=self.face_color_var, width=10).grid(row=4, column=1)
        tk.Button(ctrl, text="Pick...",
                  command=lambda: self.face_color_var.set(colorchooser.askcolor()[1])
        ).grid(row=4, column=2)

        # Face editor grid
        tk.Label(ctrl, text=f"Paint Face ({FACE_WIDTH}×{FACE_HEIGHT}):").grid(row=5, column=0, columnspan=3)
        self.ed_canvas = tk.Canvas(ctrl, width=FACE_WIDTH*EDIT_SCALE, height=FACE_HEIGHT*EDIT_SCALE, bg="#333")
        self.ed_canvas.grid(row=6, column=0, columnspan=3)
        for r in range(FACE_HEIGHT):
            for c in range(FACE_WIDTH):
                self.ed_canvas.create_rectangle(
                    c*EDIT_SCALE, r*EDIT_SCALE,
                    (c+1)*EDIT_SCALE, (r+1)*EDIT_SCALE,
                    outline="#555", fill="#333"
                )
        self.ed_canvas.bind("<Button-1>", self._on_edit)
        self.ed_canvas.bind("<Button-3>", self._on_clear)

        tk.Button(ctrl, text="Clear Face", command=self.clear_all).grid(row=7, column=0, columnspan=3, pady=5)
        tk.Button(ctrl, text="Generate Sprite", command=self.generate).grid(row=8, column=0, columnspan=3, pady=5)
        tk.Button(ctrl, text="Animate", command=self.animator.toggle).grid(row=9, column=0, columnspan=3, pady=5)
        tk.Button(ctrl, text="Export GIF", command=self.export_gif).grid(row=10, column=0, columnspan=3, pady=5)

        self.canvas = tk.Canvas(self.root, width=CANVAS_SIZE, height=CANVAS_SIZE)
        self.canvas.pack(side=tk.RIGHT, padx=10, pady=10)

    def _on_edit(self, event):
        col, row = event.x // EDIT_SCALE, event.y // EDIT_SCALE
        color = self.face_color_var.get()
        if color.startswith('#') and len(color)==7:
            self.face_template[row][col] = color
            self.ed_canvas.create_rectangle(
                col*EDIT_SCALE, row*EDIT_SCALE,
                (col+1)*EDIT_SCALE, (row+1)*EDIT_SCALE,
                outline=to_hex(OUTLINE), fill=color
            )
            self.update_preview()

    def _on_clear(self, event):
        col, row = event.x // EDIT_SCALE, event.y // EDIT_SCALE
        self.face_template[row][col] = None
        self.ed_canvas.create_rectangle(
            col*EDIT_SCALE, row*EDIT_SCALE,
            (col+1)*EDIT_SCALE, (row+1)*EDIT_SCALE,
            outline="#555", fill="#333"
        )
        self.update_preview()

    def clear_all(self):
        for r in range(FACE_HEIGHT):
            for c in range(FACE_WIDTH):
                self.face_template[r][c] = None
        self.ed_canvas.delete("all")
        for r in range(FACE_HEIGHT):
            for c in range(FACE_WIDTH):
                self.ed_canvas.create_rectangle(
                    c*EDIT_SCALE, r*EDIT_SCALE,
                    (c+1)*EDIT_SCALE, (r+1)*EDIT_SCALE,
                    outline="#555", fill="#333"
                )
        self.update_preview()

    def build_sprite(self):
        skin = tuple(int(self.skin_var.get()[i:i+2],16) for i in (1,3,5))
        hair = tuple(int(self.hair_color_var.get()[i:i+2],16) for i in (1,3,5))
        return SpriteBuilder(
            self.face_template, skin, hair,
            self.hair_var.get(), self.shirt_var.get(),
            random.choice(CLOTHES_COLORS), random.choice(PANTS_COLORS)
        )

    def update_preview(self, frame=0):
        self.canvas.delete("all")
        img = self.build_sprite().render(frame)
        preview = img.resize((CANVAS_SIZE, CANVAS_SIZE), Image.NEAREST)
        tk_img = ImageTk.PhotoImage(preview)
        self.canvas._img = tk_img
        self.canvas.create_image(0, 0, anchor=tk.NW, image=tk_img)

    def _on_frame(self, frame):
        self.update_preview(frame)

    def generate(self):
        spr = self.build_sprite().to_sprite()
        img = spr.image()
        filename = f"custom_{self.save_idx:03d}.png"
        path = os.path.join(OUTPUT_DIR, filename)
        img.save(path)
        messagebox.showinfo("Saved", f"Sprite saved to {path}")
        self.save_idx += 1

    def export_gif(self):
        frames = [self.build_sprite().render(i) for i in range(self.animator.frames)]
        filename = f"anim_{self.save_idx:03d}.gif"
        path = os.path.join(OUTPUT_DIR, filename)
        self.animator.export_gif(path, frames)
        messagebox.showinfo("Exported", f"Animation saved to {path}")
        self.save_idx += 1

    def run(self):
        self.root.mainloop()
