import pygame

class Player(pygame.sprite.Sprite):
    def __init__(self, image, pos, constraints):
        super().__init__()
        self.image = image
        self.width = self.image.get_width() // 3
        self.height = self.image.get_height() // 3
        self.image = pygame.transform.scale(self.image, (self.width, self.height))
        self.constraints = constraints
        self.rect = self.image.get_rect()
        self.rect.midbottom = pos
        self.speed = 5

    def move(self, keys, constraints):
        # TASK 1.1 - player movements
        pass

    def update(self, keys, bullets):

        # TASK 1.2 - fire bullets
        # Move the player
        self.move(keys, self.constraints)

