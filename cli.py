from simulation import Simulation, VcdSimulation

def generate_tikz_from_vcd(vcd_filename):
    from config import timing_config
    simulation: Simulation = VcdSimulation.from_filename(vcd_filename).to_simulation()
    for frame in timing_config.frames:
        print(simulation.to_tikz(start=frame.start, end=frame.end, channels_configs=timing_config.signals))
        print('\n')

if __name__ == '__main__':
    generate_tikz_from_vcd('fluxo_dados.vcd')