# IMPORT LIBRARIES
from fn__libraries import *

####################################################################################
# PAGE CONFIGURATION
from fn__page_header import create_page_header
create_page_header()

custom_horiz_line()



####################################################################################
##### ##### LOAD CACHED DATA
# Initialize df_raw in session state if it doesn't exist
if 'df1' not in st.session_state:
    st.session_state['df1'] = pd.DataFrame()  # Or your default DataFrame
    st.warning('Please upload data to proceed')

# Initialize GIA, TFA, FFF, FSA with default values if not present in session state
if 'GIA' not in st.session_state:
    st.session_state['GIA'] = 0.0  # Default value
if 'TFA' not in st.session_state:
    st.session_state['TFA'] = 0.0  # Default value
if 'FFF' not in st.session_state:
    st.session_state['FFF'] = 0.0  # Default value
if 'FSA' not in st.session_state:
    st.session_state['FSA'] = 0.0  # Default value

# Access data from session state
df1 = st.session_state['df1']


# Define op_cat__col_name before it's used
if 'op_cat__col_name' not in st.session_state:
    st.session_state['op_cat__col_name'] = 'op_cat__col_name'  # Replace with the actual column name
op_cat__col_name = st.session_state['op_cat__col_name']

if 'rics_cat__col_name' not in st.session_state:
    st.session_state['rics_cat__col_name'] = 'rics_cat__col_name'  # Replace with the actual column name
rics_cat__col_name = st.session_state['rics_cat__col_name']
cat__col_name = op_cat__col_name


# col_L1, col_L2, col_L3 = st.session_state['col_L1, col_L2, col_L3']
col_L1_op, col_L2_op, col_L3_op = st.session_state['col_L1_op', 'col_L2_op', 'col_L3_op']
col_L1_rics, col_L2_rics, col_L3_rics = st.session_state['col_L1_rics', 'col_L2_rics', 'col_L3_rics']

op_cat__list = st.session_state['op_cat__list']
rics_cat__list = st.session_state['rics_cat__list']


GIA = st.session_state['GIA']
TFA = st.session_state['TFA']
FFF = st.session_state['FFF']
FSA = st.session_state['FSA']




####################################################################################
# Let the user choose the categorization type
with st.sidebar:
    custom_horiz_line()

cat_type = st.sidebar.radio('Select categorization type:', ['RICS_cat', 'OP_cat'])

if cat_type == 'OP_cat':
    cat__col_name = op_cat__col_name
    col_L1, col_L2, col_L3 = col_L1_op, col_L2_op, col_L3_op
elif cat_type == 'RICS_cat':
    cat__col_name = rics_cat__col_name
    col_L1, col_L2, col_L3 = col_L1_rics, col_L2_rics, col_L3_rics





##### ##### MANIPULATE DATA

# Example of grouping by levels
grouped_level_1 = df1.groupby(col_L1)
grouped_level_2 = df1.groupby(col_L2)
grouped_level_3 = df1.groupby(col_L3)


# Streamlit sidebar for phase selection
df = df1
if '01__phase' in df.columns:
    unique_phases = df['01__phase'].unique()
    selected_phases = st.sidebar.multiselect('Select a phase to filter by', options=unique_phases, default=unique_phases[0])

    # Filter the DataFrame based on the selected phases
    df_filtered = df[df['01__phase'].isin(selected_phases)]

df = df_filtered

# Apply the function to create new columns for each level
df[col_L1], df[col_L2], df[col_L3] = zip(*df[cat__col_name].apply(parse_levels))

# Calculate total GWP
total_gwp = df['10__GWP'].sum()

# Grouping and summing GWP for each level
df_l1 = df.groupby(col_L1)['10__GWP'].sum().reset_index()
df_l2 = df.groupby([col_L1, col_L2])['10__GWP'].sum().reset_index()
df_l3 = df.groupby([col_L1, col_L2, col_L3])['10__GWP'].sum().reset_index()

df_l1['cat__level'] = df_l1[col_L1].apply(lambda x: f'{x}')
df_l2['cat__level'] = df_l2.apply(lambda x: f'{x[col_L1]}.{x[col_L2]}', axis=1)
df_l3['cat__level'] = df_l3.apply(lambda x: f'{x[col_L1]}.{x[col_L2]}.{x[col_L3]}', axis=1)



rics_cat__list.columns = rics_cat__list.columns.str.replace('RICS_cat_name', cat__col_name)


# Create a dictionary for mapping from op_cat__list
if cat_type == 'OP_cat':
    mapping_dict = pd.Series(op_cat__list[cat__col_name].values, index=op_cat__list['OP_level']).to_dict()

elif cat_type == 'RICS_cat':
    mapping_dict = pd.Series(rics_cat__list[cat__col_name].values, index=rics_cat__list['RICS_level']).to_dict()


# Perform the mapping for each DataFrame
df_l1['cat__col_name'] = df_l1['cat__level'].map(mapping_dict)
df_l2['cat__col_name'] = df_l2['cat__level'].map(mapping_dict)
df_l3['cat__col_name'] = df_l3['cat__level'].map(mapping_dict)






####################################################################################
# Let the user choose a color for each 'L1' category
l1_categories = df_l1[col_L1].unique()
color_palette = ['#FFFFFF', '#395F78', '#81C07A', '#F3A8B5', '#FBB789', '#8686C1']
default_color = '#808080'  # Default color for non-integer categories



main_col_1, main_col_2 = st.columns([5,6])

with main_col_2:
    with st.expander('Choose marker colours'):
        # st.markdown('###### Choose marker colours')
        color_cols = st.columns(6)

        l1_colors = []
        for col, cat in zip(color_cols, l1_categories):
            try:
                cat_index = int(cat)
                p_col = col.color_picker(f'Cat {cat}', color_palette[cat_index])
            except ValueError:
                p_col = col.color_picker(f'Cat {cat}', default_color)  # Use default color for non-integer categories
            l1_colors.append(p_col)

l1_colors = {cat: p_col for cat, p_col in zip(l1_categories, l1_colors)}
l2_colors = {cat: adjust_hsl(l1_colors[cat.split('.')[0]], lightness_change=0.05, hue_change=0) for cat in df_l2['cat__level']}
l3_colors = {cat: adjust_hsl(l1_colors[cat.split('.')[0]], lightness_change=0.05, hue_change=0) for cat in df_l3['cat__level']}




# Pie chart dimensions
pie_chart_width = 300
pie_chart_height = 450

# Create two sets of labels
l3_short_labels = df_l3['cat__level']
l3_full_labels = df_l3['cat__level'] + ' ' + df_l3['cat__col_name']
hover_text = l3_full_labels


####################################################################################
# Add donut traces for each level
fig_pie_l1 = go.Figure(data=[go.Pie(
    labels=df_l1['cat__level'] + ' ' + df_l1['cat__col_name'],
    values=df_l1['10__GWP'],
    marker=dict(
        line=dict(color='#ffffff', width=1),
        colors=[l1_colors[cat] for cat in df_l1['cat__level']]),
    hole=0.55, visible=True,
    sort=False,
)])

fig_pie_l2 = go.Figure(data=[go.Pie(
    labels=df_l2['cat__level'] + ' ' + df_l2['cat__col_name'],
    values=df_l2['10__GWP'],
    marker=dict(
        line=dict(color='#ffffff', width=1),
        colors=[l2_colors[cat] for cat in df_l2['cat__level']]),
    hole=0.55, visible=True,
    sort=False,
)])

fig_pie_l3 = go.Figure(data=[go.Pie(
    labels=df_l3['cat__level'],
    values=df_l3['10__GWP'],
    marker=dict(
        line=dict(color='#ffffff', width=1),
        colors=[l1_colors[cat] for cat in df_l3[col_L1]]),
    text=hover_text,
    hole=0.55, visible=True,
    sort=False,
)])

# Update layout for consistent legend position
fig_pie_l1.update_layout(
    legend=dict(
        orientation="h",
        yanchor="bottom", y=-0.5,
        xanchor="center", x=0.5,
    ),
)
fig_pie_l2.update_layout(
    legend=dict(
        orientation="h",
        yanchor="bottom", y=-1,
        xanchor="center", x=0.5,
    ),
)

# Add buttons for control
for fig in [fig_pie_l1, fig_pie_l2, fig_pie_l3]:
    fig.update_layout(
        width=pie_chart_width, height=pie_chart_height,
        margin=dict(l=10, r=10, t=0, b=100),
    )

# Group by 'L1' and calculate cumulative '10__GWP'
df_l1_cum = df_l1.groupby(col_L1)['10__GWP'].cumsum().reset_index()

# Create a cumulative bar chart for df_l1
fig_bar_l1 = go.Figure(
    data=[go.Bar(
        y=df_l1[col_L1],
        x=df_l1['10__GWP'],
        orientation='h',
        marker=dict(
            line=dict(color='#ffffff', width=1),
            color=[l1_colors[cat] for cat in df_l1['cat__level']]),
    )]
)
fig_bar_l2 = go.Figure(
    data=[go.Bar(
        y=df_l2[col_L1],
        x=df_l2['10__GWP'],
        orientation='h',
        marker=dict(
            line=dict(color='#ffffff', width=2),
            color=[l2_colors[cat] for cat in df_l2['cat__level']]),
        name='L1',
        text=df_l2['cat__level'],
        textposition='inside',
    )]
)
fig_bar_l3 = go.Figure(
    data=[go.Bar(
        y=df_l3[col_L1],
        x=df_l3['10__GWP'],
        orientation='h',
        marker=dict(
            line=dict(color='#ffffff', width=2),
            color=[l3_colors[cat] for cat in df_l3['cat__level']]),
        name='L1',
        text=df_l3['cat__level'],
        textposition='inside',
    )]
)

bar_pie_chart_height = 400
# Update layout for stacked barmode
fig_bar_l1.update_layout(
    barmode='stack',
    height=bar_pie_chart_height,
)
fig_bar_l2.update_layout(
    barmode='stack',
    height=bar_pie_chart_height,
)
fig_bar_l3.update_layout(
    barmode='stack',
    height=bar_pie_chart_height,
)

tables = []
for table in [df_l1, df_l2, df_l3]:
    for c in [col_L1, col_L2, col_L3]:
        try:
            table.drop([c], axis=1, inplace=True)
        except:
            pass
    table.set_index(['cat__level'], inplace=True)
    # table = percent_format_table_viz(df=table, gwp_col='10__GWP', cat_col = cat__col_name)
    tables.append(table)

total_gwp_1 = round(df_l1['10__GWP'].sum(), 0)
total_gwp_2 = round(df_l2['10__GWP'].sum(), 0)
total_gwp_3 = round(df_l3['10__GWP'].sum(), 0)

display_phases = ', '.join(sorted([ph for ph in selected_phases]))
markdown_level = "<h6 style='text-align: center;'>Phases {}</h6>".format(display_phases)
markdown_gwp = "<h5 style='text-align: center;'>GWP = {} kgCO2e</h5>".format("{:,.0f}".format(total_gwp_3))

EC_total = total_gwp_3
EC_unit_area = total_gwp_3 / GIA





####################################################################################
with main_col_1:
    col_metric_01, col_metric_02 = st.columns([1,1])


col_metric_01.markdown( 'Embodied Carbon | {}'.format(display_phases) )
col_metric_01.markdown( '#### {} kgCO2e'.format("{:,.0f}".format(EC_total)) )

col_metric_02.markdown( 'Embodied Carbon Intensity | {}'.format(display_phases) )
# col_metric_02.markdown( '#### {} kgCO2e/m2GIA'.format("{:,.1f}".format(EC_unit_area)) )
col_metric_02.markdown(
    "<h4>{} kgCO2e / m<sub style='font-size:.6em;'>2,GIA</sub></h4>".format("{:,.1f}".format(EC_unit_area)),
    unsafe_allow_html=True,
)


st.write('\n')
st.write('\n')

# custom_horiz_line()



####################################################################################
tab_pie_charts, tab_bar_charts, tab_tables, tab_ml_pie_chart = st.tabs(['Pie Charts', 'Bar Charts', 'Tables',  'Nested Pie Chart (WIP)',])

with tab_pie_charts:
    col_output_1, space, col_output_2, space, col_output_3 = st.columns([8, 1, 12, 1, 12])

    with col_output_1:
        st.markdown("<h6 style='text-align: center;'>Level 1</h6>", unsafe_allow_html=True)
        st.plotly_chart(fig_pie_l1, use_container_width=True)

    with col_output_2:
        st.markdown("<h6 style='text-align: center;'>Level 2</h6>", unsafe_allow_html=True)
        st.plotly_chart(fig_pie_l2, use_container_width=True)

    with col_output_3:
        st.markdown("<h6 style='text-align: center;'>Level 3</h6>", unsafe_allow_html=True)
        st.plotly_chart(fig_pie_l3, use_container_width=True)

with tab_bar_charts:
    col_output_1, space, col_output_2, space, col_output_3 = st.columns([8, 1, 12, 1, 12])

    with col_output_1:
        st.markdown("<h6 style='text-align: center;'>Level 1</h6>", unsafe_allow_html=True)
        st.markdown(markdown_level, unsafe_allow_html=True)
        st.markdown(markdown_gwp, unsafe_allow_html=True)
        st.plotly_chart(fig_bar_l1, use_container_width=True)

    with col_output_2:
        st.markdown("<h6 style='text-align: center;'>Level 2</h6>", unsafe_allow_html=True)
        st.markdown(markdown_level, unsafe_allow_html=True)
        st.markdown(markdown_gwp, unsafe_allow_html=True)
        st.plotly_chart(fig_bar_l2, use_container_width=True)

    with col_output_3:
        st.markdown("<h6 style='text-align: center;'>Level 3</h6>", unsafe_allow_html=True)
        st.markdown(markdown_level, unsafe_allow_html=True)
        st.markdown(markdown_gwp, unsafe_allow_html=True)
        st.plotly_chart(fig_bar_l3, use_container_width=True)

with tab_tables:
    col_output_1, space, col_output_2, space, col_output_3 = st.columns([9, 1, 12, 1, 12])

    with col_output_1:
        st.markdown("<h6 style='text-align: center;'>Level 1</h6>", unsafe_allow_html=True)
        st.markdown(markdown_level, unsafe_allow_html=True)
        st.markdown(markdown_gwp, unsafe_allow_html=True)
        st.dataframe(tables[0], use_container_width=True)

    with col_output_2:
        st.markdown("<h6 style='text-align: center;'>Level 2</h6>", unsafe_allow_html=True)
        st.markdown(markdown_level, unsafe_allow_html=True)
        st.markdown(markdown_gwp, unsafe_allow_html=True)
        st.dataframe(tables[1], use_container_width=True)

    with col_output_3:
        st.markdown("<h6 style='text-align: center;'>Level 3</h6>", unsafe_allow_html=True)
        st.markdown(markdown_level, unsafe_allow_html=True)
        st.markdown(markdown_gwp, unsafe_allow_html=True)
        st.dataframe(tables[2], height=850, use_container_width=True)

with tab_ml_pie_chart:
    spacing, multilevel_chart_col, spacing = st.columns([6, 10, 6])

    plt_chart = multilevel_donut_chart(df, col_L1, col_L2, col_L3, cat__col_name, gwp_col='10__GWP')
    multilevel_chart_col.pyplot(fig=plt_chart, use_container_width=True)
