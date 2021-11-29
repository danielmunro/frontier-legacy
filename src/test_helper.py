from src.player import Player, get_start_mobs, get_start_buildings
from src.sprites import Spritesheet


def create_player():
    start_pos = (10, 10)
    sprites = Spritesheet()
    player = Player(
        get_start_mobs(start_pos),
        get_start_buildings(start_pos),
        sprites,
        is_computer=False,
    )
    return player
