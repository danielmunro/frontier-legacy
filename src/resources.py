from enum import Enum


class Resource(Enum):
    FOOD = "food"
    WOOD = "wood"
    GOLD = "gold"
    STONE = "stone"


class Costs:
    def __init__(self, food, wood, gold, stone):
        self.food = food
        self.wood = wood
        self.gold = gold
        self.stone = stone
