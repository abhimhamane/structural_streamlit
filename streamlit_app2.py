import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

from beam_analysis import *

st.title("Simple Beam Analysis")

####### Side Bar #########
st.sidebar.header("Analysis Parameters")

analysis_params_form = st.sidebar.form("analysis_params_form")
analysis_params_form.subheader("Beam Properties")
beam_length = analysis_params_form.slider("Length (m)", 2.0, 25.0, 10.0, step=0.5)
beam_E = analysis_params_form.slider("Elastic Modulus in MPa:", 15000.0, 35000.0, 25000.0, step=5000.0)
beam_I = 0.004

#analysis_params_form.write("Second Moment of Inertia:  "+str(st.session_state.beam_I) + "m^4")


analysis_type = analysis_params_form.radio(label = 'Type of Analysis', options = ['Simple Analysis', 'What-If Analysis'])

analysis_params_form.form_submit_button("Apply")


###################################### Main content ###############################

# Creaating Layout 
if analysis_type == "Simple Analysis":
    simple_container = st.container()
    simple_container.header("Simple Analysis")

    ####### Select Type of Beam
    
    beam_type = simple_container.radio(label = 'Type of Beams', options = ['Simply Supported Beam', 'Fixed Beam', 'Proped Cantilever Beam'])

    if 'beam_type' not in st.session_state:
        simple_container.session_state.beam_type = beam_type

    # instanciate the beam
    if beam_type == "Simply Supported Beam":
        simple_beam, reacn_symbs = simply_supported_beam(beam_length, beam_E, beam_I)
    elif beam_type =="Fixed Beam":
        simple_beam ,reacn_symbs = fixed_beam(beam_length, beam_E, beam_I)
    elif beam_type =="Proped Cantilever Beam":
        simple_beam, reacn_symbs = proped_cantilever_beam(beam_length, beam_E, beam_I)
    


    ################################# Simple Analysis ############
    
    ##step1. Taking Input for type of beam
    ##step2. Taking Input for Loadings on Beam
    ##        Type of beam will be session state variable
    load_col, simple_analysis_col = simple_container.columns(2)


    ########################## LOADING COLUMN ##############
    load_col.subheader("Loading Cases")

    ########### Point Load Form ############
    pt_load_inp_form = load_col.form("simple_loadings_form_pt")
    point_load = pt_load_inp_form.slider("Point Magnitude (kN)", 0.0, 25.0, 10.0, step=1.0)
    point_load_loc = pt_load_inp_form.slider("Point Load Location (m)", 0.0, beam_length, beam_length/2, step=0.1)  
    pt_load_inp_form.form_submit_button("Apply Point Load")


    ##### UDL Form #########
    udl_load_inp_form = load_col.form("simple_loadings_form_udl")
    udl_load = udl_load_inp_form.slider("UDL Magnitude (kN/m)", 0.0, 20.0, 10.0, step=1.0)

    
    _lst = []
    for i in range(0, int(beam_length+1)):
        _lst.append(str(i))
    udl_strt_loc, udl_end_loc = udl_load_inp_form.select_slider("label", options=_lst, value=(_lst[0], _lst[-1]))
    ## start and end location is a string - later convert it to float in order to use
    
    udl_load_inp_form.form_submit_button("Apply UDL")

    ##### Moment Load Form ########
    moment_load_inp_form = load_col.form("simple_loadings_form_moment")
    moment_load = moment_load_inp_form.slider("Moment Magnitude (kN/m)", -20.0, 20.0, 0.0, step=1.0)
    moment_load_loc = moment_load_inp_form.slider("Moment Load Location (m)", 0.0, beam_length, beam_length/2, step=0.1)
    moment_load_inp_form.form_submit_button("Apply Moment Load")
    
    ######################### Analysis COLUMN ##############
    simple_analysis_col.subheader("Analysis Results")

        # then for each loading form call apply load func

    _pt_load = apply_point_load(simple_beam, point_load, point_load_loc)
    _moment_load = apply_moment_load(simple_beam, moment_load, moment_load_loc)
    _udl_load = apply_udl(simple_beam, udl_load, float(udl_strt_loc), float(udl_end_loc))

    ##### beam Visualisation
    simple_analysis_beam_viz = simple_analysis_col.container()
    simple_analysis_beam_viz.image(beam_viz(simple_beam, beam_type, reacn_symbs))

    #### Solving for reaction loads
    rxn_loads = solve_for_rxns(simple_beam ,reacn_symbs)
    rxn_loads

    simple_analysis_rxn_loads = simple_analysis_col.container()

    #### Plotting SFD, BMD and Deflections charts
    simple_analysis_plots = simple_analysis_col.container()
    shear_x, shear_y = shear_force_eqn(simple_beam)
    bm_eqn_vals = bending_moment_eqn(simple_beam)
    simple_analysis_plots.write("Plots")
    ###Plotting 
    """simple_analysis_plots.image(simple_beam.plot_shear_force())
    _fig = plt.figure(figsize=(10,6), tight_layout=True)
    #plotting
    #plt.plot(shear_x, shear_y)
    #customization
    
    plt.xlabel('x')
    plt.ylabel("Shear Force (kN)")
    plt.title("Shear Force Plot")
    plt.legend(title="Shear Force Plot", title_fontsize = 13)

    simple_analysis_plots.pyplot(_fig)"""

    





######################### What-If Analysis ###################################
elif analysis_type == "What-If Analysis":
    what_if_container = st.container()
    what_if_container.header("What-If Analysis")

    what_if_analysis_type = what_if_container.radio(label = 'Which aspect you want to Analyse?', options = ['Support Effect', 'Loading Effect'])

    if 'what_if_analysis_type' not in st.session_state:
        st.session_state.what_if_analysis_type = what_if_analysis_type

    referene_column, interactive_column = what_if_container.columns(2)

    if what_if_analysis_type == "Support Effect":
        ################ Support Effect #########


        
        simple_support_effect_column = referene_column.subheader("Support Effect")


        support_interactive_column = interactive_column.subheader("Beam Analysis")


    elif what_if_analysis_type == "Loading Effect":
        ################ Support Effect #########
        simple_loading_effect_column = referene_column.subheader("Loading Effect")

        loading_interactive_column = interactive_column.subheader("Beam Analysis")



























