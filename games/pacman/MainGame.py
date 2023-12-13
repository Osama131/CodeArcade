import pygame
from pygame import Surface
from Ghost import init_ghosts
from Pacman import Pacman
from Scoring import Scoring
from game_constants import WIDTH, HEIGHT, TOP_OFFSET, TIME_BETWEEN_ANIMATIONS
from load_image import load_image
from PillManager import PillManager
from sounds import background_sfx

ESCAPE_KEY: int = 13


class MainGame:

    # this function is called the moment the class is instanced
    # this is called the constructor in Java
    def __init__(self ):
        # init basic variables to use later
        self.running = False
        self.is_game_over = False
        self.time_to_reset = None
        self.cur_time_passed = 0
        self.time_for_next_animation = TIME_BETWEEN_ANIMATIONS
        self.sprites_to_draw = pygame.sprite.OrderedUpdates()

        # init pygame window
        pygame.init()
        self.screen: Surface = pygame.display.set_mode((WIDTH, HEIGHT))
        self.clock = pygame.time.Clock()
        self.background_surface = self.init_background()

        self.scores = self.init_scoring()

        # init all movable / eatable sprites
        self.pill_manager = PillManager(self)
        self.pacman = Pacman('pacman', (336, TOP_OFFSET + 564), self)
        self.pacman.init_hearts(self.sprites_to_draw)
        self.ghosts = init_ghosts(self)
        # The following code is currently commented out and needs to be used for a challenge later on
        # self.fruits = [
        #     Fruit('cherry', (336, TOP_OFFSET + 564), 'sprites/cherry.png', 700),
        #     Fruit('strawberry', (336, TOP_OFFSET + 564), 'sprites/strawberry.png', 1700)
        # ]


    def init_scoring(self):
        # a dictonary (dict) maps a number of keys to a respective value
        # in this case we map a str to a Scoring obj
        scores: dict[str, Scoring] = {}

        # current score is initialized with 0
        scores["current"] = Scoring("Score: ", (100, 10))
        self.sprites_to_draw.add(scores["current"])

        # high score is initialized with the content of the text file
        high_score_file = open("high_score.txt", "r")
        high_score_str = high_score_file.read()
        cur_high_score = 0
        if high_score_str != "":
            cur_high_score = int(high_score_str)
        scores["best"] = Scoring("Highscore: ", (WIDTH // 2, 10), cur_high_score)
        self.sprites_to_draw.add(scores["best"])
        return scores

    def update_high_score(self):
        # CHALLENGE 4 write code to save the highscore
        pass

    def current_score(self):
        return self.scores["current"]

    def init_background(self):
        background_image = load_image('sprites/grid.png')
        self.screen.blit(background_image, [0, TOP_OFFSET])
        background_surface = self.screen.copy()
        return background_surface

    def game_run(self):
        self.running = True
        # running is set to false, when game has been quit
        while self.running:
            self.cur_time_passed = pygame.time.get_ticks()
            # after pacman's death the game has to be reset a few seconds after
            if self.time_to_reset is not None and self.cur_time_passed > self.time_to_reset:
                self.reset()
                self.time_to_reset = None

            self.handle_events()
            self.spawn_fruits()
            self.draw_frame()
            self.check_collisions()
            self.clock.tick(120)  # sets framerate
        pygame.quit()
        self.update_high_score()

    def handle_events(self):
        for event in pygame.event.get():
            self.handle_event(event)

    # reacts to player input
    def handle_event(self, event):
        if event.type == pygame.QUIT:  # the X of the window has been clicked
            self.running = False
        elif event.type == pygame.KEYDOWN:
            # CHALLENGE 5 here you should reset the game when the player presses space bar
            if event.key == ESCAPE_KEY:
                self.running = False
            self.pacman.keyboard_input(event.key)

    def spawn_fruits(self):
        # The following code is currently commented out and needs to be used for a challenge later on
        # for fruit in self.fruits:
        #     if not fruit.has_spawned and self.current_score().score > fruit.points_till_spawn:
        #         fruit.spawn(self.sprites_to_draw)
        pass

    def draw_frame(self):
        if self.is_game_over: return  # while the game over screen is displayed, no frame has to be drawn
        self.move_characters()
        self.handle_animations()

        # draw all sprites and update the screen to display the new state
        self.sprites_to_draw.draw(self.screen)
        pygame.display.update()
        self.sprites_to_draw.clear(self.screen, self.background_surface)

    def move_characters(self):
        for ghost in self.ghosts:
            self.move_character(ghost)
        self.move_character(self.pacman)

    def move_character(self, character):
        character.movement_logic()
        character.move()
        character.show(self.sprites_to_draw)

    def handle_animations(self):
        if self.cur_time_passed > self.time_for_next_animation:
            self.animate_characters()
        if self.cur_time_passed > self.time_for_next_animation:
            self.time_for_next_animation += TIME_BETWEEN_ANIMATIONS

    def animate_characters(self):
        for ghost in self.ghosts:
            ghost.animate()
        self.pacman.animate()

    def check_collisions(self):
        for ghost in self.ghosts:
            if ghost.cur_mode != 'dead':  # dead ghosts don't collide with pacman
                if self.pacman.get_current_position() == ghost.get_current_position():
                    self.ghost_collision(ghost)
        # The following code is currently commented out and needs to be used for a challenge later on
        # for fruit in self.fruits:
        #     # fruit can only collide if it is there and hasn't been eaten yet
        #     if fruit.has_spawned and not fruit.was_eaten and self.pacman.get_current_position() == fruit.get_current_position():
        #         fruit.eat_fruit()
        #         self.current_score().add_points_for(fruit.name)

    def ghost_collision(self, ghost):
        if ghost.cur_mode == "scared": # pacman has eaten a scared ghost
            self.current_score().add_points_for('ghost')
            ghost.die()
        elif ghost.cur_mode != "dead" and not self.pacman.is_dying:
            self.pacman.die()
            if len(self.pacman.hearts) == 0:
                self.game_over()
            else:
                self.time_to_reset = self.cur_time_passed + TIME_BETWEEN_ANIMATIONS * 11

    def game_over(self):
        self.is_game_over = True
        self.update_high_score()
        background_sfx.play()

        # display the game over image in the middle of the screen
        gameover_image = load_image('sprites/pacman_gameover.png')
        gameover_image = pygame.transform.scale(gameover_image, (750, 150))
        self.screen.blit(gameover_image, gameover_image.get_rect(center=self.screen.get_rect().center))
        pygame.display.update()

    def reset(self):
        for ghost in self.ghosts:
            ghost.sprite.kill()
        self.ghosts = init_ghosts(self)
        self.pacman.reset_position()
        self.pacman.change_mode("hunt")
