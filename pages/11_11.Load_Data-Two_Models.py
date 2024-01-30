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
)
op_cat__list.dropna(inplace=True)








col_1, col_2, space = st.columns([3,3,1])

# File uploader
uploaded_file_1 = col_1.file_uploader("Choose first CSV file", type='csv')
uploaded_file_2 = col_2.file_uploader("Choose second CSV file", type='csv')



if uploaded_file_1 is not None:

    # Read and display the CSV file
    df1_raw = pd.read_csv(
        uploaded_file_1,
        header=2,
        )

    col_1.divider()
    col_1.dataframe(df1_raw)

else:
    col_1.warning('Please upload data to proceed')




if uploaded_file_2 is not None:

    # Read and display the CSV file
    df2_raw = pd.read_csv(
        uploaded_file_2,
        header=2,
        )

    col_2.divider()
    col_2.dataframe(df2_raw)
else:
    col_2.warning('Please upload data to proceed')




st.session_state['df1_raw'] = df1_raw
st.session_state['df2_raw'] = df2_raw

st.session_state['op_cat__list'] = op_cat__list
# st.session_state['op_cat__col_name'] = op_cat__col_name



st.success('Data has been uplaoded and stored successfully')

