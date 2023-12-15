import pygame
from bullet import Bullet

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
        self.speed_y = 0
        self.speed_x = 0
        self.bullets = []

    def move(self, keys, constraints):
        # TASK 1.1 - player movements
        if(keys[pygame.K_UP] or keys[pygame.K_w]):
            self.speed_y = -5
        elif(keys[pygame.K_DOWN] or keys[pygame.K_s]):
            self.speed_y = 5
        else: self.speed_y = 0

        if(keys[pygame.K_RIGHT] or keys[pygame.K_d]):
            self.speed_x = 5
        elif(keys[pygame.K_LEFT] or keys[pygame.K_a]):
            self.speed_x = -5
        else: self.speed_x = 0

        # clamp player coordinates to screen bounds
        self.rect.x = min(self.rect.x, constraints[0] - self.rect.width)
        self.rect.y = min(self.rect.y, constraints[1] - self.rect.height)
        self.rect.x = max(self.rect.x, 0)
        self.rect.y = max(self.rect.y, 0)

    def update(self, keys, bullets):

        # TASK 1.2 - fire bullets
        if(keys[pygame.K_SPACE]):
            self.bullets.append(Bullet(self.rect.midbottom, -10))
        # Move the player
        self.rect.x += self.speed_x
        self.rect.y += self.speed_y
        self.move(keys, self.constraints)

        # Update Bulltes
        for b in self.bullets:
            b.update()

