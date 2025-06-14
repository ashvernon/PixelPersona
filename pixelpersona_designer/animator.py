import tkinter as tk
from .constants import FRAME_DELAY

class SpriteAnimator:
    def __init__(self, update_callback, frames=2):
        self.update_callback = update_callback
        self.frames = frames
        self.running = False
        self._after_id = None
        self.frame = 0

    def _tick(self):
        # call update with current frame
        self.update_callback(self.frame)
        # advance frame counter
        self.frame = (self.frame + 1) % self.frames
        # schedule next tick on the GUI root
        root = self.update_callback.__self__.root
        self._after_id = root.after(FRAME_DELAY, self._tick)

    def start(self):
        if not self.running:
            self.running = True
            self.frame = 0
            self._tick()

    def stop(self):
        if self.running:
            self.running = False
            if self._after_id:
                root = self.update_callback.__self__.root
                root.after_cancel(self._after_id)
                self._after_id = None

    def toggle(self):
        if self.running:
            self.stop()
        else:
            self.start()

    def export_gif(self, path, frames, loops=0):
        frames[0].save(
            path,
            save_all=True,
            append_images=frames[1:],
            duration=FRAME_DELAY,
            loop=loops,
        )
