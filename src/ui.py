from math import floor

import pygame.display
from pygame import Surface

from src.constants import Colors, PADDING, Actions, WIDTH, TS
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
        Actions.BUILD_HOUSE: ImageButton(sprites.create(0, 1), "Build House"),
        Actions.BUILD_LUMBER_MILL: ImageButton(sprites.create(2, 5), "Build Lumber Mill"),
        Actions.BUILD_MILL: ImageButton(sprites.create(3, 23), "Build Mill"),
        Actions.BUILD_QUARRY: ImageButton(sprites.create(0, 5), "Build Quarry"),
        Actions.BUILD_BARRACKS: ImageButton(sprites.create(6, 4), "Build Barracks"),
        Actions.TRAIN_VILLAGER: ImageButton(sprites.create(5, 13), "Train Villager"),
        Actions.TRAIN_FOOTMAN: ImageButton(sprites.create(6, 15), "Train Footman"),
    }


class ImageButton:
    def __init__(self, image, helper_text=""):
        self.image = image
        self.is_button_pressed = False
        self.size = self.image.get_size()
        self.surface = Surface(
            [self.size[0] + (PADDING * 2), self.size[1] + (PADDING * 2)])
        self.coords = (0, 0)
        self.disabled = False
        self.helper_text = helper_text
        self.width = 0
        self.height = 0

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
    def __init__(self, label, helper_text=""):
        self.label = label
        self.is_button_pressed = False
        self.font = self.button_font = pygame.font.Font('freesansbold.ttf', 24)
        rendered = self._render_text()
        self.size = rendered.get_size()
        self.surface = Surface(
            [self.size[0] + (PADDING * 2), self.size[1] + (PADDING * 2)])
        self.coords = (0, 0)
        self.disabled = False
        self.helper_text = helper_text

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
