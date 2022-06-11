import streamlit as st
import pandas as pd

from beam_analysis import *

st.title("Simple Beam Analysis")

####### Side Bar #########
st.sidebar.header("Analysis Parameters")

analysis_params_form = st.sidebar.form("analysis_params_form")
analysis_params_form.subheader("Beam Properties")
beam_length = analysis_params_form.slider("Length (m)", 2.0, 25.0, 10.0, step=0.5)
beam_E = analysis_params_form.slider("Elastic Modulus in MPa:", 15000.0, 35000.0, 25000.0, step=5000.0)

"""
if 'beam_length' not in st.session_state:
    st.session_state.beam_length = beam_length

if 'beam_E' not in st.session_state:
    st.session_state.beam_E = beam_E


if 'beam_I' not in st.session_state:
    st.session_state.beam_I = 0.005
"""
#analysis_params_form.write("Second Moment of Inertia:  "+str(st.session_state.beam_I) + "m^4")


analysis_type = analysis_params_form.radio(label = 'Type of Analysis', options = ['Simple Analysis', 'What-If Analysis'])

analysis_params_form.form_submit_button("Apply")



st.write("Outside forms")
st.write(beam_E)
st.write(beam_length)