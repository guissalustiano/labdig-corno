from enum import Enum
from attr import dataclass

class SignalValues(Enum):
    ONE = 'H'
    ZERO = 'L'
    UNKNOWN = 'X'
    HIGH_Z = 'Z'

class Representations(Enum):
    BINARY = 'binary'
    HEXADECIMAL = 'hexadecimal'
    DECIMAL = 'decimal'

@dataclass
class Signal():
    representation: str
    value: str

    def to_tikz(self):
        value = self.value.lower()

        if len(self.value) == 1:
            if self.representation != Representations.BINARY:
                raise ValueError(f'Invalid representation "{self.representation}" for single bit signal.')
            if value == '1':
                return SignalValues.ONE.value
            elif '0' in self.value:
                return SignalValues.ZERO.value
            elif 'x' in value:
                return SignalValues.UNKNOWN.value
            elif 'z' in value:
                return SignalValues.HIGH_Z.value
        else:
            if 'x' in value:
                return SignalValues.UNKNOWN.value
            elif 'z' in value:
                return SignalValues.HIGH_Z.value
            elif self.representation == Representations.BINARY:
                return f'D{{{value}}}'
            elif self.representation == Representations.HEXADECIMAL:
                return f'D{{{hex(int(value, 2))}}}'
            elif self.representation == Representations.DECIMAL:
                return f'D{{0d{int(value, 2)}}}'
