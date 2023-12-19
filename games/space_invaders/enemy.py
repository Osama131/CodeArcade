import pygame
from bullet import Bullet
from spritesheet import spritesheet


class Enemy(pygame.sprite.Sprite):
    def __init__(self, enemy_spritesheet, pos, constraints, level, dir,rank=0):
        super().__init__()
        if rank == 1:
            enemy_image = enemy_spritesheet.image_at((1300, 7, 300, 232), -1)
        elif rank == 0:
            enemy_image = enemy_spritesheet.image_at((992, 7, 215, 232), -1)

        self.dead = False
        # scale the image to 1/3 of its original size
        self.image = pygame.transform.scale(enemy_image, (50, 50))
        self.rect = self.image.get_rect()
        self.rect.bottomleft = pos
        self.constraints = constraints
        self.speed_y = 0.75
        if dir == "right":
            self.speed_x = 1
        elif dir == "left":
            self.speed_x = -1
        self.rank = rank + 1
        self.health = self.rank * level
        self.explosion_frame = 0

    def update(self):
        if not self.dead:
            self.rect.y += self.speed_y
            if self.rect.right >= self.constraints[0] or self.rect.left <= 0:
                self.speed_x *= -1
            self.rect.x += self.speed_x

            if self.rect.top > self.constraints[1]:
                self.kill()
        else:
            if self.explosion_frame < len(self.explosion_images):
                self.image = self.explosion_images[self.explosion_frame]
                # image should appear at the same position as the enemy and centered in the enemy
                self.rect = self.image.get_rect(
                    center=(self.rect.x + self.rect.width/2, self.rect.y + self.rect.height/2))
                self.explosion_frame += 1
            else:
                self.kill()

    def get_position(self):
        return (self.rect.x, self.rect.y)

    def explode(self):
        if not self.dead:
            self.dead = True
            self.explosion_sound.play()

    def set_explosion_images(self, images):
        self.explosion_images = images

    def set_explosion_sound(self, sound):
        self.explosion_sound = sound


class Boss(Enemy):
    def __init__(self, screen_width, enemy_spritesheet, constraints, level, dir):
        super().__init__(enemy_spritesheet, (screen_width/2, 50), constraints, level, dir)
        enemy_image = enemy_spritesheet.image_at((1700, 7, 330, 232), -1)
        self.image = pygame.transform.scale(enemy_image, (70, 70))
        self.constraints = constraints
        self.rect = self.image.get_rect(topleft=(screen_width/2, -10))
        self.health = 3 * level
        self.last_bullet_time = 0
        self.fire_rate = 1500

    def fire_bullet(self, bullets):
        bullet_x, bullet_y = self.rect.center
        bullets.add(Bullet((bullet_x +2, bullet_y), 4, 180))

    def update(self, bullets):
        super().update()
        current_time = pygame.time.get_ticks()
        if current_time - self.last_bullet_time > self.fire_rate:
            self.fire_bullet(bullets)
            self.last_bullet_time = current_time  # Update the time since the last bullet was fired

