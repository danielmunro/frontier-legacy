from src.building import TownCenter, Barracks, LumberMill, Mill
from src.mob import Villager, Footman
from src.ui import VillagerMenu, TownCenterMenu, BarracksMenu, MilitaryMenu


def get_ui_from_unit(unit):
    if unit.__class__ == Villager:
        return VillagerMenu()
    elif unit.__class__ == TownCenter:
        return TownCenterMenu()
    elif unit.__class__ == Barracks:
        return BarracksMenu()
    elif unit.__class__ == Footman:
        return MilitaryMenu()
    elif unit.__class__ == LumberMill:
        return MilitaryMenu()
    elif unit.__class__ == Mill:
        return MilitaryMenu()
