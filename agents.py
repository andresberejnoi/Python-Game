import pygame


class BaseAgent(pygame.sprite.Sprite):
    def __init__(self, size=1, color=(30,30,30), x=100, y=100, width=50,height=50):
        super().__init__()

        self.x      = x
        self.y      = y
        self.color  = color
        self.width  = width
        self.height = height

    def update(self, screen):
        rect_bounds = (self.x, self.y, self.width, self.height)
        pygame.draw.rect(screen, self.color, rect_bounds)

class Player(BaseAgent):
    def __init__(self, screen, color=(255, 0, 255), width=50, height=50):
        x = (screen.get_width()  / 2) - (width  / 2)
        y = (screen.get_height() / 2) - (height / 2)

        super().__init__(1, color, x, y, width, height)