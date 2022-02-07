from __future__ import annotations
from typing import List
from attr import dataclass
from dataclasses import dataclass

@dataclass
class Simulation:
    channels: List[Channel]

    def __getitem__(self, key):
        return [c for c in self.channels if c.name == key][0]

@dataclass
class Channel:
    size: int
    module: str
    name: str
    events: List[ChannelEvent]

    def __init__(self, size: int, module: str, name: str, events: List[ChannelEvent]) -> None:
        self.size = size
        self.module = module
        self.name = name
        self.events = [ChannelEvent(-1, 'X'), *events] # A lista sempre tera ao minimo um elemento

    def value_at(self, time) -> str:
        return self.event_at(time).value

    def event_at(self, time) -> ChannelEvent:
        i = 0
        while i < len(self.events) and self.events[i].time <= time:
            i += 1
        return self.events[i-1]

    def next_event(self, time) -> ChannelEvent:
        i = 0
        while i < len(self.events) and self.events[i].time <= time:
            i += 1
        if i >= len(self.events):
            return None
        return self.events[i]

    def slice_event(self, start_time=0, end_time=-1):
        i = 0
        while i < len(self.events) and self.events[i].time <= start_time:
            i += 1
        start_index = i-1
        while i < len(self.events) and (end_time == -1 or self.events[i].time <= end_time):
            i += 1
        end_index = i
        return self.events[start_index:end_index]
        


@dataclass
class ChannelEvent:
    time: int
    value: str
