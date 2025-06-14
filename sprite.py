from PIL import Image
from typing import List

class Sprite:
    """A simple sprite supporting multiple frames for animation."""

    def __init__(self, frames: List[Image.Image]):
        if not frames:
            raise ValueError("Sprite requires at least one frame")
        self._frames = frames
        self._index = 0

    @property
    def size(self):
        """Return the (width, height) of the sprite frames."""
        return self._frames[0].size

    def render(self) -> Image.Image:
        """Return the current frame image."""
        return self._frames[self._index]

    def next_frame(self) -> None:
        """Advance to the next frame, looping when reaching the end."""
        self._index = (self._index + 1) % len(self._frames)

    @property
    def frame_index(self) -> int:
        return self._index
