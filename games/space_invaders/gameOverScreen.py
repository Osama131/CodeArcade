import pygame
from score import Score

class GameOverScreen:
    FONT_SIZE = 36
    font = pygame.font.Font("assets/font/Arcade Classic.ttf", FONT_SIZE)
    background_image = pygame.image.load(
        "assets/graphics/Space Sprites/Space_1.png")
    sound = pygame.mixer.Sound("assets/audio/gameover.mp3")

    def __init__(self, window, user_name, score):
        self.window = window
        self.background_image = pygame.transform.scale(
            self.background_image, (window.get_width(), window.get_height()))
        self.score = score
        self.user_name = user_name
        self.sound.play()

    def run(self):
        # set initial font size and position
        font_size = 12
        font_pos = (self.window.get_width() // 2, self.window.get_height() // 2)
        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    return "quit"
                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_RETURN:
                        return "restart"
                    elif event.key == pygame.K_SPACE:
                        return "highscore"
                    elif event.key == pygame.K_ESCAPE:
                        return "quit"

            # render the background then the text
            self.window.blit(self.background_image, (0, 0))

            # render the "game over" text with increasing font size
            self.font = pygame.font.Font("assets/font/Arcade Classic.ttf", font_size)
            game_over_text = self.font.render("Game Over", True, 'red')
            game_over_rect = game_over_text.get_rect(center=font_pos)
            self.window.blit(game_over_text, game_over_rect)

            # increase font size and move text up
            if font_size < self.FONT_SIZE:
                font_size += 1
                font_pos = (font_pos[0], font_pos[1] - 1)

            # render the username text
            username_text = self.font.render(
                f"Username: {self.user_name}", True, 'white')
            username_rect = username_text.get_rect(
                center=(self.window.get_width() // 2, self.window.get_height() // 2 + 50))
            self.window.blit(username_text, username_rect)

            # render the score text
            score_text = self.font.render(
                f"Score: {self.score}", True, 'white')
            score_rect = score_text.get_rect(
                center=(self.window.get_width() // 2, self.window.get_height() // 2 + 100))
            self.window.blit(score_text, score_rect)

            # render the "press enter to continue" text
            continue_text = pygame.font.Font("assets/font/Arcade Classic.ttf", 20).render(
                "Press Enter to play again", True, 'white')
            continue_rect = continue_text.get_rect(
                center=(self.window.get_width() // 2, self.window.get_height() // 2 + 200))
            self.window.blit(continue_text, continue_rect)

            # render the "press space to see highscores" text
            highscore_text = pygame.font.Font("assets/font/Arcade Classic.ttf", 20).render(
                "Press Space to see highscores", True, 'white')
            highscore_rect = highscore_text.get_rect(
                center=(self.window.get_width() // 2, self.window.get_height() // 2 + 250))
            self.window.blit(highscore_text, highscore_rect)

            # render the "press esc to exit" text
            exit_text = pygame.font.Font("assets/font/Arcade Classic.ttf", 20).render(
                "Press Esc to Exit", True, 'white')
            exit_rect = exit_text.get_rect(
                center=(self.window.get_width() // 2, self.window.get_height() // 2 + 300))
            self.window.blit(exit_text, exit_rect)

            pygame.time.Clock().tick(60)
            pygame.display.update()
