from ossaudiodev import control_labels
import streamlit as st

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

from conti_beam_analysis import *



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

if num_spans <= 2:
    sprt_cond = st.radio("Choose End Support Conditions:", options=['Fix-Fix', 'Fix-Pin', 'Fix-Free', 'Pin-Pin', 'Pin-Free'], horizontal=True)
elif num_spans > 2:
    sprt_cond = st.radio("Choose End Support Conditions:", options=['Fix-Fix', 'Fix-Pin', 'Fix-Free', 'Pin-Pin', 'Pin-Free', 'Free-free'], horizontal=True)


if type_of_spans == "Equal":
    equal_spans_end_sprts = st.container()
    start_sprts, end_sprts = equal_spans_end_sprts.columns([1,1])

    num_supports = num_spans + 1

    if 'num_supports' not in st.session_state:
            st.session_state.num_supports = num_supports

elif type_of_spans == "Unequal":
    
    







st.write(" Work in Progress....")

