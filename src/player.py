from src.building import Building, TownCenter
from src.mob import Mob, Villager


def get_start_buildings(player_number):
    coords = (4, 4) if player_number == 1 else (25, 25)
    return [
        Building(TownCenter(), coords),
    ]


def get_start_mobs(player_number):
    coords = (4, 5) if player_number == 1 else (25, 26)
    return [
        Mob(Villager(), (coords[0] - 1, coords[1])),
        Mob(Villager(), (coords[0], coords[1])),
        Mob(Villager(), (coords[0] + 1, coords[1])),
    ]
