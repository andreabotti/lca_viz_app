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





##### ##### LOAD CACHED DATA
# Initialize df_raw in session state if it doesn't exist
if 'df_raw' not in st.session_state:
    st.session_state['df_raw'] = pd.DataFrame()  # Or your default DataFrame
    st.warning('Please upload data to proceed')


# Now you can safely access st.session_state['df_raw']
df_raw = st.session_state['df_raw']



##### ##### NAMES
op_cat__col_name = '.OP_cat'
col_L1, col_L2, col_L3 = '.L1', '.L2', '.L3'







##### ##### MANIPULATE DATA
df = rename_headers__oclca(df_raw, op_cat__col_name=op_cat__col_name)


# Regular expression pattern to match columns starting with two digits and '__'
pattern = r'^\d{2}__'
matched_columns = list( df.filter(regex=pattern).columns )
matched_columns.append(op_cat__col_name)
matched_columns.append('.OP_comment')



with st.expander("Filtered DataFrame"):

    col1, col2 = st.columns([3,1])

    # Column selector
    all_columns = sorted( df.columns.tolist() )
    default_columns = matched_columns
    selected_columns = col1.multiselect(label="Select columns to keep", options=all_columns, default=default_columns)

    # st.divider()




    ##### ##### MANIPULATE DATA
    # Display DataFrame based on selection
    if selected_columns:

        filtered_df = df[selected_columns]

        df = filtered_df
        df = df.reindex(sorted(df.columns), axis=1)
        df = df[df['03__quantity'] >0 ]
        df[col_L1], df[col_L2], df[col_L3] = zip(*df[op_cat__col_name].apply(parse_levels))
        df = df.reindex(sorted(df.columns), axis=1)
        df = df.sort_values(by=[op_cat__col_name, '01__phase']).reset_index(drop=True)


        # Filtering by '01__phase'
        if '01__phase' in df.columns:
            unique_phases = df['01__phase'].unique()
            selected_phases = col2.multiselect('Select a phase to filter by', options=unique_phases, default=['A1-A3','A4', 'A5'])

            # Filter and display the DataFrame
            if selected_phases:
                filtered_df = df[df['01__phase'].isin(selected_phases)]
                st.dataframe(filtered_df)

            else:
                st.write("Select one or more phases to filter the data.")


        
            # # Optional: Download link for filtered DataFrame
            # @st.cache_data()
            # def convert_df_to_csv(df):
            #     return df.to_csv().encode('utf-8')

            # csv = convert_df_to_csv(filtered_df)
            # st.download_button(
            #     label="Download CSV",
            #     data=csv,
            #     file_name='filtered_data.csv',
            #     mime='text/csv',
            # )




# Filter the DataFrame
df_qty = df[df['01__phase'] == 'A5']

# Group by '05__mat_cat' and 'op_cat_col', and aggregate
grouped_df = df_qty.groupby(['05__mat_cat']).agg(
    total_quantity=('03__quantity', 'sum'),
    FU=('04__FU', 'first')  # Assuming FU is consistent within each group
)
grouped_df__cat = df_qty.groupby(['05__mat_cat', op_cat__col_name]).agg(
    total_quantity=('03__quantity', 'sum'),
    FU=('04__FU', 'first')  # Assuming FU is consistent within each group
)

grouped_df = grouped_df.sort_values(by=['05__mat_cat'])
grouped_df__cat = grouped_df__cat.sort_values(by=[op_cat__col_name, '05__mat_cat'])



# Calculate sums
sums_df = df_qty.groupby(['05__mat_cat', op_cat__col_name]).agg(
    total_quantity=('03__quantity', 'sum'),
    FU=('04__FU', 'first')  # Assuming FU is consistent within each group
).reset_index()

# Append sums to the filtered data
sums_df['02__oclca_item'] = '.total'
sums_df['.OP_comment'] = '-'
sums_df['03__quantity'] = sums_df['total_quantity']

# Concatenate the sums with the filtered data
result_df = pd.concat([df_qty, sums_df], ignore_index=True)

# Sort the DataFrame by '05__mat_cat' and '02__oclca_item'
result_df = result_df.sort_values(by=[op_cat__col_name, '05__mat_cat', '02__oclca_item'])
df_qty = df_qty.sort_values(by=[op_cat__col_name, '05__mat_cat', '02__oclca_item'])

result_df.drop([col_L1, col_L2, col_L3, '01__phase'], axis=1, inplace=True)
df_qty.drop([col_L1, col_L2, col_L3, op_cat__col_name, '01__phase'], axis=1, inplace=True)
df_qty = df_qty.sort_values(by=['.OP_comment', '05__mat_cat'])

df_qty.set_index('05__mat_cat',inplace=True)




st.divider()

col1, col2 = st.columns([1,2])
col1.markdown('###### Total Quantities - by material')
col2.markdown('###### Total Quantities - by material and OP Category')

col1.write(grouped_df)
col2.write(grouped_df__cat)

with st.expander('All Material Quantities'):
    st.write(df_qty)





df1 = df

# st.write(df1)


st.session_state['df1'] = df1
st.session_state['op_cat__col_name'] = op_cat__col_name
st.session_state['col_L1, col_L2, col_L3'] = col_L1, col_L2, col_L3
