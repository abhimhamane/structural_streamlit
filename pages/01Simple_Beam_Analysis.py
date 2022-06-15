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
beam_I = 0.0005175 # m^4

#analysis_params_form.write("Second Moment of Inertia:  "+str(st.session_state.beam_I) + "m^4")


analysis_type = analysis_params_form.radio(label = 'Type of Analysis', options = ['Simple Analysis', 'What-If Analysis'])


analysis_params_form.form_submit_button("Apply")


###################################### Main content ###############################

# Creaating Layout 
if analysis_type == "Simple Analysis":
    simple_container = st.container()
    simple_container.header("Simple Analysis")

    ####### Select Type of Beam
    
    beam_type = simple_container.radio(label = 'Type of Beams', options = ['Simply Supported Beam', 'Fixed Beam', 'Proped Cantilever Beam'], horizontal=True)

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
    

    simple_analysis_rxn_loads = simple_analysis_col.container()
    simple_analysis_rxn_loads.write(rxn_loads)

    #### Plotting SFD, BMD and Deflections charts
    simple_analysis_plots = simple_analysis_col.container()
    shear_eqn = simple_beam.shear_force()
    bm_eqn = simple_beam.bending_moment()
    #slp_eqn = simple_beam.slope()
    #defl_eqn = simple_beam.deflection()
    
    "Shear Equation:"
    shear_eqn
    " "
    "Bending Moment Equation:"
    bm_eqn
    "Deflection Equation"
    #defl_eqn


    fig, (shear_plot, bm_plot, deflection_plot) = plt.subplots(3, 1)
    ax_x = np.arange(0, simple_beam.length, 0.01)
    x_lst = []
    for i in ax_x:
        x_lst.append(i)

        
    shear_vals = []
    bm_vals = []
    defl_val = []
    x = create_sympy_symbol("x")
    for i in x_lst:
        shear_vals.append(float(shear_eqn.subs(x, i)))
        bm_vals.append(float(bm_eqn.subs(x, i)))
        #defl_val.append(float(defl_eqn.subs(x, i)))
    
    shear_plot.plot(x_lst, shear_vals, 'b')
    
    shear_max = max(shear_vals)
    shear_max_pos = shear_vals.index(shear_max)
    shear_min = min(shear_vals)
    #shear_zero = shear_vals.index(0.0)
    shear_min_pos = shear_vals.index(shear_min)
    shear_plot.annotate(str(shear_max)+" kN", xy=(shear_max_pos, shear_max), xytext=(shear_max_pos-1, shear_max+6), xycoords='data')
    
    shear_plot.spines.right.set_visible(False)
    shear_plot.spines.top.set_visible(False)

    shear_plot.set_ylabel('V (kN)')
    shear_plot.set_title("Shear Plot")
    shear_plot.x_lim = 0
    shear_plot.axhline(y=0, color='k')
    shear_plot.axvline(x=0, color='k')
    shear_plot.axvline(x=beam_length, color='k')
    
    
    shear_plot.grid(True, which='both')


    bm_plot.plot(x_lst, bm_vals, 'g')
    #bm_plot.set_xlabel('x')
    bm_plot.invert_yaxis()
    bm_plot.set_ylabel('M (kN-m)')
    bm_plot.set_title("Bending Moment Plot")
    bm_plot.axhline(y=0, color='k')
    bm_plot.axvline(x=0, color='k')
    bm_plot.axvline(x=beam_length, color='k')
    bm_plot.grid(True, which='both')


    """deflection_plot.plot(x_lst, defl_val)
    deflection_plot.set_xlabel('x')
    deflection_plot.set_ylabel('Deflection (m)')
    deflection_plot.set_title("Deflection Plot")
    deflection_plot.axhline(y=0, color='k')
    deflection_plot.axvline(x=0, color='k')
    deflection_plot.grid(True, which='both')"""


    plt.subplots_adjust(bottom=0.1,  
                    top=0.9, 
                    wspace=0.4, 
                    hspace=0.4)

    simple_analysis_plots.pyplot(fig)
    

######################### What-If Analysis ###################################
elif analysis_type == "What-If Analysis":
    what_if_container = st.container()
    what_if_container.header("What-If Analysis")

    what_if_analysis_type = what_if_container.radio(label = 'Which aspect you want to Analyse?', options = ['Support Effect', 'Loading Effect'], horizontal=True)

    if 'what_if_analysis_type' not in st.session_state:
        st.session_state.what_if_analysis_type = what_if_analysis_type

    

    if what_if_analysis_type == "Support Effect":
        ################ Support Effect #########


        #### Loading Form
        col1, col2, col3 = what_if_container.columns([1,1,1])
        pt_load_inp_form = col1.form("simple_loadings_form_pt")
        point_load = pt_load_inp_form.slider("Point Magnitude (kN)", 0.0, 25.0, 10.0, step=1.0)
        point_load_loc = pt_load_inp_form.slider("Point Load Location (m)", 0.0, beam_length, beam_length/2, step=0.1)  
        pt_load_inp_form.form_submit_button("Apply Point Load")


        ##### UDL Form #########
        udl_load_inp_form = col2.form("simple_loadings_form_udl")
        udl_load = udl_load_inp_form.slider("UDL Magnitude (kN/m)", 0.0, 20.0, 10.0, step=1.0)

        
        _lst = []
        for i in range(0, int(beam_length+1)):
            _lst.append(str(i))
        udl_strt_loc, udl_end_loc = udl_load_inp_form.select_slider("label", options=_lst, value=(_lst[0], _lst[-1]))
        ## start and end location is a string - later convert it to float in order to use
        
        udl_load_inp_form.form_submit_button("Apply UDL")

        ##### Moment Load Form ########
        moment_load_inp_form = col3.form("simple_loadings_form_moment")
        moment_load = moment_load_inp_form.slider("Moment Magnitude (kN/m)", -20.0, 20.0, 0.0, step=1.0)
        moment_load_loc = moment_load_inp_form.slider("Moment Load Location (m)", 0.0, beam_length, beam_length/2, step=0.1)
        moment_load_inp_form.form_submit_button("Apply Moment Load")
    
        #----------------------------------------------------------------------#
        referene_column, interactive_column = what_if_container.columns([2,2])
        
        simple_support_effect_column = referene_column.subheader("Support Effect")
        reference_beam, reference_rxn_symbs = simply_supported_beam(beam_length, beam_E, beam_I)
        _pt_load = apply_point_load(reference_beam, point_load, point_load_loc)
        _moment_load = apply_moment_load(reference_beam, moment_load, moment_load_loc)
        _udl_load = apply_udl(reference_beam, udl_load, float(udl_strt_loc), float(udl_end_loc))

        ##### beam Visualisation
        simple_analysis_beam_viz = referene_column.container()
        simple_analysis_beam_viz.image(beam_viz(reference_beam, "Simply Supported Beam", reference_rxn_symbs))

        #### Solving for reaction loads
        rxn_loads = solve_for_rxns(reference_beam ,reference_rxn_symbs)
    

        reference_ss_analysis_rxn_loads = referene_column.container()
        #reference_ss_analysis_rxn_loads.write(rxn_loads)

        #### Plotting SFD, BMD and Deflections charts
        reference_analysis_plots = referene_column.container()
        shear_eqn = reference_beam.shear_force()
        bm_eqn = reference_beam.bending_moment()
        #slp_eqn = simple_beam.slope()
        #defl_eqn = simple_beam.deflection()
        
        "Shear Equation:"
        shear_eqn
        " "
        "Bending Moment Equation:"
        bm_eqn
        "Deflection Equation"
        #defl_eqn


        reference_fig, (shear_plot, bm_plot, deflection_plot) = plt.subplots(3, 1)
        ax_x = np.arange(0, reference_beam.length, 0.01)
        x_lst = []
        for i in ax_x:
            x_lst.append(i)

            
        shear_vals = []
        bm_vals = []
        defl_val = []
        x = create_sympy_symbol("x")
        for i in x_lst:
            shear_vals.append(float(shear_eqn.subs(x, i)))
            bm_vals.append(float(bm_eqn.subs(x, i)))
            #defl_val.append(float(defl_eqn.subs(x, i)))
        
        shear_plot.plot(x_lst, shear_vals, 'b')
        
        shear_max = max(shear_vals)
        shear_max_pos = shear_vals.index(shear_max)
        shear_min = min(shear_vals)
        #shear_zero = shear_vals.index(0.0)
        shear_min_pos = shear_vals.index(shear_min)
        shear_plot.annotate(str(shear_max)+" kN", xy=(shear_max_pos, shear_max), xytext=(shear_max_pos-1, shear_max+6), xycoords='data')
        
        shear_plot.spines.right.set_visible(False)
        shear_plot.spines.top.set_visible(False)

        shear_plot.set_ylabel('V (kN)')
        shear_plot.set_title("Shear Plot")
        shear_plot.x_lim = 0
        shear_plot.axhline(y=0, color='k')
        shear_plot.axvline(x=0, color='k')
        shear_plot.axvline(x=beam_length, color='k')
        
        
        shear_plot.grid(True, which='both')


        bm_plot.plot(x_lst, bm_vals, 'g')
        #bm_plot.set_xlabel('x')
        bm_plot.invert_yaxis()
        bm_plot.set_ylabel('M (kN-m)')
        bm_plot.set_title("Bending Moment Plot")
        bm_plot.axhline(y=0, color='k')
        bm_plot.axvline(x=0, color='k')
        bm_plot.axvline(x=beam_length, color='k')
        bm_plot.grid(True, which='both')

        plt.subplots_adjust(bottom=0.1,  
                    top=0.9, 
                    wspace=0.4, 
                    hspace=0.4)

        #if ''
        
        reference_analysis_plots.pyplot(reference_fig)
    
        support_interactive_column = interactive_column.subheader("Beam Analysis")
        support_effect = interactive_column.radio(label = 'Type of Support', options = ['Simply Supported', 'Fixed', 'Proped Cantilever', 'Cantilever'], horizontal=True)

        if 'support_effect' not in st.session_state:
            interactive_column.session_state.beam_type = support_effect

        # instanciate the beam
        if support_effect == "Simply Supported":
            support_effect_beam, reacn_symbs = simply_supported_beam(beam_length, beam_E, beam_I)
        elif support_effect =="Fixed":
            support_effect_beam ,reacn_symbs = fixed_beam(beam_length, beam_E, beam_I)
        elif support_effect =="Proped Cantilever":
            support_effect_beam, reacn_symbs = proped_cantilever_beam(beam_length, beam_E, beam_I)
        elif support_effect =="Cantilever":
            support_effect_beam, reacn_symbs = cantilever_beam(beam_length, beam_E, beam_I)
    
        
        
        _pt_load = apply_point_load(support_effect_beam, point_load, point_load_loc)
        _moment_load = apply_moment_load(support_effect_beam, moment_load, moment_load_loc)
        _udl_load = apply_udl(support_effect_beam, udl_load, float(udl_strt_loc), float(udl_end_loc))

        ##### beam Visualisation
        simple_support_effect_viz = interactive_column.container()
        simple_support_effect_viz.image(beam_viz(support_effect_beam, support_effect+" Beam", reacn_symbs))

        #### Solving for reaction loads
        rxn_loads = solve_for_rxns(support_effect_beam ,reacn_symbs)
    

        support_effect_analysis_rxn_loads = interactive_column.container()
        #support_effect_analysis_rxn_loads.write(rxn_loads)

        #### Plotting SFD, BMD and Deflections charts
        support_effect_plots = interactive_column.container()
        shear_eqn = support_effect_beam.shear_force()
        bm_eqn = support_effect_beam.bending_moment()
        #slp_eqn = simple_beam.slope()
        #defl_eqn = simple_beam.deflection()
        
        "Shear Equation:"
        shear_eqn
        " "
        "Bending Moment Equation:"
        bm_eqn
        "Deflection Equation"
        #defl_eqn


        support_effect_fig, (shear_plot, bm_plot, deflection_plot) = plt.subplots(3, 1)
        ax_x = np.arange(0, support_effect_beam.length, 0.01)
        x_lst = []
        for i in ax_x:
            x_lst.append(i)

            
        shear_vals = []
        bm_vals = []
        defl_val = []
        x = create_sympy_symbol("x")
        for i in x_lst:
            shear_vals.append(float(shear_eqn.subs(x, i)))
            bm_vals.append(float(bm_eqn.subs(x, i)))
            #defl_val.append(float(defl_eqn.subs(x, i)))
        
        shear_plot.plot(x_lst, shear_vals, 'b')
        
        shear_max = max(shear_vals)
        shear_max_pos = shear_vals.index(shear_max)
        shear_min = min(shear_vals)
        #shear_zero = shear_vals.index(0.0)
        shear_min_pos = shear_vals.index(shear_min)
        shear_plot.annotate(str(shear_max)+" kN", xy=(shear_max_pos, shear_max), xytext=(shear_max_pos-1, shear_max+6), xycoords='data')
        
        shear_plot.spines.right.set_visible(False)
        shear_plot.spines.top.set_visible(False)

        shear_plot.set_ylabel('V (kN)')
        shear_plot.set_title("Shear Plot")
        shear_plot.x_lim = 0
        shear_plot.axhline(y=0, color='k')
        shear_plot.axvline(x=0, color='k')
        shear_plot.axvline(x=beam_length, color='k')
        
        
        shear_plot.grid(True, which='both')


        bm_plot.plot(x_lst, bm_vals, 'g')
        #bm_plot.set_xlabel('x')
        bm_plot.invert_yaxis()
        bm_plot.set_ylabel('M (kN-m)')
        bm_plot.set_title("Bending Moment Plot")
        bm_plot.axhline(y=0, color='k')
        bm_plot.axvline(x=0, color='k')
        bm_plot.axvline(x=beam_length, color='k')
        bm_plot.grid(True, which='both')

        plt.subplots_adjust(bottom=0.1,  
                    top=0.9, 
                    wspace=0.4, 
                    hspace=0.4)

        support_effect_plots.pyplot(support_effect_fig)

    elif what_if_analysis_type == "Loading Effect":
        ################ Support Effect #########
        referene_column, interactive_column = what_if_container.columns([2,1])
        simple_loading_effect_column = referene_column.subheader("Loading Effect")

        loading_interactive_column = interactive_column.subheader("Beam Analysis")
