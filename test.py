import unittest
import pygame

from src.constants import SIZE

from src.player_test import PlayerTest

pygame.init()
pygame.display.set_caption('Frontier Legacy')
screen = pygame.display.set_mode(SIZE)

if __name__ == '__main__':
    unittest.main()
