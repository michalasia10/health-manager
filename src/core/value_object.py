from decimal import Decimal, getcontext


getcontext().prec = 50


class PreciseFloat:
    def __init__(self, value):
        self.value = Decimal(str(value))

    def __add__(self, other):
        if isinstance(other, PreciseFloat):
            return PreciseFloat(self.value + other.value)
        return PreciseFloat(self.value + Decimal(str(other)))

    def __sub__(self, other):
        if isinstance(other, PreciseFloat):
            return PreciseFloat(self.value - other.value)
        return PreciseFloat(self.value - Decimal(str(other)))

    def __mul__(self, other):
        if isinstance(other, PreciseFloat):
            return PreciseFloat(self.value * other.value)
        return PreciseFloat(self.value * Decimal(str(other)))

    def __truediv__(self, other):
        if isinstance(other, PreciseFloat):
            return PreciseFloat(self.value / other.value)
        return PreciseFloat(self.value / Decimal(str(other)))

    def __repr__(self):
        return f"{self.value}"