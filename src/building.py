from src.mob import MobUnit, Villager, Ruffian
from src.resources import Costs


class BuildingUnit:
    def __init__(self, hp, defense, build_time, costs):
        self.hp = hp
        self.defense = defense
        self.build_time = build_time
        self.costs = costs

    def trains(self) -> list[MobUnit]:
        return []


class TownCenter(BuildingUnit):
    def __init__(self):
        super().__init__(
            2100,
            4,
            240,
            Costs(0, 400, 0, 100),
        )

    def trains(self) -> list[MobUnit]:
        return [
            Villager()
        ]


class Saloon(BuildingUnit):
    def __init__(self):
        super().__init__(
            700,
            1,
            120,
            Costs(0, 100, 0, 0),
        )

    def trains(self) -> list[MobUnit]:
        return [
            Ruffian()
        ]


class Building:
    def __init__(self, unit: BuildingUnit, coords):
        self.unit = unit
        self.hp = unit.hp
        self.coords = coords
