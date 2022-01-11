voltagedivider
==============

A Python library to simplify the calculations necessary for adding a voltage divider to your circuit.

Usage
-----

Calculate missing value in equation, given the other three values (resulting VoltageDivider object has missing values filled in)

```python
>>> from voltage_divider import VoltageDivider, Volt, Ohm
>>> VoltageDivider(r1=Ohm(2200), r2=Ohm(4300), v2=Volt(3.3))
<VoltageDivider v1=4.988V r1=2200Ω r2=4300Ω v2=3.3V>
```

Given a list of available resistors you have lying around, the input voltage you have, and the output voltage you want, calculate which pair of available resistors (or which pairs of resistors in series) would be suitable to achieve the output voltage, displaying the amount of error where applicable

```python
>>> VoltageDivider(v1=Volt(5), v2=Volt(3.3),
        resistors=[Ohm(1000), Ohm(2200), Ohm(3300), Ohm(4700)])
<VoltageDivider v1=5V r1=2200Ω r2=4300[1000+3300]Ω v2=3.308V ±0.008V>
```

Translation: Given the input of 5V, if you used a 2.2kΩ resistor as R1 and used a 1kΩ and a 3.3kΩ resistor in series as R2, you would get 3.308V on the output, which is within 0.008V of the expected value.

It also tolerates lazy input to the constructor, not giving it the types, since you'd only be passing Volts in to v1 or v2 anyway. It won't, however, tolerate *incorrect* inputs, values that don't match with what the equation would expect. Values past 3dp are rounded off though, because floating point inaccuracy is dumb.

```python
>>> VoltageDivider(v1=5, v2=3.3, r1=2200, r2=4270.588)
<VoltageDivider v1=5V r1=2200Ω r2=4270.588Ω v2=3.3V>
>>> VoltageDivider(v1=5, v2=3.3, r1=2200, r2=4300)
! raises ValueError
```
