from sympy.physics.continuum_mechanics import Beam
from sympy import symbols
import sympy
from sympy import SingularityFunction

import matplotlib.pyplot as plt

import pandas as pd
import numpy as np
from PIL import Image


def beam_instantiate(L: float, E: float, I: float):
    """
    Returns sympy Beam instance with input parameters like 
    L: Length (meters)
    E: Young's Modulus (MPa)
    I: Second Moment of Inertia (m^4)
    """
    E = E * (10**6) #converts from MPa to Pa
   
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
    """
    Returns a Cantilever beam instance with bundary condition and Reaction load initialized.
    L: Length (meters)
    E: Young's Modulus (MPa)
    I: Second Moment of Inertia (m^4)
    """
    cantilever_beam = beam_instantiate(L, E, I)

    # create sympy symbol for Reaction Load
    rxn_symb = []
    
    R_0 = create_sympy_symbol("R_0")
    rxn_symb.append(R_0)
    M_0 = create_sympy_symbol("M_0")
    rxn_symb.append(M_0)

    
    # Apply Reaction Loads
    cantilever_beam.apply_load(R_0, 0, -1)
    cantilever_beam.apply_load(M_0, 0, -2)

    # Apply deflections and slope constraints
    cantilever_beam.bc_slope.append((0,0))

    cantilever_beam.bc_deflection.append((0,0))
    

    return cantilever_beam, rxn_symb



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


def beam_viz(beam_inst, beam_type, rxn_symbs):
    _beam_inst_sprt = Beam(beam_inst.length, beam_inst.elastic_modulus, beam_inst.second_moment)

    #print(_beam_inst)
    _loads = beam_inst.applied_loads
    #print(_loads)
    
    """for _load in _loads:
        if _load in rxn_symbs :
            print((_load[0]))
            _beam_inst.remove_load(_load[0], _load[1], _load[2], _load[3])
        if _load[0] == 0.0:
            _beam_inst.remove_load(_load[0], _load[1], _load[2], _load[3])"""
    # This is beam Vizulization
    if beam_type == "Simply Supported Beam":
        _beam_inst_sprt.apply_support(0, "pin")
        _beam_inst_sprt.apply_support(beam_inst.length ,"roller")
    elif beam_type == "Fixed Beam":
        _beam_inst_sprt.apply_support(0, "fixed")
        _beam_inst_sprt.apply_support(beam_inst.length, "fixed")
    elif beam_type == "Proped Cantilever Beam":
        _beam_inst_sprt.apply_support(0, "fixed")
        _beam_inst_sprt.apply_support(beam_inst.length, "roller")
    elif beam_type == "Cantilever Beam":
        _beam_inst_sprt.apply_support(0, "fixed")

    _beam_sprt_loads = _beam_inst_sprt.applied_loads
    
    ## This is beam with reactions and loads
    
    for _load in _loads:
        if _load[0] != 0.0:
            _beam_inst_sprt.apply_load(_load[0], _load[1], _load[2], _load[3])
        if type(_load[0]) == sympy.core.symbol.Symbol:
            _beam_inst_sprt.remove_load(_load[0], _load[1], _load[2], _load[3])
       
    
    _beam_sprt_pen = _beam_inst_sprt.draw(pictorial=True)
    
    _beam_sprt_pen.save("temp_beam_viz.png")

    
    _image = Image.open('temp_beam_viz.png')
    _img_width, _img_height = _image.size
    
    ## Cropping the image
    x, y = 70, 150
    # Select area to crop
    area = (x, y, x+520, y+175)
    # Crop, show, and save image
    _cropped_img = _image.crop(area)
    

    return(_cropped_img)



##########

def deflection_equations(beam_inst, beam_type):
    x = sympy.symbols("x")
    C1 = sympy.symbols("C1")
    C2 = sympy.symbols("C2")

    c1_val = None
    c2_val = None

    moment_eqn = beam_inst.bending_moment()

    # integration of moment equation to obtain slope and deflection equation
    integrated_slp = sympy.integrate(moment_eqn, x)/(beam_inst.elastic_modulus*beam_inst.second_moment) + C1
    integrated_defl = sympy.integrate(integrated_slp, x) + C2

    if integrated_defl.subs(x, 0.0) == C2:
        _bc_applied = integrated_defl.subs(x, beam_inst.length)
        _bc_applied = _bc_applied.subs(C2, 0.0)

        c1_val = sympy.solvers.solve(_bc_applied, C1)[0]

        integrated_defl = integrated_defl.subs(C1, c1_val)
        integrated_defl = integrated_defl.subs(C2, 0.0)




    return integrated_defl
    