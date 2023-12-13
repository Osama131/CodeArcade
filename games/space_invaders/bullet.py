import pygame

class Bullet(pygame.sprite.Sprite):
    image = pygame.image.load("assets/graphics/bullet.png")
    sound = pygame.mixer.Sound("assets/audio/laser1.mp3")

    def __init__(self, pos, speed):
        super().__init__()
        self.image = pygame.transform.rotate(self.image)
        self.rect = self.image.get_rect()
        self.rect.center = pos
        self.speed = speed
        self.sound.play()

    def update(self):
        self.rect.y += self.speed
        if self.rect.y <= 0:
            self.kill()
