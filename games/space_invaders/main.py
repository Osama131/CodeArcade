import pygame
pygame.init()

from gameOverScreen import GameOverScreen
from spaceInvaders import SpaceInvaders
from startScreen import StartScreen
from scoreScreen import ScoreScreen
from score import Score
# initialize pygame


WINDOW_WIDTH = 800
WINDOW_HEIGHT = 700


# Set up the game window
window = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
pygame.display.set_caption("Space Invaders")

playing = True

while playing:
    # run the start screen
    startscreen = StartScreen(window)
    username = startscreen.run()

    if username == '':
        playing = False
    else:
        # run the game if username is not empty string
        spaceInvaders = SpaceInvaders(window)
        player_score = spaceInvaders.run()
        new_score = Score(username,player_score)
        new_score.save_score()
        gameOverScreen = GameOverScreen(window, username, player_score)
        next_action = gameOverScreen.run()
        if next_action == 'quit':
            playing = False
        elif next_action == 'highscore':
            scoreScreen = ScoreScreen(window)
            show = scoreScreen.run()
            if show == 'quit':
                playing = False
        else:
            # play again
            pass

# here we still have some time to do some clean up before we quit

# Quit pygame
pygame.quit()
