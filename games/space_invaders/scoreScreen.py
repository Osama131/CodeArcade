import pygame
from score import Score

class ScoreScreen:
    FONT_SIZE = 36
    font = pygame.font.Font("assets/font/Arcade Classic.ttf", FONT_SIZE)
    background_image = pygame.image.load("assets/graphics/Space Sprites/Space_1.png")

    def __init__(self, window):
        self.window = window
        self.background_image = pygame.transform.scale(self.background_image, (window.get_width(), window.get_height()))

    def run(self):
        # set initial font size and position
        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    quit()
                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_SPACE:
                        return "gameover"
                    elif event.key == pygame.K_ESCAPE:
                        pygame.quit()
                        quit()

            # render the background then the text
            self.window.blit(self.background_image, (0, 0))

            # render the score board
            score_manager = Score()
            score_manager.draw(self.window)

            # render the "press esc to exit" text
            exit_text = self.font.render(
                "Press Space to Return", True, 'white')
            exit_rect = exit_text.get_rect(
                center = (self.window.get_width() // 2, self.window.get_height() // 2 + 250))
            self.window.blit(exit_text, exit_rect)

            pygame.time.Clock().tick(60)
            pygame.display.update()
