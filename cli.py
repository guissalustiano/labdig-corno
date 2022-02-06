from simulation import Simulation, VcdSimulation
from table_generator import TableGenerator
import click

@click.group()
def cli():
    pass

@cli.command()
@click.argument('vcd_filename')
def tikz_timing(vcd_filename):
    from config import timing_config
    simulation: Simulation = VcdSimulation.from_filename(vcd_filename).to_simulation()
    for frame in timing_config.frames:
        print(simulation.to_tikz(start=frame.start,
                                 end=frame.end,
                                 channels_configs=timing_config.signals,
                                 scale=timing_config.scale))
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