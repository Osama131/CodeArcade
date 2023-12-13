# holds all variables that belong to a character mode (like ghosts are scared or hunting)
class CharacterMode:
    def __init__(self, sprite, frames_per_animation, has_direction):
        self.sprite = sprite
        self.frames_per_animation = frames_per_animation
        self.has_direction = has_direction
