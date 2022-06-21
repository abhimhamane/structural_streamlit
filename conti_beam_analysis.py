from email import header
from sympy.physics.continuum_mechanics import Beam
from sympy import symbols

from sympy import SingularityFunction

import matplotlib.pyplot as plt

import pandas as pd
from numpy import linspace
from PIL import Image


def equally_spaced_sprts(length, num_spans):
    _num_sprts = num_spans + 1
    return linspace(0, int(length), int(_num_sprts))

def create_span_list(num_spans):
    _opt_list = []
    for _span_no in range(int(num_spans)):
        _opt_list.append("span "+str(_span_no + 1))
    
    return _opt_list



def create_pandas_df():
    return pd.DataFrame(columns=['num_spans','span_length'])



