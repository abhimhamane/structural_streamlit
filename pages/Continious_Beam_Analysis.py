from ossaudiodev import control_labels


from requests import options
import streamlit as st

from sympy import symbols
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

from conti_beam_analysis import *

#--------------- E and I standard values----------#
E = 25000
I = 0.0005175


#--------Sidebar Parameters -------------#
cont_beam_analysis_params = st.sidebar.form("Continuous_beam_analysis_parameters")
cont_beam_analysis_params.header("Continuous Beam Analysis Parameters")
total_length = cont_beam_analysis_params.slider("Length (m)", 5.0, 35.0, 10.0, step=1.0)
num_spans = int(cont_beam_analysis_params.slider("Number of spans:", 2.0, 4.0, 3.0, step=1.0))
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
    #_span_choice = further_params.radio("choose span no:", options= _span_options, horizontal=True)
    
    #-- Initialization of beam

    #-------Loading Form-----#
    pt_load_frm, udl_frm, mmt_frm = further_params.columns([1,1,1])
    #----initializing a session state variable to save the user input
    #---Read More @ https://docs.streamlit.io/library/api-reference/session-state
    #---Handy tutorial @ https://www.youtube.com/watch?v=5l9COMQ3acc
    
    if 'pt_load_matrix' not in st.session_state:
        st.session_state.pt_load_matrix = generate_list(num_spans)

    if 'udl_matrix' not in st.session_state:
        st.session_state.udl_matrix = generate_list(num_spans)


    if 'moment_matrix' not in st.session_state:
        st.session_state.moment_matrix = generate_list(num_spans)

        
    # point_load_form
    pt_load_inp_form = pt_load_frm.form("simple_loadings_form_pt")
    _span_choice_pt = pt_load_inp_form.radio("choose span no:", options= _span_options, horizontal=True)
    
    _span_id_pt = int(_span_choice_pt[5])
    point_load = pt_load_inp_form.slider("Point Magnitude (kN)", 0.0, 25.0, 0.0, step=1.0)
    point_load_loc = pt_load_inp_form.slider("Point Load Location (m)", 0.0, total_length, total_length/2.0, step=0.1)  
    pt_load_inp_form.form_submit_button("Apply Point Load")

    #----- Saving Load
    
    st.session_state.pt_load_matrix
    st.session_state.pt_load_matrix[_span_id_pt-1] = [point_load, point_load_loc]
    
    
    ##### UDL Form #########
    udl_load_inp_form = udl_frm.form("simple_loadings_form_udl")
    _span_choice_udl = udl_load_inp_form.radio("choose span no:", options= _span_options, horizontal=True)
    
    
    _span_id_udl = int(_span_choice_udl[5])
    udl_load = udl_load_inp_form.slider("UDL Magnitude (kN/m)", 0.0, 20.0, 0.0, step=1.0)

    
    lat = list(np.around(np.linspace(0.0, total_length, int(total_length)+1),decimals = 2))
    udl_strt_loc, udl_end_loc = udl_load_inp_form.select_slider("label", options=lat, value=(lat[0], lat[-1]))
    
    ## start and end location is a string - later converti it to float in order to use
    udl_load_inp_form.form_submit_button("Apply UDL")

    #----- Saving Load
    st.session_state.udl_matrix[_span_id_udl-1] = [udl_load, float(udl_strt_loc), float(udl_end_loc)]

    ##### Moment Load Form ########
    moment_load_inp_form = mmt_frm.form("simple_loadings_form_moment")
    _span_choice_mmt = moment_load_inp_form.radio("choose span no:", options= _span_options, horizontal=True)
    
    _span_id_mmt = int(_span_choice_mmt[5])
    moment_load = moment_load_inp_form.slider("Moment Magnitude (kN-m)", -20.0, 20.0, 0.0, step=1.0)
    moment_load_loc = moment_load_inp_form.slider("Moment Load Location (m)", 0.0, total_length, total_length/2.0 , step=0.1)
    moment_load_inp_form.form_submit_button("Apply Moment Load")

    st.session_state.moment_matrix[_span_id_mmt-1] = [moment_load, float(moment_load_loc)]
    
    
    # Initailization of beam
    cont_beam, viz_beam = create_contnious_beam(total_length, sprt_cond, _equally_spaced_sprt_loc,E, I)
    apply_point_loads(viz_beam, st.session_state.pt_load_matrix)
    apply_udl_loads(viz_beam, st.session_state.udl_matrix ,num_spans)
    apply_moment_loads(viz_beam, st.session_state.moment_matrix)
    
       
    #--- Vizualization of beams
    _cont_beam_viz = viz_beam.draw(pictorial=True)
    
    _cont_beam_viz.save("cont_temp_beam_viz.png")
    
    
    
    _image = Image.open('cont_temp_beam_viz.png')
    further_params.image(_image)

    #--- Applying Reaction Loads to Cont Beam
    rxn_symbs = create_reaction_load_symbols(total_length,sprt_cond, _equally_spaced_sprt_loc)
    apply_end_sprt_rxn_load(cont_beam, rxn_symbs, _equally_spaced_sprt_loc)
    apply_interm_sprt_rxn_loads(cont_beam, rxn_symbs, _equally_spaced_sprt_loc)

    apply_point_loads(cont_beam, st.session_state.pt_load_matrix)
    apply_udl_loads(cont_beam, st.session_state.udl_matrix, num_spans)
    apply_moment_loads(cont_beam, st.session_state.moment_matrix)

    rxn_loads = solve_rxn_loads(cont_beam, rxn_symbs)

    cont_beam_analysis_plots = further_params.container()
    shear_eqn = cont_beam.shear_force()
    bm_eqn = cont_beam.bending_moment()
    #slp_eqn = cont_beam.slope()
    #defl_eqn = cont_beam.deflection()
    fig, (shear_plot, bm_plot, deflection_plot) = plt.subplots(3, 1)
    ax_x = np.arange(0, cont_beam.length, 0.01)
    x_lst = []
    for i in ax_x:
        x_lst.append(i)

        
    shear_vals = []
    bm_vals = []
    defl_val = []
    x = ("x")
    for i in x_lst:
        shear_vals.append(float(shear_eqn.subs(x, i)))
        bm_vals.append(float(bm_eqn.subs(x, i)))
        #defl_val.append(float(slp_eqn.subs(x, i)))
    
    shear_plot.plot(x_lst, shear_vals, 'b')
    
    
    shear_plot.spines.right.set_visible(False)
    shear_plot.spines.top.set_visible(False)

    shear_plot.set_ylabel('V (kN)')
    shear_plot.set_title("Shear Plot")
    shear_plot.x_lim = 0
    shear_plot.axhline(y=0, color='k')
    shear_plot.axvline(x=0, color='k')
    shear_plot.axvline(x=total_length, color='k')
    
    
    shear_plot.grid(True, which='both')


    bm_plot.plot(x_lst, bm_vals, 'g')
    #bm_plot.set_xlabel('x')
    if BM_preference == "Tension Side":
        bm_plot.invert_yaxis()
    
    bm_plot.set_ylabel('M (kN-m)')
    bm_plot.set_title("Bending Moment Plot")
    bm_plot.axhline(y=0, color='k')
    bm_plot.axvline(x=0, color='k')
    bm_plot.axvline(x=total_length, color='k')
    bm_plot.grid(True, which='both')



    plt.subplots_adjust(bottom=0.1,  
                    top=0.9, 
                    wspace=0.4, 
                    hspace=0.4)

    cont_beam_analysis_plots.pyplot(fig)
    

    

    # Apply imposed Loads to cont beam
    apply_point_loads(cont_beam, st.session_state.pt_load_matrix)
    
elif type_of_spans == "Unequal":
    _span_options = create_span_list(num_spans)
    
    _span_lgth_frm = st.sidebar.form("Sidebar Span Length Form")
    _span_id = _span_lgth_frm.radio("choose span no:", options= _span_options, horizontal=True)
    

    _span_lgth_frm.form_submit_button("Done Setting Span Lengths")
    

    _df = create_pandas_df()
    

    
 







st.write(" Work in Progress....")

