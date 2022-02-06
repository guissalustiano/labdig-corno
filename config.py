from config_parser import Color, ChannelConfig, SimulationConfig, Frame

timing_config = SimulationConfig(
  signals=[
    ChannelConfig(
      name='clock_in',
      render_name='clock',
      color=Color.BLUE
    ),
    ChannelConfig(
      name='db_chaves_out',
      render_name='db_chaves',
      color=Color.RED
    ),
    ChannelConfig(
      name='chaves_in',
    ),
    ChannelConfig(
      name='db_memoria',
      color=Color.ORANGE
    ),
  ],
  frames=[
    Frame(0, 50),
    Frame(30, 50),
    Frame(0, 10),
  ]
)

table_config = None

# agrupar sinais, 
# mudar cor do sinal, e representacao
