#DIRECTON
RIGHT = 0
LEFT = 1
DOWN = 3
UP = 2
NONE = 4

#Space above and below maingame (for score, highscore & hearts)
TOP_OFFSET = 50
BOTTOM_OFFSET = 50

#{DIRECTION: (direct.x, direct.y)}
DIRECTIONS = {RIGHT:(1, 0), LEFT:(-1, 0), UP:(0, -1), DOWN:(0, 1), NONE: (0, 0)}

# size of one tile / square
TILE_SIZE = 24
COLUMN_COUNT, ROW_COUNT = 28, 31

WIDTH, HEIGHT = TILE_SIZE * COLUMN_COUNT, TOP_OFFSET + TILE_SIZE * ROW_COUNT + BOTTOM_OFFSET

TIME_BETWEEN_ANIMATIONS = 100
