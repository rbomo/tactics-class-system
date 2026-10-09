import os
import random
import sys
import unittest

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from classes import MAX_LEVEL, Halberdier, Sentinel, Soldier, Weapon, change_class  # noqa: E402
from combat import Fight, damage, hit_chance  # noqa: E402


class TestLeveling(unittest.TestCase):
    def test_soldier_levels_up_and_stops_at_max_level(self):
        soldier = Soldier()
        soldier.gain_exp(100 * 50, random.Random(1))
        self.assertEqual(soldier.level, MAX_LEVEL)

    def test_stats_never_exceed_caps(self):
        soldier = Soldier()
        soldier.gain_exp(100 * 50, random.Random(2))
        for stat, cap in Soldier.stat_caps.items():
            self.assertLessEqual(getattr(soldier, stat), cap)

    def test_sentinel_max_health_actually_grows(self):
        sentinel = Sentinel()
        sentinel.gain_exp(100 * 19, random.Random(3))
        self.assertGreater(sentinel.max_health, Sentinel.base_stats["max_health"])


class TestPromotion(unittest.TestCase):
    def test_cannot_promote_before_level_20(self):
        soldier = Soldier()
        self.assertIs(change_class(soldier), soldier)
        with self.assertRaises(ValueError):
            soldier.promote()

    def test_promotion_keeps_stats_name_weapon_and_respects_minimums(self):
        soldier = Soldier(name="Rex")
        soldier.gain_exp(100 * 50, random.Random(4))
        promoted = change_class(soldier)
        self.assertIsInstance(promoted, Halberdier)
        self.assertEqual(promoted.name, "Rex")
        self.assertEqual(promoted.weapon, soldier.weapon)
        self.assertEqual(promoted.level, 1)
        self.assertEqual(promoted.health, promoted.max_health)
        self.assertGreaterEqual(
            promoted.strength, max(soldier.strength, Halberdier.base_stats["strength"])
        )

    def test_top_class_cannot_promote(self):
        sentinel = Sentinel()
        sentinel.level = MAX_LEVEL
        self.assertFalse(sentinel.can_promote())


class TestCombat(unittest.TestCase):
    def test_damage_is_never_negative(self):
        self.assertEqual(damage(Soldier(), Sentinel()), 0)

    def test_magic_weapon_uses_resistance_not_defense(self):
        mage = Soldier(magic=10, weapon=Weapon("magic", "Fire", might=5, accuracy=90))
        target = Sentinel()  # defense 21, resistance 8
        self.assertEqual(damage(mage, target), (10 + 5) - 8)

    def test_hit_chance_is_a_percentage(self):
        self.assertTrue(0 <= hit_chance(Soldier(), Sentinel()) <= 100)

    def test_dead_units_do_not_fight_and_health_never_negative(self):
        for seed in range(200):
            a, b = Sentinel(name="A"), Soldier(name="B")
            b.health = 1
            log = Fight(a, b, random.Random(seed)).attack_turn()
            self.assertGreaterEqual(a.health, 0)
            self.assertGreaterEqual(b.health, 0)
            if not b.is_alive:
                self.assertFalse(
                    any(line.startswith("B ") and ("hits" in line or "misses" in line) for line in log)
                )

    def test_double_attack_needs_speed_margin(self):
        fast, slow = Soldier(speed=20), Soldier(speed=8)
        self.assertTrue(Fight(fast, slow).attacker_doubles)
        self.assertTrue(Fight(slow, fast).defender_doubles)
        self.assertFalse(Fight(Soldier(speed=11), Soldier(speed=8)).attacker_doubles)


if __name__ == "__main__":
    unittest.main()
