from src.building import Building, TownCenter
from src.mob import Mob, Villager


def get_start_buildings(coords):
    return [
        Building(TownCenter(), coords),
    ]


def get_start_mobs(start_coords):
    coords = start_coords[0], start_coords[1] + 2
    return [
        Mob(Villager(), (coords[0] - 1, coords[1])),
        Mob(Villager(), (coords[0], coords[1])),
        Mob(Villager(), (coords[0] + 1, coords[1])),
    ]
