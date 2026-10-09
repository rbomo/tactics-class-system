# tactics-class-system

A small turn-based tactics engine in Python, inspired by the **Fire Emblem** series: unit classes, random stat growth, class promotion and a combat system. Standard library only, no external assets.

> Unofficial fan project, not affiliated with or endorsed by Nintendo or Intelligent Systems. See [Inspiration](#inspiration).

## Features
- **Class system:** `Soldier` -> `Halberdier` -> `Sentinel`, each with its own base stats, growth rates and stat caps
- **Leveling:** 100 exp per level, up to level 20, with per-stat growth chances
- **Promotion:** at level 20, stats, name and weapon carry over to the next class (with that class's minimum stats)
- **Combat:** hit chance (accuracy vs dodge), critical hits (x3), double attacks for much faster units, physical weapons vs Defense and magic weapons vs Resistance

## Run
```
python main.py        # duel + training demo (add a number as seed for a repeatable run)
python -m unittest discover -s tests -v
```

## Structure
```
classes.py   Weapon, Unit base class, Soldier / Halberdier / Sentinel, change_class()
combat.py    hit/crit/damage formulas and the Fight class
main.py      console demo
tests/       unit tests
```

## Example
```python
from classes import Soldier, change_class

recruit = Soldier(name="Recruit")
recruit.gain_exp(100 * 19)       # reach level 20
knight = change_class(recruit)   # becomes a Halberdier
```

## Inspiration
This is a personal learning project based on mechanics popularized by the Fire Emblem series:
- stat growth by percentage chance on each level-up, with per-class stat caps
- class promotion at level 20
- hit, dodge and critical-hit formulas driven by Skill, Speed and Luck
- double attacks when a unit is much faster than its opponent
- physical attacks resisted by Defense and magic attacks resisted by Resistance

I used the [Fire Emblem Wiki](https://fireemblemwiki.org/) as a reference for how these systems work. The code is entirely my own, and the repo contains no code, art, audio or other assets from the games. Class names (Soldier, Halberdier, Sentinel) and numbers are my own design. *Fire Emblem* is a trademark of Nintendo; this project is non-commercial and not endorsed by them.

## Notes
The first version was a prototype with a pygame front-end. The art assets were removed since I don't own the rights to them; the game logic is what this repo is about. A front-end with original or properly licensed art is a possible next step.

## License
Free to use, copy, modify and share, including in your own projects, **as long as you credit me**: mention **Raphaël Bomo ([@rbomo](https://github.com/rbomo))** and keep the copyright notice. See [LICENSE](LICENSE) (MIT).
