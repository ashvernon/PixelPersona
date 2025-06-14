from PIL import Image, ImageDraw

# Constants defining sprite structure
SPRITE_SIZE = 32
HEAD_WIDTH = 10
HEAD_HEIGHT = 11
HEAD_Y = 0

OUTLINE = (0, 0, 0)
WHITE = (255, 255, 255)

class Sprite:
    """Represents a basic 32x32 pixel-art sprite."""

    def __init__(self, face_template, skin, hair_color, hair_style,
                 shirt_style, clothes_color, pants_color):
        self.face_template = face_template
        self.skin = skin
        self.hair_color = hair_color
        self.hair_style = hair_style
        self.shirt_style = shirt_style
        self.clothes_color = clothes_color
        self.pants_color = pants_color

    # Drawing helpers -----------------------------------------------------
    def draw_hair(self, draw, x, y):
        style = self.hair_style
        if style == "flat":
            draw.rectangle([x, y, x + HEAD_WIDTH - 1, y + 2],
                           fill=self.hair_color, outline=OUTLINE)
        elif style == "side_part":
            draw.rectangle([x, y, x + HEAD_WIDTH - 2, y + 2],
                           fill=self.hair_color, outline=OUTLINE)
        else:
            draw.rectangle([x, y, x + HEAD_WIDTH - 1, y + 3],
                           fill=self.hair_color, outline=OUTLINE)

    def draw_body(self, draw, x, y):
        w, h = 12, 10
        draw.rectangle([x, y, x + w - 1, y + h - 1],
                       fill=self.clothes_color, outline=OUTLINE)
        style = self.shirt_style
        if style == 'shirt_tie':
            cx = x + w // 2
            draw.line([(cx, y), (cx, y + 3)], fill=WHITE)
            draw.rectangle([cx - 1, y + 3, cx + 1, y + 4], fill=WHITE)
        elif style == 'lab_coat':
            draw.line([(x + 2, y + 2), (x + 2, y + h - 2)], fill=WHITE)
            draw.line([(x + w - 3, y + 2), (x + w - 3, y + h - 2)], fill=WHITE)
        elif style == 'dress':
            draw.polygon([(x, y + h), (x + w // 2, y + h - 4), (x + w, y + h)],
                         fill=self.clothes_color, outline=OUTLINE)

    def draw_arms(self, draw, x, y):
        draw.rectangle([x - 3, y, x - 1, y + 6],
                       fill=self.clothes_color, outline=OUTLINE)
        draw.rectangle([x - 3, y + 7, x - 1, y + 9],
                       fill=self.skin, outline=OUTLINE)
        rx = x + 12
        draw.rectangle([rx, y, rx + 2, y + 6],
                       fill=self.clothes_color, outline=OUTLINE)
        draw.rectangle([rx, y + 7, rx + 2, y + 9],
                       fill=self.skin, outline=OUTLINE)

    def draw_legs(self, draw, x, y):
        leg_w = 3
        left_x = x + 1
        draw.rectangle([left_x, y, left_x + leg_w - 1, y + 8],
                       fill=self.pants_color, outline=OUTLINE)
        draw.rectangle([left_x, y + 9, left_x + leg_w - 1, y + 9],
                       fill=self.skin, outline=OUTLINE)
        right_x = x + 12 - leg_w - 1
        draw.rectangle([right_x, y, right_x + leg_w - 1, y + 8],
                       fill=self.pants_color, outline=OUTLINE)
        draw.rectangle([right_x, y + 9, right_x + leg_w - 1, y + 9],
                       fill=self.skin, outline=OUTLINE)

    def draw_face(self, draw, x, y):
        for r, row in enumerate(self.face_template):
            for c, px in enumerate(row):
                if px:
                    col = tuple(int(px[i:i + 2], 16) for i in (1, 3, 5))
                    draw.point((x + 1 + c, y + 1 + r), fill=col)

    # Public API ----------------------------------------------------------
    def draw(self, draw):
        head_x = (SPRITE_SIZE - HEAD_WIDTH) // 2
        draw.rectangle([
            head_x, HEAD_Y,
            head_x + HEAD_WIDTH - 1,
            HEAD_Y + HEAD_HEIGHT - 1
        ], fill=self.skin, outline=OUTLINE)
        self.draw_hair(draw, head_x, HEAD_Y)
        self.draw_face(draw, head_x, HEAD_Y)
        body_x = (SPRITE_SIZE - 12) // 2
        body_y = HEAD_Y + HEAD_HEIGHT
        self.draw_body(draw, body_x, body_y)
        self.draw_arms(draw, body_x, body_y + 2)
        self.draw_legs(draw, body_x, body_y + 10)

    def image(self):
        img = Image.new('RGBA', (SPRITE_SIZE, SPRITE_SIZE), (0, 0, 0, 0))
        d = ImageDraw.Draw(img)
        self.draw(d)
        return img
