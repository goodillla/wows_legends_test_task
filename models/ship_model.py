from dataclasses import dataclass

@dataclass
class Weapon:
    name: str
    reload_speed: int
    rotational_speed: int
    diameter: int
    power_volley: int
    count: int

@dataclass
class Hull:
    name: str
    armor: int
    type: int
    capacity: int

@dataclass
class Engine:
    name: str
    power: int
    type: int

@dataclass
class Ship:
    ship: str
    weapon: Weapon
    hull: Hull
    engine: Engine
