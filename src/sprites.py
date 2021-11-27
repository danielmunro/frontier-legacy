import pygame
from pygame import Surface

from src.constants import TS


class Spritesheet:
    terrain = []
    buildings = {}
    mobs = {}
    resources = {}

    def __init__(self):
        self.sheet = pygame.image.load(
            "./resources/sprites.png").convert_alpha()

    def create(self, x, y):
        it = Surface([TS, TS]).convert_alpha()
        it.blit(self.sheet, (0, 0), (x * TS, y * TS, TS, TS))
        return it
