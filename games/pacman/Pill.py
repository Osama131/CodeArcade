from MovableSprite import MovableSprite


class Pill:
    def __init__(self, pos, is_energizer: bool):
        self.x, self.y = pos
        self.is_energizer = is_energizer
        if is_energizer:
            self.sprite = MovableSprite('sprites/Power_Pill.png', scale = False)
        else:
            self.sprite = MovableSprite('sprites/pill.png', scale = False)
        self.sprite.move(self.x,self.y, True)
