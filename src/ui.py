import pygame.display
from pygame import Surface

from src.constants import Colors, MENU_HEIGHT, HEIGHT, PADDING, Actions


def create_buttons(font):
    return {
        Actions.MOVE: Button(font, "Move"),
        Actions.ATTACK_MOVE: Button(font, "Attack Move"),
        Actions.ATTACK: Button(font, "Attack"),
        Actions.HARVEST: Button(font, "Harvest"),
        Actions.BUILD: Button(font, "Build"),
        Actions.REPAIR: Button(font, "Repair"),
    }


class Menu:
    def __init__(self, font):
        self.font = font
        self.buttons = create_buttons(font)
        self.show = False
        coords = pygame.display.get_window_size()
        self.surface = Surface([coords[0], MENU_HEIGHT])

    def handle_click_event(self, pos):
        for b in self.buttons.values():
            if self._is_click_on_button(b, pos):
                b.is_button_pressed = True

    def map_click_to_action(self, pos):
        for k in self.buttons.keys():
            if self.buttons[k] and self._is_click_on_button(self.buttons[k], pos):
                return k

    def reset_ui_elements(self):
        for b in self.buttons.values():
            b.is_button_pressed = False

    @staticmethod
    def _is_click_on_button(button, pos):
        button_size = button.surface.get_size()
        return PADDING < pos[0] < button_size[0] + PADDING and \
            PADDING < pos[1] - (HEIGHT - MENU_HEIGHT) < button_size[1] + PADDING

    def redraw(self):
        pass


class VillagerMenu(Menu):
    def redraw(self):
        self.surface.fill(Colors.MENU_BLUE.value)
        button = self.buttons[Actions.MOVE]
        button.render_button()
        # button_height = button.surface.get_height()
        self.surface.blit(button.surface, (PADDING, PADDING))
        # self.surface.blit(self.buttons[Actions.HARVEST].render_button(), (PADDING, PADDING + button_height))
        # self.surface.blit(self.buttons[Actions.BUILD].render_button(), (PADDING, PADDING + (button_height * 2)))
        # self.surface.blit(self.buttons[Actions.ATTACK].render_button(), (PADDING, PADDING + (button_height * 2)))


class Button:
    def __init__(self, font, label):
        self.font = font
        self.label = label
        self.is_button_pressed = False
        rendered = self._render_text()
        self.size = rendered.get_size()
        self.surface = Surface([self.size[0] + (PADDING * 2), self.size[1] + (PADDING * 2)])

    def render_button(self):
        self.surface.blit(self._render_text(), (PADDING, PADDING))
        pygame.draw.rect(self.surface, Colors.WHITE.value, (0, 0, self.size[0] + (PADDING * 2), self.size[1] + (PADDING * 2)), 1)
        return self.surface

    def _render_text(self):
        return self.font.render(
            self.label,
            True,
            Colors.GRAY.value if self.is_button_pressed else Colors.WHITE.value,
            Colors.BLACK.value,
        )
