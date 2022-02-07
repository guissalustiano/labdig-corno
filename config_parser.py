from __future__ import annotations
from typing import List
from dataclasses import dataclass
from enum import Enum
from signal_values import Representations

@dataclass
class SimulationConfig:
    scale: float
    signals: ChannelConfig
    frames: List[Frame]
    
@dataclass
class ChannelConfig:
    name: str
    color: Color
    render_name: str
    representation: Representations
    type_: SignalDirection

    def __init__(self, name, color=None, render_name=None, type_=None, representation=Representations.BINARY):
        self.name = name
        self.color = color
        self.render_name = render_name if render_name is not None else name
        self.type_ = type_
        self.representation = representation

    @property
    def render_name_escaped(self):
        return self.render_name.replace('_', '\\_')

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

class SignalDirection(Enum):
    CLOCK = 'clock'
    INPUT = 'input'
    OUTPUT = 'output'

@dataclass
class TableConfig:
    time_samples: List[int]
    signals: List[ChannelConfig]
    