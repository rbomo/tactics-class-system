"""Console demo: a duel, then a Soldier leveling up and getting promoted.

Usage: python main.py [seed]
"""

import random
import sys

from classes import Halberdier, Sentinel, Soldier, change_class
from combat import Fight


def duel(rng):
    print("=== Duel: Sentinel vs Halberdier ===")
    ally = Sentinel(name="Ally")
    enemy = Halberdier(name="Enemy")
    for round_number in range(1, 21):
        print(f"\nRound {round_number}")
        for line in Fight(ally, enemy, rng).attack_turn():
            print("  " + line)
        if not (ally.is_alive and enemy.is_alive):
            break
    winner = ally if ally.is_alive else enemy
    print(f"\n{winner.name} wins!" if not (ally.is_alive and enemy.is_alive) else "\nDraw after 20 rounds.")


def training(rng):
    print("\n=== Training: Soldier -> Halberdier ===")
    recruit = Soldier(name="Recruit")
    while not recruit.can_promote():
        if recruit.gain_exp(100, rng):
            print(f"Level up! New level: {recruit.level}")
    print(f"Level {recruit.level} reached, promoting to {recruit.next_class.class_name}...")
    recruit = change_class(recruit)
    print(f"{recruit.name} is now a {recruit.class_name}: "
          f"HP {recruit.max_health}, STR {recruit.strength}, DEF {recruit.defense}")


if __name__ == "__main__":
    seed = int(sys.argv[1]) if len(sys.argv) > 1 else None
    rng = random.Random(seed)
    duel(rng)
    training(rng)
