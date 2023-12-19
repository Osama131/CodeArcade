import pygame


class Background:
    def __init__(self, image_path: str, speed: int, width: int, height: int):
        self.image = pygame.image.load(image_path)
        self.image = pygame.transform.scale(self.image, (width, height))
        self.speed = speed
        self.seperation_line_y = 0
        self.width = width
        self.max_height = height

    def draw(self, window: pygame.Surface):
        # draw the background image starting from seperation line
        window.blit(self.image, (0, self.seperation_line_y))
        # if seperation line is not at the top of the window, draw another image ending at seperation line
        if self.seperation_line_y != 0:
            window.blit(
                self.image, (0, self.seperation_line_y - self.max_height))

        # update seperation line for next frame
        self.seperation_line_y = (
            self.speed + self.seperation_line_y) % self.max_height
