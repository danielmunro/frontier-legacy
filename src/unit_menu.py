from src.building import TownCenter
from src.mob import Villager
from src.ui import VillagerMenu, TownCenterMenu


def get_ui_from_unit(font, unit):
    if unit.__class__ == Villager:
        return VillagerMenu(font)
    elif unit.__class__ == TownCenter:
        return TownCenterMenu(font)
