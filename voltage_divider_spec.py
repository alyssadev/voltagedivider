from mamba import description, context, it
from expects import expect, equal
from voltage_divider import VoltageDivider, Volt, Ohm

with description("Voltage Divider") as self:
    with it("can determine the missing figure when provided three values in the equation, to three decimal places"):
        # Missing v1
        vd_v1 = VoltageDivider(r1=Ohm(2200), r2=Ohm(4300), v2=Volt(3.3))
        expect(vd_v1.v1).to(equal(Volt(4.988)))
        # Missing r1
        vd_r1 = VoltageDivider(v1=Volt(5), r2=Ohm(4300), v2=Volt(3.3))
        expect(vd_r1.r1).to(equal(Ohm(2215.152)))
        # Missing r2
        vd_r2 = VoltageDivider(v1=Volt(5), r1=Ohm(2200), v2=Volt(3.3))
        expect(vd_r2.r2).to(equal(Ohm(4270.588)))
        # Missing v2
        vd_v2 = VoltageDivider(v1=Volt(5), r1=Ohm(2200), r2=Ohm(4300))
        expect(vd_v2.v2).to(equal(Volt(3.308)))

    with it("can determine which pair of available resistors would be suitable to achieve an end voltage from a start voltage, and report the amount of error"):
        # Step down 5V to 3.3V
        vd_resistor_calc = VoltageDivider(v1=Volt(5), v2=Volt(3.3),
                resistors=[Ohm(1000), Ohm(2200), Ohm(3300), Ohm(4700)])
        expect(vd_resistor_calc.r1).to(equal(Ohm(2200)))
        expect(vd_resistor_calc.r2).to(equal(Ohm(4300)))
        expect(vd_resistor_calc.v2).to(equal(Volt(3.308)))
        expect(vd_resistor_calc.v2.error).to(equal(0.008))
