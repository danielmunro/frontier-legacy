import pygame
from pygame import Surface

from src.constants import Actions, Colors, PADDING, MENU_COLUMN_WIDTH, MAX_ALPHA, HEIGHT, MENU_HEIGHT


class Menu:
    all_units = []
    all_buttons = []

    def __init__(self):
        self.font = self.button_font = pygame.font.Font('freesansbold.ttf', 24)
        coords = pygame.display.get_window_size()
        self.surface = Surface([coords[0], MENU_HEIGHT])
        self.player = None
        self.enabled = True
        self.drawn_buttons = {}

    def handle_click_event(self, pos):
        for b in self.all_buttons.values():
            if self._is_click_on_button(b, pos):
                b.is_button_pressed = True

    def map_click_to_action(self, pos):
        if not self.enabled:
            return
        for k in self.all_buttons:
            if self._is_click_on_button(
                    self.all_buttons[k], pos) and self._can_afford(k):
                return k

    def reset_ui_elements(self):
        for b in self.all_buttons.values():
            b.is_button_pressed = False

    @staticmethod
    def _is_click_on_button(button, pos):
        button_size = button.surface.get_size()
        return button.coords[0] < pos[0] < button_size[0] + button.coords[0] and \
               button.coords[1] < pos[1] - (HEIGHT - MENU_HEIGHT) < button_size[1] + button.coords[1]

    def redraw(self):
        pass

    def draw_button(self, action: Actions, x, y):
        button = self.all_buttons[action]
        surface = button.render_button()
        height = surface.get_height()
        width = surface.get_width()

        surface.set_alpha(
            MAX_ALPHA if self.enabled and self._can_afford(action) else MAX_ALPHA / 2)
        dx = (PADDING + (x * MENU_COLUMN_WIDTH))
        dy = PADDING + (height * y)
        self.surface.blit(surface, (dx, dy))
        button.coords = dx, dy
        button.width = width
        button.height = height
        button.action = action
        self.drawn_buttons[action] = button

    def draw_helper_text(self, action: Actions):
        rendered = self._render_helper_text(action)
        size = rendered.get_size()
        surface = Surface([size[0] + (PADDING * 2), size[1] + (PADDING * 2)])
        surface.blit(rendered, (0, 0))
        return surface

    def _render_helper_text(self, action: Actions):
        return self.font.render(
            self.all_buttons[action].helper_text,
            True,
            Colors.WHITE.value,
            Colors.BLACK.value,
        )

    def _can_afford(self, action: Actions):
        for u in Menu.all_units:
            if u.action == action and \
                    u.costs.food <= self.player.food and \
                    u.costs.wood <= self.player.wood and \
                    u.costs.stone <= self.player.stone and \
                    u.costs.gold <= self.player.gold:
                return True
        return False


class VillagerMenu(Menu):
    def redraw(self):
        self.draw_button(Actions.BUILD_HOUSE, 2, 0)
        self.draw_button(Actions.BUILD_LUMBER_MILL, 2, 1)
        self.draw_button(Actions.BUILD_QUARRY, 2, 2)
        self.draw_button(Actions.BUILD_MILL, 2, 3)
        self.draw_button(Actions.BUILD_BARRACKS, 2, 4)

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
