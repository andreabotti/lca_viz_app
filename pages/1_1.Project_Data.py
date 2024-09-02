# IMPORT LIBRARIES
from fn__libraries import *


####################################################################################
from fn__page_header import create_page_header
create_page_header()

custom_horiz_line()


####################################################################################




col_form_1, spacing, col_form_2, spacing, col_data_format, spacing, col_data_upload, spacing = st.columns([12, 1, 12, 6, 12, 1, 28, 6])



# Input fields
# Initialize session state variables if they don't already exist
if 'GIA' not in st.session_state:
    st.session_state['GIA'] = 0.0  # Default value
if 'TFA' not in st.session_state:
    st.session_state['TFA'] = 0.0  # Default value
if 'FSA' not in st.session_state:
    st.session_state['FSA'] = 0.0  # Default value
if 'FFF' not in st.session_state:
    st.session_state['FFF'] = 0.0  # Default value

# Update session state variables with current inputs
col_form_1.markdown('###### Floor areas')

with col_form_1:
    st.session_state['GIA'] = st.number_input('GIA', min_value=0.0, step=0.1, format="%.2f", value=st.session_state['GIA'])
    st.session_state['TFA'] = st.number_input('TFA', min_value=0.0, step=0.1, format="%.2f", value=st.session_state['TFA'])

col_form_2.markdown('###### Facade areas')
with col_form_2:
    st.session_state['FSA'] = st.number_input('FSA', min_value=0.0, step=0.1, format="%.2f", value=st.session_state['FSA'])
    st.session_state['FFF'] = st.number_input('FFF', min_value=0.0, step=0.1, format="%.2f", value=st.session_state['FFF'])

# Display the inputted values
st.write(f"GIA: {st.session_state['GIA']}, TFA: {st.session_state['TFA']}, FSA: {st.session_state['FSA']}, FFF: {st.session_state['FFF']}")

