import pygame

from src.building import Building
from src.constants import TS
from src.mob import Mob
from src.sprites import Spritesheet


class Player:
    mobs: list[Mob] = []
    buildings: list[Building] = []
    food = 100
    wood = 100
    gold = 50
    stone = 0

    def __init__(self, is_computer=True):
        self.is_computer = is_computer


class Game:
    is_playing = True

    def __init__(self, screen, scene, players: list[Player]):
        self.screen = screen
        self.scene = scene
        self.players = players
        self.sprites = Spritesheet()
        self.background = pygame.Surface(screen.get_size()).convert()
        self.background.fill((0, 0, 0))

    def loop(self):
        # self._unit_move()
        # self._unit_harvest()
        # self._unit_attack()
        self._draw_scene()
        # self._draw_players()

    def _draw_scene(self):
        for layer in self.scene:
            for y in range(len(layer)):
                for x in range(len(layer[y])):
                    index = layer[y][x]
                    self.background.blit(self.sprites.terrain[index][(x + y) % 2 == 0], (x * TS, y * TS))
        self.screen.blit(self.background, (0, 0))

    def _unit_move(self):
        pass

    def _draw_players(self):
        pass

    def _unit_attack(self):
        pass

    def _unit_harvest(self):
        pass
