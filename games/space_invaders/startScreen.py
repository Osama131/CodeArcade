import pygame
from pygame.locals import *
from score import Score
from scoreScreen import ScoreScreen

class StartScreen:
    FONT_SIZE = 36
    font = pygame.font.Font("assets/font/Arcade Classic.ttf", FONT_SIZE)
    background_image = pygame.image.load(
        "assets/graphics/Space Sprites/Space_1.png")

    def __init__(self, window):
        self.window = window
        self.background_image = pygame.transform.scale(
            self.background_image, (window.get_width(), window.get_height()))
        input_box_x = window.get_width() // 4
        input_box_y = window.get_height() // 2 - self.FONT_SIZE // 2
        input_box_width = window.get_width() // 2
        input_box_height = self.FONT_SIZE + 2
        self.input_box = pygame.Rect(
            input_box_x, input_box_y, input_box_width, input_box_height)
        self.active = True
        self.done = False
        self.current_text = ''

    def render(self):
            # render the background then the text
            self.window.blit(self.background_image, (0, 0))

            insturction_text = self.font.render(
                "Enter your name: ", True, 'white')
            insturction_rect = insturction_text.get_rect(
                center=(self.window.get_width() // 2, self.input_box.y - self.FONT_SIZE))
            self.window.blit(insturction_text, insturction_rect)

            txt_surface = self.font.render(
                self.current_text, True, 'lightskyblue3', 'black')
            self.window.blit(
                txt_surface, (self.input_box.x+5, self.input_box.y+5))
            pygame.draw.rect(self.window, 'lightskyblue3', self.input_box, 2)

            start_text = self.font.render(
                "Press Enter to start the game", True, 'white')
            start_rect = start_text.get_rect(
                top=self.input_box.bottom + self.FONT_SIZE // 2, centerx=self.window.get_width() // 2)
            self.window.blit(start_text, start_rect)

            highscore_text = self.font.render(
                "Press Space to see highscores", True, 'white')
            highscore_rect = highscore_text.get_rect(
                 center = (self.window.get_width() // 2, self.input_box.bottom + self.FONT_SIZE * 2))
            self.window.blit(highscore_text, highscore_rect)
            # update the display on the next frame
            pygame.display.flip()

    # Display the start screen and return the player's name
    def run(self):
        while not self.done:
            for event in pygame.event.get():
                if event.type == QUIT:
                    self.done = True
                elif event.type == KEYDOWN:
                    if event.key == K_ESCAPE:
                        self.done = True
                        self.current_text = ''
                    elif event.key == K_RETURN:
                        if not self.current_text == '':
                            self.done = True
                    elif event.key == pygame.K_SPACE:  # go to scoreScreen
                        self.scoreScreen = ScoreScreen(self.window)
                        self.show = self.scoreScreen.run()
                    elif event.key == K_BACKSPACE:  # added elif block to handle backspace
                        self.current_text = self.current_text[:-1]
                    else:
                        # ignore if length of text is greater than 15
                        if len(self.current_text) < 10:
                            self.current_text += event.unicode
            self.render()

        return self.current_text
