from email import header
from sympy.physics.continuum_mechanics import Beam
from sympy import symbols

from sympy import SingularityFunction

import matplotlib.pyplot as plt

import pandas as pd
from numpy import linspace
from PIL import Image


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

def apply_udl_loads(cont_beam, udl_container):
    for _udl in udl_container:
        if _udl != None:
            if _udl[0] > 0.0:
                cont_beam.apply_load(_udl[0], _udl[1], 0, end=_udl[2])

def apply_moment_loads(cont_beam, moment_container):
    for mmt in moment_container:
        if mmt != None:
            if mmt[0] > 0.0:
                cont_beam.apply_load(mmt[0], mmt[1], -2)