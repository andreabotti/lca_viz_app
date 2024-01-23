# IMPORT LIBRARIES
from fn__libraries import *







##### ##### PAGE CONFIG
st.set_page_config(page_title="LCA Viz App",   page_icon=':mostly_sunny:', layout="wide")
st.markdown(
    """<style>.block-container {padding-top: 0rem; padding-bottom: 0rem; padding-left: 2.5rem; padding-right: 2.5rem;}</style>""",
    unsafe_allow_html=True)


##### ##### TOP CONTAINER
top_col1, top_col2 = st.columns([6,1])
with top_col1:
    st.markdown("# LCA Viz App")
    # st.markdown("#### Analisi di dati meteorologici ITAliani per facilitare l'Adattamento ai Cambiamenti Climatici")
    st.caption('Developed by AB.S.RD - https://absrd.xyz/')

st.divider()





##### ##### SET NAMES
DATA_PATH = 'data/'
op_cat__list__filepath = DATA_PATH + 'OP_cat.csv'

op_cat__col_name = '.OP_cat'
col_L1, col_L2, col_L3 = '.L1', '.L2', '.L3'

op_cat__list = pd.read_csv(
    op_cat__list__filepath,
    # header=None,
)
op_cat__list.dropna(inplace=True)
# st.dataframe(op_cat__list)


# File uploader
uploaded_file = st.file_uploader("Choose a CSV file", type='csv')




if uploaded_file is not None:
    # Read and display the CSV file
    df_raw = pd.read_csv(
        uploaded_file,
        header=2,
        )

    st.divider()
    st.dataframe(df_raw)


    # with st.expander('Display column headers'):
    #     st.write("Column headers in your file:")
    #     st.write(df.columns.tolist())



st.session_state['df_raw'] = df_raw
st.session_state['op_cat__list'] = op_cat__list
