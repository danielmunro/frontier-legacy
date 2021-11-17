import pygame

from src.constants import TS, Actions
from src.mob import MobUnit, Villager, Ruffian
from src.resources import Costs
from src.sprites import Spritesheet


class BuildingUnit:
    def __init__(self, hp, defense, build_time, costs, action, size=1):
        self.hp = hp
        self.defense = defense
        self.build_time = build_time
        self.costs = costs
        self.action = action
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
            Actions.BUILD_TOWN_CENTER,
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
            30,
            Costs(0, 50, 0, 0),
            Actions.BUILD_HOUSE,
            1,
        )

    def trains(self) -> list[MobUnit]:
        return []

    def draw(self, sprites: Spritesheet):
        surface = pygame.Surface([TS * 2, TS * 2]).convert_alpha()
        surface.blit(sprites.buildings[House][0], (0, 0))
        return surface


class Building:
    selected = False
    built = False
    built_amount = 0
    last_build_tick = 0

    def __init__(self, unit: BuildingUnit, coords):
        self.unit = unit
        self.hp = unit.hp
        self.coords = coords
