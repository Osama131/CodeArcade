import pygame


class Background:
    def __init__(self, image_path: str, speed: int, width: int, height: int):
        self.image = pygame.image.load(image_path)
        self.image = pygame.transform.scale(self.image, (width, height))
        self.separation_line_y = 0
        self.width = width
        self.max_height = height

    def draw(self, window: pygame.Surface):
        # TASK 6.2 - Make the background move
        # TASK 6.2 - HINT
        # Draw the background image starting from separation line
        # If separation line is not at the top of the window, draw another image ending at seperation line
        # Update separation line for next frame
        pass
