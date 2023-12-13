import os
import subprocess
from typing import List

import pygame.surface
from pygame import Surface

from constants import GAME_HEIGHT, SPACE_FOR_NAMES, GAME_WIDTH

def load_image(fileName):
    if os.path.isfile(fileName):
        image = pygame.image.load(fileName)
        image = image.convert_alpha()
        return image
    else:
        raise Exception("Error loading image: " + fileName + " - Check filename and path?")


def fit_image_to_space(image):
    fitted_image = image
    max_height = GAME_HEIGHT / 2 + 50
    max_width = GAME_WIDTH - SPACE_FOR_NAMES - 2
    image_height = image.get_height()
    image_width = image.get_width()
    border_size = 5

    if image_width <= max_width and image_height <= max_height:
        fitted_image = image
    elif image_width - max_width > image_height - max_height:
        scale = image_width / max_width
        new_image_width = image_width / scale - 150
        new_image_height = image_height / scale - 50
        fitted_image = pygame.transform.smoothscale(image, (new_image_width - border_size * 2, new_image_height - border_size * 2))
    elif image_width - max_width < image_height - max_height:
        scale = image_height / max_height
        new_image_width = image_width / scale - 50
        new_image_height = image_height / scale - 50
        fitted_image = pygame.transform.smoothscale(image, (new_image_width - border_size * 2, new_image_height - border_size * 2))
    return fitted_image


class ArcadeGame:

    def __init__(self, name, location, difficulty, time_needed, example_image, description, additional_description):
        self.name = name
        self.location = location
        self.difficulty = difficulty
        self.time_needed = time_needed
        self.description = description + ' ' + additional_description
        #self.additional_description = additional_description
        self.example_image = load_image(example_image)
        #self.font = pygame.font.SysFont("Bahnschrift", 26,)
        self.font = pygame.font.Font('assets/font/Pixeltype.ttf', 40)
        self.detail_screen = pygame.surface.Surface((GAME_HEIGHT, GAME_WIDTH - SPACE_FOR_NAMES))
        self.init_detail_screen()

    def init_detail_screen(self):
        detail_screen_size = (self.detail_screen.get_width(), self.detail_screen.get_height())
        self.detail_screen = pygame.Surface(detail_screen_size, pygame.SRCALPHA)

        self.add_text("Game: " + str(self.name), 0)
        self.add_text("Estimated time: " + str(self.time_needed), 1)
        self.add_text("Difficulty levels: " + str(self.difficulty), 2)
        self.add_text(str(self.description), 3)
        #self.add_text(str(self.additional_description), 4)

        fitted_image = fit_image_to_space(self.example_image)
        border_color = (210,181,255)
        border_size = 5
        border_surface = pygame.Surface((fitted_image.get_width() + border_size * 2, fitted_image.get_height() + border_size * 2))
        border_surface.fill(border_color)

        border_surface.blit(fitted_image, (border_size, border_size))

        self.detail_screen.blit(border_surface, (50 , GAME_HEIGHT / 2  - 80))

    def add_text(self, text_to_add, row):
        label_color = (246,219,109)
        value_color = ("white")
        background_color = (93,51,189)

        if text_to_add in [str(self.description)]:
            words = text_to_add.split()
            lines = []
            while len(words) > 0:
                line_words = []
                while len(words) > 0:
                    line_words.append(words.pop(0))
                    fw, fh = self.font.size(' '.join(line_words + words[:1]))
                    if fw >  GAME_WIDTH - SPACE_FOR_NAMES - 110:
                        break

                line = ' '.join(line_words)
                lines.append(line)
            for text in lines:
                text = self.font.render(text, True, value_color)
                text_rect = text.get_rect()
                text_surface = pygame.Surface((text_rect.width, text_rect.height))
                text_surface.fill(background_color)
                text_surface.blit(text, (0, 0))
                text_rect.topleft = (50, 50 + row * (text_rect.height + 10))
                self.detail_screen.blit(text_surface, text_rect)
                label = ""
                value = ""
                row+=1
        else:
            if ":" in text_to_add:
                label, value = text_to_add.split(":", 1)
            else:
                label = text_to_add
                value = ""

        label_text = self.font.render(label + (":" if label else ""), True, label_color)
        value_text = self.font.render(value, True, value_color)
        label_text_rect = label_text.get_rect()
        value_text_rect = value_text.get_rect()

        label_text_surface = pygame.Surface((label_text_rect.width, label_text_rect.height))
        label_text_surface.fill(background_color)
        label_text_surface.blit(label_text, (0, 0))
        value_text_surface = pygame.Surface((value_text_rect.width, value_text_rect.height))
        value_text_surface.fill(background_color)
        value_text_surface.blit(value_text, (0, 0))

        label_text_rect.topleft = (50, 50 + row * (label_text_rect.height + 10))
        value_text_rect.topleft = (50 + label_text_rect.width, 50 + row * (value_text_rect.height + 10))
        self.detail_screen.blit(label_text_surface, label_text_rect)
        self.detail_screen.blit(value_text_surface, value_text_rect)

    def get_details(self) -> Surface:
        return self.detail_screen

    def start(self):
        working_dir = os.path.dirname(self.location)
        filename = os.path.basename(self.location)
        subprocess.run(["python", filename], cwd=working_dir)

    def get_name(self) -> str:
        return self.name
