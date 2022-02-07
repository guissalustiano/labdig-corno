from simulation import Simulation
from vcd_simulation import VcdSimulation
from table_generator import TableGenerator
import click

from tikz_generator import TikzGenerator

@click.group()
def cli():
    pass

@cli.command()
@click.argument('vcd_filename')
def tikz_timing(vcd_filename):
    from config import timing_config
    simulation: Simulation = VcdSimulation.from_filename(vcd_filename).to_simulation()
    for frame in timing_config.frames:
        tizk_gen = TikzGenerator(simulation, timing_config.signals, frame.start, frame.end, timing_config.scale)
        print(tizk_gen.generate_tikz())
        print('\n')

@cli.command()
@click.argument('vcd_filename')
def tabular(vcd_filename):
    from config import table_config
    simulation: Simulation = VcdSimulation.from_filename(vcd_filename).to_simulation()
    table_gen = TableGenerator(simulation, table_config.signals, table_config.time_samples)
    print(table_gen.generate_table())

if __name__ == '__main__':
    cli()