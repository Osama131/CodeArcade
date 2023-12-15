import math
import random
import time
import numpy as np

from Character import Character
from CharacterMode import CharacterMode
from game_constants import DIRECTIONS, RIGHT, NONE, COLUMN_COUNT, LEFT,  UP, TILE_SIZE, TOP_OFFSET
from game_grid import game_grid, map_index_to_coordinates, map_coordinates_to_index, map_column_row_to_coordinates
from MovableSprite import MovableSprite
from sounds import eat_ghost_sfx


def get_opposite_dir(direction):
    if direction == RIGHT or direction == UP:
        opposite_direction = direction + 1
    else:
        opposite_direction = direction - 1
    return opposite_direction


# Ghost inherits all function of the class Character
class Ghost(Character):
    def __init__(self, name, pos, normal_sprite_file, target_coords, game, time_till_leaving_house=0):
        # dictonary for the different modi pacman has (hunt or dead)
        self.modi : dict[str, CharacterMode] = {
            "scatter": CharacterMode(MovableSprite(normal_sprite_file, 8), 2, True),
            "hunt": CharacterMode(MovableSprite(normal_sprite_file, 8), 2, True),
            "dead": CharacterMode(MovableSprite(dead_sprite_file, 4), 4, False),
            "scared": CharacterMode(MovableSprite(scared_sprite_file, 4), 4, False)
        }

        self.cur_mode = "scatter"
        sprite = self.modi[self.cur_mode].sprite
        self.previous_mode = "scatter"
        self.game = game
        self.target_coords = target_coords
        sprite = self.modi[self.cur_mode].sprite
        self.new_direction = LEFT
        self.start_time = time.time()

        # logic for ghosts to leave the house after a certain amount of time
        self.in_house = time_till_leaving_house > 0
        self.time_till_leaving_house = time_till_leaving_house

        # target_coords = coordinates which the ghost moves towards during scatter mode
        self.target_coords = target_coords


        # call the initialization function of the class we are inheriting from (needs to happen)
        Character.__init__(self, name, pos, sprite)

    def movement_logic(self): # called every frame
        # some movement/changes happens after specific amounts of time
        elapsed_time = time.time() - self.start_time
        # CHALLENGE 6 ghost should hunt pacman
        # leave the house after spawning
        if self.in_house and elapsed_time > self.time_till_leaving_house:
            self.teleport(in_front_of_house_pos)
            self.in_house = False
        # change back from being scared
        if elapsed_time > 6 and self.cur_mode == "scared":
            self.change_mode(self.previous_mode)
        # dead ghost has found back to home
        if self.cur_mode == "dead" and (self.x, self.y) == in_front_of_house_pos:
            self.teleport(pinky_start_pos)
            self.change_mode('scatter')
            self.start_time = time.time()
            self.in_house = True
            self.time_till_leaving_house = 1
        # only check (and maybe change) direction when sprite is in tile center
        if not self.is_in_tile_centre(): return
        if self.warp(): return
        self.check_current_direction(self.direction)

    def die(self):
        # CHALLENGE 1 example:
        eat_ghost_sfx.play()
        self.previous_mode = self.cur_mode
        self.change_mode("dead")

    def get_direction_closest_to_target(self, possible_directions, target_coords):
        distances = []
        for possible_dir in possible_directions:
            next_index = self.get_next_index(possible_dir)
            coords = map_index_to_coordinates(next_index)
            dist = math.dist(coords, target_coords) # gets the distance between the given coordinates
            distances.append(dist)
        min_dist = min(distances)
        new_direction_index = distances.index(min_dist)
        return possible_directions[new_direction_index]

    def teleport(self, coords):
        self.x, self.y = coords
        self.change_direction(LEFT)
        self.grid_index = map_coordinates_to_index(self.x, self.y)

    def make_scared(self):
        self.previous_mode = self.cur_mode
        self.change_mode("scared")
        self.start_time = time.time()

        # CHALLENGE 8 the ghosts should change their direction to the opposite

    def get_new_direction_for_intersection(self, possible_directions):
        directions_without_walls = list(filter(self.is_next_tile_wall, possible_directions))
        # the decision on how to move differs between modes and ghosts
        if self.cur_mode == "scatter":
            # each ghost moves towards their own target
            return self.get_direction_closest_to_target(directions_without_walls, self.target_coords)
        elif self.cur_mode == "scared":
            # ghosts pick randomly
            return random.choice(directions_without_walls)
        elif self.cur_mode == "hunt":
            # ghosts have different hunting patterns
            if self.name == "blinky":
                target_coords = self.game.pacman.x, self.game.pacman.y
                return self.get_direction_closest_to_target(directions_without_walls, target_coords)
            elif self.name == "pinky":
                target_coords = self.get_tile_in_front_of_pacman(4)
                return self.get_direction_closest_to_target(directions_without_walls, target_coords)
            # CHALLENGE 7 clyde should have his own logic
            else:
                blinky_pos = self.game.ghosts[0].x, self.game.ghosts[0].y
                pacman_pos = self.get_tile_in_front_of_pacman(2)
                blinky_vec = np.array(blinky_pos)
                pacman_vec = np.array(pacman_pos)
                dist_vec = pacman_vec - blinky_vec
                new_pos = blinky_vec + dist_vec * 2
                return self.get_direction_closest_to_target(directions_without_walls, tuple(new_pos))
        # CHALLENGE 3.2 this should be called when the ghost is dead:
        self.die()
        '''target_coords = (13 * TILE_SIZE + TILE_SIZE // 2, TOP_OFFSET + 11 * TILE_SIZE + TILE_SIZE // 2)
        return self.get_direction_closest_to_target(directions_without_walls, target_coords)'''

    def get_tile_in_front_of_pacman(self, number_of_tiles):
        pacman_direction = DIRECTIONS[self.game.pacman.direction]
        target_x = self.game.pacman.x + pacman_direction[0] * TILE_SIZE * number_of_tiles
        target_y = self.game.pacman.y + pacman_direction[1] * TILE_SIZE * number_of_tiles
        return (target_x, target_y)

    def check_current_direction(self, direction):
        next_index = self.get_next_index(direction)
        new_direction = direction
        # ghost is in front of a wall
        if game_grid[next_index] == 9:
            possible_directions = self.get_possible_directions_except_opposite()
            possible_directions.remove(direction)
            if game_grid[self.grid_index] in (3, 4):
                new_direction = self.get_new_direction_for_intersection(possible_directions)
            else:
                new_direction = self.get_possible_direction(possible_directions[0], possible_directions[1])
            self.directX, self.directY = DIRECTIONS[NONE]
        # ghost is on an intersection
        elif game_grid[self.grid_index] in (3, 4):
            possible_directions = self.get_possible_directions_except_opposite()
            new_direction = self.get_new_direction_for_intersection(possible_directions)
        if direction != new_direction:
            self.change_direction(new_direction)

    def get_possible_directions_except_opposite(self):
        opposite_direction = get_opposite_dir(self.direction)
        possible_directions = [0, 1, 2, 3]
        possible_directions.remove(opposite_direction)
        return possible_directions

    def get_next_index(self, direction):
        directX, directY = DIRECTIONS[direction]
        next_index = self.grid_index + directX + directY * COLUMN_COUNT
        return next_index

    def get_possible_direction(self, option_one, option_two):
        next_index_one = self.get_next_index(option_one)
        if game_grid[next_index_one] == 9:
            return option_two
        else:
            return option_one

    def is_next_tile_wall(self, direction):
        next_index = self.get_next_index(direction)
        return game_grid[next_index] != 9


scared_sprite_file = 'sprites/Ghost_blink.png'
dead_sprite_file = 'sprites/Ghost_die.png'

# positions that are often used
in_front_of_house_pos = map_column_row_to_coordinates(13, 11)
pinky_start_pos = map_column_row_to_coordinates(14, 14)
inky_start_pos = map_column_row_to_coordinates(13, 14)
clyde_start_pos = map_column_row_to_coordinates(15, 14)


def init_ghosts(game):
    ghosts: list[Ghost] = []

    blinky = Ghost('blinky', in_front_of_house_pos, 'sprites/Blinky_tileset.png', (636, 12), game)
    ghosts.append(blinky)

    pinky = Ghost('pinky', pinky_start_pos, 'sprites/Pinky_tileset.png', (36, 12), game, 2)
    ghosts.append(pinky)

    inky = Ghost('pinky', inky_start_pos, 'sprites/Inky_tileset.png', (636, 832), game, 4)
    ghosts.append(inky)

    clyde = Ghost('clyde', clyde_start_pos, 'sprites/Clyde_tileset.png', (12, 832), game, 6)
    ghosts.append(clyde)

    return ghosts
