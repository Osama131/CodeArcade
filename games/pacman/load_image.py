import os

import pygame


def load_image(fileName):
    if os.path.isfile(fileName):
        image = pygame.image.load(fileName)
        image = image.convert_alpha()
        return image
    else:
        raise Exception("Error loading image: " + fileName + " - Check filename and path?")
