import tkinter as tk
from PIL import Image, ImageTk

class SpriteAnimator:
    """Simple animator that cycles through a list of PIL images."""

    def __init__(self, canvas: tk.Canvas, frames, delay=200, scale=6):
        self.canvas = canvas
        self.delay = delay
        self.frames = [
            ImageTk.PhotoImage(
                img.resize((img.width * scale, img.height * scale), Image.NEAREST)
            )
            for img in frames
        ]
        self.index = 0
        self.running = False

    def start(self):
        if not self.running:
            self.running = True
            self._animate()

    def stop(self):
        self.running = False

    def _animate(self):
        if not self.running:
            return
        frame = self.frames[self.index]
        self.canvas.delete("all")
        self.canvas.create_image(0, 0, anchor=tk.NW, image=frame)
        self.canvas.image = frame
        self.index = (self.index + 1) % len(self.frames)
        self.canvas.after(self.delay, self._animate)
