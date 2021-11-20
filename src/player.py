import pygame

from src.building import Building, TownCenter
from src.constants import Colors, HEIGHT, WIDTH, TS
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

    def __init__(self, mobs: list[Mob], buildings: list[Building], sprites, is_computer=True):
        self.mobs = mobs
        self.buildings = buildings
        self.sprites = sprites
        self.is_computer = is_computer

    def draw(self):
        scene = pygame.Surface([WIDTH, HEIGHT]).convert_alpha()
        for building in self.buildings:
            surface = building.unit.draw(self.sprites)
            if not building.built:
                surface.set_alpha(64 + (128 * (building.built_amount / building.unit.build_time)) / 2)
            scene.blit(surface, (building.coords[0] * TS, building.coords[1] * TS))
            if building.selected:
                pygame.draw.rect(
                    scene,
                    Colors.WHITE.value,
                    (
                        building.coords[0] * TS,
                        building.coords[1] * TS,
                        building.unit.size * TS,
                        building.unit.size * TS,
                    ),
                    1,
                )
        for mob in self.mobs:
            surface = mob.unit.draw(self.sprites)
            scene.blit(surface, (mob.coords[0] * TS, mob.coords[1] * TS))
            if mob.selected:
                pygame.draw.rect(
                    scene,
                    Colors.WHITE.value,
                    (
                        mob.coords[0] * TS,
                        mob.coords[1] * TS,
                        TS,
                        TS,
                    ),
                    1,
                )
        return scene
