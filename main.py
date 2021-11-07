import sys
import pygame
from pygame import DOUBLEBUF, HWSURFACE, QUIT
from pygame.time import Clock

from src.constants import SCENE_SIZE, SIZE, FPS_TARGET
from src.game import Game, Player
from src.player import get_start_buildings, get_start_mobs

pygame.init()
pygame.display.set_caption('Frontier Legacy')
clock = Clock()
screen = pygame.display.set_mode(SIZE)
background = pygame.Surface(screen.get_size()).convert_alpha()
background.fill((0, 0, 0))
screen.blit(background, (0, 0))
pygame.display.flip()
scene = [
    [[0 for _ in range(SCENE_SIZE[0])] for _ in range(SCENE_SIZE[1])],
    [[0 for _ in range(SCENE_SIZE[0])] for _ in range(SCENE_SIZE[1])],
]
game = Game(
    screen,
    scene,
    [
        Player(
            get_start_mobs(1),
            get_start_buildings(1),
            is_computer=False,
        ),
        Player(
            get_start_mobs(2),
            get_start_buildings(2),
        ),
    ],
)

# Event loop
while game.is_playing:
    game.loop()
    pygame.display.flip()
    clock.tick(FPS_TARGET)
