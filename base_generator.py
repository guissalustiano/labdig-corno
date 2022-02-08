from typing import Callable

from simulation import Channel, Simulation


class BaseGenerator:
    simulation: Simulation
    channel_criteria: Callable[[Channel], bool] = lambda _: True

    def __init__(self, simulation: Simulation, channel_criteria: Callable[[Channel], bool]):
        self.simulation = simulation
        self.channel_criteria = channel_criteria


    def escape_latex(self, text):
        return text.replace("_", "\\_")

    @property
    def channels(self):
        return [channel for channel in self.simulation.channels if self.channel_criteria(channel)]