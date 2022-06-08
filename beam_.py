
from sympy.physics.continuum_mechanics import Beam
import sympy

import pandas as pd


E = 25000
I = 0.0005

#print(beam_data, point_data)

L = 20
lt_sprt = "Fix"
rt_sprt = "Pin"

beam_inst = Beam(L, E, I)

def sympy_variable(x:str):
        return sympy.symbols(x)

def apply_end_support_loads(beam_inst, L):
    sympy_symbols = []
    if lt_sprt == "Fix":
        R_0 = sympy_variable("R_0")
        M_0 = sympy_variable("M_0")
        sympy_symbols.append(R_0)
        sympy_symbols.append(M_0)
        beam_inst.apply_support(0, "fixed")
    else:
        R_0 = sympy_variable("R_0")
        sympy_symbols.append(R_0)
        beam_inst.apply_support(0, "pin")

    if rt_sprt == "Fix":
        r_end = sympy_variable("R_" + str(L))
        m_end = sympy_variable("M_" + str(L))
        sympy_symbols.append(r_end)
        sympy_symbols.append(m_end)
        beam_inst.apply_support(L, "fixed")
    else:
        r_end = sympy_variable("R_" + str(L))
        sympy_symbols.append(r_end)
        beam_inst.apply_support(L, "pin")
    
    return sympy_symbols

reaction_symbols = apply_end_support_loads(beam_inst ,L)

beam_inst.apply_load(point_data[0], point_data[1], -1)
beam_inst.apply_load(moment_data[0], moment_data[1], -2)
beam_inst.apply_load(UDL_data[0], UDL_data[1], 0, end=UDL_data[2])

print(beam_inst.load)
draw_pen = beam_inst.draw(pictorial=True)
draw_pen.save("beam_viz.png")



