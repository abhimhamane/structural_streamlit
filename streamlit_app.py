import streamlit as st

st.title("Structural Analysis - Learning Tool")
st.write("--------")
info_content, info_marg_right = st.columns([3,1])
beam_info = info_content.container()
beam_info.header("Beam")

beam_info.markdown("""
    A beam is a structural element that primarily resists loads applied laterally to the beam's axis (an element 
    designed to carry primarily axial load would be a strut or column). 
    
    Its mode of deflection is primarily by bending. The loads applied to the beam result in reaction forces at the beam's support 
    points. The total effect of all the forces acting on the beam is to produce shear forces and bending moments within the beams, 
    that in turn induce internal stresses, strains and deflections of the beam. 
    
    Beams are characterized by their manner of support, profile (shape of cross-section), equilibrium conditions, length, and their material.
    
""")



















beam_info.write("Work in Progress....")




