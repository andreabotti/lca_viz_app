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







def adjust_hsl(color, lightness_change=0.1, saturation_change=0):
    # Function to adjust the HSL values
    # Convert hex color to HSL
    h, l, s = colorsys.rgb_to_hls(*[x/255.0 for x in bytes.fromhex(color[1:])])
    # Adjust lightness and saturation
    l = min(1, max(0, l + lightness_change))
    s = min(1, max(0, s + saturation_change))
    # Convert back to hex
    new_color = '#{:02x}{:02x}{:02x}'.format(
        *[round(x * 255) for x in colorsys.hls_to_rgb(h, l, s)]
    )
    return new_color





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



def adjust_hsl(color, lightness_change, hue_change):
    # Convert hex color to HSL
    h, l, s = colorsys.rgb_to_hls(*[x/255.0 for x in bytes.fromhex(color[1:])])
    # Adjust lightness and hue
    l = min(1, max(0, l + lightness_change))
    h = (h + hue_change) % 1.0  # Ensure hue stays within [0, 1]
    # Convert back to hex
    new_color = '#{:02x}{:02x}{:02x}'.format(
        *[round(x * 255) for x in colorsys.hls_to_rgb(h, l, s)]
    )
    return new_color


l1_colors = {cat: p_col for cat, p_col in zip(l1_categories, l1_colors)}

# # Then, adjust the l2_colors and l3_colors generation:
l2_colors = {cat: adjust_hsl(l1_colors[cat.split('.')[1]], lightness_change=0.05, hue_change=0.05) for cat in df_l2['OP_cat_level']}
l3_colors = {cat: adjust_hsl(l1_colors[cat.split('.')[1]], lightness_change=0.05, hue_change=0.05) for cat in df_l3['OP_cat_level']}

# st.write(l2_colors)
# st.write(l3_colors)



# Create Plotly figure
fig = go.Figure()
chart_width = 600
chart_height = 500


# Create two sets of labels
l3_short_labels = df_l3['OP_cat_level']
l3_full_labels  = df_l3['OP_cat_level'] + ' ' + df_l3['OP_cat_name']

# Create custom hover text that includes both full and short labels
# hover_text = [f'{full} ({short})' for full, short in zip(l3_full_labels, l3_short_labels)]
hover_text = l3_full_labels


# Add donut traces for each level
fig.add_trace(go.Pie(
    labels=df_l1['OP_cat_level']+ ' ' + df_l1['OP_cat_name'],
    values=df_l1['10__GWP'],
    marker=dict(colors=[l1_colors[cat] for cat in df_l1['OP_cat_level']]),
    hole=0.55, visible=True,
    )
)
fig.add_trace(go.Pie(
    labels=df_l2['OP_cat_level'] + ' ' + df_l2['OP_cat_name'],
    values=df_l2['10__GWP'],
    marker=dict(colors=[l2_colors[cat] for cat in df_l2['OP_cat_level']]),
    hole=0.55, visible=False,
    )
)
fig.add_trace(go.Pie(
    labels=df_l3['OP_cat_level'],
    values=df_l3['10__GWP'],
    marker=dict(colors=[l1_colors[cat] for cat in df_l3[col_L1]]),
    text=hover_text,
    hole=0.55, visible=False,
    )
)

# Update layout for consistent legend position
fig.update_traces(textinfo='percent+label')
fig.update_layout(
    legend=dict(
        orientation="h",
        # yanchor="bottom", y=0.9,
        xanchor="right", x=1,
        ),
    uniformtext_minsize=12,
    uniformtext_mode='hide',
)




# Add buttons for control
fig.update_layout(
    width=chart_width,
    height=chart_height,
    updatemenus=[
        dict(
            type="buttons",
            direction="right",
            x=0.6,
            y=1.3,
            showactive=True,
            buttons=list([
                dict(label="L1",    method="update",    args=[{"visible": [True, False, False]}]),
                dict(label="L2",    method="update",    args=[{"visible": [False, True, False]}]),
                dict(label="L3",    method="update",    args=[{"visible": [False, False, True]}]),
            ]),
        )
    ])





col_output_1, col_output_2 = st.columns([2,3])


with col_output_1:
    with st.container():
        st.markdown('##### Data grouped by L1')
        st.dataframe(df_l1)

    with st.container():
        st.markdown('##### Data grouped by L2')
        st.dataframe(df_l2)

    with st.expander('Data grouped by L3'):
        st.dataframe(df_l3)


with col_output_2:
    st.plotly_chart(fig, use_container_width=True)



