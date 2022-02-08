from typing import Callable, List
from base_generator import BaseGenerator

from config_parser import ChannelConfig, SignalDirection
from simulation import Channel, Simulation
from vcd_simulation import VcdSimulation

class TableGenerator(BaseGenerator):
    times: List[int]

    def __init__(
        self, 
        simulation: Simulation,
        times: List[int],
        channel_criteria: Callable[[Channel], bool] = lambda _: True,
    ):
        super().__init__(simulation, channel_criteria)
        self.times = times


    def generate_begin(self):
        return f"\\begin{{tabular}}{{ccr{'c'*(len(self.channels)-1)}}}\n"

    def generate_end(self):
        return "\end{tabular}\n"

    def generate_toprule(self):
        return "  \\toprule\n"

    def generate_sub_header(self):
        return (' Caso && '
                + ' & '.join([f'\\textit{{{channel.name}}}' for channel in self.channels])
                + " \\\\ \n")
    
    def generate_bottomrule(self):
        return '  \\bottomrule\n'

    def generate_body_line(self, i, t):
        return (f'    {i:3}  &&  '
            + ' & '.join(['{:>4}'.format(channel.value_at(t)) for channel in self.channels])
            + " \\\\ \n")

    def generate_body(self):
        return ''.join([self.generate_body_line(i, t) for i, t in enumerate(self.times)])


    def generate_table(self):
        return (
                self.generate_begin()
                + self.generate_toprule()
                + self.escape_latex(self.generate_sub_header())
                + self.generate_toprule()
                + self.generate_body()
                + self.generate_bottomrule() 
                + self.generate_end())

if __name__ == '__main__':
    from config import table_config
    simulation: Simulation = VcdSimulation.from_filename("wave.vcd").to_simulation()
    table_gen = TableGenerator(simulation, table_config.time_samples, lambda c: c.module == 'dut')
    print(table_gen.generate_table())
