import pygame

from src.constants import TS
from src.mob import MobUnit, Villager, Ruffian
from src.resources import Costs
from src.sprites import Spritesheet


class BuildingUnit:
    def __init__(self, hp, defense, build_time, costs, size=1):
        self.hp = hp
        self.defense = defense
        self.build_time = build_time
        self.costs = costs
        self.size = size

    def trains(self) -> list[MobUnit]:
        return []

    def draw(self, sprites: Spritesheet):
        pass


class TownCenter(BuildingUnit):
    def __init__(self):
        super().__init__(
            2100,
            4,
            240,
            Costs(0, 400, 0, 100),
            2
        )

    def trains(self) -> list[MobUnit]:
        return [
            Villager()
        ]

    def draw(self, sprites: Spritesheet):
        surface = pygame.Surface([TS * 2, TS * 2]).convert_alpha()
        surface.blit(sprites.buildings[TownCenter][0], (0, 0))
        surface.blit(sprites.buildings[TownCenter][1], (TS, 0))
        surface.blit(sprites.buildings[TownCenter][2], (0, TS))
        surface.blit(sprites.buildings[TownCenter][3], (TS, TS))
        return surface


class House(BuildingUnit):
    def __init__(self):
        super().__init__(
            800,
            0,
            60,
            Costs(0, 50, 0, 0),
            1
        )

    def trains(self) -> list[MobUnit]:
        return []

    def draw(self, sprites: Spritesheet):
        surface = pygame.Surface([TS * 2, TS * 2]).convert_alpha()
        surface.blit(sprites.buildings[House][0], (0, 0))
        return surface


class Saloon(BuildingUnit):
    def __init__(self):
        super().__init__(
            700,
            1,
            120,
            Costs(0, 100, 0, 0),
        )

    def trains(self) -> list[MobUnit]:
        return [
            Ruffian()
        ]


class Building:
    selected = False
    built = False
    built_amount = 0

    def __init__(self, unit: BuildingUnit, coords):
        self.unit = unit
        self.hp = unit.hp
        self.coords = coords
