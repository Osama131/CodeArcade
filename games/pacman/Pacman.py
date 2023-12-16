import time

import pygame

from Character import Character
from CharacterMode import CharacterMode
from game_constants import TOP_OFFSET, RIGHT, LEFT, UP, DOWN, NONE, HEIGHT, TILE_SIZE, DIRECTIONS, COLUMN_COUNT

from MovableSprite import MovableSprite
from game_grid import game_grid
from sounds import pacman_death_sfx


# pacman inherits all function of the class Character
class Pacman(Character):
    def __init__(self, name, pos, game):

        # dictonary for the different modi pacman has (hunt or dead)
        self.modi: dict[str, CharacterMode] = {
            "hunt": CharacterMode(MovableSprite('sprites/Pacman_Tileset.bmp', 12), 3, True),
            "dead": CharacterMode(MovableSprite('sprites/pacman_die.bmp', 12), 12, False)
        }
        self.cur_mode = "hunt"
        sprite = self.modi[self.cur_mode].sprite
        self.hearts = []
        self.game = game
        self.is_dying = False
        self.time_of_death = None
        # call the initialization function of the class we are inheriting from (needs to happen)
        Character.__init__(self, name, pos, sprite)
        self.keyboardMemory = 0

    def die(self):
        self.change_mode("dead")
        self.is_dying = True
        self.remove_heart()
        self.time_of_death = time.time()

    def reset_position(self):
        self.x, self.y = 336, TOP_OFFSET + 564
        self.keyboardMemory = RIGHT
        self.direction = RIGHT
        self.directX, self.directY = DIRECTIONS[RIGHT]


    def movement_logic(self):
        if self.is_dying:
            if time.time() - self.time_of_death > 3:
                self.is_dying = False
        # only check (and maybe change) direction when sprite is in tile center
        if not self.is_in_tile_centre(): return
        if self.warp(): return
        self.game.pill_manager.eat_pill(self.grid_index)
        self.change_direction(self.keyboardMemory)
        self.check_current_direction(self.direction)
        if self.cur_mode == 'dead': # pacman doesn't move when he is dead
            self.change_direction(NONE)

    def check_current_direction(self, direction):
        self.directX, self.directY = DIRECTIONS[direction]
        next_index = self.grid_index + self.directX + self.directY * COLUMN_COUNT
        if game_grid[next_index] == 9:  # next tile is wall, pacman should stop
            self.directX, self.directY = DIRECTIONS[NONE]

    # Reads and saves player input
    def keyboard_input(self, key):
        if key == pygame.K_RIGHT: self.keyboardMemory = RIGHT
        if key == pygame.K_LEFT: self.keyboardMemory = LEFT
        if key == pygame.K_UP: self.keyboardMemory = UP
        if key == pygame.K_DOWN: self.keyboardMemory = DOWN

    # Adds hearts at bottom, location is dependent on the indes
    def create_heart_sprite(self, index):
        heart_sprite = MovableSprite('sprites/pacman_hearts.bmp')
        heart_sprite.move(50 + TILE_SIZE * 2 * index, HEIGHT - TILE_SIZE * 2)
        return heart_sprite

    def init_hearts(self, sprite_group):
        # CHALLENGE 9
        sprite = self.create_heart_sprite(0)
        self.hearts.append(sprite)
        sprite_group.add(sprite)

    def remove_heart(self):
        if len(self.hearts) > 0:
            heart = self.hearts.pop()
            heart.kill()
