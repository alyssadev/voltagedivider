class Unit:
    suffix = ""
    def __init__(self, value, precise=False):
        self.precise = precise
        if self.precise:
            self.value = value
        else:
            self.value = round(value,3)

    def __add__(self, other):
        return self.value + (other.value if other is Unit else other)
    def __sub__(self, other):
        return self.value - (other.value if other is Unit else other)
    def __mul__(self, other):
        return self.value * (other.value if other is Unit else other)
    def __div__(self, other):
        return self.value / (other.value if other is Unit else other)
    def __radd__(self, other):
        return self.__add__(other)
    def __rsub__(self, other):
        return self.__sub__(other)
    def __rmul__(self, other):
        return self.__mul__(other)
    def __rdiv__(self, other):
        return self.__div__(other)

    def __eq__(self, other):
        return type(self) is type(other) and self.value == other.value and self.precise == other.precise

    def __repr__(self):
        return f"{self.value}{self.suffix}"

class Volt(Unit):
    suffix="V"

class Ohm(Unit):
    suffix="Ω"

class VoltageDivider:
    def __init__(self, v1: Volt=None, r1: Ohm=None, r2: Ohm=None, v2: Volt=None):
        self.v1 = v1
        self.r1 = r1
        self.r2 = r2
        self.v2 = v2
        missing = len([a for a in [v1,r1,r2,v2] if a is None])
        if missing > 1:
            raise ValueError("Missing input")
        if missing == 1:
            self.fix_missing()
    def fix_missing(self):
        v1 = self.v1.value if self.v1 else None
        v2 = self.v2.value if self.v2 else None
        r1 = self.r1.value if self.r1 else None
        r2 = self.r2.value if self.r2 else None
        if self.v1 is None:
            self.v1 = Volt(v2 * (r1+r2)/r2)
        if self.r1 is None:
            self.r1 = Ohm((r2 * (v1-v2)) / v2)
        if self.r2 is None:
            self.r2 = Ohm((v2*r1) / (v1-v2))
        if self.v2 is None:
            self.v2 = Volt(v1 * (r2 / (r1+r2)))
