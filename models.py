from __future__ import annotations
from dataclasses import dataclass, field
from copy import deepcopy
from typing import Dict, Protocol, List

# =====================
# SINGLETON (metaclase)
# =====================
class Singleton(type):
    _instances: Dict[type, object] = {}
    def __call__(cls, *args, **kwargs):
        if cls not in cls._instances:
            cls._instances[cls] = super().__call__(*args, **kwargs)
        return cls._instances[cls]


class GameConfig(metaclass=Singleton):
    def __init__(self):
        self.theme: str = "fantasy"
        self.max_enemies: int = 5
        self.level: int = 1


class GameEngine(metaclass=Singleton):
    def __init__(self):
        self.config = GameConfig()
        self.enemies: List[Enemy] = []
        self.background: str = ""
        self.skin_palette: Dict[str, str] = {}

    def reset(self):
        self.enemies.clear()


# =====================
# ABSTRACT FACTORY
# =====================
class ThemeFactory(Protocol):
    def create_background(self) -> str: ...
    def create_skin_palette(self) -> Dict[str, str]: ...


class FantasyThemeFactory:
    def create_background(self) -> str:
        return "Bosque encantado con luciérnagas"

    def create_skin_palette(self) -> Dict[str, str]:
        return {"orc": "verde musgo", "dragon": "escamas carmesí", "goblin": "verde limón"}


class SciFiThemeFactory:
    def create_background(self) -> str:
        return "Estación espacial con vista a nebulosas"

    def create_skin_palette(self) -> Dict[str, str]:
        return {"drone": "metal pulido", "android": "cromo azul", "alien": "púrpura biolum."}


def get_theme_factory(theme: str) -> ThemeFactory:
    return SciFiThemeFactory() if theme == "scifi" else FantasyThemeFactory()


# =====================
# PROTOTYPE
# =====================
@dataclass
class Enemy:
    kind: str
    hp: int
    atk: int
    skin: str = ""
    def clone(self) -> "Enemy":
        return deepcopy(self)


class EnemyPrototypeRegistry(metaclass=Singleton):
    def __init__(self):
        self._protos: Dict[str, Enemy] = {
            "orc": Enemy("orc", hp=20, atk=4),
            "dragon": Enemy("dragon", hp=60, atk=10),
            "goblin": Enemy("goblin", hp=12, atk=3),
            "drone": Enemy("drone", hp=18, atk=5),
            "android": Enemy("android", hp=30, atk=6),
            "alien": Enemy("alien", hp=26, atk=7),
        }
    def get(self, kind: str) -> Enemy:
        base = self._protos.get(kind)
        if not base:
            raise ValueError(f"No hay prototipo para {kind}")
        return base.clone()


# =====================
# FACTORY METHOD
# =====================
class EnemyFactory:
    @staticmethod
    def create(kind: str) -> Enemy:
        registry = EnemyPrototypeRegistry()
        enemy = registry.get(kind)
        engine = GameEngine()
        palette = engine.skin_palette
        enemy.skin = palette.get(kind, "color estándar")
        return enemy


# =====================
# BUILDER
# =====================
@dataclass
class Level:
    number: int
    goal: str
    background: str
    enemy_wave: List[str] = field(default_factory=list)


class LevelBuilder:
    def __init__(self):
        self._number = 1
        self._goal = "Sobrevive"
        self._background = ""
        self._enemy_wave: List[str] = []

    def with_number(self, n: int) -> "LevelBuilder":
        self._number = n
        return self

    def with_goal(self, goal: str) -> "LevelBuilder":
        self._goal = goal
        return self

    def with_background(self, bg: str) -> "LevelBuilder":
        self._background = bg
        return self

    def add_enemy(self, kind: str) -> "LevelBuilder":
        self._enemy_wave.append(kind)
        return self

    def build(self) -> Level:
        if not self._background:
            self._background = "Área de entrenamiento"
        return Level(self._number, self._goal, self._background, self._enemy_wave)