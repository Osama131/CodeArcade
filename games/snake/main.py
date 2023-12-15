import random

import pygame

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

if snake_position[0] > window_x:
    font = pygame.font.SysFont('Arial', 25)
    textGameOver = font.render("Score: {0}".format(score), True, red)
    rectGameOver = textGameOver.get_rect(center=game_window.get_rect().center)
    game_window.blit(textGameOver, rectGameOver)
    pygame.display.update()

while True:
    # Handling key events
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            quit()
        # CHALLENGE 2
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_LEFT:
                change_to = 'LEFT'
            if event.key == pygame.K_UP:
                change_to = 'UP'
            if event.key == pygame.K_DOWN:
                change_to = 'DOWN'
            if event.key == pygame.K_RIGHT:
                change_to = 'RIGHT'

    # CHALLENGE 3
    if change_to == 'LEFT':
        direction = 'LEFT'
    if change_to == 'RIGHT':
        direction = 'RIGHT'
    if change_to == 'UP':
        direction = 'UP'
    if change_to == 'DOWN':
        direction = 'DOWN'
    if change_to == 'STOP':
        direction = 'STOP'

    # Moving snake
    # CHALLENGE 1
    if direction == 'RIGHT':
        snake_position[0] += 10
    elif direction == 'LEFT':
        snake_position[0] -= 10
    elif direction == 'UP':
        snake_position[1] -= 10
    elif direction == 'DOWN':
        snake_position[1] += 10
    elif direction == 'STOP':
        snake_position[0] = snake_body[0][0]


    # Snake body growing mechanism if fruit and snake collide score
    # then scores will be incremented by 10
    snake_body.insert(0, list(snake_position))
    if snake_position[0] == fruit_position[0] and snake_position[1] == fruit_position[1]:
        score += 10
        fruit_spawn = False
    else:
        snake_body.pop()

    # CHALLENGE 4
    if snake_position[0] == fruit_position[0] and snake_position[1] == fruit_position[1]:
        fruit_position = [random.randrange(1, (window_x // 10)) * 10,
                        random.randrange(1, (window_y // 10)) * 10]
        fruit_spawn = True



    game_window.fill(black)

    for pos in snake_body:
        pygame.draw.rect(game_window, green, pygame.Rect(pos[0], pos[1], 10, 10))

    pygame.draw.rect(game_window, white, pygame.Rect(fruit_position[0], fruit_position[1], 10, 10))

    # CHALLENGE 7
    if snake_position[0] > window_x or snake_position[0] < 0 or snake_position[1] < 0 or snake_position[1] > window_y or snake_body[0] in snake_body[1:]:
        change_to = 'STOP'
        pygame.draw.rect(game_window, red, pygame.Rect(0, 0, window_x, window_y))
        font = pygame.font.SysFont('Arial', 50)
        textGameOver = font.render("Game Over", True, black)
        rectGameOver = textGameOver.get_rect(center=game_window.get_rect().center)
        game_window.blit(textGameOver, rectGameOver)
        pygame.display.flip()




    # CHALLENGE 5
    font = pygame.font.SysFont('Arial', 25)
    textTitle = font.render("Score: {0}".format(score), True, red)
    rectTitle = textTitle.get_rect(center=(60, 20))
    # game_window.get_rect().center (um in der Mitte zu haben)
    game_window.blit(textTitle, rectTitle)

    # Refresh game screen
    pygame.display.update()

    # Frame per Second Refresh rate
    fps.tick(snake_speed)


