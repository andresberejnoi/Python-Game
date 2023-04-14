'''
This class helps in loading images from a spritesheet for animations. 
I followed a tutorial used for this video:
    * https://youtu.be/nXOVcOBqFwM
'''

import pygame
from config import *

class SpriteSheet():
    def __init__(self, image, single_width=24, single_height=24, num_cols=8, num_rows=1, scale=1):
        self.sheet = image
        self.single_width  = single_width
        self.single_height = single_height

        self.num_cols = num_cols
        self.num_rows = num_rows

        self.scale = scale

    @staticmethod
    def load_from_file(spritesheet_file, single_width=24, single_height=24, num_cols=8, num_rows=1, scale=1):
        img = pygame.image.load(spritesheet_file).convert_alpha()
        return SpriteSheet(img, single_width=single_width, single_height=single_height, num_cols=num_cols, num_rows=num_rows, scale=scale)

    def get_image(self, frame_pos, width=None, height=None, scale=None, chromakey=(0,0,0)):
        if width is None:
            width = self.single_width
        if height is None:
            height = self.single_height

        if isinstance(frame_pos, tuple) or isinstance(frame_pos, list):
            frame_col = frame_pos[0]
            frame_row = frame_pos[1]
        elif isinstance(frame_pos, int):
            frame_col = frame_pos


        if scale is None:
            scale = self.scale   #use default scale if it is not provided

        img = pygame.Surface((width, height)).convert_alpha()
        img.blit(self.sheet, (0,0), ((frame_col * width), (frame_row * height), width, height))

        img = pygame.transform.scale(img, (width * scale, height * scale))
        print("Setting Chromakey to:", chromakey)
        img.set_colorkey(chromakey)

        return img
    
    def get_all_sprites(self, scale=1, chromakey=BLACK) -> list:
        """Returns a list of all sprites in spritesheet, based on self.num_cols x self.num_rows"""
        sprites_list = []
        for col in range(self.num_cols):
            for row in range(self.num_rows):
                img = self.get_image((col,row), scale=scale, chromakey=chromakey)
                sprites_list.append(img)

        return sprites_list