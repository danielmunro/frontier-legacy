from src.building import Building, TownCenter
from src.mob import Mob, Villager


def get_start_buildings(player_number):
    coords = (4, 4) if player_number == 1 else (25, 25)
    return [
        Building(TownCenter(), coords),
    ]


def get_start_mobs(player_number):
    coords = (4, 6) if player_number == 1 else (25, 27)
    return [
        Mob(Villager(), (coords[0] - 1, coords[1])),
        Mob(Villager(), (coords[0], coords[1])),
        Mob(Villager(), (coords[0] + 1, coords[1])),
    ]
