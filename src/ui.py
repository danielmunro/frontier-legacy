from math import floor

import pygame.display
from pygame import Surface

from src.constants import Colors, MENU_HEIGHT, HEIGHT, PADDING, Actions, MENU_COLUMN_WIDTH, MAX_ALPHA


def create_buttons():
    return {
        Actions.MOVE: Button("Move"),
        Actions.ATTACK_MOVE: Button("Attack Move"),
        Actions.ATTACK: Button("Attack"),
        Actions.HARVEST: Button("Harvest"),
        Actions.BUILD: Button("Build"),
        Actions.REPAIR: Button("Repair"),
        Actions.GARRISON: Button("Garrison"),
        Actions.BUILD_HOUSE: Button("House"),
        Actions.BUILD_LUMBER_MILL: Button("Lumber Mill"),
        Actions.BUILD_MILL: Button("Mill"),
        Actions.BUILD_BARRACKS: Button("Barracks"),
        Actions.TRAIN_VILLAGER: Button("Villager"),
        Actions.TRAIN_FOOTMAN: Button("Footman"),
    }


class Menu:
    def __init__(self):
        self.buttons = create_buttons()
        coords = pygame.display.get_window_size()
        self.surface = Surface([coords[0], MENU_HEIGHT])
        self.enabled = True

    def handle_click_event(self, pos):
        for b in self.buttons.values():
            if self._is_click_on_button(b, pos):
                b.is_button_pressed = True

    def map_click_to_action(self, pos):
        if not self.enabled:
            return
        for k in self.buttons:
            if self._is_click_on_button(self.buttons[k], pos):
                return k

    def reset_ui_elements(self):
        for b in self.buttons.values():
            b.is_button_pressed = False

    @staticmethod
    def _is_click_on_button(button, pos):
        button_size = button.surface.get_size()
        return button.coords[0] < pos[0] < button_size[0] + button.coords[0] and \
            button.coords[1] < pos[1] - (HEIGHT - MENU_HEIGHT) < button_size[1] + button.coords[1]

    def redraw(self):
        pass

    def draw_button(self, button, x, y):
        surface = button.render_button()
        height = surface.get_height()
        if not self.enabled:
            surface.set_alpha(MAX_ALPHA / 2)
        self.surface.blit(surface,
                          (PADDING + (x * MENU_COLUMN_WIDTH), PADDING + (height * y)))
        button.coords = (PADDING + (x * MENU_COLUMN_WIDTH), PADDING + (height * y))


class VillagerMenu(Menu):
    def redraw(self):
        self.draw_button(self.buttons[Actions.BUILD_HOUSE], 2, 0)
        self.draw_button(self.buttons[Actions.BUILD_LUMBER_MILL], 2, 1)
        self.draw_button(self.buttons[Actions.BUILD_MILL], 2, 2)
        self.draw_button(self.buttons[Actions.BUILD_BARRACKS], 2, 3)

        self.draw_button(self.buttons[Actions.MOVE], 3, 0)
        self.draw_button(self.buttons[Actions.HARVEST], 3, 1)
        self.draw_button(self.buttons[Actions.BUILD], 3, 2)
        self.draw_button(self.buttons[Actions.ATTACK], 3, 3)
        self.draw_button(self.buttons[Actions.GARRISON], 3, 4)


class MilitaryMenu(Menu):
    def redraw(self):
        self.draw_button(self.buttons[Actions.MOVE], 3, 0)
        self.draw_button(self.buttons[Actions.ATTACK], 3, 1)
        self.draw_button(self.buttons[Actions.GARRISON], 3, 2)


class TownCenterMenu(Menu):
    def redraw(self):
        self.draw_button(self.buttons[Actions.TRAIN_VILLAGER], 2, 0)


class BarracksMenu(Menu):
    def redraw(self):
        self.draw_button(self.buttons[Actions.TRAIN_FOOTMAN], 2, 0)


class Button:
    def __init__(self, label):
        self.font = self.button_font = pygame.font.Font('freesansbold.ttf', 24)
        self.label = label
        self.is_button_pressed = False
        rendered = self._render_text()
        self.size = rendered.get_size()
        self.surface = Surface([self.size[0] + (PADDING * 2), self.size[1] + (PADDING * 2)])
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
        pygame.draw.rect(self.surface, Colors.GREEN.value, (0, 0, floor(16 * self.amount_completed), 3))
