import pygame
class Life(pygame.sprite.Sprite):
    image = pygame.image.load("assets/graphics/heart16.png")
    def __init__(self, pos):
        super().__init__()
        self.rect = self.image.get_rect()
        self.rect.center = pos