# IMPORT LIBRARIES
from fn__libraries import *


####################################################################################
from fn__page_header import create_page_header
create_page_header()

custom_horiz_line()




####################################################################################
col_form_1, spacing, col_form_2, spacing, col_image = st.columns([6, 1, 6, 3, 15])

# Input fields
# Initialize session state variables if they don't already exist
if 'GIA' not in st.session_state:
    st.session_state['GIA'] = 1  # Default value
if 'TFA' not in st.session_state:
    st.session_state['TFA'] = 1  # Default value
if 'FSA' not in st.session_state:
    st.session_state['FSA'] = 1  # Default value
if 'FFF' not in st.session_state:
    st.session_state['FFF'] = 0.0  # Default value (float)

# Update session state variables with current inputs
col_form_1.markdown('###### Floor areas (m2)')

with col_form_1:
    GIA = st.number_input('Gross Internal Area - GIA', min_value=0, step=1, value=st.session_state['GIA'], format="%d")
    st.metric(label='GIA', value=f"{GIA} m2")
    
    custom_horiz_line()

    TFA = st.number_input('Treated Floor Area - TFA', min_value=0, step=1, value=st.session_state['TFA'], format="%d")
    st.metric(label='TFA', value=f"{TFA} m2")


col_form_2.markdown('###### Facade areas (m2)')
with col_form_2:
    FSA = st.number_input('Facade Surface Area - FSA', min_value=1, step=1, value=st.session_state['FSA'], format="%d")
    st.metric(label='FSA', value=f"{FSA} m2")

    custom_horiz_line()

    st.latex(r"FFF = \frac{FSA \, (m^2)}{GIA \, (m^2)}")
    FFF = FSA / GIA

    FFF_col1, spacing, FFF_col2 = st.columns([8,1,5])
    FFF_col1.metric(label='Facade Form Factor - FFF', value=f"{FFF:.3f}")
    # FFF_col2.metric(label='FFF %', value=f"{100*FFF:.1f}%")



col_image.image('./img/CWCT__GIA_FSA_sketch.png')
col_image.caption('Source: \"How to calculate the embodied carbon of facades: A methodology\"')
# col_image.caption('https://www.cwct.co.uk/pages/embodied-carbon-methodology-for-facades')




####################################################################################
GIA = st.session_state['GIA']
TFA = st.session_state['TFA']
FSA = st.session_state['FSA']
FFF = st.session_state['GIA']