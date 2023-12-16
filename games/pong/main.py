import pygame
import random

pygame.init()

# Bounces the ball off the rectangle and gives the direction
# TASK 2 - Ball Bounce
# TASK 2.1 - Make ball move in different ways
# TASK 2.2 - Bounce off the top and bottom of the window
def bounce_off_rectangle(rectangle):
    global ball_speed_x, ball_speed_y
    HIT_SOUND.play()

    if(rectangle == wall_top or rectangle == wall_bottom): 
        ball_speed_y *= -1

    elif(rectangle == player_left):
        ball_speed_x *= -1
        ball_speed_y = ball_speed_y + (player_left_speed )

    elif(rectangle == player_right):
        ball_speed_x *= -1
        ball_speed_y = ball_speed_y + (player_right_speed )


# Ball behaviour, starts the movement, checks if the ball collides with players or hits the wall
def ball_bounce():
    global ball_speed_x, ball_speed_y
    if is_playing and not is_reset:
        ball.x += ball_speed_x
        ball.y += ball_speed_y

    if ball.colliderect(player_left):
        bounce_off_rectangle(player_left)
        
        ball.left = player_left.right  # Set the ball position to the right side of the player

    elif ball.colliderect(player_right):
        bounce_off_rectangle(player_right)
        ball.right = player_right.left

    elif ball.colliderect(wall_top):
        bounce_off_rectangle(wall_top)
    
    elif ball.colliderect(wall_bottom):
        bounce_off_rectangle(wall_bottom)

    elif ball.colliderect(random_object):
        #If collide with up or down
        if(ball.top <= random_object.bottom and ball.bottom >= random_object.top):
            ball_speed_y *= -1
        #If collide with left
        elif(ball.right >= random_object.left and ball.left <= random_object.left) or (ball.left <= random_object.right and ball.right >= random_object.right):
            ball_speed_x *= -1


    


# Checks if the ball goes beyond the bound and resets the pos and adds a point to the player
def scoring():
    global player_left_score, player_right_score

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

def random_object_function(random_object, counter):
    if counter == 420:
        random_object.x = random.randint(0, WINDOW_WIDTH - random_object.width)
        random_object.y = random.randint(0, WINDOW_HEIGHT - random_object.height)
        counter = 0
    else:
        counter += 1
    return counter


# Resets the ball to the center and stops the movement and randomizes the movement
def ball_reset():
    global ball_speed_x, is_reset, is_playing, ball_speed_y
    ball.center = (WINDOW_WIDTH/2, WINDOW_HEIGHT/2)
    ball_speed_x = 6 * random.choice((1, -1))
    ball_speed_y = random.choice((0.1 * random.randint(-10, -5), 0.1 * random.randint(5, 10)))
    is_reset = True


# Resets the players to the startingpositions and stops the movement
def players_reset():
    global player_left_speed #player_right_speed
    global player_right_speed
    player_left.midleft = (10, WINDOW_HEIGHT/2)
    player_right.midright = (WINDOW_WIDTH-10, WINDOW_HEIGHT/2)
    player_left_speed = 0
    player_right_speed = 0


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

# TASK 4 - Scoring System
# TASK 4.1 - Implement saving, loading and updating functions
# TASK 4.2/4.3 - End the game based on the score or based on the time played

def load_scores():
    global highscores
    scores = open(SCORE_FILE, "r").read()
    scorelines = scores.split("\n")
    for line in scorelines:
        split = line.split(" ", 1)
        if(split != []):
            print(split)
            score = split[0]
            name = split[1]
            highscores.append([name, score])

def save_scores():
    global highscores
    text_to_write = ""
    for i in range(len(highscores)):
        s = highscores[i]
        text_to_write += str(s[1]) + " " + str(s[0])
        if(not i == len(highscores) - 1):
            text_to_write += "\n"
    text_to_write.removesuffix("\n")
    open(SCORE_FILE, "w").write(text_to_write)

def update_scores():
    global player_left_score, player_right_score, is_score_saved, highscores
    is_score_saved = True
    
    highscores.append([player_left_name, player_left_score])
    highscores.append([player_right_name, player_right_score])
    highscores.sort(key=compare_player, reverse=True)
    save_scores()
    print(highscores)
    print(is_score_saved)

def compare_player(p):
    return int(p[1])

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
RED = (255, 0, 0)
WINDOW_WIDTH = 950
WINDOW_HEIGHT = 600
WINDOW = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
pygame.display.set_caption("Pong")

# Set up the ball, players by directly creating rectangles, first position then own size
ball = pygame.Rect(WINDOW_WIDTH/2-11, WINDOW_HEIGHT/2-11, 22, 22)
player_left = pygame.Rect(10, WINDOW_HEIGHT/2-45, 20, 90)
player_right = pygame.Rect(WINDOW_WIDTH-30, WINDOW_HEIGHT/2-45, 20, 90)
wall_top = pygame.Rect(0, 0, WINDOW_WIDTH, 1)
wall_bottom = pygame.Rect(0, WINDOW_HEIGHT, WINDOW_WIDTH, 1)
random_object = pygame.Rect(WINDOW_WIDTH/2-11, WINDOW_HEIGHT/2-11, 45, 45)

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

player_left_speed = 0
player_left_score = 0
player_right_score = 0
player_right_speed = 0
ball_speed_x = 6 * random.choice((1, -1))
ball_speed_y = random.choice((0.1 * random.randint(-10, -5), 0.1 * random.randint(5, 10)))

timer_wert = 100
timer_temp = 0
counter = 0

highscores = []

SPEED_UP_BALL_EVENT = pygame.USEREVENT + 2
SCORE_FILE = "scores.txt"
START_PROMPT = SCORE_FONT.render(f'Press Enter To Start', False, WHITE)
GAME_NAME = GAME_OVER_FONT.render(f'PONG', False, WHITE)
INPUT_BOX = pygame.Rect(WINDOW_WIDTH/2-150, WINDOW_HEIGHT/2-25, 300, 50)

# Main loop
running = True
load_scores()
player_left_name = get_player_name("", "Player 1")
player_right_name = get_player_name("", "Player 2")
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                running = False

        # Start the game if enter is pressed
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_RETURN and not is_playing:
                #is in main menu
                if not is_game_over:
                    is_playing = True
                    is_score_saved = False
                #is in game over screen
                else:
                    is_game_over = False
                    timer_wert = 100

        # Reset the game if space is pressed
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE and is_playing and is_reset:
                is_reset = False
                pygame.time.set_timer(SPEED_UP_BALL_EVENT, 30000)

        

        # TASK 1 - Player Right Movement
        # TASK 1.1 - Help Player right to move
        # Check if the player presses the keys and move the players
        pressed_keys = pygame.key.get_pressed()
        if is_playing and not is_reset:
            #Player Left
            if pressed_keys[pygame.K_w] and not pressed_keys[pygame.K_s]:
                player_left_speed = -7
            elif pressed_keys[pygame.K_s] and not pressed_keys[pygame.K_w]:
                player_left_speed = 7
            else:
                player_left_speed = 0
            #Player Right
            if pressed_keys[pygame.K_UP] and not pressed_keys[pygame.K_DOWN]:
                player_right_speed = -7
            elif pressed_keys[pygame.K_DOWN] and not pressed_keys[pygame.K_UP]:
                player_right_speed = 7
            else:
                player_right_speed = 0
            

        if event.type == SPEED_UP_BALL_EVENT and is_playing and not is_reset:
            ball_speed_x *= 1.2

    # Calling the functions
    ball_bounce()
    scoring()
    player_boundaries()
    counter = random_object_function(random_object, counter)

    # Updating the player movement
    player_left.y += player_left_speed
    player_right.y += player_right_speed

    if is_game_over and not is_score_saved:
        update_scores()

    WINDOW.fill(BACKGROUND_COLOR)

   
    if is_game_over:
        # Draw game over screen
        is_playing = False

        game_over_text = SCORE_FONT.render("Game Over", False, RED, BACKGROUND_COLOR)
        WINDOW.blit(game_over_text, (WINDOW_WIDTH/2-60, WINDOW_HEIGHT/16)) 
        WINDOW.blit(GAME_NAME, (WINDOW_WIDTH//2 - GAME_NAME.get_width() // 2, 100))
        WINDOW.blit(START_PROMPT, (WINDOW_WIDTH//2 - START_PROMPT.get_width() // 2, 500))

        #highscores
        highscores_textfeld = SCORE_FONT.render("HIGHSCORES:", False, WHITE, BACKGROUND_COLOR)
        WINDOW.blit(highscores_textfeld, (WINDOW_WIDTH/12, (WINDOW_HEIGHT/8) - 40))
        i = 0
        for s in highscores:
            i += 1
            text = str(s[1]) + "    " + str(s[0])
            textfeld = SCORE_FONT.render(text, False, WHITE, BACKGROUND_COLOR)
            WINDOW.blit(textfeld, (WINDOW_WIDTH/8, (WINDOW_HEIGHT/8) + i * 30))

        if player_left_score > player_right_score:
            winner_text = SCORE_FONT.render(player_left_name + " has won!", False, WHITE, BACKGROUND_COLOR)
            winner_text_width = winner_text.get_width() 
            WINDOW.blit(winner_text, (WINDOW_WIDTH/2 - winner_text_width/2, WINDOW_HEIGHT/2)) 
        elif player_left_score < player_right_score: 
            winner_text = SCORE_FONT.render(player_right_name + " has won!", False, WHITE, BACKGROUND_COLOR)
            winner_text_width = winner_text.get_width() 
            WINDOW.blit(winner_text, (WINDOW_WIDTH/2-winner_text_width/2, WINDOW_HEIGHT/2)) 
        else:
            draw_text = SCORE_FONT.render("Draw!", False, WHITE, BACKGROUND_COLOR)
            draw_text_width = draw_text.get_width()
            WINDOW.blit(draw_text, (WINDOW_WIDTH/2-draw_text_width/2, WINDOW_HEIGHT/2)) 
        

    elif is_playing:
        # Drawing and coloring the rectangles and the ball as a ellipse, and the middle line
        pygame.draw.rect(WINDOW, WHITE, player_left)
        pygame.draw.rect(WINDOW, WHITE, player_right)
        pygame.draw.ellipse(WINDOW, WHITE, ball)
        pygame.draw.aaline(WINDOW, WHITE, (WINDOW_WIDTH/2, 0),(WINDOW_WIDTH/2, WINDOW_HEIGHT))
        pygame.draw.rect(WINDOW, WHITE, random_object)

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
    
    

    # TASK 3 - Game Over
    # TASK 3.1 - Make the game end
    # TASK 3.2 - Announce the winner
    # TASK 3.3 - Add a game over display and possibility to restart the game

    
    
    if is_playing:
        timer_text = SCORE_FONT.render(f"{timer_wert}", False, WHITE, BACKGROUND_COLOR)
        WINDOW.blit(timer_text, (WINDOW_WIDTH/2-20, WINDOW_HEIGHT/16))
        timer_temp += 1
        if timer_temp == 60 and timer_wert >0:
            timer_wert -= 1
            timer_temp = 0
    
    if(timer_wert <= 0):
        is_game_over = True

    # Drawing the crt lines
    CRT_IMAGE.set_alpha(random.randint(50, 65))
    create_crt_lines()
    WINDOW.blit(CRT_IMAGE, (0, 0))

    pygame.display.update()

    # Frames per second
    CLOCK.tick(60)

pygame.quit()