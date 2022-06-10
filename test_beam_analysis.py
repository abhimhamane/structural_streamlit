from functools import singledispatchmethod
from re import X
import unittest
from beam_analysis import *
from sympy.physics.continuum_mechanics import Beam
from sympy import symbols
import pandas as pd


# length in meters
_L = 10.0 
# E in MPa
_E = 25000.0
# I in m^4
_I = 0.004

# Instaintiating beam 
_b1 = beam_instantiate(_L, _E, _I)
# asserting the Sympy-Beam instance variables
assert(_b1.length == 10.0)
assert(_b1.elastic_modulus == 25000.0)
assert(_b1.second_moment == 0.004)
assert(_b1.bc_deflection == [])
assert(_b1.bc_slope == [])


# assert that sympy symbols is working
_alpha = symbols("A")
assert(create_sympy_symbol("A") == _alpha)


def test_simply_supported_beam(L, E, I):
    # Simply supported beam instance
    ss_beam, reacn_symbs = simply_supported_beam(L, E, I)
   
    # asserting instance variables
    assert(ss_beam.length == 10.0)
    assert(ss_beam.elastic_modulus == 25000.0)
    assert(ss_beam.second_moment == 0.004)

    # assert simply supported support boundary condition
    assert(ss_beam.bc_deflection == [(0,0),(10.0,0)])
    assert(ss_beam.bc_slope == [])

    assert(reacn_symbs == [create_sympy_symbol("R_0"), create_sympy_symbol("R_10.0")])

    # assert simply supported Reactions
    sprt_rxn = [(reacn_symbs[0], 0, -1, None), (reacn_symbs[1], ss_beam.length, -1, None)]
    assert(ss_beam.applied_loads == sprt_rxn)

    # checking sprt rxn loads are as expected
    x = create_sympy_symbol("x")
    sprt_rxn_loads = reacn_symbs[0]*SingularityFunction(x, 0, -1) + reacn_symbs[1]*SingularityFunction(x, ss_beam.length, -1)
    assert(ss_beam.load == sprt_rxn_loads)

def test_fixed_beam(L, E,I):
    # Fixed beam instance
    fix_beam, reacn_symbs = fixed_beam(L, E, I)

    # asserting instance varaibles
    assert(fix_beam.length == L)
    assert(fix_beam.elastic_modulus == 25000.0)
    assert(fix_beam.second_moment == 0.004)

    ## assert Fixed support boundary condition
    assert(fix_beam.bc_deflection == [(0,0),(10.0,0)])
    assert(fix_beam.bc_slope == [(0,0),(10.0,0)])

    # assert Fixed support Reactions
    sprt_rxn = [(reacn_symbs[0], 0, -1, None), (reacn_symbs[1], 0, -2, None),  (reacn_symbs[2], fix_beam.length, -1, None), (reacn_symbs[3], fix_beam.length, -2, None)]
    assert(fix_beam.applied_loads == sprt_rxn)

    # checking sprt rxn loads are as expected
    x = create_sympy_symbol("x")
    sprt_rxn_loads = reacn_symbs[0]*SingularityFunction(x, 0, -1) + reacn_symbs[1]*SingularityFunction(x, 0, -2) + reacn_symbs[2]*SingularityFunction(x, fix_beam.length, -1) + reacn_symbs[3]*SingularityFunction(x, fix_beam.length, -2)
    assert(fix_beam.load == sprt_rxn_loads)


def test_proped_cantilever_beam(L, E, I):
    # Proped Cantilever beam instance
    proped_canti, reacn_symbs = proped_cantilever_beam(L, E, I)

    # assert instance variables
    assert(proped_canti.length == L)
    assert(proped_canti.elastic_modulus == 25000.0)
    assert(proped_canti.second_moment == 0.004)

    ## assert Proped Cantilever support boundary condition
    assert(proped_canti.bc_deflection == [(0,0),(10.0,0)])
    assert(proped_canti.bc_slope == [(0,0)])

    # assert Proped Cantilever support Reactions
    sprt_rxn = [(reacn_symbs[0], 0, -1, None), (reacn_symbs[1], 0, -2, None),  (reacn_symbs[2], proped_canti.length, -1, None)]
    assert(proped_canti.applied_loads == sprt_rxn)

    # checking sprt rxn loads are as expected
    x = create_sympy_symbol("x")
    sprt_rxn_loads = reacn_symbs[0]*SingularityFunction(x, 0, -1) + reacn_symbs[1]*SingularityFunction(x, 0, -2) + reacn_symbs[2]*SingularityFunction(x, proped_canti.length, -1)
    assert(proped_canti.load == sprt_rxn_loads)


test_simply_supported_beam(_L, _E, _I)
test_fixed_beam(_L, _E, _I)
test_proped_cantilever_beam(_L, _E, _I)






