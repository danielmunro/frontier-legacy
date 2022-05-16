from enum import Enum
from math import floor

from src.constants import SECOND_IN_MS
from src.sprites import Spritesheet
from src.ui import Menu


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
            can_harvest,
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
        self.can_harvest = can_harvest

    def draw(self, sprites: Spritesheet):
        pass

    def get_menu(self) -> Menu:
        pass


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
        self.harvest_coords = None
        self.resource_harvesting = None
        self.amount_collected = 0
        self.last_collection_ticks = None
        self.drop_off_building = None

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

    def set_move_to(self, coords):
        self.move_to = (floor(coords[0]), floor(coords[1]))

    def can_harvest(self, collect_amount, ticks):
        return self.unit.can_harvest and self.harvest_coords is not None and not self.move_to and \
               (self.last_collection_ticks is None or ticks - self.last_collection_ticks > SECOND_IN_MS) and \
               self.amount_collected < collect_amount
