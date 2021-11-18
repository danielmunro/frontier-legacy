from enum import Enum

SIZE = WIDTH, HEIGHT = 1200, 800
SCENE_SIZE = 100, 100
TS = 16
FPS_TARGET = 60
MENU_HEIGHT = 300
PADDING = 10
MENU_COLUMN_WIDTH = 300
BUTTON_HEIGHT = 20


class Menus(Enum):
    VILLAGER = 1
    BUILD = 2
    MELEE = 3
    RANGED = 4
    SIEGE = 5


class Actions(Enum):
    MOVE = 1
    ATTACK_MOVE = 2
    ATTACK = 3
    REPAIR = 4
    HARVEST = 5
    BUILD = 6
    GARRISON = 7

    BUILD_HOUSE = 8
    BUILD_BARRACKS = 9
    BUILD_ARCHERY = 10
    BUILD_MILL = 11
    BUILD_FARM = 12
    BUILD_LUMBER_MILL = 13
    BUILD_STABLE = 14
    BUILD_CASTLE = 15
    BUILD_OUTPOST = 16
    BUILD_WALL = 17
    BUILD_TOWN_CENTER = 18


class Colors(Enum):
    WHITE = (255, 255, 255)
    GRAY = (100, 100, 100)
    BLACK = (0, 0, 0)
    MENU_BLUE = (0, 100, 200)


BUILD_ACTIONS = [
    Actions.BUILD_HOUSE,
    Actions.BUILD_BARRACKS,
    Actions.BUILD_ARCHERY,
    Actions.BUILD_MILL,
    Actions.BUILD_FARM,
    Actions.BUILD_LUMBER_MILL,
    Actions.BUILD_STABLE,
    Actions.BUILD_CASTLE,
    Actions.BUILD_OUTPOST,
    Actions.BUILD_WALL,
    Actions.BUILD_TOWN_CENTER,
]
