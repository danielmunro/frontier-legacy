from math import floor

import pygame

from src.constants import SECOND_IN_MS, Actions, TS
from src.mob import MobUnit, AttackType, Gender
from src.resources import Costs
from src.sprites import Spritesheet
from src.ui import MilitaryMenu, VillagerMenu


class Villager(MobUnit):
    def __init__(self):
        self.gender = Gender.FEMALE
        super().__init__(
            20,
            1,
            1,
            AttackType.MELEE,
            1,
            1,
            0,
            0,
            800,
            60,
            Costs(25, 0, 0, 0),
            Actions.TRAIN_VILLAGER,
            True,
        )

    def draw(self, sprites: Spritesheet):
        surface = pygame.Surface([TS, TS]).convert_alpha()
        surface.blit(
            sprites.mobs[Villager][0 if self.gender == Gender.FEMALE else 1], (0, 0))
        return surface

    def get_menu(self):
        return VillagerMenu()


class Ruffian(MobUnit):
    def __init__(self):
        super().__init__(
            28,
            2,
            1,
            AttackType.MELEE,
            1,
            1,
            0,
            0,
            1,
            45,
            Costs(60, 0, 10, 0),
            Actions.TRAIN_RUFFIAN,
            False,
        )

    def get_menu(self):
        return MilitaryMenu()


class Footman(MobUnit):
    def __init__(self):
        super().__init__(
            35,
            4,
            1,
            AttackType.MELEE,
            1,
            1,
            1,
            1,
            800,
            30,
            Costs(75, 0, 20, 0),
            Actions.TRAIN_FOOTMAN,
            False,
        )

    def draw(self, sprites: Spritesheet):
        surface = pygame.Surface([TS, TS]).convert_alpha()
        surface.blit(sprites.mobs[Footman][0], (0, 0))
        return surface

    def get_menu(self):
        return MilitaryMenu()


class Swordsman(MobUnit):
    def __init__(self):
        super().__init__(
            40,
            6,
            1,
            AttackType.MELEE,
            1,
            2,
            1,
            1,
            1,
            60,
            Costs(100, 0, 25, 0),
            Actions.TRAIN_SWORDSMAN,
            False,
        )

    def get_menu(self):
        return MilitaryMenu()


class Rifleman(MobUnit):
    def __init__(self):
        super().__init__(
            35,
            8,
            6,
            AttackType.RANGED,
            0.70,
            1,
            0,
            0,
            1,
            60,
            Costs(100, 25, 25, 0),
            Actions.TRAIN_RIFLEMAN,
            False,
        )

    def get_menu(self):
        return MilitaryMenu()


class Archer(MobUnit):
    def __init__(self):
        super().__init__(
            30,
            5,
            6,
            AttackType.RANGED,
            0.85,
            1,
            0,
            0,
            1,
            55,
            Costs(50, 40, 20, 0),
            Actions.TRAIN_ARCHER,
            False,
        )

    def get_menu(self):
        return MilitaryMenu()


class Crossbowman(MobUnit):
    def __init__(self):
        super().__init__(
            35,
            6,
            6,
            AttackType.RANGED,
            0.75,
            1,
            0,
            0,
            1,
            60,
            Costs(65, 50, 25, 0),
            Actions.TRAIN_CROSSBOWMAN,
            False,
        )

    def get_menu(self):
        return MilitaryMenu()


all_mobs = [
    Villager(),
    Ruffian(),
    Footman(),
    Swordsman(),
    Archer(),
    Crossbowman(),
    Rifleman(),
]
