import pygame

from src.all_mobs import Villager
from src.building import BuildingUnit
from src.constants import Actions, TS
from src.mob import MobUnit
from src.resources import Resource, Costs
from src.sprites import Spritesheet
from src.ui import EmptyMenu, Menu, BarracksMenu, TownCenterMenu


class TownCenter(BuildingUnit):
    def __init__(self):
        super().__init__(
            2100,
            4,
            240,
            Costs(0, 400, 0, 100),
            Actions.BUILD_TOWN_CENTER,
            [Resource.FOOD, Resource.WOOD, Resource.GOLD, Resource.STONE],
            2,
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

    def get_menu(self) -> Menu:
        return TownCenterMenu()


class House(BuildingUnit):
    def __init__(self):
        super().__init__(
            800,
            0,
            20,
            Costs(0, 50, 0, 0),
            Actions.BUILD_HOUSE,
            [],
            1,
        )

    def trains(self) -> list[MobUnit]:
        return []

    def draw(self, sprites: Spritesheet):
        surface = pygame.Surface([TS, TS]).convert_alpha()
        surface.blit(sprites.buildings[House][0], (0, 0))
        return surface

    def get_menu(self) -> Menu:
        return EmptyMenu()


class Barracks(BuildingUnit):
    def __init__(self):
        super().__init__(
            1600,
            0,
            10,
            Costs(0, 150, 0, 0),
            Actions.BUILD_BARRACKS,
            [],
            1,
        )

    def trains(self) -> list[MobUnit]:
        return []

    def draw(self, sprites: Spritesheet):
        surface = pygame.Surface([TS, TS]).convert_alpha()
        surface.blit(sprites.buildings[Barracks][0], (0, 0))
        return surface

    def get_menu(self) -> Menu:
        return BarracksMenu()


class LumberMill(BuildingUnit):
    def __init__(self):
        super().__init__(
            1600,
            0,
            30,
            Costs(0, 100, 0, 0),
            Actions.BUILD_LUMBER_MILL,
            [Resource.WOOD],
            1,
        )

    def trains(self) -> list[MobUnit]:
        return []

    def draw(self, sprites: Spritesheet):
        surface = pygame.Surface([TS, TS]).convert_alpha()
        surface.blit(sprites.buildings[LumberMill][0], (0, 0))
        return surface

    def get_menu(self) -> Menu:
        return EmptyMenu()


class Quarry(BuildingUnit):
    def __init__(self):
        super().__init__(
            1600,
            0,
            30,
            Costs(0, 100, 0, 0),
            Actions.BUILD_QUARRY,
            [Resource.GOLD, Resource.STONE],
            1,
        )

    def trains(self) -> list[MobUnit]:
        return []

    def draw(self, sprites: Spritesheet):
        surface = pygame.Surface([TS, TS]).convert_alpha()
        surface.blit(sprites.buildings[Quarry][0], (0, 0))
        return surface

    def get_menu(self) -> Menu:
        return EmptyMenu()


class Mill(BuildingUnit):
    def __init__(self):
        super().__init__(
            1600,
            0,
            30,
            Costs(0, 150, 0, 0),
            Actions.BUILD_MILL,
            [Resource.FOOD],
            1,
        )

    def trains(self) -> list[MobUnit]:
        return []

    def draw(self, sprites: Spritesheet):
        surface = pygame.Surface([TS, TS]).convert_alpha()
        surface.blit(sprites.buildings[Mill][0], (0, 0))
        return surface

    def get_menu(self) -> Menu:
        return EmptyMenu()


def create_building_from_action(action):
    if action == Actions.BUILD_HOUSE:
        return House()
    elif action == Actions.BUILD_BARRACKS:
        return Barracks()
    elif action == Actions.BUILD_LUMBER_MILL:
        return LumberMill()
    elif action == Actions.BUILD_MILL:
        return Mill()
    elif action == Actions.BUILD_QUARRY:
        return Quarry()


all_buildings = [
    TownCenter(),
    House(),
    Barracks(),
    LumberMill(),
    Mill(),
    Quarry(),
]
