from typing import List

class Unit:
    suffix = ""
    def __init__(self, value, precise=False, parts=None, expected=None):
        self.parts = parts
        self.precise = precise
        self.error = 0
        if self.precise:
            self.value = value
        else:
            self.value = round(value,3)
        if expected:
            self.expected = expected
            self.error = round(abs(self.value - self.expected),3)

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
        out = f"{str(self.value)}{self.suffix}"
        if self.parts:
            out = f"{str(self.value)}[{'+'.join(str(p.value) for p in self.parts)}]{self.suffix}"
        if self.error != 0:
            out += f" ±{str(self.error)}{self.suffix}"
        return out

class Volt(Unit):
    suffix="V"

class Ohm(Unit):
    suffix="Ω"

class VoltageDivider:
    def __init__(self, v1: Volt=None, r1: Ohm=None, r2: Ohm=None, v2: Volt=None, resistors: List[Ohm]=None):
        self.v1 = v1
        self.r1 = r1
        self.r2 = r2
        self.v2 = v2
        self.resistors = resistors

        # Calculate missing value
        if len([a for a in [v1,r1,r2,v2] if a is None]) == 1:
            self.fix_missing_value()

        # Determine matching resistors from listed available parts
        if self.v1 is not None and self.v2 is not None and self.r1 is None and self.r2 is None:
            if not self.resistors:
                raise ValueError("Expected list of resistors with which to calculate best options")
            self.fix_missing_resistance()

    def __repr__(self):
        return f"<VoltageDivider v1={self.v1} r1={self.r1} r2={self.r2} v2={self.v2}>"

    def fix_missing_value(self, expected_v1=None, expected_r1=None, expected_r2=None, expected_v2=None):
        v1 = self.v1.value if self.v1 else None
        v2 = self.v2.value if self.v2 else None
        r1 = self.r1.value if self.r1 else None
        r2 = self.r2.value if self.r2 else None
        if self.v1 is None:
            self.v1 = Volt(v2 * (r1+r2)/r2, expected=expected_v1)
        if self.r1 is None:
            self.r1 = Ohm((r2 * (v1-v2)) / v2, expected=expected_r1)
        if self.r2 is None:
            self.r2 = Ohm((v2*r1) / (v1-v2), expected=expected_r2)
        if self.v2 is None:
            self.v2 = Volt(v1 * (r2 / (r1+r2)), expected=expected_v2)

    def fix_missing_resistance(self):
        outp = {}
        v1 = self.v1.value
        goal_v2 = self.v2.value
        # Add pairs of resistors in series to options
        resistors = [r.value for r in self.resistors]
        for _r1 in self.resistors:
            for _r2 in self.resistors:
                r1 = _r1.value
                r2 = _r2.value
                resistors.append((r1,r2))
        # Iterate over options and build output
        for r1 in resistors:
            for r2 in resistors:
                _r1 = r1
                _r2 = r2
                if type(r1) is tuple:
                    r1 = sum(r1)
                if type(r2) is tuple:
                    r2 = sum(r2)
                outp[(_r1,_r2)] = abs(goal_v2-(v1 * (r2 / (r1 + r2))))
        r1, r2 = min(outp, key=outp.get)
        if type(r1) is tuple:
            self.r1 = Ohm(sum(r1), parts=[Ohm(o) for o in r1])
        else:
            self.r1 = Ohm(r1)
        if type(r2) is tuple:
            self.r2 = Ohm(sum(r2), parts=[Ohm(o) for o in r2])
        else:
            self.r2 = Ohm(r2)

        expected_v2 = self.v2.value
        self.v2 = None
        self.fix_missing_value(expected_v2=expected_v2)
