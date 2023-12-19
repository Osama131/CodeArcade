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
# Display score function
def show_score(color, font, size):
    # Creating font object score_font
    score_font = pygame.font.SysFont(font, size)

    # Create display surface object score_surface
    score_surface = score_font.render("Score: " + str(score), True, color)

    # Create rectangular object for the text surface object
    score_rect = score_surface.get_rect()

    # Displaying text
    game_window.blit(score_surface, score_rect)
# CHALLENGE 5 END

# CHALLENGE 6
# Game over function
def game_over():
    # Creating font object my_font
    my_font = pygame.font.SysFont("times new roman", 50)

    # Creating text surface on which text will be drawn
    game_over_surface = my_font.render("Your score is: " + str(score), True, red)

    # Create a rectangular object for the text surface object
    game_over_rect = game_over_surface.get_rect()

    # Setting position of the text
    game_over_rect.midtop = (window_x/2, window_y/4)

    # Blit will draw text on screen
    game_window.blit(game_over_surface, game_over_rect)
    pygame.display.flip()

    # After 2 seconds we will quit program
    time.sleep(2)

    # Deactivating pygame library
    pygame.quit()

    # quit program
    quit()
# CHALLENGE 6 END

while True:

    # Handling key events
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            quit()
        # CHALLENGE 2
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_UP:
                change_to = 'UP'
            if event.key == pygame.K_DOWN:
                change_to = 'DOWN'
            if event.key == pygame.K_LEFT:
                change_to = 'LEFT'
            if event.key == pygame.K_RIGHT:
                change_to = 'RIGHT'
        # CHALLENGE 2 END

    # CHALLENGE 3
    # If two keys pressed simultaneously we dont want snake to move
    # into two directions simultaneously
    if change_to == 'UP' and direction != 'DOWN':
        direction = 'UP'
    if change_to == 'DOWN' and direction != 'UP':
        direction = 'DOWN'
    if change_to == 'LEFT' and direction != 'RIGHT':
        direction = 'LEFT'
    if change_to == 'RIGHT' and direction != 'LEFT':
        direction = 'RIGHT'
    # CHALLENGE 3 END

    # Moving snake
    # CHALLENGE 1
    if direction == 'UP':
        snake_position[1] -= 10
    if direction == 'DOWN':
        snake_position[1] += 10
    if direction == 'LEFT':
        snake_position[0] -= 10
    # CHALLENGE 1 END
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
    if not fruit_spawn:
        fruit_position = [random.randrange(1, (window_x//10)) * 10,
                          random.randrange(1, (window_y//10)) * 10]
    fruit_spawn = True
    # CHALLENGE 4 END

    game_window.fill(black)

    for pos in snake_body:
        pygame.draw.rect(game_window, green, pygame.Rect(pos[0], pos[1], 10, 10))

    pygame.draw.rect(game_window, white, pygame.Rect(fruit_position[0], fruit_position[1], 10, 10))

    # CHALLENGE 7
    # Game over conditions
    if snake_position[0] < 0 or snake_position[0] > window_x - 10:
        game_over()
    if snake_position[1] < 0 or snake_position[1] > window_y - 10:
        game_over()

    # Touching snake body
    for block in snake_body[1:]:
        if snake_position[0] == block[0] and snake_position[1] == block[1]:
            game_over()
    # CHALLENGE 7 END

    # CHALLENGE 5
    # Displaying score continuously
    show_score(white, 'times new roman', 20)
    # CHALLENGE 5 END

    # Refresh game screen
    pygame.display.update()

    # Frame per Second Refresh rate
    fps.tick(snake_speed)


