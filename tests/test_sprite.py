import os
import sys
from PIL import Image

sys.path.insert(0, os.path.dirname(os.path.dirname(__file__)))
from sprite import Sprite


def make_frames(count, size=(32, 32)):
    return [Image.new("RGBA", size, (i, i, i, 255)) for i in range(count)]


def test_sprite_render_size():
    frames = make_frames(2)
    sprite = Sprite(frames)
    img = sprite.render()
    assert img.size == (32, 32)


def test_animation_loops_frames():
    frames = make_frames(3)
    sprite = Sprite(frames)

    # advance through all frames plus one to ensure loop
    sprite.next_frame()  # -> frame 1
    assert sprite.render() == frames[1]

    sprite.next_frame()  # -> frame 2
    assert sprite.render() == frames[2]

    sprite.next_frame()  # loops back to frame 0
    assert sprite.render() == frames[0]
