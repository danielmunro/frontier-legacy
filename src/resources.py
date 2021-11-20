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


def get_resource_from_index(index: int):
    if index == 1:
        return Resource.WOOD
    elif index == 2:
        return Resource.GOLD
    elif index == 3:
        return Resource.STONE
    elif index == 4:
        return Resource.FOOD
