from __future__ import annotations
from typing import List, Dict, Union
from datetime import datetime
from functools import cached_property
import vcd
from vcd.reader import TokenKind

from simulation import Channel, ChannelEvent, Simulation

class VcdSimulation:
    _tokens: List[vcd.reader.Token]

    def __init__(self, vcd_stream: vcd.reader.HasReadinto):
        self._tokens = list(vcd.reader.tokenize(vcd_stream))

    @staticmethod
    def from_filename(filename: str) -> VcdSimulation:
        with open(filename, 'rb') as f:
            return VcdSimulation(f)

    def _filtered_tokens(self, tokenKind: TokenKind):
        return [token for token in self._tokens if tokenKind == token.kind]

    def date(self) -> datetime:
        token = self._filtered_tokens(TokenKind.DATE)[0]
        return datetime.strptime(token.data.strip(), '%a %b %d %H:%M:%S %Y')

    @cached_property
    def timescale(self) -> vcd.reader.Timescale:
        token = self._filtered_tokens(TokenKind.TIMESCALE)[0]
        return token.data

    @cached_property
    def scope_vars(self) -> Dict[vcd.reader.ScopeDecl, Dict[int, vcd.reader.VarDecl]]:
        acc = {}
        for token in self._tokens:
            if token.kind == TokenKind.SCOPE:
                scope = token.data.ident
                acc[scope] = {}
            elif token.kind == TokenKind.VAR:
                var = token.data.reference
                if var not in acc[scope]:
                    acc[scope][var] = {}
                acc[scope][var][token.data.bit_index] = token.data
                
        return acc

    @cached_property
    def time_changes(self) -> Dict[int, Union[vcd.reader.ScalarChange, vcd.reader.VectorChange, vcd.reader.RealChange, vcd.reader.StringChange]]:
        acc = {}
        for token in self._tokens:
            if token.kind == TokenKind.CHANGE_TIME:
                time = token.data
                acc[time] = []
            elif token.kind == TokenKind.CHANGE_SCALAR or token.kind == TokenKind.CHANGE_VECTOR or token.kind == TokenKind.CHANGE_REAL == token.kind == TokenKind.CHANGE_STRING:
                change = token.data
                acc[time].append(change)
        return acc

    def to_events(self, vars: Dict[Union[None, int], vcd.reader.VarDecl])-> List[ChannelEvent]:
        acc = []
        value = ['X'] * len(vars)
        vars = sorted(vars.values(), key=lambda x: x.bit_index, reverse=True)
        for time, changes in self.time_changes.items():
            has_changed = False
            for change in changes:
                for var in vars:
                    if change.id_code == var.id_code:
                        index = var.bit_index if isinstance(var.bit_index, int) else 0
                        value[index] = str(change.value)
                        has_changed = True
            if has_changed:
                event = ChannelEvent(time, ''.join(value))
                acc.append(event)
        return acc 

    def to_channel(self) -> List[Channel]:
        acc = []
        for module, channels in self.scope_vars.items():
            for channel_name, vars in channels.items():
                size = len(vars)
                events = self.to_events(vars)
                acc.append(Channel(size, module, channel_name, events))
        return acc

    def to_simulation(self) -> Simulation:
        return Simulation(self.to_channel())