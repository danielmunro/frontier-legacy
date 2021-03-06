import pygame
from pygame.time import Clock

from src.all_units import all_units
from src.constants import SIZE, FPS_TARGET, Colors
from src.game import Game
from src.menu import Menu
from src.player import get_start_buildings, get_start_mobs, Player
from src.scene import create_plains, Scene, create_resources
from src.sprite_initializer import initialize_sprites
from src.sprites import Spritesheet
from src.ui import create_buttons

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
sprites = Spritesheet()
Menu.all_units = all_units
Menu.all_buttons = create_buttons()
game = Game(
    screen,
    Scene(
        create_plains(),
        [],
        create_resources([player1_start, player2_start]),
        sprites,
    ),
    [
        Player(
            get_start_mobs(player1_start),
            get_start_buildings(player1_start),
            sprites,
            is_computer=False,
        ),
        Player(
            get_start_mobs(player2_start),
            get_start_buildings(player2_start),
            sprites,
        ),
    ],
    sprites,
)
initialize_sprites(game.sprites)

# Event loop
while game.is_playing:
    ticks = pygame.time.get_ticks()
    game.loop(ticks)
    pygame.display.flip()
    clock.tick(FPS_TARGET)
