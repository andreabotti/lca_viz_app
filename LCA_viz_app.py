# IMPORT LIBRARIES
from fn__libraries import *


####################################################################################
from fn__page_header import create_page_header
create_page_header()



####################################################################################





# Define a function to navigate to a page
def navigate_to_page(page_name):
    st.session_state.current_page = page_name
    st.experimental_rerun()
    st.session_state.runpage = page_name





AppPath_Local       = 'https://lca-viz.streamlit.app/'
AppPath_Streamlit   = 'http://localhost:8501/'
AppPath = AppPath_Local


##### ##### SET NAMES
st.markdown('### How to use the app:')


col_single, col_comp, space = st.columns([4,4,3])


with col_single:
    st.markdown('---')
    st.markdown('##### For explorations of a single LCA model')

    st.markdown('##### Step 1')
    st.markdown('Open the Load Data page, and choose to either: \
                <br> - upload a **csv** file \
                <br> - provide a URL for a csv file hosted on the cloud (.e.g OneDrive or Dropbox)', unsafe_allow_html=True)

    st.markdown('')
    st.markdown('##### Step 2')
    st.markdown('Visit "Clean Input" page and choose whether to filter the data by life cycle phases.', unsafe_allow_html=True)

    st.markdown('')
    st.markdown('##### Step 3')
    st.markdown('Visit the "Output - GWP" page and visualise charts and table for the uploaded data.', unsafe_allow_html=True)



with col_comp:
    st.markdown('---')
    st.markdown('##### For comparative explorations of two LCA models')

    st.markdown('##### Step 11')
    st.markdown('Open the Load Data page, and choose to either: \
                <br> - upload a **csv** file \
                <br> - provide a URL for a csv file hosted on the cloud (.e.g OneDrive or Dropbox)', unsafe_allow_html=True)

    # Initialize the current page in session state
    # if st.button('Go to page Load Data - Two Models'):
    #     navigate_to_page('1_Load_Data')

    st.markdown('')
    st.markdown('##### Step 2')
    st.markdown('Visit "Clean Input" page and choose whether to filter the data by life cycle phases.', unsafe_allow_html=True)

    # if st.button('Go to page Clean Input - Two Models'):
    #     navigate_to_page( AppPath + 'Clean_Input')


    st.markdown('')
    st.markdown('##### Step 3')
    st.markdown('Visit the "Output - GWP" page and visualise charts and table for the uploaded data.', unsafe_allow_html=True)

