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
    
    return _viz_beam


def create_reaction_loads(total_length: float, end_supports: str, support_list: list):
    pass