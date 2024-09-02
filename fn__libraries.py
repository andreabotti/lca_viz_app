import pandas as pd, numpy as np
import os, subprocess, base64, requests
from datetime import datetime, timedelta

import plotly.express as px
import plotly.graph_objects as go
import plotly.io as pio
import altair as alt
import colorsys
import matplotlib.pyplot as plt
import matplotlib as mpl
from matplotlib import rc

import streamlit as st
from streamlit_super_slider import st_slider
from streamlit_option_menu import option_menu

# from streamlit_pdf import st_pdf
from st_aggrid import AgGrid, GridOptionsBuilder, GridUpdateMode




# Set various display options for pandas DataFrames
pd.options.display.max_colwidth = 400  # Adjust this value for maximum column width
pd.options.display.max_rows = 40       # Maximum number of rows to display
pd.options.display.max_columns = None  # Display all columns
pd.options.display.precision = 2       # Set precision for decimal numbers
pd.options.display.float_format = '{:.2f}'.format  # Format for floating point numbers
pd.options.display.expand_frame_repr = True  # Do not allow DataFrames to be printed over multiple lines
pd.options.display.colheader_justify = 'center'  # Center-align column headers





def custom_horiz_line():
    # Inject custom CSS to reduce vertical spacing before and after the horizontal line
    st.markdown("""
        <style>
            .hr-line {
                margin-top: -5px;
                margin-bottom: 0px;
            }
        </style>
    """, unsafe_allow_html=True)
    # Adding the horizontal line with reduced vertical spacing
    st.markdown('<hr class="hr-line">', unsafe_allow_html=True)






def apply_categorization(df, category_type, cat__col_name, col_L1, col_L2, col_L3):
    """
    Apply the selected categorization to the DataFrame.
    """

    # Apply categorization to the DataFrame
    df[col_L1], df[col_L2], df[col_L3] = zip(*df[cat__col_name].apply(parse_levels))
    
    return df, {'col_L1': col_L1, 'col_L2': col_L2, 'col_L3': col_L3, 'cat_col_name': cat__col_name}



def parse_levels(s):
    # Check if 's' is a string
    if isinstance(s, str):
        parts = s.split('.')  # Split by dot
        # Return the first three parts or None if they don't exist
        return parts[0] if len(parts) > 0 else None, \
               parts[1] if len(parts) > 1 else None, \
               parts[2][0] if len(parts) > 2 else None
    else:
        # Return None for all levels if 's' is not a string
        return None, None, None




# Helper function to format the DataFrame
def percent_format_table_viz(df, gwp_col, cat_col):
    
    df[gwp_col] = pd.to_numeric(df[gwp_col]).round(0)
    total_gwp = df[gwp_col].sum()
    df['% of total'] = (df[gwp_col] / total_gwp * 100).round(1)
    df['% of total'] = df['% of total'].astype(str) + '%'
    
    df = df[[cat_col, gwp_col, '% of total']]

    return df




def compare_dataframes(df1, df2, name_df1, name_df2, merge_dir, merge_col, keep_cols, qty_col, gwp_col):
    """
    Compare two dataframes based on a key column and highlight differences in 'Quantity' and 'GWP'.
    :param df1: First DataFrame
    :param df2: Second DataFrame
    :param key_column: Column name on which to base the comparison
    :return: A DataFrame with the comparison results, including highlighted differences
    """

    df1 = df1[keep_cols]
    df2 = df2[keep_cols]

    # Merge the dataframes on the unique key
    if merge_dir == 'left':
        comparison_df = pd.merge(df1, df2, on=merge_col, how='inner', suffixes=(f'__{name_df1}', f'__{name_df2}'))
    if merge_dir == 'right':
        comparison_df = pd.merge(df2, df1, on=merge_col, how='inner', suffixes=(f'__{name_df2}', f'__{name_df1}'))


    comparison_df[f'{qty_col}__diff'] = comparison_df[f'{qty_col}__{name_df1}'] != comparison_df[f'{qty_col}__{name_df2}']
    comparison_df[f'{gwp_col}__diff'] = comparison_df[f'{gwp_col}__{name_df1}'] != comparison_df[f'{gwp_col}__{name_df2}']

    # comparison_df.drop([merge_col], axis=1, inplace=True)
    
    return comparison_df




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



def rename_headers__oclca(df):
    # df1 = df
    df.rename(columns={
    'Section'           :   '01__phase',   
    'Resource'          :   '02__oclca_item',
    'User input'        :   '03__quantity',   
    'Unit'              :   '04__FU',
    'RICS category'     :   '05__rics_cat',
    'Resource type'     :   '06__mat_cat',
    'Comment'           :   '07_comment',
    'Global warming kg CO₂e'    :   '10__GWP',
    'TOTAL kg CO2e kg CO₂e'     :   '10__GWP',
    }, inplace=True)

    return df




def rename_headers__oclca__OpenProject(df, op_cat__col_name):
    # df1 = df
    df.rename(columns={
    'Section'           :   '01__phase',   
    'Resource'          :   '02__oclca_item',
    'User input'        :   '03__quantity',   
    'Unit'              :   '04__FU',
    # 'Building Parts'    :   '07__levels_cat',
    'Resource type'     :   '05__mat_cat',
    'OP_cat'            :   op_cat__col_name,
    'Comment'           :   '.OP_comment',
    'Global warming kg CO₂e'        :   '10__GWP',
    'Ozone Depletion kg CFC11e'     :   '11__ODP',
    }, inplace=True)

    return df




def multilevel_donut_chart(df, col_L1, col_L2, col_L3, op_cat__col_name, gwp_col):

    # Group the data by '.L1', '.L2', '.L3', and '.OP_cat', then sum the '10__GWP' values
    grouped_gwp = df.groupby([col_L1, col_L2, col_L3,op_cat__col_name])[gwp_col].sum()

    # Reset index to work with the grouped data more easily
    grouped_gwp_reset = grouped_gwp.reset_index()

    # Recalculate counts to reflect the new grouping
    counts_gwp = grouped_gwp_reset.groupby([col_L1, col_L2, col_L3,op_cat__col_name])[gwp_col].sum()


    # Define primary colormaps (cycle if levels > 6)
    cmaps = np.resize(['Blues_r', 'Greens_r', 'Oranges_r', 'Purples_r', 'Reds_r', 'Greys_r'],
                    counts_gwp.index.get_level_values(0).size)


    # Define missing constants
    WEDGE_SIZE = 0.45
    LABEL_THRESHOLD = 50000



    fig, ax = plt.subplots(figsize=(12, 8))

    for level in range(3):  # We have three levels: .L1, .L2, .L3
        # Compute grouped sums up to current level, including .OP_cat for labeling purposes
        if level == 2:  # At the last level, include .OP_cat in the grouping
            wedges = counts_gwp.groupby(level=list(range(level + 2))).sum()
        else:
            wedges = counts_gwp.groupby(level=list(range(level + 1))).sum()

        # print(wedges)
        # Extract annotation labels
        if level == 2:  # Use .OP_cat as labels for the outermost layer
            labels = wedges.index.get_level_values(level + 1)
        else:
            labels = wedges.index.get_level_values(level)

        # Generate color shades per group
        index = [i for i in wedges.index.tolist()]  # Index is already standardized due to reset_index above
        g0 = pd.DataFrame(index).groupby(0)
        maps = g0.ngroup()
        shades = g0.cumcount() / g0.size().max()
        colors = [plt.get_cmap(cmaps[m])(s) for m, s in zip(maps, shades)]
        
        # Plot colorized/labeled donut layer
        ax.pie(x=wedges,
            radius=1 + (level * WEDGE_SIZE),
            colors=colors,
            labels=np.where(wedges >= LABEL_THRESHOLD, labels, ''),  # unlabel if under threshold
            rotatelabels=True,
            labeldistance=1.02 - 1.4 / (level + 3.5),  # put labels inside wedge instead of outside
            wedgeprops=dict(width=WEDGE_SIZE, linewidth=0, alpha=0.6),
            )

        # # Example: Setting font properties for labels
        # for label in labels:
        #     label.set_fontsize(12)
        #     label.set_fontname('Roboto')

        # # Plot colorized donut layer with adjusted labeling for small slices
        # wedges, texts = ax.pie(x=wedges,
        #                     radius=1 + (level * WEDGE_SIZE),
        #                     colors=colors,
        #                     labels=None,  # Handle labels separately to use callouts
        #                     startangle=90,
        #                     counterclock=False,
        #                     wedgeprops=dict(width=WEDGE_SIZE, linewidth=0, alpha=0.7))

        # # Add labels with callouts for small slices
        # for i, (wedge, label) in enumerate(zip(wedges, labels)):
        #     if small_wedges.iloc[i]:
        #         x, y = wedge.theta1, wedge.r
        #         ax.annotate(label, xy=(x, y), xytext=(1.5*np.sign(x), 1.2*y),
        #                     textcoords='polar', horizontalalignment='center',
        #                     arrowprops=dict(arrowstyle="->", color='black'))


    # ax.set_title('Hierarchical Donut Chart Grouped by .L1, .L2, .L3 and .OP_cat, Summed by 10__GWP')

    # plt.rcParams['font.size'] = 12
    # plt.rcParams['font.family'] = 'Roboto'
    # rc('text', usetex=True)

    return plt









# def multilevel_donut_chart(mapping_df)


# # Prepare a mapping dictionary from the mapping dataframe
# mapping_dict = pd.Series(mapping_df.OP_cat_name.values, index=mapping_df.OP_level).to_dict()

# # Function to apply mapping to labels
# def apply_mapping(label):
#     return mapping_dict.get(str(label), label)

# # Adjusting the plotting code with the specified enhancements
# fig, ax = plt.subplots(figsize=(12, 10))
# total_gwp = counts_gwp.sum()

# for level in range(3):  # We have three levels: .L1, .L2, .L3
#     if level == 2:  # At the last level, include .OP_cat in the grouping
#         wedges = counts_gwp.groupby(level=list(range(level + 2))).sum()
#     else:
#         wedges = counts_gwp.groupby(level=list(range(level + 1))).sum()

#     labels = [apply_mapping(label) if level < 2 else label for label in wedges.index.get_level_values(level)]
#     small_wedges = wedges < (total_gwp * 0.02)  # Identify small wedges
#     autopct = lambda pct: "{:.1f}%".format(pct) if pct >= 2 else ''

#     # Generate color shades per group
#     index = [i for i in wedges.index.tolist()]
#     g0 = pd.DataFrame(index).groupby(0)
#     maps = g0.ngroup()
#     shades = g0.cumcount() / g0.size().max()
#     colors = [plt.get_cmap(cmaps[m])(s) for m, s in zip(maps, shades)]
    
#     # Plot colorized donut layer with adjusted labeling for small slices
#     wedges, texts = ax.pie(x=wedges,
#                            radius=1 + (level * WEDGE_SIZE),
#                            colors=colors,
#                            labels=None,  # Handle labels separately to use callouts
#                            startangle=90,
#                            counterclock=False,
#                            wedgeprops=dict(width=WEDGE_SIZE, linewidth=0, alpha=0.7))

#     # Add labels with callouts for small slices
#     for i, (wedge, label) in enumerate(zip(wedges, labels)):
#         if small_wedges.iloc[i]:
#             x, y = wedge.theta1, wedge.r
#             ax.annotate(label, xy=(x, y), xytext=(1.5*np.sign(x), 1.2*y),
#                         textcoords='polar', horizontalalignment='center',
#                         arrowprops=dict(arrowstyle="->", color='black'))

# ax.set_title('Hierarchical Donut Chart with Enhanced Labeling and Custom Fonts')
# plt.show()
