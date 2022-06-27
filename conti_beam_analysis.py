from email import header
from unicodedata import decimal
from sympy.physics.continuum_mechanics import Beam
from sympy import symbols
from sympy import integrate
from sympy.solvers import solve
from sympy import SingularityFunction

import matplotlib.pyplot as plt

import pandas as pd
from numpy import linspace, around
from PIL import Image

def generate_list(num_spans):
    _lst = []
    num_spans = int(num_spans)
    for _i in range(num_spans):
        _lst.append(None)
    return _lst

def equally_spaced_sprts(length, num_spans):
    
    return linspace(0, length, num_spans + 1)

def create_span_list(num_spans):
    _opt_list = []
    for _span_no in range(int(num_spans)):
        _opt_list.append("span "+str(_span_no + 1))
    
    return _opt_list


def create_pandas_df():
    return pd.DataFrame(columns=['num_spans','span_length'])


def create_contnious_beam(total_length: float, end_supports: str, support_list: list,_E, _I):
    _E = _E * (10**6)
    _beam = Beam(total_length, _E, _I)
    _viz_beam = Beam(total_length, _E, _I)
    # apply End support conditions
    if end_supports == "Fix-Fix":
        _viz_beam.apply_support(0, "fixed")
        _viz_beam.apply_support(total_length, "fixed")

    elif end_supports == "Fix-Pin":
        _viz_beam.apply_support(0, "fixed")
        _viz_beam.apply_support(total_length, "pin")
    elif end_supports == "Fix-Free":
        _viz_beam.apply_support(0, "fixed")
        
    elif end_supports == "Pin-Pin":
        _viz_beam.apply_support(0, "pin")
        _viz_beam.apply_support(total_length, "pin")
    elif end_supports == "Pin-Free":
        _viz_beam.apply_support(0, "pin")
    
    
    for inter_sprt in support_list[1:-1]:
        _viz_beam.apply_support(float(inter_sprt), "roller")
    
    return _beam, _viz_beam


def create_reaction_load_symbols(total_length: float, end_supports: str, support_list: list):
    sprt_rxn_symb_list=[[], []]

    if end_supports == "Fix-Fix":
        r_strt = symbols("R_0")
        sprt_rxn_symb_list[0].append(r_strt)
        m_strt = symbols("M_0")
        sprt_rxn_symb_list[0].append(m_strt)
        r_end = symbols("R_"+str(total_length))
        sprt_rxn_symb_list[0].append(r_end)
        m_end = symbols("M_"+str(total_length))
        sprt_rxn_symb_list[0].append(m_end)

    elif end_supports == "Fix-Pin":
        r_strt = symbols("R_0")
        sprt_rxn_symb_list[0].append(r_strt)
        m_strt = symbols("M_0")
        sprt_rxn_symb_list[0].append(m_strt)
        r_end = symbols("R_"+str(total_length))
        sprt_rxn_symb_list[0].append(r_end)
        
    elif end_supports == "Fix-Free":
        r_strt = symbols("R_0")
        sprt_rxn_symb_list[0].append(r_strt)
        m_strt = symbols("M_0")
        sprt_rxn_symb_list[0].append(m_strt)
        
    elif end_supports == "Pin-Pin":
        r_strt = symbols("R_0")
        sprt_rxn_symb_list[0].append(r_strt)
        
        r_end = symbols("R_"+str(total_length))
        sprt_rxn_symb_list[0].append(r_end)
        
    elif end_supports == "Pin-Free":
        r_strt = symbols("R_0")
        sprt_rxn_symb_list[0].append(r_strt)
        
    # Intermediate Sprts
    for inter_sprt in support_list[1:-1]:
        sprt_rxn_symb_list[1].append(symbols("R_" + str(inter_sprt)))
    
    return sprt_rxn_symb_list


def apply_end_sprt_rxn_load(cont_beam, sprt_rxn_symb_list, support_list):
    for sprt_rxn_symb in sprt_rxn_symb_list[0]:
        if float(str(sprt_rxn_symb)[2:]) == 0:
            if str(sprt_rxn_symb)[0] == "R":
                cont_beam.apply_load(sprt_rxn_symb, 0, -1)
                cont_beam.bc_deflection.append((0, 0))
            elif str(sprt_rxn_symb)[0] == "M":
                cont_beam.apply_load(sprt_rxn_symb, 0, -2)
                cont_beam.bc_slope.append((0, 0))
        else:
            if str(sprt_rxn_symb)[0] == "R":
                cont_beam.apply_load(sprt_rxn_symb, cont_beam.length, -1)
                cont_beam.bc_deflection.append((cont_beam.length, 0))
            elif str(sprt_rxn_symb)[0] == "M":
                cont_beam.apply_load(sprt_rxn_symb, cont_beam.length, -2)
                cont_beam.bc_slope.append((cont_beam.length, 0))
        

def apply_interm_sprt_rxn_loads(cont_beam, sprt_rxn_symb_list, support_list):
    interm_sprt = support_list[1:-1]
    for i in range(len(sprt_rxn_symb_list[1])):
        cont_beam.apply_load(sprt_rxn_symb_list[1][i], interm_sprt[i], -1)
        cont_beam.bc_deflection.append((interm_sprt[i], 0))


def apply_point_loads(cont_beam, pt_load_container: list):
    for i in range(len(pt_load_container)):
        if pt_load_container[i] != None:
            if pt_load_container[i][0] > 0.0:
                cont_beam.apply_load(float(pt_load_container[i][0]), float(pt_load_container[i][1]), -1)

def apply_udl_loads(cont_beam, udl_container, num_spans):
    _cnt = len(udl_container)
    for _udl in udl_container:
        if _udl != None:
            if _udl[0] > 0.0:
                cont_beam.apply_load(_udl[0], _udl[1], 0, end=_udl[2])
    
    

def apply_moment_loads(cont_beam, moment_container):
    for mmt in moment_container:
        if mmt != None:
            if mmt[0] > 0.0:
                cont_beam.apply_load(mmt[0], mmt[1], -2)


def open_rxn_symbs_list(rxn_symb_list):
    _lst = []
    for _rxn in rxn_symb_list[0]:
        _lst.append(_rxn)
    for _rxn in rxn_symb_list[1]:
        _lst.append(_rxn)
    
    return _lst

def clean_rxn_results(rxn_vals: dict):
    _key = (rxn_vals.keys())
    _vals = (rxn_vals.values())
    _rxn_loads = [(str(k)[:2]+str(around(float(str(k)[2:]), 2)),around(float(v), 3)) for k,v in zip(_key, _vals)]
    return _rxn_loads

def solve_rxn_loads(cont_beam, rxn_symb_list):
    rxn_symb_list = open_rxn_symbs_list(rxn_symb_list)
    _leng = len(rxn_symb_list)
    
    if _leng == 7:
        cont_beam.solve_for_reaction_loads(rxn_symb_list[0],rxn_symb_list[1], rxn_symb_list[2], rxn_symb_list[3], rxn_symb_list[4], rxn_symb_list[5],rxn_symb_list[6])
    elif _leng == 6:
        cont_beam.solve_for_reaction_loads(rxn_symb_list[0],rxn_symb_list[1], rxn_symb_list[2], rxn_symb_list[3], rxn_symb_list[4], rxn_symb_list[5])
    elif _leng == 5:
        cont_beam.solve_for_reaction_loads(rxn_symb_list[0],rxn_symb_list[1], rxn_symb_list[2], rxn_symb_list[3], rxn_symb_list[4])
    elif _leng == 4:
        cont_beam.solve_for_reaction_loads(rxn_symb_list[0],rxn_symb_list[1], rxn_symb_list[2], rxn_symb_list[3])
    elif _leng == 3:
        cont_beam.solve_for_reaction_loads(rxn_symb_list[0],rxn_symb_list[1], rxn_symb_list[2])
    elif _leng == 2:
        cont_beam.solve_for_reaction_loads(rxn_symb_list[0],rxn_symb_list[1])
    
    _cleaned_results = clean_rxn_results(cont_beam.reaction_loads)

    return _cleaned_results

def continous_beam_deflection(cont_beam, support_condition):
    x = symbols("x")
    C1 = symbols("C1")
    C2 = symbols("C2")

    c1_val = None
    
    moment_eqn = cont_beam.bending_moment()

    # integration of moment equation to obtain slope and deflection equation
    integrated_slp = (integrate(moment_eqn, x)/(cont_beam.elastic_modulus*cont_beam.second_moment)) + C1
    integrated_defl = integrate(integrated_slp, x) + C2

    if integrated_defl.subs(x, 0.0) == C2:
        _bc_applied = integrated_defl.subs(x, cont_beam.length)
        _bc_applied = _bc_applied.subs(C2, 0.0)
        if support_condition == "Pin-Pin" or support_condition == "Pin-Free":
            c1_val = solve(_bc_applied, C1)[0]

            integrated_defl = integrated_defl.subs(C1, c1_val)
            integrated_defl = integrated_defl.subs(C2, 0.0)

        else:    
            integrated_defl = integrated_defl.subs(C1, 0.0)
            integrated_defl = integrated_defl.subs(C2, 0.0)


    return integrated_defl

def provide_bc(cont_beam):
    raise NotImplementedError







