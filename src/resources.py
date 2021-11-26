from enum import Enum


class Resource(Enum):
    FOOD = 1
    WOOD = 2
    GOLD = 3
    STONE = 4


class Costs:
    def __init__(self, food, wood, gold, stone):
        self.food = food
        self.wood = wood
        self.gold = gold
        self.stone = stone
