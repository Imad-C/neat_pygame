from enum import Enum

class Settings(Enum):
    WIN_WIDTH = 800
    WIN_HEIGHT = 500
    SPEED = 60
    BLOCK_SIZE = 25

class Colour(Enum):
    BLACK = (0,0,0)
    GRAY = (125,125,125)
    TRANSP_GRAY = (125,125,125,90)
    BLUE = (0,0,200)
    LIGHT_BLUE = (0,150,255)
    GREEN = (0,200,0)
    LIGHT_GREEN = (0,255,0)
    RED = (200,0,0),
    LIGHT_RED = (255,0,0)

class Direction(Enum):
    LEFT = 1
    RIGHT = 2
    NONE = 3
