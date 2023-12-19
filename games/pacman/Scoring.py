import pygame
from pygame.sprite import Sprite


points = {
    "pill": 10,
    "ghost": 200,
    "energizer": 50,
    "cherry": 100,
    "strawberry": 300
}


class Scoring(Sprite):
    def __init__(self, text, pos, initial_score=0):
        Sprite.__init__(self)
        self.text = text
        self.score = initial_score
        self.ghosts_eaten = 0
        self.font = pygame.font.SysFont("Calibri", 36)
        self.pos = pos
        self.display_score()

# Shows scores on top of screen
    def display_score(self):
        # displays the score saved in the variable self.score
        self.textSurf = self.font.render(f"{self.text}{self.score:03d}", 1, "white")
        self.image = pygame.Surface((self.textSurf.get_width(), self.textSurf.get_height()))
        self.image.blit(self.textSurf, [0, 0])
        self.rect = self.image.get_rect()
        self.rect.topleft = self.pos

    # values for eaten may be:
    # pill, energizer, ghost, cherry, strawberry
    def add_points_for(self, eaten: str):
        # CHALLENGE 1.1
        points_to_add = points[eaten]
        self.score += points_to_add
        # CHALLENGE 1.1 END
        self.display_score()

