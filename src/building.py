from src.mob import MobUnit
from src.sprites import Spritesheet
from src.menu import Menu
from src.ui import ProgressBar


class BuildingUnit:
    def __init__(self, hp, defense, build_time, costs,
                 action, resource_drop_off, size):
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
