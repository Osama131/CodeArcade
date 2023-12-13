from typing import List

import pygame
import random
from pygame import Surface
from pygame.font import Font

import ArcadeGame
from Star import Star
from constants import SPACE_FOR_NAMES, GAME_HEIGHT, GAME_WIDTH

ENTER_KEY: int = 13

class ArcadeMachine:

    def __init__(self, bg_color):
        self.font: Font
        self.height = GAME_HEIGHT
        self.width = GAME_WIDTH
        self.clock = None
        self.space_for_names = SPACE_FOR_NAMES
        self.screen: Surface
        self.selected_game: int = 0
        self.background = bg_color
        self.running = False
        self.arcade_games: List[ArcadeGame] = list()
        self.__height_start = 0
        self.stars = []
        self.star_rects = []
        self.create_stars()

    def game_init(self):
        pygame.init()
        pygame.display.set_caption("Arcade Machine")
        self.screen: Surface = pygame.display.set_mode((self.width, self.height))
        self.clock = pygame.time.Clock()
        self.font: Font = pygame.font.Font('assets/font/Pixeltype.ttf', 60)
        self.title_font: Font = pygame.font.Font('assets/font/Pixeltype.ttf', 100)
        self.selection_sound = pygame.mixer.Sound("assets/sound/selection.wav")
        self.bridge = pygame.image.load("assets/graphics/bridge.png")
        self.building_left = pygame.image.load("assets/graphics/building1.png")
        self.building_left2 = pygame.image.load("assets/graphics/building2.png")
        self.building_right = pygame.image.load("assets/graphics/building3.png")
        self.building_right2 = pygame.image.load("assets/graphics/building4.png")
        self.instructions = pygame.image.load("assets/graphics/start.png")
        self.mouse = pygame.image.load("assets/graphics/mouse.png")
        self.billboard = pygame.image.load("assets/graphics/billboard.png")
        

    def register_game(self, game: ArcadeGame):
        self.arcade_games.append(game)
        self.__height_start = (self.height / 2) - (len(self.arcade_games) * 75 / 2)

    def game_run(self):
        pygame.mixer.music.load('assets/sound/background.mp3')
        pygame.mixer.music.play(-1,0,1500)
        pygame.mixer.music.set_volume(0.2)

        self.running = True
        while self.running:
            self.handle_events()
            self.set_background()
            self.draw_current_scene()
            pygame.display.flip()
            self.clock.tick(60)  # limits FPS to 60

            keys = pygame.key.get_pressed()
            if keys[pygame.K_ESCAPE]:
                self.running = False

        pygame.quit()

    def draw_current_scene(self):
        self.draw_stars()
        pygame.draw.line(self.screen, (210,181,255), (self.space_for_names ,0), (self.space_for_names ,self.height), 5)
        self.city_images()
        self.instruction_image()
        self.display_hackathon_name()
        for game_index in range(len(self.arcade_games)):
            game = self.arcade_games[game_index]
            self.display_game_name(game.get_name(), game_index)
        cur_detail_screen = self.arcade_games[self.selected_game].get_details()
        self.screen.blit(cur_detail_screen, (self.space_for_names + 2, 0))

    def set_background(self):
        self.screen.fill(self.background)

    def handle_events(self):
        for event in pygame.event.get():
            self.handle_event(event)

    def handle_event(self, event):
        if event.type == pygame.QUIT:
            self.running = False
        elif event.type == pygame.KEYDOWN:
            self.handle_game_selection(event)
        elif event.type == pygame.WINDOWMINIMIZED:
            pygame.mixer.music.pause()
        elif event.type == pygame.WINDOWRESTORED:
            pygame.mixer.music.unpause()


    def handle_game_selection(self, event):
        if (event.key == pygame.K_UP or event.key == pygame.K_w): 
            self.selection_sound.play()
            self.selected_game -= 1
        elif (event.key == pygame.K_DOWN or event.key == pygame.K_s): 
            self.selection_sound.play()
            self.selected_game += 1
        elif event.key == ENTER_KEY:
            pygame.mixer.music.fadeout(1500)
            self.arcade_games[self.selected_game].start()
            pygame.mixer.music.play(-1,0,1500)
            pygame.mixer.music.set_volume(0.2)
        self.selected_game %= len(self.arcade_games) # start on beginning when selecting element after last one

    def create_stars(self):
        self.stars = [self.place_star("assets/graphics/star.png", (15, 15)) for _ in range(10)]
        self.stars += [self.place_star("assets/graphics/star1.png", (10, 10)) for _ in range(7)]

    def place_star(self, image_path, size):
        while True:
            x = random.randint(0, self.width)
            y = random.randint(0, self.height)
            star_rect = pygame.Rect(x, y, size[0], size[1])
            if not any(existing_star_rect.colliderect(star_rect) for existing_star_rect in self.star_rects):
                self.star_rects.append(star_rect)
                return Star(x, y, image_path, size)

    def draw_stars(self):
        for star in self.stars:
            star.draw(self.screen)

    def create_text_surface(self, text, text_color, background_color):
        text_render = self.font.render(text, False, text_color)
        text_rect = text_render.get_rect()
        text_surface = pygame.Surface((text_rect.width, text_rect.height))
        text_surface.fill(background_color)
        text_surface.blit(text_render, (0, 0))
        return text_surface, text_rect

    def display_hackathon_name(self):
        title = "CODE ARCADE"
        text_surface, text_rect = self.create_text_surface(title, (246,219,109), self.background)
        text_rect.center = (self.space_for_names / 2, 60)
        self.screen.blit(text_surface, text_rect)

        original_width, original_height = self.billboard.get_size()
        new_height = self.height - 570
        new_width = original_width * new_height / original_height
        self.billboard = pygame.transform.smoothscale(self.billboard, (int(new_width), int(new_height)))
        billboard_rect = self.billboard.get_rect(midleft=(0, text_rect.bottom))
        self.screen.blit(self.billboard, billboard_rect)

    def display_game_name(self, game_name, index):
        color = (84,223,189) if index == self.selected_game else "white"
        text_surface, text_rect = self.create_text_surface(game_name, color, self.background)
        text_rect.center=(self.space_for_names  / 2, self.get_game_name_height(index))
        self.screen.blit(text_surface, text_rect)
        if index == self.selected_game:
            original_width, original_height = self.mouse.get_size()
            new_height = self.font.get_height()
            new_width = original_width * new_height / original_height
            self.mouse = pygame.transform.scale(self.mouse, (int(new_width), int(new_height)))
            mouse_rect = self.mouse.get_rect(midleft=(text_rect.right + 10, text_rect.centery))  # 10 is the space between the image and the text
            self.screen.blit(self.mouse, mouse_rect)

    def instruction_image(self):
        original_width, original_height = self.instructions.get_size()
        desired_width = self.space_for_names / 3
        desired_height = self.height - 150
        new_width = min(desired_width, original_width * desired_height / original_height)
        new_height = min(desired_height, original_height * desired_width / original_width)
        self.instructions = pygame.transform.scale(self.instructions, (int(new_width), int(new_height)))
        instructions_rect = self.instructions.get_rect(center=(self.space_for_names / 2, self.height - 110))
        self.screen.blit(self.instructions, instructions_rect)

    def city_images(self):
        self.bridge = pygame.transform.smoothscale(self.bridge, (80, 40))
        self.building_left = pygame.transform.smoothscale(self.building_left, (80, 100))
        self.building_left2 = pygame.transform.smoothscale(self.building_left2, (80, 100))
        self.building_right = pygame.transform.smoothscale(self.building_right, (40, 200))
        self.building_right2 = pygame.transform.smoothscale(self.building_right2, (40, 210))
        
        bridge_width, bridge_height = self.bridge.get_size()
        building_left_height = self.building_left.get_height()
        building_right_height = self.building_right.get_height()
        building_left2_height = self.building_left2.get_height()
        building_right2_height = self.building_right2.get_height()

        for pixel in range(0, self.width, bridge_width):
            self.screen.blit(self.bridge, (pixel, self.height - bridge_height))
        self.screen.blit(self.building_left, (10, self.height - building_left_height))
        self.screen.blit(self.building_left2, (self.space_for_names - 70, self.height - building_left2_height))
        self.screen.blit(self.building_right, (self.width - 100, self.height - building_right_height))
        self.screen.blit(self.building_right2, (self.width - 50, self.height - building_right2_height))

    def get_game_name_height(self, index):
        return self.__height_start + 80 * index
