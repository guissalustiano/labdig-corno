from typing import Callable, List
from base_generator import BaseGenerator
from config_parser import ChannelConfig
from signal_values import Representations, Signal
from simulation import Channel, ChannelEvent, Simulation
from vcd_simulation import VcdSimulation


class TikzGenerator(BaseGenerator):
    start: int
    end: int
    scale: float

    def __init__(
        self, 
        simulation: Simulation,
        start: int,
        end: int,
        scale: float,
        channel_criteria: Callable[[Channel], bool] = lambda _: True,
    ):
        super().__init__(simulation, channel_criteria)
        self.start = start
        self.end = end
        self.scale = scale

    def generate_tikz(self):
        return ('\\begin{tikztimingtable}\n'
                + self.generate_body() + '\n'
                + '\\end{tikztimingtable}')

    def generate_body(self):
        return '\n'.join([
                self.generate_line(channel)
                for channel in self.channels
            ]
        )

    def generate_line(self, channel: Channel):
        return f'    {self.escape_latex(channel.name)} & {self.generate_channel(channel)} \\\\'

    def _signal_str(self, duration, type_, color=None):
        if color is None:
            return '{0}{1}'.format(duration, type_)
        return  '{0}{1} [{2}]'.format(duration, type_, color.value)

    def generate_channel(self, channel: Channel):
        tikz_line = []
        cn_events = channel.slice_event(self.start, self.end)
        for i in range(len(cn_events)):
            current = cn_events[i]
            next = cn_events[i+1] if i+1 < len(cn_events) else ChannelEvent(self.end, 'U')
            signal_duration = (next.time - current.time)*self.scale

            representation = Representations.BINARY if channel.size == 1 else Representations.HEXADECIMAL
            signal = Signal(representation, value=current.value).to_tikz()
            signal_str = self._signal_str(
                signal_duration, signal)

            tikz_line.append(signal_str)
        return ' '.join(tikz_line)


if __name__ == '__main__':
    from config import timing_config
    simulation = VcdSimulation.from_filename("wave.vcd").to_simulation()
    frame = timing_config.frames[0]
    tizk_gen = TikzGenerator(simulation, 0, 850000000, 0.0000001, lambda c: c.module == 'dut')
    print(tizk_gen.generate_tikz())
