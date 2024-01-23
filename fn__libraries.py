import pandas as pd, numpy as np
import os
import subprocess
from datetime import datetime, timedelta
import plotly.express as px
import plotly.graph_objects as go
import altair as alt
import colorsys

import streamlit as st
from streamlit_super_slider import st_slider
# from streamlit_pdf import st_pdf
import base64
from st_aggrid import AgGrid, GridOptionsBuilder, GridUpdateMode






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
def percent_format_table_viz(df, gwp_col):
    
    df[gwp_col] = pd.to_numeric(df[gwp_col]).round(0)
    total_gwp = df[gwp_col].sum()
    df['% of total'] = (df[gwp_col] / total_gwp * 100).round(1)
    df['% of total'] = df['% of total'].astype(str) + '%'
    
    df = df[['OP_cat_name', gwp_col, '% of total']]

    return df




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




def rename_headers__oclca(df, op_cat__col_name):
    # df1 = df
    df.rename(columns={
    'Section'           :   '01__phase',   
    'Resource'          :   '02__oclca_item',
    'User input'        :   '03__quantity',   
    'Unit'              :   '04__FU',
    # 'Building Parts'    :   '07__levels_cat',
    'Resource type'     :   '05__mat_cat',
    'OP_cat'            :   op_cat__col_name,
    'Global warming kg CO₂e'        :   '10__GWP',
    'Ozone Depletion kg CFC11e'     :   '11__ODP',
    }, inplace=True)

    return df

# 5:'Biogenic carbon storage kg CO₂e bio'
# 7:'Acidification kg SO₂e'
# 8:'Eutrophication kg PO₄e'
# 9:'Formation of ozone of lower atmosphere kg Ethenee'
# 10:'Abiotic depletion potential (ADP-elements) for non fossil resources kg Sbe'
# 11:'Abiotic depletion potential (ADP-fossil fuels) for fossil resources MJ'
# 12:'Use of renewable primary energy resources as raw materials MJ'
# 13:'Total use of primary energy ex. raw materials MJ'
# 14:'Total use of renewable primary energy MJ'
# 15:'Total use of non renewable primary energy MJ'
# 16:'Use of net fresh water m³'
# 17:'Energy kWh'
# 18:'Water consumption m³'
# 19:'Distance traveled km'
# 20:'Fuel consumption litres'
# 21:'Mass of raw materials kg'
# 22:'Question'
# 23:'Thickness mm'
# 24:'Comment'
# 25:'Building Parts'
# 28:'Construction'
# 29:'Resource type'
# 30:'Datasource'
# 31:'Name'
# 32:'Transformation process'
# 33:'uniClass'
# 34:'csiMasterformat'
# 35:'class'
# 36:'Imported label'
