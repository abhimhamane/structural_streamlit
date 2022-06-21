from ossaudiodev import control_labels

from requests import options
import streamlit as st

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

from conti_beam_analysis import *

#--------------- E and I standard values----------#
E = 25000
I = 0.000525


#--------Sidebar Parameters -------------#
cont_beam_analysis_params = st.sidebar.form("Continuous_beam_analysis_parameters")
cont_beam_analysis_params.header("Continuous Beam Analysis Parameters")
total_length = cont_beam_analysis_params.slider("Length (m)", 5.0, 35.0, 10.0, step=1.0)
num_spans = cont_beam_analysis_params.slider("Number of spans:", 2.0, 4.0, 3.0, step=1.0)
type_of_spans = cont_beam_analysis_params.radio("Nature of Spans:", options=['Equal', 'Unequal'], horizontal=True)

BM_preference = cont_beam_analysis_params.radio("Choose your BM Drawing convention:", options=['Compression Side' ,'Tension Side'], horizontal=True)
cont_beam_analysis_params.form_submit_button("Apply Changes")

#------------Main Content --------------#

st.title("Continuous Beam Analysis")
further_params = st.container()
if num_spans <= 2:
    sprt_cond = further_params.radio("Choose End Support Conditions:", options=['Fix-Fix', 'Fix-Pin', 'Fix-Free', 'Pin-Pin', 'Pin-Free'], horizontal=True)
elif num_spans > 2:
    sprt_cond = further_params.radio("Choose End Support Conditions:", options=['Fix-Fix', 'Fix-Pin', 'Fix-Free', 'Pin-Pin', 'Pin-Free', 'Free-free'], horizontal=True)

# initialization of continuous beam
cont_beam = Beam(total_length, E, I)

if type_of_spans == "Equal":
    equal_spans_end_sprts = further_params.container()
    

    num_supports = num_spans + 1

    if 'num_supports' not in st.session_state:
            st.session_state.num_supports = num_supports
    

    _equally_spaced_sprt_loc = equally_spaced_sprts(int(total_length), int(num_spans))
    
    #print(_equally_spaced_sprt_loc)
    _span_options = create_span_list(num_spans)
    _span_choice = further_params.radio("choose span no:", options= _span_options, horizontal=True)

    #-- Initialization of beam

    


    #-------Loading Form-----#
    pt_load_frm, udl_frm, mmt_frm = further_params.columns([1,1,1])
    #----initializing a session state variable to save the user input
    #---Read More @ https://docs.streamlit.io/library/api-reference/session-state
    #---Handy tutorial @ https://www.youtube.com/watch?v=5l9COMQ3acc
    if 'pt_load_matrix' not in st.session_state:
        st.session_state.pt_load_matrix = [None, None, None, None]

    if 'udl_matrix' not in st.session_state:
        st.session_state.udl_matrix = [None, None, None, None]

    if 'moment_matrix' not in st.session_state:
        st.session_state.moment_matrix = [None, None, None, None]
    
    pt_load_container = st.session_state.pt_load_matrix
    udl_container = st.session_state.udl_matrix
    moment_container = st.session_state.moment_matrix
    
    # point_load_form
    pt_load_inp_form = pt_load_frm.form("simple_loadings_form_pt")
    pt_load_inp_form.write(_span_choice)
    _span_id = int(_span_choice[5])
    
    point_load = pt_load_inp_form.slider("Point Magnitude (kN)", 0.0, 25.0, 10.0, step=1.0)
    point_load_loc = pt_load_inp_form.slider("Point Load Location (m)", float(_equally_spaced_sprt_loc[_span_id-1]), float(_equally_spaced_sprt_loc[_span_id]), float(_equally_spaced_sprt_loc[_span_id]+_equally_spaced_sprt_loc[_span_id-1])/2, step=0.1)  
    pt_load_inp_form.form_submit_button("Apply Point Load")

    #----- Saving Load
    st.session_state.pt_load_matrix[_span_id-1] = (point_load, point_load_loc)
    
    ##### UDL Form #########
    udl_load_inp_form = udl_frm.form("simple_loadings_form_udl")
    udl_load_inp_form.write(_span_choice)
    _span_id = int(_span_choice[5])
    udl_load = udl_load_inp_form.slider("UDL Magnitude (kN/m)", 0.0, 20.0, 10.0, step=1.0)

    
    lat = list(np.around(np.linspace(float(_equally_spaced_sprt_loc[_span_id-1]), float(_equally_spaced_sprt_loc[_span_id]), 5),decimals = 2))
    udl_strt_loc, udl_end_loc = udl_load_inp_form.select_slider("label", options=lat, value=(lat[0], lat[-1]))
    
    ## start and end location is a string - later convert it to float in order to use
    
    udl_load_inp_form.form_submit_button("Apply UDL")

    st.session_state.udl_matrix[_span_id-1]=(udl_load, float(udl_strt_loc), float(udl_end_loc))
    
    ##### Moment Load Form ########
    moment_load_inp_form = mmt_frm.form("simple_loadings_form_moment")
    moment_load_inp_form.write(_span_choice)
    _span_id = int(_span_choice[5])
    moment_load = moment_load_inp_form.slider("Moment Magnitude (kN/m)", -20.0, 20.0, 0.0, step=1.0)
    moment_load_loc = moment_load_inp_form.slider("Moment Load Location (m)", float(_equally_spaced_sprt_loc[_span_id-1]), float(_equally_spaced_sprt_loc[_span_id]), float(_equally_spaced_sprt_loc[_span_id]+_equally_spaced_sprt_loc[_span_id-1])/2, step=0.1)
    moment_load_inp_form.form_submit_button("Apply Moment Load")
    
    st.session_state.moment_matrix[_span_id-1]=(moment_load, float(moment_load_loc))
    

    # Initailization of beam
    viz_beam = create_contnious_beam(total_length, sprt_cond, _equally_spaced_sprt_loc,E, I)
    cont_beam_sprt_pen = viz_beam.draw(pictorial=True)
    
    cont_beam_sprt_pen.save("cont_temp_beam_viz.png")

    
    _image = Image.open('cont_temp_beam_viz.png')
    further_params.image(_image)

    st.write(create_reaction_load_symbols(total_length,sprt_cond, _equally_spaced_sprt_loc))


elif type_of_spans == "Unequal":
    _span_options = create_span_list(num_spans)
    
    _span_lgth_frm = st.sidebar.form("Sidebar Span Length Form")
    _span_id = _span_lgth_frm.radio("choose span no:", options= _span_options, horizontal=True)
    

    _span_lgth_frm.form_submit_button("Done Setting Span Lengths")
    

    _df = create_pandas_df()
    

    
    







st.write(" Work in Progress....")

