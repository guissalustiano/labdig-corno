import time
from config_parser import Color, ChannelConfig, SignalDirection, SimulationConfig, Frame, TableConfig
from signal import Representations

signals=[
  ChannelConfig(
    name='clock_in',
    type_=SignalDirection.CLOCK,
    render_name='clock',
    color=Color.BLUE,
  ),
  ChannelConfig(
    name='db_chaves_out',
    render_name='db_chaves',
    type_=SignalDirection.OUTPUT,
    color=Color.RED,
    representation=Representations.HEXADECIMAL,
  ),
  ChannelConfig(
    name='chaves_in',
    type_=SignalDirection.INPUT,
    representation=Representations.DECIMAL,
  ),
  ChannelConfig(
    name='db_memoria',
    color=Color.ORANGE,
    type_=SignalDirection.INPUT,
    representation=Representations.BINARY,
  ),
]

timing_config = SimulationConfig(
  scale=0.1,
  signals=signals,
  frames=[
    Frame(0, 50),
    Frame(30, 50),
    Frame(0, 10),
  ]
)

table_config = TableConfig(
  time_samples=range(10, 720, 20),
  signals=signals
)
