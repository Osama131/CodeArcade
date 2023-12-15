import pygame
import random
from bullet import Bullet
from spritesheet import spritesheet


class Enemy(pygame.sprite.Sprite):
    def __init__(self, enemy_spritesheet, pos, constraints, rank, level):
        super().__init__()
        # TASK 2.1 - Add a second type of basic enemy
        # TASK 2.2 - Implement health system based on rank
        # TASK 2.3 - Increase health of the enemies based on the level of the player

        enemy_image = enemy_spritesheet.image_at((1300, 7, 300, 232), -1)

        self.dead = False
        # scale the image to 1/3 of its original size
        self.image = pygame.transform.scale(enemy_image, (50, 50))
        self.rect = self.image.get_rect()
        self.rect.bottomleft = pos
        self.constraints = constraints
        self.timer = 0
        self.speed_x = random.randint(-5, 5)
        self.speed_y = 0.75
        self.rank = rank
        self.level = level
        self.health = self.rank

    def update(self):
        if not self.dead:
            self.timer += 1
            self.rect.y += self.speed_y
            self.rect.x += self.speed_x
            # TASK 2.4 - Make enemies move left and right
            if self.rect.left < 0 or self.rect.right > self.constraints[0]:
                self.speed_x = -self.speed_x
                self.timer = 0
            elif self.timer % 120 == 0:
                self.speed_x = -self.speed_x
            

            

            if self.rect.top > self.constraints[1]:
                self.kill()
        else:
            self.image = self.explosion_images[0]
            self.rect = self.image.get_rect()
            self.rect.center = self.get_position()
            self.explosion_sound.play()
            pass

    def get_position(self):
        return (self.rect.x, self.rect.y)

    def set_explosion_images(self, images):
        self.explosion_images = images

    def set_explosion_sound(self, sound):
        self.explosion_sound = sound

    def set_health(self):
        self.health = self.rank+self.level*0.5

    def hit(self):
        self.health -= 1
        if self.health <= 0:
            self.kill()
            self.dead = True
    
    def kill(self) -> None:
        return super().kill()

    
    

# TASK 5 - Add special enemy - Boss
# Boss should look bigger than normal enemies, move faster and have more health
