from math import sqrt

import pygame
import sys

from src.all_buildings import TownCenter, Barracks
from src.all_mobs import Footman, Villager
from src.constants import TS, MENU_HEIGHT, Colors, Actions, HEIGHT, PADDING, BUILD_ACTIONS
from src.coords import px_to_tile, floor_coords
from src.mouse import get_abs_mouse
from src.pathfind import get_path, create_neighbors, find_nearest_resource
from src.player import Player
from src.resources import Resource
from src.scene import Scene
from src.ui import TopMenu


class Game:
    mouse_down_start = None
    mouse_down_end = None
    is_playing = True
    action = None
    menu = None

    def __init__(self, screen, scene: Scene, players: list[Player], sprites):
        self.screen = screen
        self.scene = scene
        self.players = players
        self.top_menu = TopMenu(self.players[0])
        self.sprites = sprites
        self.number_font = pygame.font.Font('freesansbold.ttf', 12)
        self.background = pygame.Surface(screen.get_size()).convert_alpha()
        self.background.fill(Colors.BLACK.value)

    def loop(self, ticks):
        self._handle_events()
        self._unit_move(ticks)
        self._build_buildings(ticks)
        self._train_mobs(ticks)
        self._harvest(ticks)
        self._draw_scene()
        self._draw_players()
        self._draw_mouse_border()
        self.screen.blit(self.top_menu.draw(), (0, 0))
        if self.menu:
            self._draw_menu()

    def _draw_mouse_border(self):
        if self.mouse_down_start:
            pos = pygame.mouse.get_pos()
            start, end = get_abs_mouse(self.mouse_down_start, pos)
            width = end[0] - start[0]
            height = end[1] - start[1]
            surface = pygame.Surface([width, height]).convert_alpha()
            pygame.draw.rect(surface, Colors.WHITE.value,
                             (0, 0, width, height), 1)
            self.screen.blit(
                surface,
                (start, end)
            )

    def _handle_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                sys.exit()
            elif event.type == pygame.KEYDOWN:
                self._handle_key_down(event.key)
            elif event.type == pygame.MOUSEBUTTONDOWN:
                self._handle_mouse_down()
            elif event.type == pygame.MOUSEBUTTONUP:
                self._handle_mouse_up()

    def _handle_key_down(self, key):
        if key == pygame.K_m:
            self.action = Actions.MOVE

    def _handle_mouse_up(self):
        self.mouse_down_end = pygame.mouse.get_pos()
        if self.menu:
            self.menu.reset_ui_elements()
        self._evaluate_mouse_click()

    def _handle_mouse_down(self):
        self.mouse_down_start = pygame.mouse.get_pos()
        if self.menu:
            self.menu.handle_click_event(self.mouse_down_start)

    def _harvest(self, ticks):
        for player in self.players:
            for mob in player.mobs:
                if mob.can_harvest(player.villager_collect_amount, ticks):
                    self._villager_harvest_neighbor(player, mob, ticks)
                if mob.unit.can_harvest and mob.drop_off_building is not None:
                    self._villager_drop_off(player, mob)

    def _villager_drop_off(self, player, mob):
        neighbors = create_neighbors(mob.coords)
        for neighbor in neighbors:
            if neighbor == mob.drop_off_building.coords:
                if mob.resource_harvesting == Resource.FOOD:
                    player.food += mob.amount_collected
                elif mob.resource_harvesting == Resource.WOOD:
                    player.wood += mob.amount_collected
                elif mob.resource_harvesting == Resource.GOLD:
                    player.gold += mob.amount_collected
                elif mob.resource_harvesting == Resource.STONE:
                    player.stone += mob.amount_collected
                mob.amount_collected = 0
                mob.drop_off_building = None
                mob.move_to = self._nearest_available_neighbor(
                    mob.coords,
                    find_nearest_resource(
                        self, mob.coords, mob.resource_harvesting),
                )
                return

    def _villager_harvest_neighbor(self, player, mob, ticks):
        neighbors = create_neighbors(mob.coords)
        for neighbor in neighbors:
            try:
                amount = self.scene.resource_amounts[neighbor]
            except KeyError:
                continue
            if amount is not None and amount["resource"] == mob.resource_harvesting:
                amount["amount"] -= 1
                mob.amount_collected += 1
                mob.last_collection_ticks = ticks
                if amount["amount"] < 1:
                    del self.scene.resource_amounts[neighbor]
                    self.scene.resources[neighbor[1]][neighbor[0]] = 0
                    mob.move_to = self._nearest_available_neighbor(
                        mob.coords,
                        find_nearest_resource(
                            self, mob.coords, mob.resource_harvesting)
                    )
                if mob.amount_collected == player.villager_collect_amount:
                    building = next(
                        filter(
                            lambda b: mob.resource_harvesting in b.unit.resource_drop_off,
                            player.buildings))
                    mob.move_to = self._nearest_available_neighbor(
                        mob.coords, building.coords)
                    mob.drop_off_building = building
                return

    def _train_mobs(self, ticks):
        for player in self.players:
            player.train_mobs(ticks)

    def _build_buildings(self, ticks):
        for player in self.players:
            player.build_buildings(ticks)

    def _start_moving_mobs(self, coords):
        self.players[0].move_selected_mobs(coords)

    def _villager_build(self, coords):
        coords = floor_coords(coords)
        mobs = self.players[0].villager_build(self.action, coords)
        for mob in mobs:
            mob.move_to = self._nearest_available_neighbor(mob.coords, coords)
            mob.resource_harvesting = None

    def _train_mob(self, building_class, mob):
        self.players[0].train_mob(building_class, mob)

    def _evaluate_mouse_click(self):
        _start, _end = get_abs_mouse(
            self.mouse_down_start, self.mouse_down_end)
        start = px_to_tile(_start)
        end = px_to_tile(_end)

        if self.menu and self.mouse_down_end[1] > HEIGHT - MENU_HEIGHT:
            self._evaluate_menu_click()
            return

        if self.action is not None and self._evaluate_action(end):
            self.action = None
            self.mouse_down_start = None
            return

        player = self.players[0]
        player.deselect_all()
        clicked, enabled = player.select_from_box(start, end)
        if clicked:
            self.menu = clicked.unit.get_menu()
            self.menu.enabled = enabled
            self.menu.player = player
            clicked.menu = self.menu
        else:
            self.menu = None
        self.mouse_down_start = None
        self.mouse_down_end = None

    def _evaluate_menu_click(self):
        self.mouse_down_start = None
        m = self.mouse_down_end
        self.mouse_down_end = None
        self.action = self.menu.map_click_to_action(m)
        if self.action == Actions.TRAIN_VILLAGER:
            self._train_mob(TownCenter, Villager())
        elif self.action == Actions.TRAIN_FOOTMAN:
            self._train_mob(Barracks, Footman())

    def _evaluate_action(self, end):
        if self.action == Actions.MOVE:
            self._start_moving_mobs(end)
            return True
        elif self.action == Actions.HARVEST:
            self._start_moving_mobs(end)
            selected_mobs = self.players[0].get_selected_mobs()
            floor_end = floor_coords(end)
            for sel in selected_mobs:
                nearest = self._nearest_available_neighbor(
                    sel.coords, floor_end)
                sel.set_move_to(nearest)
                sel.harvest_coords = end
                sel.resource_harvesting = self.scene.resource_amounts[floor_end]["resource"]
            return True
        elif self.action in BUILD_ACTIONS:
            self._villager_build(end)
            return True

    def _draw_scene(self):
        self.screen.blit(self.scene.draw(), (0, 0))

    def _unit_move(self, ticks):
        stationed = {}
        for player in self.players:
            for mob in player.mobs:
                if mob.move_to:
                    if not mob.can_move(ticks):
                        continue
                    if not mob.path:
                        mob.path = get_path(self, mob.coords, mob.move_to)
                    move_to = mob.get_next_path()
                    if not move_to:
                        continue
                    if not self.is_passable(move_to):
                        mob.reset()
                        if mob.coords in stationed:
                            self._move_mob_disperse(mob, stationed, ticks)
                        continue
                    mob.move(ticks, move_to)
                elif mob.coords in stationed:
                    self._move_mob_disperse(mob, stationed, ticks)
                elif mob.resource_harvesting is None:
                    stationed[mob.coords] = 1

    def _nearest_available_neighbor(self, from_coords, to_coords):
        least_cost = None
        nearest_neighbor = None
        for neighbor in create_neighbors(to_coords):
            if self.is_passable(neighbor):
                cost = sqrt(
                    pow(neighbor[0] - from_coords[0], 2) + pow(neighbor[1] - from_coords[1], 2))
                if least_cost is None or cost < least_cost:
                    least_cost = cost
                    nearest_neighbor = neighbor
        return nearest_neighbor

    def _move_mob_disperse(self, mob, stationed, ticks):
        for neighbor in create_neighbors(mob.coords):
            if self.is_passable(neighbor) and neighbor not in stationed:
                mob.move_to = neighbor
                mob.last_move_ticks = ticks
                stationed[neighbor] = mob
                return

    def is_passable(self, coords):
        for player in self.players:
            if player.is_blocking(coords):
                return False
        return self.scene.is_passable(coords)

    def _draw_players(self):
        for player in self.players:
            self.screen.blit(player.draw(), (0, 0))

    def _draw_menu(self):
        coords = self.screen.get_size()
        self.menu.surface.fill(Colors.MENU_BLUE.value)
        self.menu.redraw()
        mx, my = pygame.mouse.get_pos()
        for action, b in self.menu.drawn_buttons.items():
            bx, by = b.coords
            ymod = HEIGHT - MENU_HEIGHT
            if bx < mx < bx + b.width and by < my - ymod < by + b.height and b.helper_text:
                self.screen.blit(self.menu.draw_helper_text(b.action), (0, ymod - 40))
        self._draw_selected()
        self.screen.blit(self.menu.surface, (0, coords[1] - MENU_HEIGHT))

    def _draw_selected(self):
        mobs = {}
        for mob in self.players[0].mobs:
            if mob.selected:
                if mob.unit.__class__ not in mobs:
                    mobs[mob.unit.__class__] = {"mob": mob.unit, "count": 0}
                mobs[mob.unit.__class__]["count"] += 1
        offset_x = 0
        for mob in mobs.keys():
            s = mobs[mob]["mob"].draw(self.sprites)
            self.menu.surface.blit(s, (offset_x * TS, PADDING))
            self.menu.surface.blit(
                self.number_font.render(
                    str(mobs[mob]["count"]), True, Colors.WHITE.value),
                ((offset_x * TS) + TS, PADDING + 4),
            )
            offset_x += 2
