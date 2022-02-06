from typing import List

from config_parser import ChannelConfig, SignalDirection
from simulation import Simulation, VcdSimulation

class TableGenerator():
    simulation: Simulation
    config_channels: List[ChannelConfig]
    times: List[int]

    def __init__(\
        self, 
        simulation: Simulation,
        config_channels: List[ChannelConfig],
        times: List[int]
    ):
        self.simulation = simulation
        self.config_channels = config_channels
        self.times = times


    @property
    def clock_signals(self) -> ChannelConfig:
        clocks = [c for c in self.config_channels if c.type_ == SignalDirection.CLOCK]
        if len(clocks) == 0:
            return None
        return clocks[0]

    @property
    def input_signals(self) -> List[ChannelConfig]:
        return [c for c in self.config_channels if c.type_ == SignalDirection.INPUT]

    @property
    def output_signals(self) -> List[ChannelConfig]:
        return [c for c in self.config_channels if c.type_ == SignalDirection.OUTPUT]

    @property
    def input_len(self) -> int:
        return len(self.input_signals)

    @property
    def output_len(self) -> int:
        return len(self.output_signals)

    def generate_begin(self):
        return f"\\begin{{tabular}}{{ccr{'c'*self.input_len}c{'c'*self.output_len}}}\n"

    def generate_end(self):
        return "\end{tabular}\n"

    def generate_toprule(self):
        return "  \\toprule\n"

    def generate_header(self):
        input_len = self.input_len + 1 # + Clock
        output_len = self.output_len

        return ("    \\multirow{2}{*}{Caso} && "
                + f"\multicolumn{{{input_len}}}{{c}}{{Sinais de controle}} && "
                + f"\multicolumn{{{output_len}}}{{c}}{{Resultado esperado}}"
                + " \\\\ \n")

    def generate_midrule(self):
        COLS_BEFORE_INPUT = 3
        COLS_BETWEEN_INPUT_OUTPUT = 2
        INITIAL_INPUT_COL = COLS_BEFORE_INPUT
        INITIAL_OUTPUT_COL = COLS_BEFORE_INPUT + COLS_BETWEEN_INPUT_OUTPUT
        input_end = INITIAL_INPUT_COL+self.input_len
        output_start = INITIAL_OUTPUT_COL+self.input_len
        output_end = INITIAL_OUTPUT_COL+self.input_len+self.output_len-1
        return f"  \cmidrule{{3-{input_end}}} \cmidrule{{{output_start}-{output_end}}} \n\t"

    def escape_latex(self, text):
        return text.replace("_", "\\_")

    def generate_sub_header(self):
        return ('    && \\multicolumn{1}{c}{\\textit{clock}} & '
                + ' & '.join([f'\\textit{{{c.render_name}}}' for c in self.input_signals])
                + '&&\t'
                + ' & '.join([f'\\textit{{{c.render_name}}}' for c in self.output_signals])
                + " \\\\ \n")
    
    def generate_bottomrule(self):
        return '  \\bottomrule\n'

    def generate_body_line(self, i, t):
        return (f'    {i:2}  &&   $\\uparrow$ & '
            + ' & '.join([self.simulation[cc.name].value_at(t) for cc in self.input_signals])
            + ' && '
            + ' & '.join([self.simulation[cc.name].value_at(t) for cc in self.output_signals])
            + " \\\\ \n")

    def generate_body(self):
        return ''.join([self.generate_body_line(i, t) for i, t in enumerate(self.times)])


    def generate_table(self):
        return (
                self.generate_begin()
                + self.generate_toprule()
                + self.generate_header() 
                + self.generate_midrule()
                + self.escape_latex(self.generate_sub_header())
                + self.generate_toprule()
                + self.generate_body()
                + self.generate_bottomrule() 
                + self.generate_end())

if __name__ == '__main__':
    from config import table_config
    simulation: Simulation = VcdSimulation.from_filename("fluxo_dados.vcd").to_simulation()
    table_gen = TableGenerator(simulation, table_config.signals, table_config.time_samples)
    print(table_gen.generate_table())
