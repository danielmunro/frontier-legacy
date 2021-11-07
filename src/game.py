from math import floor

import pygame
import sys

from src.building import Building, TownCenter
from src.constants import TS, MENU_HEIGHT
from src.mob import Mob, Villager
from src.sprites import Spritesheet


class Player:
    food = 100
    wood = 100
    gold = 50
    stone = 0

    def __init__(self, mobs: list[Mob], buildings: list[Building], is_computer=True):
        self.mobs = mobs
        self.buildings = buildings
        self.is_computer = is_computer


class Game:
    mouse_down_start = None
    mouse_down_end = None
    is_playing = True

    def __init__(self, screen, scene, players: list[Player]):
        self.screen = screen
        self.scene = scene
        self.players = players
        self.sprites = Spritesheet()
        self.sprites.terrain = [
                [
                    self.sprites.create(0, 0),
                    self.sprites.create(1, 0),
                ],
                [
                    self.sprites.create(2, 0),
                    self.sprites.create(3, 0),
                ],
                [
                    self.sprites.create(0, 24),
                    self.sprites.create(1, 24),
                ],
                [
                    self.sprites.create(0, 24),
                    self.sprites.create(1, 24),
                ],
                [
                    self.sprites.create(2, 24),
                    self.sprites.create(3, 24),
                ],
            ]
        self.sprites.buildings = {
            TownCenter.__class__: [
                self.sprites.create(2, 7),
                self.sprites.create(3, 7),
                self.sprites.create(2, 8),
                self.sprites.create(3, 8),
            ],
        }
        self.sprites.mobs = {
            Villager.__class__: [
                self.sprites.create(5, 13),
                self.sprites.create(6, 13),
            ],
        }
        self.background = pygame.Surface(screen.get_size()).convert_alpha()
        self.background.fill((0, 0, 0))
        self.show_menu = False

    def loop(self):
        self._handle_events()
        self._unit_move()
        self._unit_harvest()
        self._unit_attack()
        self._draw_scene()
        self._draw_players()
        self._draw_mouse_border()
        if self.show_menu:
            self._draw_menu()

    def _draw_mouse_border(self):
        if self.mouse_down_start:
            pos = pygame.mouse.get_pos()
            width = pos[0] - self.mouse_down_start[0]
            height = pos[1] - self.mouse_down_start[1]
            surface = pygame.Surface([width, height]).convert_alpha()
            pygame.draw.rect(surface, (255, 255, 255), (0, 0, width, height), 1)
            self.screen.blit(surface, self.mouse_down_start)

    def _handle_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                sys.exit()
            elif event.type == pygame.KEYDOWN:
                # key_down(event.key, event.unicode)
                pass
            elif event.type == pygame.MOUSEBUTTONDOWN:
                self.mouse_down_start = pygame.mouse.get_pos()
            elif event.type == pygame.MOUSEBUTTONUP:
                self.mouse_down_end = pygame.mouse.get_pos()
                self._evaluate_mouse_click()

    def _evaluate_mouse_click(self):
        start = (self.mouse_down_start[0] / TS, self.mouse_down_start[1] / TS)
        end = (self.mouse_down_end[0] / TS, self.mouse_down_end[1] / TS)
        player = self.players[0]
        clicked = False
        for building in player.buildings:
            building.selected = False
        for mob in player.mobs:
            mob.selected = False
        for building in player.buildings:
            building_start = building.coords
            building_end = (building.coords[0] + building.unit.size, building.coords[1] + building.unit.size)
            if start[0] >= building_start[0] and \
                    start[1] >= building_start[1] and \
                    end[0] <= building_end[0] and \
                    end[1] <= building_end[1]:
                clicked = True
                building.selected = not building.selected
        for mob in player.mobs:
            if floor(start[0]) <= mob.coords[0] <= floor(end[0]) and \
                    floor(start[1]) <= mob.coords[1] <= floor(end[1]):
                clicked = True
                mob.selected = not mob.selected
        self.show_menu = clicked
        self.mouse_down_start = None
        self.mouse_down_end = None

    def _draw_scene(self):
        for layer in self.scene:
            for y in range(len(layer)):
                for x in range(len(layer[y])):
                    index = layer[y][x]
                    self.background.blit(self.sprites.terrain[index][(x + y) % 2 == 0], (x * TS, y * TS))
        self.screen.blit(self.background, (0, 0))

    def _unit_move(self):
        pass

    def _draw_players(self):
        for player in self.players:
            for building in player.buildings:
                surface = building.unit.draw(self.sprites)
                self.screen.blit(surface, (building.coords[0] * TS, building.coords[1] * TS))
                if building.selected:
                    pygame.draw.rect(
                        self.screen,
                        (255, 255, 255),
                        (
                            building.coords[0] * TS,
                            building.coords[1] * TS,
                            building.unit.size * TS,
                            building.unit.size * TS,
                        ),
                        1,
                    )
            for mob in player.mobs:
                surface = mob.unit.draw(self.sprites)
                self.screen.blit(surface, (mob.coords[0] * TS, mob.coords[1] * TS))
                if mob.selected:
                    pygame.draw.rect(
                        self.screen,
                        (255, 255, 255),
                        (
                            mob.coords[0] * TS,
                            mob.coords[1] * TS,
                            TS,
                            TS,
                        ),
                        1,
                    )

    def _unit_attack(self):
        pass

    def _unit_harvest(self):
        pass

    def _draw_menu(self):
        coords = self.screen.get_size()
        surface = pygame.Surface([coords[0], MENU_HEIGHT])
        surface.fill((0, 100, 200))
        self.screen.blit(surface, (0, coords[1] - MENU_HEIGHT))
