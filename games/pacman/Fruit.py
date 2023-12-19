from sounds import eat_fruit_sfx
from MovableSprite import MovableSprite
from game_grid import map_coordinates_to_index


#CHALLENGE
class Fruit:
    def __init__(self, name, pos, sprite_file, points_till_spawn):
        self.name = name
        self.x, self.y = pos
        self.sprite = MovableSprite(sprite_file)
        self.has_spawned = False
        self.was_eaten = False
        self.points_till_spawn = points_till_spawn

    def spawn(self, sprite_group):
        self.sprite.move(self.x, self.y, True)
        self.has_spawned = True
        sprite_group.add(self.sprite)

    def eat_fruit(self):
        eat_fruit_sfx.play()
        self.sprite.kill()
        self.was_eaten = True

    def get_current_position(self):
        return map_coordinates_to_index(self.x, self.y)
