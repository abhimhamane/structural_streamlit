from sympy.physics.continuum_mechanics import Beam
from sympy import symbols

from sympy import SingularityFunction

import matplotlib.pyplot as plt

import pandas as pd
from numpy import linspace
from PIL import Image


def equally_spaced_sprts(cont_beam_inst, num_spans):
    _num_sprts = num_spans + 1
    return linspace(0, cont_beam_inst.length, _num_sprts)

def span_list(num_spans):
    _opt_list = []
    for _span_no in range(num_spans):
        _opt_list.append("span "+str(_span_no + 1))
    
    return _opt_list

