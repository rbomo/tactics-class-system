"""Turn-based combat between two units."""

from __future__ import annotations

import random

from classes import Unit


def _clamp(value: float, low: float = 0, high: float = 100) -> float:
    return max(low, min(high, value))


def hit_chance(attacker: Unit, target: Unit) -> float:
    accuracy = attacker.weapon.accuracy + attacker.luck + attacker.skill * 2
    dodge = target.speed + target.luck
    return _clamp(accuracy - dodge)


def crit_chance(attacker: Unit, target: Unit) -> float:
    return _clamp(attacker.weapon.crit + attacker.skill / 2 - target.luck)


def damage(attacker: Unit, target: Unit, crit: bool = False) -> int:
    """Physical weapons use Strength vs Defense, magic weapons Magic vs Resistance."""
    if attacker.weapon.kind == "physical":
        power, mitigation = attacker.strength, target.defense
    else:
        power, mitigation = attacker.magic, target.resistance
    raw = power + attacker.weapon.might
    if crit:
        raw *= 3
    return max(0, raw - mitigation)


class Fight:
    """One exchange: attacker strikes, defender counters, then a much faster unit strikes again."""

    DOUBLE_SPEED_MARGIN = 3  # a unit needs more than +3 Speed to attack twice

    def __init__(self, attacker: Unit, defender: Unit, rng=random):
        self.attacker = attacker
        self.defender = defender
        self.rng = rng
        self.attacker_doubles = attacker.speed > defender.speed + self.DOUBLE_SPEED_MARGIN
        self.defender_doubles = defender.speed > attacker.speed + self.DOUBLE_SPEED_MARGIN

    def strike(self, attacker: Unit, target: Unit) -> str:
        """Resolve a single attack and return a line describing it."""
        if self.rng.random() * 100 >= hit_chance(attacker, target):
            return f"{attacker.name} misses {target.name}"
        crit = self.rng.random() * 100 < crit_chance(attacker, target)
        dealt = damage(attacker, target, crit)
        target.take_damage(dealt)
        suffix = " (critical!)" if crit else ""
        return f"{attacker.name} hits {target.name} for {dealt}{suffix}"

    def attack_turn(self) -> list[str]:
        """Play the exchange and return the log. Dead units stop fighting."""
        a, d = self.attacker, self.defender
        log = [self.strike(a, d)]
        if d.is_alive:
            log.append(self.strike(d, a))
        if a.is_alive and d.is_alive:
            if self.attacker_doubles:
                log.append(self.strike(a, d))
            elif self.defender_doubles:
                log.append(self.strike(d, a))
        log.append(f"{a.name}: {a.health}/{a.max_health} HP | {d.name}: {d.health}/{d.max_health} HP")
        return log
