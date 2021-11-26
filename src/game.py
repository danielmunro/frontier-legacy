from math import floor, sqrt

import pygame
import sys

from src.building import TownCenter, Barracks, all_buildings
from src.constants import TS, MENU_HEIGHT, Colors, Actions, HEIGHT, PADDING, BUILD_ACTIONS
from src.coords import is_within, px_to_tile, floor_coords
from src.mob import Villager, Footman, all_mobs, Mob
from src.mouse import get_abs_mouse
from src.pathfind import get_path, create_neighbors
from src.player import Player
from src.scene import Scene
from src.ui import TopMenu


class Game:
    mouse_down_start = None
    mouse_down_end = None
    is_playing = True
    action = None
    menu = None
    all_units = all_mobs + all_buildings

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
                if self.menu:
                    self.menu.handle_click_event(self.mouse_down_start)
            elif event.type == pygame.MOUSEBUTTONUP:
                self.mouse_down_end = pygame.mouse.get_pos()
                if self.menu:
                    self.menu.reset_ui_elements()
                self._evaluate_mouse_click()

    def _harvest(self, ticks):
        for player in self.players:
            for mob in player.mobs:
                if mob.unit.__class__ == Villager and mob.harvest_coords is not None and not mob.move_to and \
                        (mob.last_collection_ticks is None or ticks - mob.last_collection_ticks > 1000) and \
                        mob.amount_collected < 10:
                    print("sanity")
                    neighbors = create_neighbors(mob.coords)
                    for neighbor in neighbors:
                        try:
                            amount = self.scene.resource_amounts[neighbor]
                        except KeyError:
                            continue
                        print("found amount")
                        if amount is not None and amount["resource"] == mob.resource_harvesting:
                            amount["amount"] -= 1
                            mob.amount_collected += 1
                            mob.last_collection_ticks = ticks
                            print("amount harvested", mob.amount_collected)

                # part 2 -- return to collection building
                # part 3 -- go back to harvest more

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

    def _train_mob(self, building_class, mob):
        self.players[0].train_mob(building_class, mob)

    def _evaluate_mouse_click(self):
        _start, _end = get_abs_mouse(self.mouse_down_start, self.mouse_down_end)
        start = px_to_tile(_start)
        end = px_to_tile(_end)
        m = self.mouse_down_end

        if self.menu and m[1] > HEIGHT - MENU_HEIGHT:
            self.mouse_down_start = None
            self.mouse_down_end = None
            self.action = self.menu.map_click_to_action(m)
            if self.action == Actions.TRAIN_VILLAGER:
                self._train_mob(TownCenter, Villager())
            elif self.action == Actions.TRAIN_FOOTMAN:
                self._train_mob(Barracks, Footman())
            return

        if self.action is not None:
            if self.action == Actions.MOVE:
                self._start_moving_mobs(end)
                self.action = None
                self.mouse_down_start = None
                return
            elif self.action == Actions.HARVEST:
                self._start_moving_mobs(end)
                selected_mobs = self._get_selected()
                floor_end = floor_coords(end)
                for sel in selected_mobs:
                    nearest = self._nearest_available_neighbor(sel.coords, floor_end)
                    sel.set_move_to(nearest)
                    sel.harvest_coords = end
                    sel.resource_harvesting = self.scene.resource_amounts[floor_end]["resource"]
                self.action = None
                self.mouse_down_start = None
                return
            elif self.action in BUILD_ACTIONS:
                self._villager_build(end)
                self.action = None
                self.mouse_down_start = None
                return

        player = self.players[0]
        clicked = None
        built = True
        for building in player.buildings:
            building.selected = False
        for mob in player.mobs:
            mob.selected = False
        for building in player.buildings:
            building_start = building.coords
            building_end = (building.coords[0] + building.unit.size, building.coords[1] + building.unit.size)
            if is_within((start, end), (building_start, building_end)):
                clicked = building
                built = building.built
                building.selected = True
        for mob in player.mobs:
            if floor(start[0]) <= mob.coords[0] <= floor(end[0]) and \
                    floor(start[1]) <= mob.coords[1] <= floor(end[1]):
                clicked = mob
                mob.selected = True
        if clicked:
            self.menu = clicked.unit.get_menu()
            self.menu.enabled = built
            self.menu.player = player
            self.menu.all_units = self.all_units
            clicked.menu = self.menu
        else:
            self.menu = None
        self.mouse_down_start = None
        self.mouse_down_end = None

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
                else:
                    stationed[mob.coords] = 1

    def _nearest_available_neighbor(self, from_coords, to_coords):
        least_cost = None
        nearest_neighbor = None
        for neighbor in create_neighbors(to_coords):
            if self.is_passable(neighbor):
                cost = sqrt(pow(neighbor[0] - from_coords[0], 2) + pow(neighbor[1] - from_coords[1], 2))
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
                self.number_font.render(str(mobs[mob]["count"]), True, Colors.WHITE.value),
                ((offset_x * TS) + TS, PADDING + 4),
            )
            offset_x += 2

    def _get_selected(self) -> list[Mob]:
        mobs = []
        for mob in self.players[0].mobs:
            if mob.selected:
                mobs.append(mob)
        return mobs
