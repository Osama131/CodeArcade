import pygame
import time
import random

# Speed of snake
snake_speed = 15

# Window size
window_x = 720
window_y = 480

# Colors
black = pygame.Color(0, 0, 0)
white = pygame.Color(255, 255, 255)
red = pygame.Color(255, 0, 0)
green = pygame.Color(0, 255, 0)
blue = pygame.Color(0, 0, 255)

# Initialize pygame
pygame.init()

# Initialize window
pygame.display.set_caption("Snake")
game_window = pygame.display.set_mode((window_x, window_y))

# Define frames per second
fps = pygame.time.Clock()

# Define snake default position
snake_position = [100, 50]

# Define first 4 blocks of snake body
snake_body = [[100, 50], [90, 50], [80, 50], [70, 50]]

# Fruit position
fruit_position = [random.randrange(1, (window_x//10)) * 10,
                  random.randrange(1, (window_y//10)) * 10]
fruit_spawn = True

# Snake default direction
direction = 'RIGHT'
change_to = direction

# Initial score
score = 0

# CHALLENGE 5

# CHALLENGE 6

while True:

    # Handling key events
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            quit()
        # CHALLENGE 2

    # CHALLENGE 3

    # Moving snake
    # CHALLENGE 1
    if direction == 'RIGHT':
        snake_position[0] += 10

    # Snake body growing mechanism if fruit and snake collide score
    # then scores will be incremented by 10
    snake_body.insert(0, list(snake_position))
    if snake_position[0] == fruit_position[0] and snake_position[1] == fruit_position[1]:
        score += 10
        fruit_spawn = False
    else:
        snake_body.pop()

    # CHALLENGE 4

    game_window.fill(black)

    for pos in snake_body:
        pygame.draw.rect(game_window, green, pygame.Rect(pos[0], pos[1], 10, 10))

    pygame.draw.rect(game_window, white, pygame.Rect(fruit_position[0], fruit_position[1], 10, 10))

    # CHALLENGE 7

    # CHALLENGE 5

    # Refresh game screen
    pygame.display.update()

    # Frame per Second Refresh rate
    fps.tick(snake_speed)


