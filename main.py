import sys
import pygame
from pygame import DOUBLEBUF, HWSURFACE, QUIT
from pygame.time import Clock

from src.constants import SCENE_SIZE, SIZE, FPS_TARGET
from src.game import Game, Player
from src.player import get_start_buildings, get_start_mobs
from src.scene import create_plains, Scene, create_resources

pygame.init()
pygame.display.set_caption('Frontier Legacy')
clock = Clock()
screen = pygame.display.set_mode(SIZE)
background = pygame.Surface(screen.get_size()).convert_alpha()
background.fill((0, 0, 0))
screen.blit(background, (0, 0))
pygame.display.flip()
game = Game(
    screen,
    Scene(
        create_plains(),
        [],
        create_resources(),
    ),
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
    ticks = pygame.time.get_ticks()
    game.loop(ticks)
    pygame.display.flip()
    clock.tick(FPS_TARGET)
