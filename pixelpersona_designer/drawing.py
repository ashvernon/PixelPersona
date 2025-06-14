# pixelpersona_designer/drawing.py

from PIL import ImageDraw
from .constants import HEAD_WIDTH, HEAD_HEIGHT, HEAD_Y, BODY_WIDTH, BODY_HEIGHT, LEG_WIDTH, OUTLINE

class Drawer:
    @staticmethod
    def draw_hair(draw: ImageDraw, x: int, y: int, color: tuple, style: str):
        # indent the whole body of this method by 8 spaces (one level inside the class)
        height = 2 if style == "flat" else (2 if style == "side_part" else 3)
        width  = HEAD_WIDTH - 1 if style != "side_part" else HEAD_WIDTH - 2
        draw.rectangle([x, y, x + width, y + height], fill=color, outline=OUTLINE)

    @staticmethod
    def draw_body(draw: ImageDraw, x: int, y: int, clothes: tuple, style: str):
        w, h = BODY_WIDTH, BODY_HEIGHT
        draw.rectangle([x, y, x + w - 1, y + h - 1], fill=clothes, outline=OUTLINE)
        if style == "shirt_tie":
            cx = x + w // 2
            # 1) draw the knot 4px higher (was y+3→y+4, now y−1→y+0)
            draw.rectangle(
                [cx - 1, y - 1, cx + 1, y], 
                fill=(255, 255, 255), 
                outline=False
            )
            # 2) draw the tail starting just below the knot, ending 4px above the bottom
            draw.line(
                [(cx, y), (cx, y + h - 4)],
                fill=(255, 255, 255)
    )
        elif style == "lab_coat":
            draw.line([(x + 2, y + 2), (x + 2, y + h - 2)], fill=(255,255,255))
            draw.line([(x + w - 3, y + 2), (x + w - 3, y + h - 2)], fill=(255,255,255))
        elif style == "dress":
            draw.polygon(
                [(x, y + h), (x + w // 2, y + h - 4), (x + w, y + h)],
                fill=clothes,
                outline=OUTLINE,
            )

    @staticmethod
    def draw_arms(draw: ImageDraw, x: int, y: int, skin: tuple, clothes: tuple, frame: int = 0):
        left_off  = frame % 2
        right_off = 1 - left_off
        # left arm
        draw.rectangle([x - 3, y + left_off, x - 1, y + 6 + left_off], fill=clothes, outline=OUTLINE)
        draw.rectangle([x - 3, y + 7 + left_off, x - 1, y + 9 + left_off], fill=skin,    outline=OUTLINE)
        # right arm
        rx = x + BODY_WIDTH
        draw.rectangle([rx, y + right_off, rx + 2, y + 6 + right_off], fill=clothes, outline=OUTLINE)
        draw.rectangle([rx, y + 7 + right_off, rx + 2, y + 9 + right_off], fill=skin,    outline=OUTLINE)

    @staticmethod
    def draw_legs(draw: ImageDraw, x: int, y: int, skin: tuple, pants: tuple, frame: int = 0):
        left_x  = x + 1
        right_x = x + BODY_WIDTH - LEG_WIDTH - 1
        left_off, right_off = frame % 2, 1 - (frame % 2)
        # left leg
        draw.rectangle([left_x, y + left_off, left_x + LEG_WIDTH - 1, y + 8 + left_off],
                       fill=pants, outline=OUTLINE)
        draw.rectangle([left_x, y + 9 + left_off, left_x + LEG_WIDTH - 1, y + 9 + left_off],
                       fill=skin,  outline=OUTLINE)
        # right leg
        draw.rectangle([right_x, y + right_off, right_x + LEG_WIDTH - 1, y + 8 + right_off],
                       fill=pants, outline=OUTLINE)
        draw.rectangle([right_x, y + 9 + right_off, right_x + LEG_WIDTH - 1, y + 9 + right_off],
                       fill=skin,  outline=OUTLINE)
