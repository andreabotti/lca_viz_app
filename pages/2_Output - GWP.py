# IMPORT LIBRARIES
from fn__libraries import *







##### ##### PAGE CONFIG
st.set_page_config(page_title="LCA Viz App",   page_icon=':mostly_sunny:', layout="wide")
st.markdown(
    """<style>.block-container {padding-top: 0rem; padding-bottom: 0rem; padding-left: 2.5rem; padding-right: 2.5rem;}</style>""",
    unsafe_allow_html=True)


##### ##### TOP CONTAINER
TopColA, TopColB = st.columns([6,3])
with TopColA:
    st.markdown("# LCA Viz App")
    # st.markdown("#### Analisi di dati meteorologici ITAliani per facilitare l'Adattamento ai Cambiamenti Climatici")
    st.caption('Developed by AB.S.RD - https://absrd.xyz/')

st.divider()




##### ##### LOAD CACHED DATA
df1 = st.session_state['df1']
op_cat__col_name = st.session_state['op_cat__col_name']
op_cat__list = st.session_state['op_cat__list']
col_L1, col_L2, col_L3 = st.session_state['col_L1, col_L2, col_L3']



##### ##### MANIPULATE DATA

# Example of grouping by Level 1
grouped_level_1 = df1.groupby(col_L1)
grouped_level_2 = df1.groupby(col_L2)
grouped_level_3 = df1.groupby(col_L3)


df = df1


# Streamlit sidebar for phase selection
if '01__phase' in df.columns:
    unique_phases = df['01__phase'].unique()
    selected_phases = st.sidebar.multiselect('Select a phase to filter by', options=unique_phases, default=unique_phases[0])

    # Filter the DataFrame based on the selected phases
    df_filtered = df[df['01__phase'].isin(selected_phases)]

df = df_filtered

# Apply the function to create new columns for each level
df[col_L1], df[col_L2], df[col_L3] = zip(*df[op_cat__col_name].apply(parse_levels))

# Calculate total GWP
total_gwp = df['10__GWP'].sum()



# Example: Sum of '10__GWP' for each col_L1, col_L2, col_L3
df_l1 = df.groupby(col_L1)['10__GWP'].sum().reset_index()
df_l2 = df.groupby([col_L1, col_L2])['10__GWP'].sum().reset_index()
df_l3 = df.groupby([col_L1, col_L2, col_L3])['10__GWP'].sum().reset_index()

df_l1['OP_cat_level'] = df_l1[col_L1].apply(lambda x: f'{x}')
df_l2['OP_cat_level'] = df_l2.apply(lambda x: f'{x[col_L1]}.{x[col_L2]}', axis=1)
df_l3['OP_cat_level'] = df_l3.apply(lambda x: f'{x[col_L1]}.{x[col_L2]}.{x[col_L3]}', axis=1)


# Create a dictionary for mapping from op_cat__list
mapping_dict = pd.Series(op_cat__list['OP_cat_name'].values, index=op_cat__list['OP_level']).to_dict()



# Perform the mapping for each DataFrame
df_l1['OP_cat_name'] = df_l1['OP_cat_level'].map(mapping_dict)
df_l2['OP_cat_name'] = df_l2['OP_cat_level'].map(mapping_dict)
df_l3['OP_cat_name'] = df_l3['OP_cat_level'].map(mapping_dict)







# Let the user choose a color for each 'L1' category
l1_categories = df_l1[col_L1].unique()
color_palette = ['#FFFFFF', '#395F78', '#81C07A', '#F3A8B5',  '#FBB789', '#8686C1']
# #6898AF

with TopColB:
    # Introduce vertical spaces
    st.markdown('<div style="margin: 35px;"></div>', unsafe_allow_html=True) 

    with st.container():

        st.markdown('###### Scegli colore dei markers')
        color_cols = st.columns(7)

        l1_colors = []
        i=0
        for col, cat in zip(color_cols, l1_categories):
            p_col = col.color_picker(f'Cat {cat}', color_palette[int(cat)])
            l1_colors.append(p_col)
            i+=1




l1_colors = {cat: p_col for cat, p_col in zip(l1_categories, l1_colors)}
l2_colors = {cat: adjust_hsl(l1_colors[cat.split('.')[0]], lightness_change=0.05, hue_change=0) for cat in df_l2['OP_cat_level']}
l3_colors = {cat: adjust_hsl(l1_colors[cat.split('.')[1]], lightness_change=0.05, hue_change=0) for cat in df_l3['OP_cat_level']}




chart_width = 300
chart_height = 450


# Create two sets of labels
l3_short_labels = df_l3['OP_cat_level']
l3_full_labels  = df_l3['OP_cat_level'] + ' ' + df_l3['OP_cat_name']
hover_text = l3_full_labels


# Add donut traces for each level
fig_l1 = go.Figure(data=[go.Pie(
    labels=df_l1['OP_cat_level']+ ' ' + df_l1['OP_cat_name'],
    values=df_l1['10__GWP'],
    marker=dict(
        line=dict(color='#ffffff', width=1),
        colors=[l1_colors[cat] for cat in df_l1['OP_cat_level']]),
    hole=0.55, visible=True,
    )]
)

fig_l2 = go.Figure(data=[go.Pie(
    labels=df_l2['OP_cat_level'] + ' ' + df_l2['OP_cat_name'],
    values=df_l2['10__GWP'],
    marker=dict(
        line=dict(color='#ffffff', width=1),
        colors=[l2_colors[cat] for cat in df_l2['OP_cat_level']]),
    hole=0.55, visible=True,
    )]
)

fig_l3 = go.Figure(data=[go.Pie(
    labels=df_l3['OP_cat_level'],
    values=df_l3['10__GWP'],
    marker=dict(
        line=dict(color='#ffffff', width=1),
        colors=[l1_colors[cat] for cat in df_l3[col_L1]]),
    text=hover_text,
    hole=0.55, visible=True,
    )]
)

# Update layout for consistent legend position
# fig_l2.update_traces(textinfo='percent+label')
fig_l1.update_layout(
    legend=dict(
        orientation="h",
        yanchor="bottom", y=-0.5,
        xanchor="center", x=0.5,
        ),
)
fig_l2.update_layout(
    legend=dict(
        orientation="h",
        yanchor="bottom", y=-1,
        xanchor="center", x=0.5,
        ),
)


# Add buttons for control
for fig in [fig_l1, fig_l2, fig_l3]:
    fig.update_layout(
        width=chart_width, height=chart_height,
        margin=dict(l=10, r=10, t=0, b=100),
    )


col_output_1, space, col_output_2, space, col_output_3 = st.columns([8,1,12,1,12])

tables = []
for table in [df_l1, df_l2, df_l3]:
    
    for c in [col_L1, col_L2, col_L3]:
        try:
            print(c)
            table.drop([c], axis=1, inplace=True)
        except:
            ''
    table.set_index(['OP_cat_level'], inplace=True)
    table = percent_format_table_viz(df=table, gwp_col='10__GWP')


    tables.append(table)


display_phases = ', '.join( sorted( [ph for ph in selected_phases] ) )
markdown_title = "<h6 style='text-align: center;'>  GWP - Phases {} </h6>".format(display_phases)

with col_output_1:
    st.markdown( "<h5 style='text-align: center;'>Level 1</h5>", unsafe_allow_html=True )
    st.markdown(markdown_title, unsafe_allow_html=True)
    st.plotly_chart(fig_l1, use_container_width=True)
    st.dataframe(tables[0], use_container_width=True)

with col_output_2:
    st.markdown( "<h5 style='text-align: center;'>Level 2</h5>", unsafe_allow_html=True )
    st.markdown(markdown_title, unsafe_allow_html=True)
    st.plotly_chart(fig_l2, use_container_width=True)
    st.dataframe(tables[1], use_container_width=True)

with col_output_3:
    st.markdown( "<h5 style='text-align: center;'>Level 2</h5>", unsafe_allow_html=True )
    st.markdown(markdown_title, unsafe_allow_html=True)
    st.dataframe(tables[2], height=850, use_container_width=True)
