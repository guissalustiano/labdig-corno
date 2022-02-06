from typing import List
from config_parser import ChannelConfig, SignalDirection
from simulation import Simulation

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
        return "\end{tabular} \n"

    def generate_header(self):
        COLS_BEFORE_INPUT = 3
        COLS_BETWEEN_INPUT_OUTPUT = 2
        INITIAL_INPUT_COL = COLS_BEFORE_INPUT
        INITIAL_OUTPUT_COL = COLS_BEFORE_INPUT + COLS_BETWEEN_INPUT_OUTPUT

        input_len = self.input_len + 1 # + Clock
        output_len = self.output_len
        acc = ""
        acc += "\\toprule\n"

        acc += "\t\\multirow{2}{*}{Caso} && "
        acc += f"\multicolumn{{{input_len}}}{{c}}{{Sinais de controle}} && "
        acc += f"\multicolumn{{{output_len}}}{{c}}{{Resultado esperado}} \\\\ \n"

        acc += f"\t\cmidrule{{3-{INITIAL_INPUT_COL+input_len-1}}} \cmidrule{{{INITIAL_OUTPUT_COL+input_len-1}-{INITIAL_OUTPUT_COL+input_len+output_len-2}}} \n\t"
        
        acc += '&& \\multicolumn{1}{c}{\\textit{clock}} & '
        acc += ' & '.join([f'\\textit{{{c.render_name}}}' for c in self.input_signals]).replace("_", "\\_")
        acc += '&&\t'
        acc += ' & '.join([f'\\textit{{{c.render_name}}}' for c in self.output_signals]).replace("_", "\\_")
        acc += " \\\\ \n"

        acc += "\\toprule\n"

        return acc

    def generate_body(self):
        acc = ""
        for i, t in enumerate(self.times):
            acc += f'{i}\t&& $\\uparrow$ &'
            for config_channel in self.input_signals:
                channel = self.simulation[config_channel.name]
                acc += f"\t{channel.value_at(t)} &"
            acc += "&\t"
            for config_channel in self.output_signals:
                channel = self.simulation[config_channel.name]
                acc += f" {channel.value_at(t)} &"
            acc = acc[:-1]
            acc += "\\\\ \n"
        acc += '\\bottomrule\n'
        return acc


    def generate_table(self):
        return (self.generate_begin()
                + self.generate_header() 
                + self.generate_body() 
                + self.generate_end())

# \begin{tabular}{ccrcccccccccccc}
#     \toprule
#         \multirow{2}{*}{caso} && \multicolumn{6}{c}{sinais de controle} && \multicolumn{5}{c}{resultado esperado} \\
#     \cmidrule{3-8} \cmidrule{10-14}
#         && \multicolumn{1}{c}{\textit{clock}} & \textit{zerac} & \textit{contac} & \textit{zerar} & \textit{registrar} & \textit{chaves} && \textit{chavesigualmemoria} & \textit{fimc} & \textit{db\_contagem} & \textit{db\_memoria} & \textit{db\_chaves} \\
#     \toprule
#         inicial && 0                & 0 & 0 & 0 & 0 & 0000  && 0 & 0 & 0000 & 0001 & 0000 \\
#         1       && $\uparrow$       & 1 & 0 & 1 & 0 & 0000  && 0 & 0 & 0000 & 0001 & 0000 \\
#         2       && $\uparrow$       & 0 & 0 & 0 & 0 & 0001  && 0 & 0 & 0000 & 0001 & 0000 \\
#         3       && $\uparrow$       & 0 & 0 & 0 & 1 & 0001  && 1 & 0 & 0000 & 0001 & 0001 \\
#         4       && $\uparrow$       & 0 & 0 & 0 & 0 & 0001  && 1 & 0 & 0000 & 0001 & 0001 \\
#         5       && $\uparrow$       & 0 & 1 & 0 & 0 & 0001  && 0 & 0 & 0001 & 0010 & 0001 \\
#         6       && $\uparrow$       & 0 & 0 & 0 & 1 & 0010  && 1 & 0 & 0001 & 0010 & 0010 \\
#         7       && $\uparrow$       & 0 & 0 & 0 & 0 & 0010  && 1 & 0 & 0001 & 0010 & 0010 \\
#         8       && $\uparrow$       & 0 & 1 & 0 & 0 & 0010  && 0 & 0 & 0010 & 0100 & 0010 \\
#         9       && $\uparrow$       & 0 & 0 & 0 & 1 & 1000  && 0 & 0 & 0010 & 0100 & 1000 \\
#         10      && $\uparrow$       & 0 & 0 & 0 & 0 & 1000  && 0 & 0 & 0010 & 0100 & 1000 \\
#         11      && 13 $\uparrow$    & 0 & 1 & 0 & 0 & 1000  && 0 & 1 & 1111 & 0100 & 1000 \\
#      \bottomrule
# \end{tabular}
