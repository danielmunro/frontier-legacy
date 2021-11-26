import pygame

from src.constants import TS, Actions
from src.mob import MobUnit, Villager
from src.resources import Costs, Resource
from src.sprites import Spritesheet
from src.ui import ProgressBar, Menu, TownCenterMenu, EmptyMenu, BarracksMenu


class BuildingUnit:
    def __init__(self, hp, defense, build_time, costs, action, resource_drop_off, size):
        self.hp = hp
        self.defense = defense
        self.build_time = build_time
        self.costs = costs
        self.action = action
        self.resource_drop_off = resource_drop_off
        self.size = size

    def trains(self) -> list[MobUnit]:
        return []

    def draw(self, sprites: Spritesheet):
        pass

    def get_menu(self) -> Menu:
        pass


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
            Costs(0, 150, 0, 0),
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


class Building:
    def __init__(self, unit: BuildingUnit, coords):
        self.unit = unit
        self.hp = unit.hp
        self.coords = coords
        self.progress_bar = ProgressBar()
        self.selected = False
        self.built = False
        self.built_amount = 0
        self.last_build_tick = 0
        self.queue = []
        self.menu = None


def create_building_from_action(action):
    if action == Actions.BUILD_HOUSE:
        return House()
    elif action == Actions.BUILD_BARRACKS:
        return Barracks()
    elif action == Actions.BUILD_LUMBER_MILL:
        return LumberMill()
    elif action == Actions.BUILD_MILL:
        return Mill()


all_buildings = [
    TownCenter(),
    House(),
    Barracks(),
    LumberMill(),
    Mill(),
]
