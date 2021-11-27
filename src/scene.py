from random import random, randrange

from pygame import Surface

from src.constants import SCENE_SIZE, TS, HEIGHT, WIDTH
from src.resources import Resource


class Scene:
    def __init__(self, background, blocking, resources, sprites):
        self.background = background
        self.blocking = blocking
        self.resources = resources
        self.sprites = sprites
        self.resource_amounts = {}
        for y in range(len(self.resources)):
            for x in range(len(self.resources[y])):
                r = self.resources[y][x]
                if r:
                    amount = 0
                    if r == Resource.FOOD:
                        amount = 150
                    elif r == Resource.WOOD:
                        amount = 200
                    elif r == Resource.GOLD:
                        amount = 600
                    elif r == Resource.STONE:
                        amount = 400
                    self.resource_amounts[(x, y)] = {
                        "resource": r,
                        "amount": amount,
                    }

    def is_passable(self, coords):
        x = coords[0]
        y = coords[1]
        return 0 < x < len(self.resources[0]) and 0 < y < len(
            self.resources) and self.resources[y][x] == 0

    def draw(self):
        surface = Surface([WIDTH, HEIGHT]).convert_alpha()
        for y in range(len(self.background)):
            for x in range(len(self.background[y])):
                index = self.background[y][x]
                surface.blit(self.sprites.terrain[index][(
                    x + y) % 2 == 0], (x * TS, y * TS))
        for y in range(len(self.resources)):
            for x in range(len(self.resources[y])):
                resource = self.resources[y][x]
                if resource != 0:
                    surface.blit(
                        self.sprites.resources[resource], (x * TS, y * TS))
        return surface


def create_plains():
    return [[0 if random() < 0.9 else 1 for _ in range(SCENE_SIZE[0])]
            for _ in range(SCENE_SIZE[1])]


def create_resources(player_start_positions):
    scene = [[0 for _ in range(SCENE_SIZE[0])] for _ in range(SCENE_SIZE[1])]
    create_forest(scene)
    create_gold(scene)
    create_stone(scene)
    for player in player_start_positions:
        for x in range(player[0] - 6, player[0] + 7):
            for y in range(player[1] - 6, player[1] + 7):
                scene[y][x] = 0
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
