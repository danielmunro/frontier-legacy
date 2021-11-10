from enum import Enum

SIZE = WIDTH, HEIGHT = 1200, 800
SCENE_SIZE = 100, 100
TS = 16
FPS_TARGET = 60
MENU_HEIGHT = 300
PADDING = 10


class Actions(Enum):
    MOVE = 1


class Colors(Enum):
    WHITE = (255, 255, 255)
    GRAY = (100, 100, 100)
    BLACK = (0, 0, 0)
    MENU_BLUE = (0, 100, 200)
