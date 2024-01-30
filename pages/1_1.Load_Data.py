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



col_form_1,col_form_2, col_data_format, col_data_upload = st.columns([2,2,3,8])


# Input fields
col_form_1.markdown('##### Floor areas')
gia = col_form_1.number_input('Gross Internal Area (GIA)', min_value=0.0, format='%.1f')
tfa = col_form_1.number_input('Treated Floor Area (TFA)', min_value=0.0, format='%.1f')

col_form_1.markdown('<br>', unsafe_allow_html=True)

col_form_1.markdown('##### Facade areas')
fsa = col_form_1.number_input('Facade Surface Area (FSA)', min_value=0.0, format='%.1f')
fff = col_form_1.number_input('Facade Form Factor (FFF)', min_value=0.0, format='%.2f')


upload_data_format = col_data_format.radio('Choose input data format: _csv_ or _xls_:', options=['csv', 'xls'])

with col_data_upload:
    if upload_data_format == 'csv':
        uploaded_csv = st.file_uploader("Choose a file in **CSV** format", type='csv')

        if uploaded_csv is not None:
            df_raw = pd.read_csv(
                uploaded_csv,
                header=2,
                )
# 
    elif upload_data_format == 'xls':
        uploaded_xls = st.file_uploader("Choose a file in **XLS** format", type='xls')

        if uploaded_xls is not None:
            df_raw = pd.read_excel(
                uploaded_xls,
                header=2,
                # sheet_name='Sheet1',
                )

    else:
        st.warning('Please upload data to proceed')


st.divider()
try:
    st.dataframe(df_raw)
except:
    st.warning('Please upload data to proceed')




try:
    st.session_state['df_raw'] = df_raw
    st.session_state['op_cat__list'] = op_cat__list
    st.session_state['op_cat__col_name'] = op_cat__col_name

except:
    st.warning('Please upload data to proceed')

