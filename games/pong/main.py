import pygame
import random
import os
import time
import math

pygame.init()

# Calculates the angle of the ball when it hits the player
def calculate_angle(rectangle):
    relative_position = (ball.centery - rectangle.top) / (rectangle.height / 2) - 1  # -1 to 1 range
    angle = relative_position * math.pi / 4  # -45 to 45 degrees
    
    return angle + random.uniform(-0.1, 0.1)  # return angle + some very small random float to prevent the ball from getting stuck


# Bounces the ball off the rectangle and calculates the y direction
def bounce_off_rectangle(rectangle):
    global ball_speed_x, ball_speed_y
    HIT_SOUND.play()

    angle = calculate_angle(rectangle)
    ball_speed_x *= -1
    ball_speed_y = 9 * math.sin(angle)  # sin is the y direction


# Ball behaviour, starts the movement, checks if the ball collides with players or hits the wall
def ball_bounce():
    global ball_speed_x, ball_speed_y
    if is_playing and not is_reset:
        ball.x += ball_speed_x
        ball.y += ball_speed_y

    # Reverts the y ball direction if it hits the game windows top or bottom
    if ball.top <= 0 or ball.bottom >= WINDOW_HEIGHT:
        ball_speed_y *= -1
        if ball.top <= 0:
            ball.top = 0
        elif ball.bottom >= WINDOW_HEIGHT:
            ball.bottom = WINDOW_HEIGHT

    if ball.colliderect(player_left):
        bounce_off_rectangle(player_left)
        
        ball.left = player_left.right  # Set the ball position to the right side of the player

    elif ball.colliderect(player_right):
        bounce_off_rectangle(player_right)
        ball.right = player_right.left

    elif obstacle != None and ball.colliderect(obstacle) and obstacle_exists:
        bounce_off_rectangle(obstacle)


# Creates a random placed obstacle
def create_obstacle() -> pygame.Rect:
    obstacle = pygame.Rect(random.randint(100, WINDOW_WIDTH-100), random.randint(100, WINDOW_HEIGHT-100), 40, 40)
    return obstacle


# Draws the obstacle
def draw_obstacle(obstacle: pygame.Rect):
    pygame.draw.rect(WINDOW, WHITE, obstacle)


# Checks if the ball goes beyond the bound and resets the pos and adds a point to the player
def scoring():
    global player_left_score, player_right_score, is_reset

    if ball.left <= 0:
        player_right_score += 1
        ball_reset()
        players_reset()
        if player_right_score <= 4:
            SCORE_SOUND.play()
        else:
            FINISH_SOUND.play()

    if ball.right >= WINDOW_WIDTH:
        player_left_score += 1
        ball_reset()
        players_reset()
        if player_left_score <= 4:
            SCORE_SOUND.play()
        else:
            FINISH_SOUND.play()


# Resets the ball to the center and stops the movement and randomizes the movement
def ball_reset():
    global ball_speed_x, ball_speed_y, is_reset, is_playing
    ball.center = (WINDOW_WIDTH/2, WINDOW_HEIGHT/2)
    ball_speed_x = 6 * random.choice((1, -1))
    ball_speed_y = 6 * random.choice((1, -1))
    is_reset = True


# Resets the players to the startingpositions and stops the movement
def players_reset():
    global player_left_speed, player_right_speed
    player_left.midleft = (10, WINDOW_HEIGHT/2)
    player_right.midright = (WINDOW_WIDTH-10, WINDOW_HEIGHT/2)
    player_left_speed = 0
    player_right_speed = 0


# Resets the score to 0
def score_reset():
    global player_left_score, player_right_score
    player_left_score = 0
    player_right_score = 0


# Checks if the players goes beyond the bound and resets the pos
def player_boundaries():
    if player_left.top <= 0:
        player_left.top = 0
    elif player_left.bottom >= WINDOW_HEIGHT:
        player_left.bottom = WINDOW_HEIGHT

    if player_right.top <= 0:
        player_right.top = 0
    elif player_right.bottom >= WINDOW_HEIGHT:
        player_right.bottom = WINDOW_HEIGHT


# Gets the player name and returns it
def get_player_name(text, player_number):
    max_length = 15
    placeholder = " . . . ."
    text = placeholder
    name_prompt = SCORE_FONT.render(
        f'Enter Your Name {player_number}', False, WHITE)

    is_active = True
    while is_active:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()
            if event.type == pygame.KEYDOWN:  # If a key is pressed
                if text == placeholder:
                    text = ""  # Empty the text
                if event.key == pygame.K_BACKSPACE:
                    text = text[:-1]  # Remove the last character
                elif event.key == pygame.K_ESCAPE:  # If the key is escape
                    pygame.quit()
                    quit()
                elif event.key == pygame.K_RETURN:  # If the key is enter
                    if not text == "":
                        is_active = False
                elif event.key == pygame.K_COMMA:  # Filter comma
                    pass
                else:
                    if len(text) < max_length:  # If the text is not longer than the max length
                        text += event.unicode  # unicode is the character that was pressed

        txt_surface = SCORE_FONT.render(text, False, WHITE)
        text_y = INPUT_BOX.y + INPUT_BOX.height/2 - txt_surface.get_height() / 2
        WINDOW.fill(BACKGROUND_COLOR)
        WINDOW.blit(GAME_NAME, (WINDOW_WIDTH//2 - GAME_NAME.get_width() // 2, 100))
        WINDOW.blit(name_prompt, (WINDOW_WIDTH//2 - name_prompt.get_width() // 2, 240))
        WINDOW.blit(txt_surface, (INPUT_BOX.x + 5, text_y))
        pygame.draw.rect(WINDOW, WHITE, INPUT_BOX, 2)

        CRT_IMAGE.set_alpha(random.randint(50, 65))  # Randomize the alpha value
        create_crt_lines()
        WINDOW.blit(CRT_IMAGE, (0, 0))

        pygame.display.flip()

        CLOCK.tick(60)

    return text


# Loads the txt file with the scores and returns the list
def load_scores():
    if os.path.exists(SCORE_FILE):  # Check if the file exists
        with open(SCORE_FILE, 'r') as file:
            scores = [line.strip().split(',')  # Remove the whitespace and comma.
                      for line in file if len(line.strip()) > 1]  # Split the line into a list
            return [(score_entry[0], float(score_entry[1])) for score_entry in scores ]  # Convert the second element to a float
    else:
        return []


# Saves the scores to the txt file
def save_scores(scores):
    with open(SCORE_FILE, 'w') as file:
        for name, game_duration in scores:
            file.write(f'{name}, {game_duration}\n')


# Updates the scores and sorts them and only keeps the top 5
def update_scores(name, game_duration):
    scores = load_scores()
    game_duration = round(float(game_duration), 2)  # Round the game_duration to 2 decimals
    scores.append((name, game_duration))

    scores.sort(key=lambda score_entry: score_entry[1])  # Sort by game_duration, 1 index in the list, 0 is name
    scores = scores[:5]  # only keep the top 5 scores using slicing

    save_scores(scores)

# Creates the crt lines depending on the window size
def create_crt_lines():
    global CRT_IMAGE, WINDOW_WIDTH, WINDOW_HEIGHT
    LINE_HEIGHT = 2
    LINE_AMOUNT = int(WINDOW_HEIGHT // LINE_HEIGHT)
    for line in range(LINE_AMOUNT):
        y_pos = line * LINE_HEIGHT
        pygame.draw.line(CRT_IMAGE, BLACK, (0, y_pos), (WINDOW_WIDTH, y_pos), 1)


CLOCK = pygame.time.Clock()

BACKGROUND_COLOR = (37, 37, 38)
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
WINDOW_WIDTH = 950
WINDOW_HEIGHT = 600
WINDOW = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
pygame.display.set_caption("Pong")

# Set up the ball, players and obstacle by directly creating rectangles, first position then own size
ball = pygame.Rect(WINDOW_WIDTH/2-11, WINDOW_HEIGHT/2-11, 22, 22)
player_left = pygame.Rect(10, WINDOW_HEIGHT/2-45, 20, 90)
player_right = pygame.Rect(WINDOW_WIDTH-30, WINDOW_HEIGHT/2-45, 20, 90)
obstacle = None

CRT_IMAGE = pygame.image.load('graphics/crt.png').convert_alpha()
CRT_IMAGE = pygame.transform.scale(CRT_IMAGE, (WINDOW_WIDTH, WINDOW_HEIGHT))
HIT_SOUND = pygame.mixer.Sound('sounds/hit.mp3')
SCORE_SOUND = pygame.mixer.Sound('sounds/score.mp3')
FINISH_SOUND = pygame.mixer.Sound('sounds/finish.mp3')
SCORE_FONT = pygame.font.Font('font/Pixeltype.ttf', 40)
GAME_OVER_FONT = pygame.font.Font('font/Pixeltype.ttf', 80)

is_reset = True
is_playing = False
is_game_over = False
is_score_saved = False
obstacle_exists = False

player_left_speed = 0
player_right_speed = 0
player_left_score = 0
player_right_score = 0
game_start_time = None
ball_speed_x = 6 * random.choice((1, -1))
ball_speed_y = 6 * random.choice((1, -1))

ADD_OBSTACLE_EVENT = pygame.USEREVENT + 1  # Custom event
SPEED_UP_BALL_EVENT = pygame.USEREVENT + 2
SCORE_FILE = "scores.txt"
START_PROMPT = SCORE_FONT.render(f'Press Enter To Start', False, WHITE)
GAME_NAME = GAME_OVER_FONT.render(f'PONG', False, WHITE)
INPUT_BOX = pygame.Rect(WINDOW_WIDTH/2-150, WINDOW_HEIGHT/2-25, 300, 50)

# Main loop
running = True
player_left_name = get_player_name("", "Player 1")
player_right_name = get_player_name("", "Player 2")
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                pygame.quit()
                quit()

        # Start the game if enter is pressed
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_RETURN and (is_playing == False or is_game_over):
                is_playing = True
                is_game_over = False
                is_score_saved = False
                obstacle_exists = False
                obstacle = None
                score_reset()  # Reset the score
                game_start_time = time.time()  # Save the start time

        # Reset the game if space is pressed
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE and is_playing and is_reset and not is_game_over:
                is_reset = False
                obstacle_exists = False
                obstacle = None
                pygame.time.set_timer(ADD_OBSTACLE_EVENT,15000)  # Every 15 seconds
                pygame.time.set_timer(SPEED_UP_BALL_EVENT, 30000)

        # Check if the player presses the keys and move the players
        pressed_keys = pygame.key.get_pressed()
        if is_playing and not is_reset:
            if pressed_keys[pygame.K_w] and not pressed_keys[pygame.K_s]:
                player_left_speed = -7
            elif pressed_keys[pygame.K_s] and not pressed_keys[pygame.K_w]:
                player_left_speed = 7
            else:
                player_left_speed = 0

            if pressed_keys[pygame.K_UP] and not pressed_keys[pygame.K_DOWN]:
                player_right_speed = -7
            elif pressed_keys[pygame.K_DOWN] and not pressed_keys[pygame.K_UP]:
                player_right_speed = 7
            else:
                player_right_speed = 0

        if event.type == ADD_OBSTACLE_EVENT and is_playing and not is_reset:
            obstacle_exists = True
            obstacle = create_obstacle()

        if event.type == SPEED_UP_BALL_EVENT and is_playing and not is_reset:
            ball_speed_x *= 1.2

    # Calling the functions
    ball_bounce()
    scoring()
    player_boundaries()

    # Updating the player movement
    player_left.y += player_left_speed
    player_right.y += player_right_speed

    WINDOW.fill(BACKGROUND_COLOR)

    if is_playing:
        # Drawing and coloring the rectangles and the ball as a ellipse, and the middle line
        pygame.draw.rect(WINDOW, WHITE, player_left)
        pygame.draw.rect(WINDOW, WHITE, player_right)
        pygame.draw.ellipse(WINDOW, WHITE, ball)
        pygame.draw.aaline(WINDOW, WHITE, (WINDOW_WIDTH/2, 0),
                           (WINDOW_WIDTH/2, WINDOW_HEIGHT))

        # Drawing the obstacle
        if obstacle_exists and not is_reset and not is_game_over:
            draw_obstacle(obstacle)

        # Drawing and updating the score
        player_left_text = SCORE_FONT.render(
            f'{player_left_score}', False, WHITE)
        WINDOW.blit(player_left_text, (WINDOW_WIDTH/2-60, WINDOW_HEIGHT/2-20))

        player_right_text = SCORE_FONT.render(
            f'{player_right_score}', False, WHITE)
        WINDOW.blit(player_right_text, (WINDOW_WIDTH/2+50, WINDOW_HEIGHT/2-20))

        # Drawing the reset text
        if is_reset and player_left_score == 0 and player_right_score == 0:
            reset_text = SCORE_FONT.render(f'Press Space', False, WHITE)
            WINDOW.blit(reset_text, (WINDOW_WIDTH//2 -
                        reset_text.get_width() // 2, 240))
    else:
        # Drawing the start screen
        instructions_left = SCORE_FONT.render(f'Left Player   =   W  &  S  Key', False, WHITE)
        instructions_right = SCORE_FONT.render(f'Right Player   =   Up  &  Down  Arrows', False, WHITE)
        WINDOW.blit(GAME_NAME, (WINDOW_WIDTH//2 - GAME_NAME.get_width() // 2, 100))
        WINDOW.blit(instructions_left, (WINDOW_WIDTH//2 - instructions_left.get_width() // 2, 280))
        WINDOW.blit(instructions_right, (WINDOW_WIDTH//2 - instructions_right.get_width() // 2, 340))
        WINDOW.blit(START_PROMPT, (WINDOW_WIDTH//2 - START_PROMPT.get_width() // 2, 500))

    # Checking the score and stopping the game if it reaches 5
    if player_left_score == 5 or player_right_score == 5:
        is_playing = False
        is_game_over = True

    # Save the time, update the scores, displaying the game over screen and the winner
    if is_game_over:
        # Only save the time and score once
        if game_start_time is not None and is_score_saved == False:
            game_end_time = time.time()
            game_duration = game_end_time - game_start_time
            game_start_timestart_time = None
            if player_left_score == 5:
                update_scores(player_left_name, game_duration)
            elif player_right_score == 5:
                update_scores(player_right_name, game_duration)
            is_score_saved = True

        scores = load_scores()
        scores.sort(key=lambda s: s[1])  # Sort by game_duration, 1 index in the list, 0 is name

        WINDOW.fill(BACKGROUND_COLOR)

        # Drawing the game over screen
        winner_text = None
        if player_left_score == 5:
            winner_text = GAME_OVER_FONT.render(f'The Winner is {player_left_name}', False, WHITE)
        elif player_right_score == 5:
            winner_text = GAME_OVER_FONT.render(f'The Winner is {player_right_name}', False, WHITE)
        WINDOW.blit(winner_text, (WINDOW_WIDTH//2 - winner_text.get_width() // 2, 100))

        scoreboard_text = SCORE_FONT.render(f'--  Scoreboard  --', False, WHITE)
        WINDOW.blit(scoreboard_text, (WINDOW_WIDTH//2 - scoreboard_text.get_width() // 2, 200))
        
        for score_index, (name, game_duration) in enumerate(scores):  # enumerate gives the index and the value
            score_text = SCORE_FONT.render(f'{name}  -  {game_duration}s', False, WHITE)
            WINDOW.blit(score_text, (WINDOW_WIDTH//2 - score_text.get_width() // 2, 255 + score_index * 40))

        WINDOW.blit(START_PROMPT, (WINDOW_WIDTH//2 - START_PROMPT.get_width() // 2, 500))

    # Drawing the crt lines
    CRT_IMAGE.set_alpha(random.randint(50, 65))
    create_crt_lines()
    WINDOW.blit(CRT_IMAGE, (0, 0))

    pygame.display.update()

    # Frames per second
    CLOCK.tick(60)

pygame.quit()
