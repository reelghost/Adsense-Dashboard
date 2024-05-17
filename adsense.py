import streamlit as st
import pandas as pd
from streamlit_extras.metric_cards import style_metric_cards
from streamlit_extras.customize_running import center_running
from streamlit_extras.streaming_write import write
from streamlit_extras.card import card
import adsense_util
import base64
from googleapiclient import discovery
from googleapiclient.discovery import build

def convert_to_dataframe(data):
    headers = [header['name'] for header in data['headers']]
    rows = [[cell['value'] for cell in row['cells']] for row in data['rows']]
    df = pd.DataFrame(rows, columns=headers)
    return df


def main():
    """
    Get AdSense data
    """
    # Authenticate and construct service.
    credentials = adsense_util.get_adsense_credentials()
    with discovery.build('adsense', 'v2', credentials = credentials) as service:
        # Let the user pick account if more than one.
        account_id = adsense_util.get_account_id(service)
        
        # Retrieve report.
        result = service.accounts().reports().generate(
                account=account_id, dateRange='TODAY',
                metrics=['PAGE_VIEWS','CLICKS', 'TOTAL_IMPRESSIONS'],
                dimensions=['COUNTRY_NAME'],
                orderBy=['+COUNTRY_NAME']).execute()
        
        return result


# Streamlit app
st.header('So far, So :orange[good] :sunglasses:', divider='rainbow')


# Date input widgets in a flex container
col1, col2 = st.columns(2)


center_running()
data = main()

if 'rows' in data:
    page_views_label = data['headers'][1]['name']  
    page_views = data['totals']['cells'][1]['value']
    clicks_label = data['headers'][2]['name']  
    clicks = data['totals']['cells'][2]['value']
    imp_label = data['headers'][3]['name']  
    imp = data['totals']['cells'][3]['value']


    card_1, card_2, card_3 = st.columns(3)
    card_1.metric(page_views_label,page_views)
    card_2.metric(clicks_label,clicks)
    card_3.metric(imp_label,imp, label_visibility='visible')
    style_metric_cards(border_left_color="orange", border_color='BLACK', background_color='rgba(237,235,230,0.7959558823529411)')
    st.markdown(
            f"""
            <style>
                div[data-testid="stMetric"],
                div[data-testid="metric-container"] {{
                    color:white;
                    background-image: linear-gradient(135deg, rgb(203, 17, 17) 0%, rgb(203, 17, 17) 23%,rgb(209, 42, 24) 23%, rgb(209, 42, 24) 37%,rgb(215, 67, 30) 37%, rgb(215, 67, 30) 40%,rgb(239, 168, 57) 40%, rgb(239, 168, 57) 41%,rgb(233, 143, 51) 41%, rgb(233, 143, 51) 44%,rgb(221, 92, 37) 44%, rgb(221, 92, 37) 54%,rgb(245, 193, 64) 54%, rgb(245, 193, 64) 66%,rgb(227, 118, 44) 66%, rgb(227, 118, 44) 100%);
                }}
                div[data-testid="stMarkdownContainer"],p {{
                    
                    font-weight:bold;
                    font-size:50px;
                }}
            </style>
            """,
            unsafe_allow_html=True,
        )

    # Find the indices for each metric
    headers = data['headers']
    indices = {header['name']: i for i, header in enumerate(headers)}

         # Display the metrics by country
    for row in data['rows']:
        df = convert_to_dataframe(data)
    # filtered_df = dataframe_explorer(df, case=True)
    st.dataframe(df, use_container_width=True, hide_index=True)
else:
    write("We do not have data for now ...")

