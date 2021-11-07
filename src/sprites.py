import pygame
from pygame import Surface
from src.constants import TS


class Spritesheet:
    def __init__(self):
        self.sheet = pygame.image.load("./resources/sprites.png").convert_alpha()
        self.terrain = [
            [
                self._create_sprite(0, 0),
                self._create_sprite(1, 0),
            ],
            [
                self._create_sprite(2, 0),
                self._create_sprite(3, 0),
            ],
            [
                self._create_sprite(0, 24),
                self._create_sprite(1, 24),
            ],
            [
                self._create_sprite(0, 24),
                self._create_sprite(1, 24),
            ],
            [
                self._create_sprite(2, 24),
                self._create_sprite(3, 24),
            ],
        ]

    def _create_sprite(self, x, y):
        it = Surface([TS, TS]).convert_alpha()
        it.blit(self.sheet, (0, 0), (x * TS, y * TS, TS, TS))
        return it

# def create_sprite(sheet, x, y):
#     it = Surface([TS, TS]).convert_alpha()
#     it.blit(sheet, (0, 0), (x, y, TS, TS))
#     return it
#
#
# def get_sprites(sheet):
#     return [
#         create_sprite(sheet, x * TS, y * TS) for y in range(15) for x in range(8)
#     ]
#
#
# def get_character_sprites():
#     sheet = pygame.image.load("./resources/characters.png").convert_alpha()
#     s = Surface([192, 168]).convert_alpha()
#     s.blit(sheet, (0, 0))
#     return s
