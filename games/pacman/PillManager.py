from Pill import Pill
from game_grid import map_index_to_coordinates, game_grid


class PillManager:
    def __init__(self, game):
        self.pill_array: dict[Pill] = {}
        self.game = game
        self.init_pills()

    def eat_pill(self, pill_index):
        pill_to_eat = self.pill_array.get(pill_index)
        # CHALLENGE 3.1 differentiate between an energizer and a normal pill
        if pill_to_eat is None: return # pill has already been eaten
        else:
            self.game.current_score().add_points_for("pill")
        pill_to_eat.sprite.kill(self.game.ghosts)
        del self.pill_array[pill_index]

    def init_pills(self):
        for cur_index, tile_type in enumerate(game_grid):
            if tile_type not in (1, 2, 3): continue
            # 1,3 = pill
            # 2 = energizer
            new_pill = Pill(map_index_to_coordinates(cur_index), is_energizer=(tile_type == 2))
            self.pill_array[cur_index] = new_pill
            self.game.sprites_to_draw.add(new_pill.sprite)
