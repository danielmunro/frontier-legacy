from src.building import Building, TownCenter
from src.mob import Mob, Villager


def get_start_buildings(coords):
    tc = Building(TownCenter(), coords)
    tc.built = True
    return [
        tc,
    ]


def get_start_mobs(start_coords):
    coords = start_coords[0], start_coords[1] + 2
    return [
        Mob(Villager(), (coords[0] - 1, coords[1])),
        Mob(Villager(), (coords[0], coords[1])),
        Mob(Villager(), (coords[0] + 1, coords[1])),
    ]


class Player:
    food = 100
    wood = 100
    gold = 50
    stone = 0

    def __init__(self, mobs: list[Mob], buildings: list[Building], is_computer=True):
        self.mobs = mobs
        self.buildings = buildings
        self.is_computer = is_computer
