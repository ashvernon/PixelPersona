import random
from PIL import Image, ImageDraw
from .constants import SPRITE_SIZE, HEAD_WIDTH, HEAD_HEIGHT, HEAD_Y, BODY_WIDTH, BODY_HEIGHT, LEG_WIDTH, OUTLINE
from .drawing import Drawer
from .sprite import Sprite

class SpriteBuilder:
    def __init__(self, face_template, skin, hair, hair_style, shirt_style, clothes, pants):
        self.face_template = face_template
        self.skin = skin
        self.hair = hair
        self.hair_style = hair_style
        self.shirt_style = shirt_style
        self.clothes = clothes
        self.pants = pants

    @classmethod
    def random(cls, face_template, skin, hair_style, shirt_style):
        from .constants import CLOTHES_COLORS, PANTS_COLORS
        clothes = random.choice(CLOTHES_COLORS)
        pants = random.choice(PANTS_COLORS)
        return cls(face_template, skin, hair, hair_style, shirt_style, clothes, pants)

    def render(self, frame: int = 0):
        img = Image.new("RGBA", (SPRITE_SIZE, SPRITE_SIZE), (0, 0, 0, 0))
        draw = ImageDraw.Draw(img)

        # Draw head
        head_x = (SPRITE_SIZE - HEAD_WIDTH) // 2
        draw.rectangle(
            [head_x, HEAD_Y, head_x + HEAD_WIDTH - 1, HEAD_Y + HEAD_HEIGHT - 1],
            fill=self.skin,
            outline=OUTLINE,
        )
        # Hair
        Drawer.draw_hair(draw, head_x, HEAD_Y, self.hair, self.hair_style)

        # Face pixels
        for r, row in enumerate(self.face_template):
            for c, px in enumerate(row):
                if px:
                    col = tuple(int(px[i : i + 2], 16) for i in (1, 3, 5))
                    draw.point((head_x + 1 + c, HEAD_Y + 1 + r), fill=col)

        # Draw body, arms, legs
        body_x = (SPRITE_SIZE - BODY_WIDTH) // 2
        body_y = HEAD_Y + HEAD_HEIGHT
        Drawer.draw_body(draw, body_x, body_y, self.clothes, self.shirt_style)
        Drawer.draw_arms(draw, body_x, body_y + 2, self.skin, self.clothes, frame)
        Drawer.draw_legs(draw, body_x, body_y + BODY_HEIGHT, self.skin, self.pants, frame)

        return img

    def to_sprite(self):
        return Sprite(
            self.face_template,
            self.skin,
            self.hair,
            self.hair_style,
            self.shirt_style,
            self.clothes,
            self.pants,
        )
