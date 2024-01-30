import pandas as pd, numpy as np
import os, subprocess, base64, requests
from datetime import datetime, timedelta

import plotly.express as px
import plotly.graph_objects as go
import altair as alt
import colorsys

import streamlit as st
from streamlit_super_slider import st_slider
from streamlit_option_menu import option_menu

# from streamlit_pdf import st_pdf
from st_aggrid import AgGrid, GridOptionsBuilder, GridUpdateMode











# Step 1: Register your app to get client_id and client_secret

# Step 2: Implement OAuth2
client_id = 'c0e0e22b-461a-40ad-ac46-c25791227ca6'
client_secret = 'your_client_secret'
redirect_uri = 'http://localhost:8000/'  # As set in Azure

# Define scope and OAuth endpoints
scope = ['https://graph.microsoft.com/.default']
token_url = 'https://login.microsoftonline.com/common/oauth2/v2.0/token'

# Create OAuth session
oauth = OAuth2Session(client_id, redirect_uri=redirect_uri, scope=scope)

# Get authorization URL
authorization_url, state = oauth.authorization_url(token_url)
print('Please go to %s and authorize access.' % authorization_url)
authorization_response = input('Enter the full callback URL: ')

# Fetch the access token
token = oauth.fetch_token(token_url, authorization_response=authorization_response, 
                          client_secret=client_secret)

# Step 3: Access OneDrive/SharePoint
onedrive_api_url = 'https://graph.microsoft.com/v1.0/me/drive/root/children'
response = requests.get(onedrive_api_url, headers={'Authorization': f'Bearer {token["access_token"]}'})

# Handle the response
# ...





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
    'Comment'           :   '.OP_comment',
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
