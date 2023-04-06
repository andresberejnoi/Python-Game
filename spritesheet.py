import pygame

class SpriteSheet():
    def __init__(self, image, single_width=24, single_height=24):
        self.sheet = image
        self.single_width  = single_width
        self.single_height = single_height

    def get_image(self, frame_pos, width=None, height=None, scale=1, chromakey=(0,0,0)):
        if width is None:
            width = self.single_width
        if height is None:
            height = self.single_height

        if isinstance(frame_pos, tuple) or isinstance(frame_pos, list):
            frame_col = frame_pos[0]
            frame_row = frame_pos[0]
        elif isinstance(frame_pos, int):
            frame_col = frame_pos

        img = pygame.Surface((width, height)).convert_alpha()
        img.blit(self.sheet, (0,0), ((frame_col * width), (frame_row * height), width, height))

        img = pygame.transform.scale(img, (width * scale, height * scale))
        img.set_colorkey(chromakey)

        return img