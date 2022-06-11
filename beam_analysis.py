from sympy.physics.continuum_mechanics import Beam
from sympy import symbols
from sympy import SingularityFunction

import matplotlib.pyplot as plt

import pandas as pd
import numpy as np

def beam_instantiate(L: float, E: float, I: float):
    """
    Returns sympy Beam instance with input parameters like 
    L: Length (meters)
    E: Young's Modulus (MPa)
    I: Second Moment of Inertia (m^4)
    """
    return Beam(L, E, I)

def create_sympy_symbol(variable: str):
    """
    In order to use sympy, sympy symbols are required.
    variable: a string input with same name as symbol name
    """
    return symbols(variable)

def simply_supported_beam(L: float, E: float, I: float):
    """
    Returns a simply( supported beam instance with bundary condition and Reaction load initialized.
    L: Length (meters)
    E: Young's Modulus (MPa)
    I: Second Moment of Inertia (m^4)
    """
    simply_suported = beam_instantiate(L, E, I)

    # create R_0 sympy symbol 
    rxn_symb = []

    R_0 = create_sympy_symbol("R_0")
    rxn_symb.append(R_0)
    r_end = create_sympy_symbol("R_"+ str(L))
    rxn_symb.append(r_end)

    # Apply reaction Point load 
    simply_suported.apply_load(R_0, 0, -1) 
    simply_suported.apply_load(r_end, L, -1) 

    #print(simply_suported.applied_loads)
    
    # Apply deflections and slope constraints
    simply_suported.bc_deflection.append((0,0))
    simply_suported.bc_deflection.append((L,0))

    return simply_suported, rxn_symb

def fixed_beam(L: float, E: float, I: float):
    """
    Returns a Fixed beam instance with bundary condition and Reaction load initialized.
    L: Length (meters)
    E: Young's Modulus (MPa)
    I: Second Moment of Inertia (m^4)
    """
    fix_beam = beam_instantiate(L, E, I)

    # create sympy symbol for Reaction Load
    rxn_symb = []

    R_0 = create_sympy_symbol("R_0")
    rxn_symb.append(R_0)
    M_0 = create_sympy_symbol("M_0")
    rxn_symb.append(M_0)

    r_end = create_sympy_symbol("R_" + str(L))
    rxn_symb.append(r_end)
    m_end = create_sympy_symbol("M_" + str(L))
    rxn_symb.append(m_end)

    # Apply Reaction Loads
    fix_beam.apply_load(R_0, 0, -1)
    fix_beam.apply_load(M_0, 0, -2)

    fix_beam.apply_load(r_end, fix_beam.length, -1)
    fix_beam.apply_load(m_end, fix_beam.length, -2)

    # Apply deflections and slope constraints
    fix_beam.bc_slope.append((0,0))
    fix_beam.bc_slope.append((L,0))

    fix_beam.bc_deflection.append((0,0))
    fix_beam.bc_deflection.append((L,0))

    return fix_beam, rxn_symb

def proped_cantilever_beam(L: float, E: float, I: float):
    """
    Returns a Proped Cantilever beam instance with bundary condition and Reaction load initialized.
    L: Length (meters)
    E: Young's Modulus (MPa)
    I: Second Moment of Inertia (m^4)
    """
    proped_cantilever = beam_instantiate(L, E, I)

    # create sympy symbol for Reaction Load
    rxn_symb = []
    
    R_0 = create_sympy_symbol("R_0")
    rxn_symb.append(R_0)
    M_0 = create_sympy_symbol("M_0")
    rxn_symb.append(M_0)

    r_end = create_sympy_symbol("R_" + str(L))
    rxn_symb.append(r_end)

    # Apply Reaction Loads
    proped_cantilever.apply_load(R_0, 0, -1)
    proped_cantilever.apply_load(M_0, 0, -2)

    proped_cantilever.apply_load(r_end, proped_cantilever.length, -1)

    # Apply deflections and slope constraints
    proped_cantilever.bc_slope.append((0,0))

    proped_cantilever.bc_deflection.append((0,0))
    proped_cantilever.bc_deflection.append((proped_cantilever.length,0))

    return proped_cantilever, rxn_symb


def cantilever_beam(L: float, E: float, I: float):

    raise NotImplementedError



def apply_point_load(beam_inst, magnitude: float, load_loc: float):
    beam_inst.apply_load(magnitude, load_loc, -1)
    _data = {'type': "Point Load",
            'magnitude': magnitude,
            'location': load_loc    
            }

    _load_def = pd.DataFrame(_data, index=[0])
    #print(_load_def)

    return _load_def

def apply_moment_load(beam_inst, magnitude: float, load_loc: float):
    beam_inst.apply_load(magnitude, load_loc, -2)
    _data = {'type': "Moment Load",
            'magnitude': magnitude,
            'location': load_loc    
            }

    _load_def = pd.DataFrame(_data, index=[0])
    #print(_load_def)

    return _load_def

def apply_udl(beam_inst, magnitude: float, start_loc: float, end_loc: float):
    beam_inst.apply_load(magnitude, start_loc, 0 ,end = end_loc)
    _data = {'type': "UDL",
            'magnitude': magnitude,
            'start_loc': start_loc,
            'end_loc': end_loc    
            }
    _load_def = pd.DataFrame(_data, index=[0])
    #print(_load_def)

    return _load_def


def solve_for_rxns(beam_inst, rxn_symb: list):
    """
    
    """
    if len(rxn_symb) == 4:
        beam_inst.solve_for_reaction_loads(rxn_symb[0], rxn_symb[1], rxn_symb[2] ,rxn_symb[3])
    
    elif len(rxn_symb) == 3:
        beam_inst.solve_for_reaction_loads(rxn_symb[0], rxn_symb[1], rxn_symb[2])
    
    else:
        beam_inst.solve_for_reaction_loads(rxn_symb[0], rxn_symb[1])
    
    _key = (beam_inst.reaction_loads.keys())
    _vals = (beam_inst.reaction_loads.values())
    _rxn_loads = [(k,v) for k,v in zip(_key, _vals)]

    return _rxn_loads

def shear_force_eqn(beam_inst):
    """
    
    """
    _shear_eqn = beam_inst.shear_force()
    ax_x = np.arange(0, beam_inst.length+0.05, 0.05)
    x = create_sympy_symbol("x")
    shear_y = []
    for i in ax_x:
        shear_y.append(_shear_eqn.subs(x, i))
    
    return [ax_x, shear_y]
    
def bending_moment_eqn(beam_inst):
    """
    
    """
    _bm_eqn = beam_inst.bending_moment()
    ax_x = np.arange(0, beam_inst.length+0.05, 0.05)
    x = create_sympy_symbol("x")
    bm_y = []
    for i in ax_x:
        bm_y.append(_bm_eqn.subs(x, i))
    
    return [ax_x ,bm_y]

def slope_eqn(beam_inst):
    """
    
    """
    raise NotImplementedError

def deflection_eqn(beam_inst):

    raise NotImplementedError

def matplotlib_plot_with_presets(beam_inst, eqn: list, plt_title: str, y_label: str):
    """
    This function takes the [x, y] input list and plots the values
    with certain presets of matplotlib to buitify the plot without
    """
    plt.figure(figsize=(10,6), tight_layout=True)
    #plotting
    plt.plot(eqn[0], eqn[1])
    #customization
    plt.xticks(np.arange(0, beam_inst.length+0.5, 1))
    plt.xlabel('x')
    plt.ylabel(y_label)
    plt.title(plt_title)
    plt.legend(title=plt_title, title_fontsize = 13)
    plt.show()




