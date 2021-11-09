import sys
import pygame
from pygame import DOUBLEBUF, HWSURFACE, QUIT
from pygame.time import Clock

from src.constants import SCENE_SIZE, SIZE, FPS_TARGET, Colors
from src.game import Game, Player
from src.player import get_start_buildings, get_start_mobs
from src.scene import create_plains, Scene, create_resources

pygame.init()
pygame.display.set_caption('Frontier Legacy')
clock = Clock()
screen = pygame.display.set_mode(SIZE)
background = pygame.Surface(screen.get_size()).convert_alpha()
background.fill(Colors.BLACK.value)
screen.blit(background, (0, 0))
pygame.display.flip()
player1_start = 10, 10
player2_start = 50, 40
game = Game(
    screen,
    Scene(
        create_plains(),
        [],
        create_resources([player1_start, player2_start]),
    ),
    [
        Player(
            get_start_mobs(player1_start),
            get_start_buildings(player1_start),
            is_computer=False,
        ),
        Player(
            get_start_mobs(player2_start),
            get_start_buildings(player2_start),
        ),
    ],
)

# Event loop
while game.is_playing:
    ticks = pygame.time.get_ticks()
    game.loop(ticks)
    pygame.display.flip()
    clock.tick(FPS_TARGET)
