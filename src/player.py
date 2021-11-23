from math import floor

import pygame

from src.building import Building, TownCenter, create_building_from_action
from src.constants import Colors, HEIGHT, WIDTH, TS, MAX_ALPHA
from src.mob import Mob, Villager
from src.pathfind import create_neighbors


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
                surface.set_alpha(
                    (MAX_ALPHA / 2) + ((MAX_ALPHA * (building.built_amount / building.unit.build_time)) / 2)
                )
                building.progress_bar.draw()
                surface.blit(building.progress_bar.surface, (0, 13))
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

    def train_mobs(self, ticks):
        for building in self.buildings:
            if len(building.queue) > 0:
                mob = building.queue[0]
                amount = floor((ticks - mob.last_built_ticks) / 1000)
                if amount > 1:
                    mob.time_built += amount
                    mob.last_built_ticks = ticks
                    if mob.time_built >= mob.unit.build_time:
                        self.mobs.append(mob)
                        building.queue.pop(0)

    def build_buildings(self, ticks):
        to_build = {}
        for mob in self.mobs:
            if mob.to_build is not None:
                to_build[mob.to_build] = mob
        for building in self.buildings:
            if not building.built:
                try:
                    mob_building = to_build[building.unit.action]
                except KeyError:
                    continue
                if not building.last_build_tick:
                    building.last_build_tick = ticks
                amount = floor((ticks - building.last_build_tick) / 1000)
                if amount > 1 and mob_building is not None:
                    neighbors = create_neighbors(building.coords)
                    next_to = False
                    for neighbor in neighbors:
                        if mob_building.coords == neighbor:
                            next_to = True
                    if not next_to:
                        continue
                    building.built_amount += amount
                    building.progress_bar.amount_completed = building.built_amount / building.unit.build_time
                    if building.built_amount >= building.unit.build_time:
                        building.built = True
                        if building.menu:
                            building.menu.enabled = True
                    building.last_build_tick = ticks

    def is_blocking(self, coords):
        for building in self.buildings:
            if building.coords == coords:
                return True

    def move_selected_mobs(self, coords):
        for mob in self.mobs:
            if mob.selected:
                mob.move_to = (floor(coords[0]), floor(coords[1]))

    def villager_build(self, action, coords) -> list[Mob]:
        self.buildings.append(Building(create_building_from_action(action), coords))
        mobs = []
        for mob in self.mobs:
            if mob.selected:
                mob.to_build = action
                mobs.append(mob)
        return mobs

    def train_mob(self, building_class, mob):
        for building in self.buildings:
            if building.selected and building.unit.__class__ == building_class:
                building.queue.append(Mob(mob, (building.coords[0], building.coords[1] + building.unit.size)))
                return
