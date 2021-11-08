from random import random

from src.constants import SCENE_SIZE


class Scene:
    def __init__(self, background, blocking, resources):
        self.background = background
        self.blocking = blocking
        self.resources = resources


def create_plains():
    return [[0 if random() < 0.9 else 1 for _ in range(SCENE_SIZE[0])] for _ in range(SCENE_SIZE[1])]


def create_resources():
    scene = [[0 for _ in range(SCENE_SIZE[0])] for _ in range(SCENE_SIZE[1])]
    for y in range(len(scene)):
        for x in range(len(scene[y])):
            percent = 0.1
            if random() < percent:
                scene[y][x] = 1
    for y in range(len(scene)):
        for x in range(len(scene[y])):
            percent = 0.01
            if random() < percent:
                scene[y][x] = 2
    for y in range(len(scene)):
        for x in range(len(scene[y])):
            percent = 0.01
            if random() < percent:
                scene[y][x] = 3
    return scene
