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

    #-------Loading Form-----#
    pt_load_matrix = []
    # point_load_form
    pt_load_inp_form = further_params.form("simple_loadings_form_pt")
    pt_load_inp_form.write(_span_choice)
    _span_id = int(_span_choice[5])
    
    point_load = pt_load_inp_form.slider("Point Magnitude (kN)", 0.0, 25.0, 10.0, step=1.0)
    point_load_loc = pt_load_inp_form.slider("Point Load Location (m)", float(_equally_spaced_sprt_loc[_span_id-1]), float(_equally_spaced_sprt_loc[_span_id]), float(_equally_spaced_sprt_loc[_span_id]+_equally_spaced_sprt_loc[_span_id-1])/2, step=0.1)  
    pt_load_inp_form.form_submit_button("Apply Point Load")


    pt_load_matrix.append((point_load, point_load_loc))
    if 'pt_load_matrix' not in st.session_state:
            st.session_state.pt_load_matrix = pt_load_matrix 

    pt_load_matrix
    



elif type_of_spans == "Unequal":
    _span_options = create_span_list(num_spans)
    
    _span_lgth_frm = st.sidebar.form("Sidebar Span Length Form")
    _span_id = _span_lgth_frm.radio("choose span no:", options= _span_options, horizontal=True)
    

    _span_lgth_frm.form_submit_button("Done Setting Span Lengths")
    

    _df = create_pandas_df()
    

    
    







st.write(" Work in Progress....")

