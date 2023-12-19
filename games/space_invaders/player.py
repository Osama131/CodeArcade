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
        self.speed = 5
        self.fire_rate = 200
        self.last_bullet_time = 0
    
    def fire_bullet(self, bullets):
        bullet_x = self.rect.centerx 
        bullet_y = self.rect.y
        bullets.add(Bullet((bullet_x, bullet_y), -10, 0))

    def move(self, keys, constraints):
        if keys[pygame.K_LEFT] or keys[pygame.K_a]:
            if self.rect.left > 0:
                self.rect.x -= self.speed
        elif keys[pygame.K_RIGHT] or keys[pygame.K_d]:
            if self.rect.right < constraints[0]:
                self.rect.x += self.speed
        if keys[pygame.K_UP] or keys[pygame.K_w]:
            if self.rect.top > constraints[1] // 2:
                self.rect.y -= self.speed
        elif keys[pygame.K_DOWN] or keys[pygame.K_s]:
            if self.rect.bottom < constraints[1]:
                self.rect.y += self.speed

    def update(self, keys, bullets):

        # Fire bullets if the space key is pressed and enough time has elapsed since the last bullet was fired
        if keys[pygame.K_SPACE]:
            current_time = pygame.time.get_ticks()
            if  current_time - self.last_bullet_time > self.fire_rate:
                self.fire_bullet(bullets)
                self.last_bullet_time = current_time  # Update the time since the last bullet was fired
    
        # Move the player
        self.move(keys, self.constraints)

