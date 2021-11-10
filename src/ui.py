import pygame.display
from pygame import Surface

from src.constants import Colors, MENU_HEIGHT, HEIGHT, PADDING, Actions


class Menu:
    def __init__(self, font):
        self.font = font
        self.move_button = Button(font, "Move")
        self.gather_button = Button(font, "Gather")
        self.attack_button = Button(font, "Attack")
        self.show = False
        coords = pygame.display.get_window_size()
        self.surface = Surface([coords[0], MENU_HEIGHT])

    def handle_click_event(self, pos):
        if self._is_click_on_button(self.move_button, pos):
            self.move_button.is_button_pressed = True

    def map_click_to_action(self, pos):
        if self._is_click_on_button(self.move_button, pos):
            return Actions.MOVE

    def reset_ui_elements(self):
        self.move_button.is_button_pressed = False

    @staticmethod
    def _is_click_on_button(button, pos):
        button_size = button.surface.get_size()
        return PADDING < pos[0] < button_size[0] + PADDING and \
            PADDING < pos[1] - (HEIGHT - MENU_HEIGHT) < button_size[1] + PADDING

    def redraw(self):
        self.surface.fill(Colors.MENU_BLUE.value)
        self.move_button.render_button()
        button_height = self.move_button.surface.get_height()
        self.surface.blit(self.move_button.surface, (PADDING, PADDING))
        self.surface.blit(self.gather_button.render_button(), (PADDING, PADDING + button_height))
        self.surface.blit(self.attack_button.render_button(), (PADDING, PADDING + (button_height * 2)))


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
