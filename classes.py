"""Unit classes for a small turn-based tactics game (Fire Emblem-style).

A Soldier gains experience, levels up with random stat growth, and at level 20
can be promoted to a stronger class (Soldier -> Halberdier -> Sentinel).
"""

from __future__ import annotations

import random
from dataclasses import dataclass

MAX_LEVEL = 20
EXP_PER_LEVEL = 100
STATS = (
    "max_health", "strength", "magic", "skill",
    "speed", "luck", "defense", "resistance",
)


@dataclass(frozen=True)
class Weapon:
    kind: str  # "physical" (uses Strength/Defense) or "magic" (uses Magic/Resistance)
    name: str
    might: int
    accuracy: int
    crit: int = 0

    def __post_init__(self):
        if self.kind not in ("physical", "magic"):
            raise ValueError(f"unknown weapon kind: {self.kind!r}")


BRONZE_SPEAR = Weapon("physical", "Bronze Spear", might=4, accuracy=90, crit=0)


class Unit:
    """Base class: stats, level-up logic and promotion. Subclasses only provide data."""

    class_name = "Unit"
    base_stats: dict = {}     # minimum stats of the class
    growth_rates: dict = {}   # % chance to gain +1 in each stat on level-up
    stat_caps: dict = {}      # max value per stat (missing key = no cap)
    next_class = None         # class this one promotes to, or None

    def __init__(self, name=None, weapon=BRONZE_SPEAR, **stats):
        unknown = set(stats) - set(STATS)
        if unknown:
            raise TypeError(f"unknown stat(s): {', '.join(sorted(unknown))}")
        self.name = name or self.class_name
        self.level = 1
        self.exp = 0
        # Stats passed in (e.g. when promoting) can't go below the class minimum.
        for stat in STATS:
            setattr(self, stat, max(stats.get(stat, 0), self.base_stats[stat]))
        self.health = self.max_health
        self.weapon = weapon

    def __repr__(self):
        return f"<{self.class_name} {self.name!r} lvl {self.level} hp {self.health}/{self.max_health}>"

    @property
    def is_alive(self) -> bool:
        return self.health > 0

    def take_damage(self, amount: int) -> None:
        self.health = max(0, self.health - max(0, amount))

    def gain_exp(self, amount: int, rng=random) -> int:
        """Add experience and level up if possible. Returns the number of levels gained."""
        self.exp += amount
        return self.level_up(rng)

    def level_up(self, rng=random) -> int:
        """Spend 100 exp per level (up to level 20) and roll stat growths."""
        gained = 0
        while self.exp >= EXP_PER_LEVEL and self.level < MAX_LEVEL:
            self.exp -= EXP_PER_LEVEL
            self.level += 1
            gained += 1
            for stat in STATS:
                cap = self.stat_caps.get(stat)
                if cap is not None and getattr(self, stat) >= cap:
                    continue
                if rng.random() * 100 < self.growth_rates[stat]:
                    setattr(self, stat, getattr(self, stat) + 1)
                    if stat == "max_health":
                        self.health += 1  # extra max HP also heals, as in Fire Emblem
        return gained

    def can_promote(self) -> bool:
        return self.level >= MAX_LEVEL and self.next_class is not None

    def promote(self) -> "Unit":
        """Return a new unit of the next class, keeping stats, name and weapon."""
        if not self.can_promote():
            raise ValueError(f"{self.name} cannot be promoted yet")
        carried = {stat: getattr(self, stat) for stat in STATS}
        return self.next_class(name=self.name, weapon=self.weapon, **carried)


class Soldier(Unit):
    """Starting class."""

    class_name = "Soldier"
    base_stats = dict(max_health=20, strength=8, magic=0, skill=8,
                      speed=8, luck=0, defense=7, resistance=2)
    growth_rates = dict(max_health=70, strength=50, magic=20, skill=45,
                        speed=50, luck=25, defense=50, resistance=50)
    stat_caps = dict(max_health=40, strength=20, magic=10, skill=20,
                     speed=20, luck=30, defense=20, resistance=20)


class Halberdier(Unit):
    class_name = "Halberdier"
    base_stats = dict(max_health=33, strength=17, magic=6, skill=18,
                      speed=18, luck=0, defense=15, resistance=12)
    growth_rates = dict(max_health=55, strength=35, magic=35, skill=30,
                        speed=30, luck=50, defense=55, resistance=20)
    stat_caps = dict(max_health=45, strength=26, magic=15, skill=26,
                     speed=26, luck=30, defense=24, resistance=17)


class Sentinel(Unit):
    """Top class: promotes to nothing and has no stat caps."""

    class_name = "Sentinel"
    base_stats = dict(max_health=53, strength=21, magic=3, skill=21,
                      speed=17, luck=0, defense=21, resistance=8)
    growth_rates = dict(max_health=75, strength=45, magic=20, skill=45,
                        speed=40, luck=25, defense=45, resistance=40)
    stat_caps = {}


Soldier.next_class = Halberdier
Halberdier.next_class = Sentinel


def change_class(unit: Unit) -> Unit:
    """Promote the unit if it is eligible, otherwise return it unchanged."""
    return unit.promote() if unit.can_promote() else unit
