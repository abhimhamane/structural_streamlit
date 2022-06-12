import streamlit as st
import pandas as pd
import numpy as np

from beam_analysis import *

st.title("Simple Beam Analysis")

####### Side Bar #########
st.sidebar.header("Analysis Parameters")

analysis_params_form = st.sidebar.form("analysis_params_form")
analysis_params_form.subheader("Beam Properties")
beam_length = analysis_params_form.slider("Length (m)", 2.0, 25.0, 10.0, step=0.5)
beam_E = analysis_params_form.slider("Elastic Modulus in MPa:", 15000.0, 35000.0, 25000.0, step=5000.0)


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
    # then for each loading form call apply load func


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

    _lst = np.zeros((10, ))
    udl_start_loc, udl_end_loc = udl_load_inp_form.select_slider("Select start and end location", options=['1', '2', '3'], value=('1', '2'))    
    udl_load_inp_form.form_submit_button("Apply UDL")


    ##### Moment Load Form ########
    moment_load_inp_form = load_col.form("simple_loadings_form_moment")
    moment_load = moment_load_inp_form.slider("Moment Magnitude (kN/m)", -20.0, 20.0, 0.0, step=1.0)
    moment_load_loc = moment_load_inp_form.slider("Moment Load Location (m)", 0.0, beam_length, beam_length/2, step=0.1)
    moment_load_inp_form.form_submit_button("Apply Moment Load")
    
    ######################### Analysis COLUMN ##############
    simple_analysis_col.subheader("Analysis Results")


elif analysis_type == "What-If Analysis":
    what_if_container = st.container()
    what_if_container.header("What-If Analysis")

    what_if_analysis_type = what_if_container.radio(label = 'Which aspect you want to Analyse?', options = ['Support Effect', 'Loading Effect'])

    if 'support_effect' not in st.session_state:
        st.session_state.support_effect = what_if_analysis_type


    referene_column, interactive_column = what_if_container.columns(2)

    ################ Support Effect #########

























