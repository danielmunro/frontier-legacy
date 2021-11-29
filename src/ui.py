from math import floor

import pygame.display
from pygame import Surface
import sys

from src.constants import Colors, MENU_HEIGHT, HEIGHT, PADDING, Actions, MENU_COLUMN_WIDTH, MAX_ALPHA, WIDTH, TS
from src.sprites import Spritesheet


def create_buttons():
    sprites = Spritesheet()
    return {
        Actions.MOVE: TextButton("Move"),
        Actions.ATTACK_MOVE: TextButton("Attack Move"),
        Actions.ATTACK: TextButton("Attack"),
        Actions.HARVEST: TextButton("Harvest"),
        Actions.BUILD: TextButton("Build"),
        Actions.REPAIR: TextButton("Repair"),
        Actions.GARRISON: TextButton("Garrison"),
        Actions.BUILD_HOUSE: ImageButton(sprites.create(0, 1)),
        Actions.BUILD_LUMBER_MILL: ImageButton(sprites.create(2, 5)),
        Actions.BUILD_MILL: ImageButton(sprites.create(3, 23)),
        Actions.BUILD_BARRACKS: ImageButton(sprites.create(6, 4)),
        Actions.TRAIN_VILLAGER: ImageButton(sprites.create(5, 13)),
        Actions.TRAIN_FOOTMAN: ImageButton(sprites.create(6, 15)),
    }


class Menu:
    def __init__(self):
        self.buttons = create_buttons()
        coords = pygame.display.get_window_size()
        self.surface = Surface([coords[0], MENU_HEIGHT])
        self.player = None
        self.all_units = []
        self.enabled = True

    def handle_click_event(self, pos):
        for b in self.buttons.values():
            if self._is_click_on_button(b, pos):
                b.is_button_pressed = True

    def map_click_to_action(self, pos):
        if not self.enabled:
            return
        for k in self.buttons:
            if self._is_click_on_button(
                    self.buttons[k], pos) and self._can_afford(k):
                return k

    def reset_ui_elements(self):
        for b in self.buttons.values():
            b.is_button_pressed = False

    @staticmethod
    def _is_click_on_button(button, pos):
        button_size = button.surface.get_size()
        return button.coords[0] < pos[0] < button_size[0] + button.coords[0] and \
            button.coords[1] < pos[1] - \
            (HEIGHT - MENU_HEIGHT) < button_size[1] + button.coords[1]

    def redraw(self):
        pass

    def draw_button(self, action: Actions, x, y):
        button = self.buttons[action]
        surface = button.render_button()
        height = surface.get_height()

        surface.set_alpha(
            MAX_ALPHA if self.enabled and self._can_afford(action) else MAX_ALPHA / 2)
        self.surface.blit(surface,
                          (PADDING + (x * MENU_COLUMN_WIDTH),
                           PADDING + (height * y)))
        button.coords = (PADDING + (x * MENU_COLUMN_WIDTH),
                         PADDING + (height * y))

    def _can_afford(self, action: Actions):
        try:
            to_create = next(
                filter(
                    lambda i: i.action == action,
                    self.all_units))
            if to_create.costs.food > self.player.food or \
                    to_create.costs.wood > self.player.wood or \
                    to_create.costs.gold > self.player.gold or \
                    to_create.costs.stone > self.player.stone:
                return False
        except StopIteration:
            pass
        return True


class VillagerMenu(Menu):
    def redraw(self):
        self.draw_button(Actions.BUILD_HOUSE, 2, 0)
        self.draw_button(Actions.BUILD_LUMBER_MILL, 2, 1)
        self.draw_button(Actions.BUILD_MILL, 2, 2)
        self.draw_button(Actions.BUILD_BARRACKS, 2, 3)

        self.draw_button(Actions.MOVE, 3, 0)
        self.draw_button(Actions.HARVEST, 3, 1)
        self.draw_button(Actions.BUILD, 3, 2)
        self.draw_button(Actions.ATTACK, 3, 3)
        self.draw_button(Actions.GARRISON, 3, 4)


class MilitaryMenu(Menu):
    def redraw(self):
        self.draw_button(Actions.MOVE, 3, 0)
        self.draw_button(Actions.ATTACK, 3, 1)
        self.draw_button(Actions.GARRISON, 3, 2)


class TownCenterMenu(Menu):
    def redraw(self):
        self.draw_button(Actions.TRAIN_VILLAGER, 2, 0)


class BarracksMenu(Menu):
    def redraw(self):
        self.draw_button(Actions.TRAIN_FOOTMAN, 2, 0)


class EmptyMenu(Menu):
    def redraw(self):
        pass


class ImageButton:
    def __init__(self, image):
        self.image = image
        self.is_button_pressed = False
        self.size = self.image.get_size()
        self.surface = Surface(
            [self.size[0] + (PADDING * 2), self.size[1] + (PADDING * 2)])
        self.coords = (0, 0)
        self.disabled = False

    def render_button(self):
        self.surface.fill(Colors.RED.value if self.is_button_pressed else Colors.BLACK.value)
        self.surface.blit(self.image, (PADDING, PADDING))
        pygame.draw.rect(
            self.surface,
            Colors.WHITE.value,
            (0, 0, self.size[0] + (PADDING * 2), self.size[1] + (PADDING * 2)),
            1,
        )
        return self.surface


class TextButton:
    def __init__(self, label):
        self.font = self.button_font = pygame.font.Font('freesansbold.ttf', 24)
        self.label = label
        self.is_button_pressed = False
        rendered = self._render_text()
        self.size = rendered.get_size()
        self.surface = Surface(
            [self.size[0] + (PADDING * 2), self.size[1] + (PADDING * 2)])
        self.coords = (0, 0)
        self.disabled = False

    def render_button(self):
        self.surface.fill(Colors.BLACK.value)
        self.surface.blit(self._render_text(), (PADDING, PADDING))
        pygame.draw.rect(
            self.surface,
            Colors.WHITE.value,
            (0, 0, self.size[0] + (PADDING * 2), self.size[1] + (PADDING * 2)),
            1,
        )
        return self.surface

    def _render_text(self):
        return self.font.render(
            self.label,
            True,
            Colors.GRAY.value if self.is_button_pressed else Colors.WHITE.value,
            Colors.BLACK.value,
        )


class ProgressBar:
    amount_completed = 0
    surface = Surface([16, 3])

    def draw(self):
        pygame.draw.rect(self.surface, Colors.RED.value, (0, 0, 16, 3))
        pygame.draw.rect(self.surface, Colors.GREEN.value,
                         (0, 0, floor(16 * self.amount_completed), 3))


class TopMenu:
    surface = Surface([WIDTH, TS])

    def __init__(self, player):
        self.player = player
        self.font = pygame.font.Font('freesansbold.ttf', 14)

    def draw(self):
        self.surface.fill(Colors.MENU_BLUE.value)
        text = self.font.render(
            f'{self.player.food} food - {self.player.wood} wood - {self.player.gold} gold - {self.player.stone} stone',
            True,
            Colors.WHITE.value,
            Colors.MENU_BLUE.value)
        self.surface.blit(text, (1, 1))
        return self.surface
