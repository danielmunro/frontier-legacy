from src.building import TownCenter, Barracks
from src.mob import Villager, Footman
from src.ui import VillagerMenu, TownCenterMenu, BarracksMenu, MilitaryMenu


def get_ui_from_unit(font, unit):
    if unit.__class__ == Villager:
        return VillagerMenu(font)
    elif unit.__class__ == TownCenter:
        return TownCenterMenu(font)
    elif unit.__class__ == Barracks:
        return BarracksMenu(font)
    elif unit.__class__ == Footman:
        return MilitaryMenu(font)
