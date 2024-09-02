# IMPORT LIBRARIES
from fn__libraries import *
pd.options.display.max_rows = 40       # Maximum number of rows to display
pd.options.display.expand_frame_repr = True  # Do not allow DataFrames to be printed over multiple lines




####################################################################################
# PAGE CONFIGURATION
from fn__page_header import create_page_header
create_page_header()

custom_horiz_line()

####################################################################################
##### ##### SET NAMES
DATA_PATH = 'data/'
op_cat__list__filepath = DATA_PATH + 'OP_cat.csv'

# Import OP_cat data
op_cat__list__filepath = DATA_PATH + 'OP_cat.csv'
op_cat__col_name = '.OP_cat'
col_L1_op, col_L2_op, col_L3_op = '.L1', '.L2', '.L3'
op_cat__list = pd.read_csv(op_cat__list__filepath)
op_cat__list.dropna(inplace=True)

# Import RICS_cat data
rics_cat__list__filepath = DATA_PATH + 'RICS_cat.csv'  # Make sure this file exists with the correct structure
rics_cat__col_name = '05__rics_cat'
col_L1_rics, col_L2_rics, col_L3_rics = 'RICS_L1', 'RICS_L2', 'RICS_L3'
rics_cat__list = pd.read_csv(rics_cat__list__filepath)
rics_cat__list.dropna(inplace=True)

cat__col_name = rics_cat__col_name
col_L1, col_L2, col_L3 = col_L1_rics, col_L2_rics, col_L3_rics




####################################################################################
# Sidebar for file upload and format selection
with st.sidebar:
    st.markdown('#### Upload data - Choose data format')

    upload_data_format = st.radio('Choose input data format: _csv_ or _xlsx_:', options=['xlsx', 'csv'])

    if upload_data_format == 'csv':
        uploaded_csv = st.file_uploader("Choose a file in **CSV** format", type='csv')
        if uploaded_csv is not None:
            df_raw = pd.read_csv(uploaded_csv, header=2)
            st.session_state['df_raw'] = df_raw  # Store in session state
    elif upload_data_format == 'xlsx':
        uploaded_xls = st.file_uploader("Choose a file in **XLSX** format", type=['xlsx'])
        if uploaded_xls is not None:
            df_raw = pd.read_excel(uploaded_xls, header=2, engine='openpyxl')
            st.session_state['df_raw'] = df_raw  # Store in session state

# Retrieve the DataFrame from session state if it exists
if 'df_raw' in st.session_state:
    df_raw = st.session_state['df_raw']
else:
    df_raw = None
    st.warning('Please upload data to proceed')







####################################################################################
if df_raw is not None:
    with st.expander("Uploaded DataFrame"):
        st.dataframe(df_raw)

    # Rename columns to ensure we are working with the correct names
    df = df_raw.rename(
        columns=lambda x: x.strip(),  # Strip any leading/trailing whitespace from column names
    ).rename(
        columns={
            'Section': '01__phase',
            'Resource': '02__oclca_item',
            'User input': '03__quantity',
            'Unit': '04__FU',
            'RICS category': '05__rics_cat',
            'Resource type': '06__mat_cat',
            'Comment': '07_comment',
            'Global warming kg CO₂e': '10__GWP',
            'TOTAL kg CO2e kg CO₂e': '10__GWP',
        },
    )


    # # Display the columns to ensure correct names
    # st.write("Available columns in the DataFrame:", df.columns.tolist())

    # Check if the required columns are present in the DataFrame
    required_columns = ['03__quantity', '04__FU', '06__mat_cat', cat__col_name, '02__oclca_item']
    missing_columns = [col for col in required_columns if col not in df.columns]

    if missing_columns:
        st.error(f"Missing columns in the uploaded data: {missing_columns}")
    else:
        pattern = r'^\d{2}__'
        matched_columns = list(df.filter(regex=pattern).columns)

        with st.expander("Filtered DataFrame"):
            col1, col2 = st.columns([3, 1])

            all_columns = sorted(df.columns.tolist())
            default_columns = matched_columns
            selected_columns = col1.multiselect("Select columns to keep", options=all_columns, default=default_columns)

            if selected_columns:
                filtered_df = df[selected_columns]

                df = filtered_df
                df = df.reindex(sorted(df.columns), axis=1)
                df = df[df['03__quantity'] > 0]

                df[col_L1], df[col_L2], df[col_L3] = zip(*df[cat__col_name].apply(parse_levels))
                df = df.reindex(sorted(df.columns), axis=1)
                df = df.sort_values(by=[cat__col_name, '01__phase']).reset_index(drop=True)

                if '01__phase' in df.columns:
                    unique_phases = df['01__phase'].unique()
                    selected_phases = col2.multiselect('Select a phase to filter by', options=unique_phases, default=['A1-A3', 'A4', 'A5'])

                    if selected_phases:
                        filtered_df = df[df['01__phase'].isin(selected_phases)]
                        st.markdown('###### Filtered Dataframe')
                        st.dataframe(filtered_df)
                    else:
                        st.write("Select one or more phases to filter the data.")

        df_qty = df[df['01__phase'] == 'A5']



        # Group by operations using the first FU value and sorting by total_quantity
        grouped_df = df_qty.groupby(['06__mat_cat']).agg(
            total_quantity=('03__quantity', 'sum'),
            FU=('04__FU', 'first')  # Take the first value from the "04__FU" column
        ).sort_values(by='total_quantity', ascending=False)  # Sort by total_quantity

        grouped_df__mat_cat = df_qty.groupby(['06__mat_cat', cat__col_name]).agg(
            total_quantity=('03__quantity', 'sum'),
            FU=('04__FU', 'first')  # Take the first value from the "04__FU" column
        ).sort_values(by='total_quantity', ascending=False)  # Sort by total_quantity

        grouped_df__oclca_item = df_qty.groupby(['02__oclca_item']).agg(
            total_quantity=('03__quantity', 'sum'),
            FU=('04__FU', 'first')  # Take the first value from the "04__FU" column
        ).sort_values(by='total_quantity', ascending=False)  # Sort by total_quantity

        grouped_df__gwp = df_qty.groupby(['02__oclca_item']).agg(
            total_carbon_kgCO2e=('10__GWP', 'sum'),
        ).sort_values(by='total_carbon_kgCO2e', ascending=False)  # Sort by total_quantity

        # Calculate the percentage of the total
        total_carbon = grouped_df__gwp['total_carbon_kgCO2e'].sum()
        grouped_df__gwp['%_of_total'] = ( (grouped_df__gwp['total_carbon_kgCO2e'] / total_carbon) * 100 ).round(2)



        ####################################################################################
        custom_horiz_line()

        col_table_1, col_table_2 = st.columns([1,1])
        col_table_1.markdown('###### Material Quantities - by OneClickLCA data item (sortable and searchable)')
        col_table_1.dataframe(grouped_df__oclca_item)

        col_table_2.markdown('###### Carbon Impact (GWP) - by OneClickLCA data item (sortable and searchable)')
        col_table_2.dataframe(grouped_df__gwp)

        # Style the DataFrame with custom CSS for all cell types
        styled_df = grouped_df__oclca_item.style.set_table_styles(
            [
                {
                    'selector': 'th',  # Style for table headers
                    'props': [
                        ('font-size', '14px'),         # Font size
                        ('font-weight', 'normal'),       # Bold font
                        # ('color', 'white'),            # Text color
                        # ('background-color', '#4CAF50'), # Header background color
                        ('text-align', 'left'),      # Center-align text
                        ('padding', '10px')            # Padding around text
                    ]
                },
                {
                    'selector': 'td',  # Style for table data cells
                    'props': [
                        ('font-size', '14px'),         # Font size
                        ('font-weight', 'normal'),     # Normal font weight
                        # ('font-style', 'italic'),      # Italic font
                        ('text-align', 'left'),        # Left-align text
                        # ('padding', '8px'),            # Padding around text
                        # ('border', '1px solid #ddd')   # Border for each cell
                    ]
                },
                {
                    'selector': '.row_heading, .blank',  # Style for index and blank cells
                    'props': [
                        ('font-size', '14px'),         # Font size
                        ('font-weight', 'normal'),       # Bold font
                        ('text-align', 'left'),       # Right-align text
                        ('padding', '0px'),            # Padding around text
                        # ('background-color', '#f2f2f2') # Background color for index cells
                    ]
                }
            ]
        )

        # Render the styled DataFrame as HTML in Streamlit
        # st.markdown(styled_df.to_html(), unsafe_allow_html=True)




        ####################################################################################
        df1 = df
        st.session_state['df1'] = df1

        st.session_state['op_cat__col_name'] = op_cat__col_name
        st.session_state['rics_cat__col_name'] = rics_cat__col_name
        st.session_state['col_L1, col_L2, col_L3'] = col_L1, col_L2, col_L3

        st.session_state['col_L1_op', 'col_L2_op', 'col_L3_op'] = col_L1_op, col_L2_op, col_L3_op
        st.session_state['col_L1_rics', 'col_L2_rics', 'col_L3_rics'] = col_L1_rics, col_L2_rics, col_L3_rics


        st.session_state['op_cat__list'] = op_cat__list
        st.session_state['rics_cat__list'] = rics_cat__list


else:
    st.warning('Please upload data to proceed - use the sidebar widget')
