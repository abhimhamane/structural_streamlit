
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


_mag = 22.5
_load_loc = 5.0
_start_loc = 2.0
_end_loc = 7.0

def test_apply_point_load(b1, magnitude, load_loc):

    load_df = apply_point_load(b1, magnitude, load_loc)

    x = create_sympy_symbol("x")
    assert(b1.applied_loads == [(22.5, 5.0, -1, None)])
    
    assert(b1.load == magnitude * SingularityFunction(x, load_loc, -1))
    
def test_apply_moment_load(b1, magnitude, load_loc):

    _df = apply_moment_load(b1, magnitude, load_loc)

    x = create_sympy_symbol("x")
    assert(b1.applied_loads == [(magnitude, load_loc, -2, None)])
    
    assert(b1.load == magnitude * SingularityFunction(x, load_loc, -2))
    
def test_apply_udl(b1, magnitude, start_loc, end_loc):

    _df = apply_udl(b1, magnitude, start_loc, end_loc)

    x = create_sympy_symbol("x")
    assert(b1.applied_loads == [(magnitude, start_loc, 0, end_loc)])
    
    assert(b1.load == magnitude * SingularityFunction(x, start_loc, 0) - magnitude*SingularityFunction(x, end_loc, 0))
    

test_simply_supported_beam(_L, _E, _I)
test_fixed_beam(_L, _E, _I)
test_proped_cantilever_beam(_L, _E, _I)

##### While testing loadings check individually

### All cases pass the test so commented out do they 
### won't cause any interference ahead
#test_apply_point_load(_b1, _mag ,_load_loc) 
#test_apply_moment_load(_b1, _mag ,_load_loc)
#test_apply_udl(_b1, _mag, _start_loc, _end_loc)



def testing_ss_beam(L, E, I):
    """
    Testing simply supported beam 

        1. for supoort reactions with
        2. shear force eqn
        3. Bending Moment eqn
        4. Slope and Deflection equation (Not Yet Implemented)
    """
    mag = 10.0
    load_loc = 5.0
    start_loc = 0.0
    end_loc = 10.0

    ss_beam, rxn_symb = simply_supported_beam(_L, _E, _I)

    ###Case 1: Point load at center

    apply_point_load(ss_beam, mag, load_loc)

    ### Downward load is positive
    ### Upward reactions are negative
    rxn_loads = solve_for_rxns(ss_beam, rxn_symb)

    R_0, R_10 = symbols("R_0 R_10.0")
    _expected_rxns = [(R_0, -mag/2), (R_10, -mag/2)]
    
    assert(rxn_loads == _expected_rxns) #This assert statement is satisfied

    ###Case 2: Moment Load
    ss_beam, rxn_symb = simply_supported_beam(_L, _E, _I)
    ###### Anti-clockwise moment load is positive
    apply_moment_load(ss_beam, mag, load_loc)

    rxn_loads = solve_for_rxns(ss_beam, rxn_symb)

    R_0, R_10 = symbols("R_0 R_10.0")
    _expected_rxns = [(R_0, -mag/ss_beam.length), (R_10, mag/ss_beam.length)]
        
    assert(rxn_loads == _expected_rxns)

    #case 3: UDL
    ss_beam, rxn_symb = simply_supported_beam(_L, _E, _I)
    apply_udl(ss_beam, mag, start_loc, end_loc)

    rxn_loads = solve_for_rxns(ss_beam, rxn_symb)

    R_0, R_10 = symbols("R_0 R_10.0")
    _expected_rxns = [(R_0, -(mag*(end_loc-start_loc))/2), (R_10, -(mag*(end_loc-start_loc))/2)]
        
    assert(rxn_loads == _expected_rxns)

    # Case 4 Superpositions of all 4 forces
    ss_beam, rxn_symb = simply_supported_beam(_L, _E, _I)

    apply_point_load(ss_beam, mag, load_loc)
    apply_moment_load(ss_beam, mag, load_loc)
    apply_udl(ss_beam, mag, start_loc, end_loc)

    rxn_loads = solve_for_rxns(ss_beam, rxn_symb)

    R_0, R_10 = symbols("R_0 R_10.0")
    _expected_rxns = [(R_0, -mag/2-(mag/ss_beam.length) + (-(mag*(end_loc-start_loc))/2)), (R_10, -mag/2+(mag/ss_beam.length)+(-(mag*(end_loc-start_loc))/2))]

    assert(rxn_loads == _expected_rxns)

    ####### All test passed

#testing_ss_beam(_L, _E, _I)
