from math import floor

import pygame
import sys

from src.building import Building, TownCenter
from src.constants import TS, MENU_HEIGHT, Colors, Actions, HEIGHT
from src.mob import Mob, Villager
from src.mouse import get_abs_mouse
from src.resources import Resource
from src.scene import Scene
from src.sprites import Spritesheet
from src.ui import Button, Menu


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
    action = None
    menu = None

    def __init__(self, screen, scene: Scene, players: list[Player], font):
        self.screen = screen
        self.scene = scene
        self.players = players
        self.font = font
        self.sprites = Spritesheet()
        self.menu = Menu(font)
        self.background = pygame.Surface(screen.get_size()).convert_alpha()
        self.background.fill((0, 0, 0))

    def loop(self, ticks):
        self._handle_events()
        self._unit_move(ticks)
        self._unit_harvest()
        self._unit_attack()
        self._draw_scene()
        self._draw_players()
        self._draw_mouse_border()
        if self.menu.show:
            self._draw_menu()

    def _draw_mouse_border(self):
        if self.mouse_down_start:
            pos = pygame.mouse.get_pos()
            start, end = get_abs_mouse(self.mouse_down_start, pos)
            width = end[0] - start[0]
            height = end[1] - start[1]
            surface = pygame.Surface([width, height]).convert_alpha()
            pygame.draw.rect(surface, Colors.WHITE.value, (0, 0, width, height), 1)
            self.screen.blit(
                surface,
                (start, end)
            )

    def _handle_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                sys.exit()
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_m:
                    self.action = Actions.MOVE
            elif event.type == pygame.MOUSEBUTTONDOWN:
                self.mouse_down_start = pygame.mouse.get_pos()
                self.menu.handle_click_event(self.mouse_down_start)
            elif event.type == pygame.MOUSEBUTTONUP:
                self.mouse_down_end = pygame.mouse.get_pos()
                self.menu.reset_ui_elements()
                self._evaluate_mouse_click()

    def _start_moving_mobs(self, end):
        for mob in self.players[0].mobs:
            if mob.selected:
                mob.move_to = end
        self.action = None
        self.mouse_down_start = None

    def _evaluate_mouse_click(self):
        _start, _end = get_abs_mouse(self.mouse_down_start, self.mouse_down_end)
        start = (_start[0] / TS, _start[1] / TS)
        end = (_end[0] / TS, _end[1] / TS)

        if self.action == Actions.MOVE:
            self._start_moving_mobs(end)
            return

        m = self.mouse_down_end
        if self.menu.show and m[1] > HEIGHT - MENU_HEIGHT:
            self.mouse_down_start = None
            self.mouse_down_end = None
            self.action = self.menu.map_click_to_action(m)
            return

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
        self.menu.show = clicked
        self.mouse_down_start = None
        self.mouse_down_end = None

    def _draw_scene(self):
        for y in range(len(self.scene.background)):
            for x in range(len(self.scene.background[y])):
                index = self.scene.background[y][x]
                self.background.blit(self.sprites.terrain[index][(x + y) % 2 == 0], (x * TS, y * TS))
        for y in range(len(self.scene.resources)):
            for x in range(len(self.scene.resources[y])):
                index = self.scene.resources[y][x]
                resource = None
                if index == 1:
                    resource = Resource.WOOD
                elif index == 2:
                    resource = Resource.GOLD
                elif index == 3:
                    resource = Resource.STONE
                elif index == 4:
                    resource = Resource.FOOD
                if resource is not None:
                    self.background.blit(self.sprites.resources[resource], (x * TS, y * TS))
        self.screen.blit(self.background, (0, 0))

    def _unit_move(self, ticks):
        for player in self.players:
            for mob in player.mobs:
                if mob.move_to:
                    x = floor(mob.move_to[0] - mob.coords[0])
                    y = floor(mob.move_to[1] - mob.coords[1])
                    if mob.last_move_ticks is None:
                        mob.last_move_ticks = ticks
                    tick_diff = ticks - mob.last_move_ticks
                    if tick_diff > mob.unit.movement_speed:
                        amount = floor(tick_diff / mob.unit.movement_speed)
                    else:
                        amount = 0
                    if x < 0:
                        amount_x = -amount
                    elif x > 0:
                        amount_x = amount
                    else:
                        amount_x = 0
                    if y < 0:
                        amount_y = -amount
                    elif y > 0:
                        amount_y = amount
                    else:
                        amount_y = 0
                    coords_x = mob.coords[0] + amount_x
                    coords_y = mob.coords[1] + amount_y
                    mob.coords = (coords_x, coords_y)
                    if amount > 0:
                        mob.last_move_ticks = ticks
                    if mob.move_to[0] == coords_x and mob.move_to[1] == coords_y:
                        mob.move_to = None
                        mob.last_move_ticks = None

    def _draw_players(self):
        for player in self.players:
            for building in player.buildings:
                surface = building.unit.draw(self.sprites)
                self.screen.blit(surface, (building.coords[0] * TS, building.coords[1] * TS))
                if building.selected:
                    pygame.draw.rect(
                        self.screen,
                        Colors.WHITE.value,
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
                        Colors.WHITE.value,
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
        self.menu.redraw()
        self.screen.blit(self.menu.surface, (0, coords[1] - MENU_HEIGHT))

    def _button(self, label):
        return Button(
            self.font,
            label,
        )
