# IMPORT LIBRARIES
from fn__libraries import *

def create_page_header():

    st.set_page_config(page_title="LCA Viz App",   page_icon=':mostly_sunny:', layout="wide")
    st.markdown(
        """<style>.block-container {padding-top: 1rem; padding-bottom: 0rem; padding-left: 2.5rem; padding-right: 2.5rem;}</style>""",
        unsafe_allow_html=True)


    ##### ##### TOP CONTAINER
    TopColA, TopColB = st.columns([6,3])
    with TopColA:
        st.markdown("# LCA Viz App")
        # st.markdown("#### Analisi di dati meteorologici ITAliani per facilitare l'Adattamento ai Cambiamenti Climatici")
        st.caption('Developed by AB.S.RD - https://absrd.xyz/')
