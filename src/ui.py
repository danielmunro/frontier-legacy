import pygame.display
from pygame import Surface

from src.constants import Colors, MENU_HEIGHT, HEIGHT, PADDING


class Menu:
    def __init__(self, font):
        self.font = font
        self.move_button = Button(font, "Move")
        self.show = False
        coords = pygame.display.get_window_size()
        self.surface = Surface([coords[0], MENU_HEIGHT])

    def is_click_on_move(self):
        m = pygame.mouse.get_pos()
        button_size = self.move_button.surface.get_size()
        return PADDING < m[0] < button_size[0] + PADDING and PADDING < m[1] - (HEIGHT - MENU_HEIGHT) < button_size[1] + PADDING

    def redraw(self):
        self.surface.fill(Colors.MENU_BLUE.value)
        self.surface.blit(self.move_button.surface, (PADDING, PADDING))
        size = self.move_button.surface.get_size()
        pygame.draw.rect(self.surface, Colors.WHITE.value, (PADDING, PADDING, size[0], size[1]), 1)


class Button:
    def __init__(self, font, label):
        self.font = font
        self.label = label
        self.surface = self.font.render(
            self.label,
            True,
            Colors.WHITE.value,
            Colors.BLACK.value,
        )
