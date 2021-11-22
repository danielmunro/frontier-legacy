from src.building import TownCenter, House, Barracks, LumberMill
from src.mob import Villager, Footman
from src.resources import Resource
from src.sprites import Spritesheet
import sys


def initialize_sprites(sprites: Spritesheet):
    sprites.terrain = [
        [
            sprites.create(0, 0),
            sprites.create(1, 0),
        ],
        [
            sprites.create(2, 0),
            sprites.create(3, 0),
        ],
        [
            sprites.create(0, 24),
            sprites.create(1, 24),
        ],
        [
            sprites.create(0, 24),
            sprites.create(1, 24),
        ],
        [
            sprites.create(2, 24),
            sprites.create(3, 24),
        ],
    ]
    sprites.buildings = {
        TownCenter: [
            sprites.create(2, 7),
            sprites.create(3, 7),
            sprites.create(2, 8),
            sprites.create(3, 8),
        ],
        House: [
            sprites.create(0, 1),
        ],
        Barracks: [
            sprites.create(6, 4),
        ],
        LumberMill: [
            sprites.create(2, 5),
            sprites.create(3, 5),
            sprites.create(4, 5),
            sprites.create(5, 5),
        ],
    }
    sprites.mobs = {
        Villager: [
            sprites.create(5, 13),
            sprites.create(6, 13),
        ],
        Footman: [
            sprites.create(6, 15),
        ],
    }
    sprites.resources = {
        Resource.FOOD: sprites.create(0, 44),
        Resource.GOLD: sprites.create(6, 29),
        Resource.STONE: sprites.create(6, 28),
        Resource.WOOD: sprites.create(4, 0),
    }
