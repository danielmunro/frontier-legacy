from enum import Enum

import pygame

from src.constants import TS, Actions
from src.resources import Costs
from src.sprites import Spritesheet
from src.ui import VillagerMenu, Menu, MilitaryMenu


class AttackType(Enum):
    MELEE = 1
    RANGED = 2


class Gender(Enum):
    FEMALE = 1
    MALE = 2


class MobUnit:
    def __init__(
            self,
            hp,
            attack,
            attack_range,
            attack_type,
            accuracy,
            aoe,
            defense_melee,
            defense_ranged,
            movement_speed,
            build_time,
            costs,
            action,
    ):
        self.hp = hp
        self.attack = attack
        self.attack_range = attack_range
        self.attack_type = attack_type
        self.accuracy = accuracy
        self.aoe = aoe
        self.defense_melee = defense_melee
        self.defense_ranged = defense_ranged
        self.movement_speed = movement_speed
        self.build_time = build_time
        self.costs = costs
        self.action = action

    def draw(self, sprites: Spritesheet):
        pass

    def get_menu(self) -> Menu:
        pass


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
            30,
            Costs(25, 0, 0, 0),
            Actions.TRAIN_VILLAGER,
        )

    def draw(self, sprites: Spritesheet):
        surface = pygame.Surface([TS, TS]).convert_alpha()
        surface.blit(sprites.mobs[Villager][0 if self.gender == Gender.FEMALE else 1], (0, 0))
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
            Actions.TRAIN_RUFFIAN
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
        )

    def get_menu(self):
        return MilitaryMenu()


class Mob:
    def __init__(self, unit: MobUnit, coords):
        self.unit = unit
        self.hp = unit.hp
        self.coords = coords
        self.selected = False
        self.move_to = None
        self.last_move_ticks = None
        self.path = None
        self.to_build = None
        self.time_built = 0
        self.last_built_ticks = 0

    def get_next_path(self):
        try:
            return self.path.pop(0)
        except IndexError:
            self.move_to = None

    def reset(self):
        self.move_to = None
        self.last_move_ticks = None
        self.path = None

    def can_move(self, ticks):
        if self.last_move_ticks is None:
            self.last_move_ticks = ticks
        tick_diff = ticks - self.last_move_ticks
        return tick_diff > self.unit.movement_speed

    def move(self, ticks, coords):
        self.coords = coords
        self.last_move_ticks = ticks
        if self.move_to == coords:
            self.reset()


all_mobs = [
    Villager(),
    Ruffian(),
    Footman(),
    Swordsman(),
    Archer(),
    Crossbowman(),
    Rifleman(),
]
