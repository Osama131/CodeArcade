import pygame
import time
import random
import os

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

#game over 
game_over = False

# CHALLENGE 5
my_font = pygame.font.Font("C:\Windows\Fonts\AGENCYR.TTF", 30)
def font():
    text_surface = my_font.render(f"Score: {score}" , True, white)
    game_window.blit(text_surface, (10, 10))

# CHALLENGE 6
def game_over():
    game_window.fill(white)
    text_over = my_font.render(f"GAME OVER   YOUR SCORE: {score}", True, black)
    game_window.blit(text_over, (100, 100))
    pygame.display.update()
    time.sleep(1.2)
    quit()

    

while True:
    # Handling key events
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            quit()
        # CHALLENGE 2
    
     # CHALLENGE 3

    # Moving snake
        keys=pygame.key.get_pressed()
        if keys[pygame.K_LEFT]:
            direction = 'LEFT'
        if keys[pygame.K_RIGHT]:
            direction='RIGHT'
        if keys[pygame.K_UP]:
            direction='UP'
        if keys[pygame.K_DOWN]:
            direction='DOWN'

    # CHALLENGE 1
    if direction == 'RIGHT':
        snake_position[0] += 10
    if direction == 'UP':
        snake_position[1] -= 10
    if direction == 'DOWN':
        snake_position[1] += 10
    if direction == 'LEFT':
        snake_position[0] -= 10
    

    # Snake body growing mechanism if fruit and snake collide score
    # then scores will be incremented by 10
    snake_body.insert(0, list(snake_position))
    if snake_position[0] == fruit_position[0] and snake_position[1] == fruit_position[1]:
        score+=10
        fruit_spawn = False
    else:
        snake_body.pop()

    game_window.fill(black)

    for pos in snake_body:
        pygame.draw.rect(game_window, green, pygame.Rect(pos[0], pos[1], 10, 10))
        pygame.draw.rect(game_window, white, pygame.Rect(fruit_position[0], fruit_position[1], 10, 10))
    # CHALLENGE 4
        if snake_position[0] == fruit_position[0] and snake_position[1] == fruit_position[1]:
            fruit_position = [random.randrange(1, (window_x//10)) * 10, random.randrange(1, (window_y//10)) * 10]
        if snake_position[0] >= window_x or snake_position[1] >= window_y or snake_position[0] < 0 or snake_position[1] < 0:
            game_over()
    # CHALLENGE 7
        for i in snake_body[1:]:
            if snake_position == i and score >= 10:
                game_over()
                
    font()

    # CHALLENGE 8

    # Refresh game screen
    pygame.display.update()

    # Frame per Second Refresh rate
    fps.tick(snake_speed)


