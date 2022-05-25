from random import random, randrange

from pygame import Surface

from src.constants import SCENE_SIZE, TS, HEIGHT, WIDTH
from src.resources import Resource


FOOD_AMOUNT_PER_UNIT = 150
WOOD_AMOUNT_PER_UNIT = 200
GOLD_AMOUNT_PER_UNIT = 600
STONE_AMOUNT_PER_UNIT = 400


def get_amount_of_resource_per_instance(resource: Resource) -> int:
    if resource == Resource.FOOD:
        return FOOD_AMOUNT_PER_UNIT
    elif resource == Resource.WOOD:
        return WOOD_AMOUNT_PER_UNIT
    elif resource == Resource.GOLD:
        return GOLD_AMOUNT_PER_UNIT
    elif resource == Resource.STONE:
        return STONE_AMOUNT_PER_UNIT
    return 0


class Scene:
    def __init__(self, background, blocking, resources, sprites):
        self.background = background
        self.blocking = blocking
        self.resources = resources
        self.sprites = sprites
        self.resource_amounts = {}
        self._initialize_resources()

    def _initialize_resources(self):
        for y in range(len(self.resources)):
            for x in range(len(self.resources[y])):
                r = self.resources[y][x]
                if r:
                    self.resource_amounts[(x, y)] = {
                        "resource": r,
                        "amount": get_amount_of_resource_per_instance(r),
                    }

    def _draw_resources(self, surface: Surface):
        for y in range(len(self.resources)):
            for x in range(len(self.resources[y])):
                resource = self.resources[y][x]
                if resource != 0:
                    surface.blit(
                        self.sprites.resources[resource], (x * TS, y * TS))

    def _draw_terrain(self, surface: Surface):
        for y in range(len(self.background)):
            for x in range(len(self.background[y])):
                index = self.background[y][x]
                surface.blit(self.sprites.terrain[index][(
                    x + y) % 2 == 0], (x * TS, y * TS))

    def is_passable(self, coords):
        x = coords[0]
        y = coords[1]
        return 0 < x < len(self.resources[0]) and 0 < y < len(
            self.resources) and self.resources[y][x] == 0

    def draw(self):
        surface = Surface([WIDTH, HEIGHT]).convert_alpha()
        self._draw_terrain(surface)
        self._draw_resources(surface)
        return surface


def create_plains():
    return [[0 if random() < 0.9 else 1 for _ in range(SCENE_SIZE[0])]
            for _ in range(SCENE_SIZE[1])]


def clear_space_around_player(player, scene):
    for x in range(player[0] - 6, player[0] + 7):
        for y in range(player[1] - 6, player[1] + 7):
            scene[y][x] = 0


def create_resources(player_start_positions):
    scene = [[0 for _ in range(SCENE_SIZE[0])] for _ in range(SCENE_SIZE[1])]
    create_forest(scene)
    create_gold(scene)
    create_stone(scene)
    for player in player_start_positions:
        clear_space_around_player(player, scene)
        add_main_patch(scene, player, randrange(1, 4), Resource.FOOD)
        add_main_patch(scene, player, randrange(1, 4), Resource.GOLD)
        add_main_patch(scene, player, randrange(1, 4), Resource.STONE)
    return scene


def add_main_patch(scene, pos, side, fill_in):
    x = randrange(pos[0] - 8, pos[0] + 8)
    y = randrange(pos[1] - 8, pos[1] + 8)
    if side == 1:
        y = randrange(pos[1] - 16, pos[1] - 8)
    elif side == 2:
        x = randrange(pos[0] + 8, pos[0] + 16)
    elif side == 3:
        y = randrange(pos[1] + 8, pos[1] + 16)
    elif side == 4:
        x = randrange(pos[0] - 16, pos[0] - 8)
    for x1 in range(x - 4, x + 4):
        for y1 in range(y - 4, y + 4):
            percent = 0.1
            if scene[y1 - 1][x1] == fill_in or scene[y1][x1 - 1] == fill_in:
                percent = 0.4
            if random() < percent:
                scene[y1][x1] = fill_in


def create_fruit_bushes(scene):
    y_len = len(scene)
    x_len = len(scene[0])
    for y in range(y_len):
        for x in range(x_len):
            if not scene[y][x]:
                percent = 0.001
                if scene[y - 1][x] == Resource.FOOD or scene[y][x -
                                                                1] == Resource.FOOD:
                    percent = 0.2
                if random() < percent:
                    scene[y][x] = Resource.FOOD


def create_stone(scene):
    y_len = len(scene)
    x_len = len(scene[0])
    for y in range(y_len):
        for x in range(x_len):
            if not scene[y][x]:
                percent = 0.001
                if scene[y - 1][x] == Resource.STONE or scene[y][x -
                                                                 1] == Resource.STONE:
                    percent = 0.15
                if random() < percent:
                    scene[y][x] = Resource.STONE


def create_gold(scene):
    y_len = len(scene)
    x_len = len(scene[0])
    for y in range(y_len):
        for x in range(x_len):
            if not scene[y][x]:
                percent = 0.001
                if scene[y - 1][x] == Resource.GOLD or scene[y][x -
                                                                1] == Resource.GOLD:
                    percent = 0.15
                if random() < percent:
                    scene[y][x] = Resource.GOLD


def create_forest(scene):
    y_len = len(scene)
    x_len = len(scene[0])
    for y in range(y_len):
        for x in range(x_len):
            percent = 0.01
            if scene[y - 1][x] == Resource.WOOD or scene[y][x -
                                                            1] == Resource.WOOD:
                percent = 0.6
            if random() < percent:
                scene[y][x] = Resource.WOOD
