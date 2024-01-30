# IMPORT LIBRARIES
from fn__libraries import *







##### ##### PAGE CONFIG
st.set_page_config(page_title="LCA Viz App",   page_icon=':mostly_sunny:', layout="wide")
st.markdown(
    """<style>.block-container {padding-top: 0rem; padding-bottom: 0rem; padding-left: 2.5rem; padding-right: 2.5rem;}</style>""",
    unsafe_allow_html=True)


##### ##### TOP CONTAINER
top_col_columns, top_col_phases = st.columns([6,1])
with top_col_columns:
    st.markdown("# LCA Viz App")
    # st.markdown("#### Analisi di dati meteorologici ITAliani per facilitare l'Adattamento ai Cambiamenti Climatici")
    st.caption('Developed by AB.S.RD - https://absrd.xyz/')

st.divider()





##### ##### LOAD CACHED DATA
# Initialize df_raw in session state if it doesn't exist
if 'df1_raw' not in st.session_state:
    st.session_state['df1_raw'] = pd.DataFrame()  # Or your default DataFrame
    st.warning('Please upload data to proceed')

# Initialize df_raw in session state if it doesn't exist
if 'df2_raw' not in st.session_state:
    st.session_state['df2_raw'] = pd.DataFrame()  # Or your default DataFrame
    st.warning('Please upload data to proceed')

df1_raw = st.session_state['df1_raw']
df2_raw = st.session_state['df2_raw']


##### ##### NAMES
op_cat__col_name = '.OP_cat'
op_comment__col_name = '.OP_comment'

col_L1, col_L2, col_L3 = '.L1', '.L2', '.L3'




##### ##### MANIPULATE DATA
df1 = rename_headers__oclca(df1_raw, op_cat__col_name=op_cat__col_name)
df2 = rename_headers__oclca(df2_raw, op_cat__col_name=op_cat__col_name)




# Regular expression pattern to match columns starting with two digits and '__'
pattern = r'^\d{2}__'
matched_columns = list( df1.filter(regex=pattern).columns )
matched_columns.append(op_cat__col_name)
matched_columns.append(op_comment__col_name)


col_columns, col_phases = st.columns([3,1])
st.divider()
col_df1, col_df2 = st.columns([1,1])



# Column selector
all_columns = sorted( df1.columns.tolist() )
default_columns = matched_columns
selected_columns = col_columns.multiselect(label="Select columns to keep", options=all_columns, default=default_columns)




# Display DataFrame based on selection
if selected_columns:

    df = df1[selected_columns]
    df = df.reindex(sorted(df.columns), axis=1)
    df = df[df['03__quantity'] >0 ]
    # df[col_L1], df[col_L2], df[col_L3] = zip(*df[op_cat__col_name].apply(parse_levels))
    df = df.reindex(sorted(df.columns), axis=1)
    df = df.sort_values(by=[op_cat__col_name, '01__phase']).reset_index(drop=True)
    df1 = df

    df = df2[selected_columns]
    df = df.reindex(sorted(df.columns), axis=1)
    df = df[df['03__quantity'] >0 ]
    # df[col_L1], df[col_L2], df[col_L3] = zip(*df[op_cat__col_name].apply(parse_levels))
    df = df.reindex(sorted(df.columns), axis=1)
    df = df.sort_values(by=[op_cat__col_name, '01__phase']).reset_index(drop=True)
    df2 = df


    # Filtering by '01__phase'.
    if '01__phase' in df.columns:
        unique_phases = df1['01__phase'].unique()
        selected_phases = col_phases.multiselect('Select a phase to filter by', options=unique_phases, default=['A1-A3'])

        # Filter and display the DataFrame
        if selected_phases:

            filtered_df1 = df1[df1['01__phase'].isin(selected_phases)]
            filtered_df2 = df2[df2['01__phase'].isin(selected_phases)]

            col_df1.write("Filtered DataFrame:")
            col_df1.dataframe(filtered_df1, height=300)

            col_df2.write("Filtered DataFrame:")
            col_df2.dataframe(filtered_df2, height=300)

        else:
            col_df1.write("Select one or more phases to filter the data.")

df1 = filtered_df1
df2 = filtered_df2





keep_cols = [
    # '.OP_cat',
    '.OP_comment',
    '02__oclca_item',
    '03__quantity',
    '10__GWP',
    'merge_key',
    ]  # Replace with your column names


# Define logic for merging df, by creating a unique key in both dataframes
# df1['merge_key'] = df1['.OP_cat_name'].astype(str) + '_' + df1['02__oclca_item'].astype(str)
# df2['merge_key'] = df2['.OP_cat_name'].astype(str) + '_' + df2['02__oclca_item'].astype(str)
df1['merge_key'] = df1['.OP_cat'].astype(str) + ' | ' + df1['05__mat_cat'].astype(str)
df2['merge_key'] = df2['.OP_cat'].astype(str) + ' | ' + df2['05__mat_cat'].astype(str)

name_df1 = 'MOLO_041'
name_df2 = 'MOLO_Riba3'

df_compo = compare_dataframes(
    df1=df1, df2=df2,
    merge_dir='left',
    merge_col='merge_key',
    qty_col = '03__quantity',
    gwp_col = '10__GWP',
    keep_cols= keep_cols,
    name_df1 = 'MOLO_041', name_df2 = 'MOLO_Riba3',
    )

table_compo = df_compo[[
    'merge_key',
    f'.OP_comment__{name_df1}',      f'03__quantity__{name_df1}',
    f'.OP_comment__{name_df2}',      f'03__quantity__{name_df2}',
    f'02__oclca_item__{name_df1}',   f'02__oclca_item__{name_df2}',
    # '03__quantity__diff',
    # f'10__GWP__{name_df2}', f'10__GWP__{name_df2}',
#     # '10__GWP__diff',
]]
        

# table_compo = df_compo    
# st.dataframe(df_compo)
st.dataframe(table_compo, hide_index=True, column_config={'02__oclca_item': None})

print(df_compo.columns)


st.session_state['df1'] = df1

st.session_state['op_cat__col_name'] = op_cat__col_name
st.session_state['col_L1, col_L2, col_L3'] = col_L1, col_L2, col_L3
