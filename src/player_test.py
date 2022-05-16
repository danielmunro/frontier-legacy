import unittest

from src.all_buildings import TownCenter, House
from src.constants import Actions
from src.mob import Villager
from src.test_helper import create_player


class PlayerTest(unittest.TestCase):
    def test_deselect_all(self):
        """
        Test that player can deselect all mobs and buildings
        """
        # setup
        player = create_player()

        # given
        for mob in player.mobs:
            mob.selected = True
        for building in player.buildings:
            building.selected = True

        # when
        player.deselect_all()

        # then
        for mob in player.mobs:
            self.assertFalse(mob.selected)
        for building in player.buildings:
            self.assertFalse(building.selected)

    def test_get_selected(self):
        """
        Test that player can get all selected mobs
        """
        # setup
        player = create_player()

        # given
        for mob in player.mobs:
            mob.selected = True

        # when
        mobs = player.get_selected_mobs()

        # then
        self.assertEqual(player.mobs, mobs)

    def test_train_villager(self):
        """
        Test that player can train villagers
        """
        # setup
        player = create_player()
        food = player.food
        building = next(filter(lambda i: i.unit.__class__ == TownCenter, player.buildings))
        mob = Villager()

        # given
        building.selected = True

        # when
        player.train_mob(TownCenter, mob)

        # then
        self.assertEqual(player.food, food - mob.costs.food)
        self.assertEqual(1, len(building.queue))

    def test_build_buildings(self):
        """
        Test that player can use villagers to build buildings
        """
        # setup
        player = create_player()
        wood = player.wood
        player.mobs[0].selected = True

        # when
        mobs_building = player.villager_build(Actions.BUILD_HOUSE, (0, 0))

        # then
        self.assertEqual(player.wood, wood - House().costs.wood)
        self.assertEqual(1, len(mobs_building))
        self.assertEqual(Actions.BUILD_HOUSE, player.mobs[0].to_build)
