from typing import List
from base_generator import BaseGenerator
from config_parser import ChannelConfig
from signal_values import Signal
from simulation import Channel, ChannelEvent, Simulation
from vcd_simulation import VcdSimulation


class TikzGenerator(BaseGenerator):
    config_channels: List[ChannelConfig]
    start: int
    end: int
    scale: float

    def __init__(\
        self, 
        simulation: Simulation,
        config_channels: List[ChannelConfig],
        start: int,
        end: int,
        scale: float
    ):
        self.simulation = simulation
        self.config_channels = config_channels
        self.start = start
        self.end = end
        self.scale = scale

    def generate_tikz(self):
        return ('\\begin{tikztimingtable}\n'
                + self.generate_body() + '\n'
                + '\\end{tikztimingtable}')

    def generate_body(self):
        return '\n'.join([
                self.generate_line(config_channel)
                for config_channel in self.config_channels
            ]
        )

    def generate_line(self, config_channel: ChannelConfig):
        return f'    {config_channel.render_name_escaped} & {self.generate_channel(config_channel)} \\\\'

    def _signal_str(self, duration, type_, color=None):
        if color is None:
            return '{0}{1}'.format(duration, type_)
        return  '{0}{1} [{2}]'.format(duration, type_, color.value)

    def generate_channel(self, config: ChannelConfig):
        tikz_line = []
        channel = self.simulation[config.name]
        cn_events = channel.slice_event(self.start, self.end)
        for i in range(len(cn_events)):
            current = cn_events[i]
            next = cn_events[i+1] if i+1 < len(cn_events) else ChannelEvent(self.end, 'U')
            signal_duration = (next.time - current.time)*self.scale

            signal = Signal(representation=config.representation,
                                 value=current.value).to_tikz()
            signal_str = self._signal_str(
                signal_duration, signal, config.color)

            tikz_line.append(signal_str)
        return ' '.join(tikz_line) 

if __name__ == '__main__':
    from config import timing_config
    simulation = VcdSimulation.from_filename("fluxo_dados.vcd").to_simulation()
    frame = timing_config.frames[0]
    tizk_gen = TikzGenerator(simulation, timing_config.signals, 0, 500, 0.05)
    print(tizk_gen.generate_tikz())