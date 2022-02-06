from __future__ import annotations
from typing import List
from dataclasses import dataclass
from enum import Enum

@dataclass
class SimulationConfig:
    signals: ChannelConfig
    frames: List[Frame]
    
@dataclass
class ChannelConfig:
    name: str
    color: Color
    render_name: str

    def __init__(self, name, color=None, render_name=None):
        self.name = name
        self.color = color
        self.render_name = render_name if render_name is not None else name

@dataclass
class Frame:
    start: int
    end: int

class Color(Enum):
    RED = 'red'
    BLUE = 'blue'
    GREEN = 'green'
    ORANGE = 'orange'
    YELLOW = 'yellow'
    