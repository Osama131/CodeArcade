import pygame

class Star:
    def __init__(self, x, y, image_path, size):
        self.x = x
        self.y = y
        self.image = pygame.image.load(image_path)
        self.image = pygame.transform.smoothscale(self.image, size)

    def draw(self, screen):
        star_rect = self.image.get_rect(center=(self.x, self.y))
        screen.blit(self.image, star_rect)