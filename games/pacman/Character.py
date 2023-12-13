from CharacterMode import CharacterMode
from game_constants import DIRECTIONS, COLUMN_COUNT, RIGHT, NONE
from game_grid import map_coordinates_to_index, map_index_to_coordinates, game_grid
from MovableSprite import MovableSprite


class Character:

    def __init__(self, name, pos, sprite: MovableSprite):
        self.sprite = sprite
        self.name = name

        # Starting position
        self.x, self.y = pos
        self.grid_index = map_coordinates_to_index(self.x, self.y)

        # Starting direction
        self.direction = RIGHT
        self.directX, self.directY = DIRECTIONS[self.direction]

        self.cur_animation_frame = 0

    def show(self, sprite_group):
        sprite_group.add(self.sprite)

    def move(self):
        # adjust the x and y based on the current direction
        self.x += self.directX
        self.y += self.directY
        # update the grid index, so it fits the current x and y
        self.grid_index = map_coordinates_to_index(self.x, self.y)
        self.sprite.move(self.x, self.y, True)

    def is_in_tile_centre(self):
        x_centre, y_centre = map_index_to_coordinates(self.grid_index)
        return self.x == x_centre and self.y == y_centre

    # checks if figure is on a portal tile (5 or 6) --> if not leave function, if yes use the portal
    def warp(self):
        # CHALLENGE 10
        pass


    def change_mode(self, mode):
        # replace sprite with new one
        self.sprite.kill()
        self.sprite = self.modi[mode].sprite

        self.cur_mode = mode
        self.cur_animation_frame = 0

    def change_direction(self, direction):
        self.direction = direction
        self.directX, self.directY = DIRECTIONS[direction]
        return True


    def animate(self):
        cur_mode: CharacterMode = self.modi[self.cur_mode]
        self.cur_animation_frame = (self.cur_animation_frame + 1) % cur_mode.frames_per_animation
        if cur_mode.has_direction:
            self.cur_animation_frame += cur_mode.frames_per_animation * self.direction
        cur_mode.sprite.change_image(self.cur_animation_frame)

    def get_current_position(self):
        # this is used to check for collisions with other characters
        return self.grid_index

