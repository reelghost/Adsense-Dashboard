import streamlit as st
import pandas as pd
from streamlit_extras.metric_cards import style_metric_cards
from streamlit_extras.streaming_write import write
from streamlit_extras.card import card
import adsense_util
import datetime
from googleapiclient import discovery
from googleapiclient.discovery import build

def convert_to_dataframe(data):
    headers = [header['name'] for header in data['headers']]
    rows = [[cell['value'] for cell in row['cells']] for row in data['rows']]
    df = pd.DataFrame(rows, columns=headers)
    return df

def main(start_date, end_date):
    """
    Get AdSense data
    """
    # Authenticate and construct service.
    credentials = adsense_util.get_adsense_credentials()
    with discovery.build('adsense', 'v2', credentials=credentials) as service:
        # Let the user pick account if more than one.
        account_id = adsense_util.get_account_id(service)
        
        # Retrieve payment balance.
        payment_request = service.accounts().payments().list(parent=account_id).execute()
        balance = payment_request['payments'][0]['amount']

        # Retrieve report.
        result = service.accounts().reports().generate(
            account=account_id, dateRange='CUSTOM',
            startDate_year=start_date.year, startDate_month=start_date.month, startDate_day=start_date.day,
            endDate_year=end_date.year, endDate_month=end_date.month, endDate_day=end_date.day,
            metrics=['PAGE_VIEWS', 'CLICKS', 'IMPRESSIONS', 'ESTIMATED_EARNINGS'],
            dimensions=['COUNTRY_NAME'],
            orderBy=['+COUNTRY_NAME']
        ).execute()
        
        return result, balance

# Streamlit app
st.set_page_config(page_title="Adsense", page_icon="🧨", layout="centered", menu_items=None)
st.header('So far, So :orange[good] :sunglasses:', divider='rainbow')

# Date input widgets in a flex container
today = datetime.date.today()
col1, col2 = st.columns(2)
with col1:
    start_date = st.date_input('Start Date', value=today)
with col2:
    end_date = st.date_input('End Date', value=today)

# Fetch data for the current date when the page loads
if 'initial_load' not in st.session_state:
    st.session_state.initial_load = True
    data, balance = main(start_date=today, end_date=today)
else:
    data, balance = None, None

def display_data(data, balance):
    if 'rows' in data:
        page_views_label = data['headers'][1]['name']
        page_views = data['totals']['cells'][1]['value']
        clicks_label = data['headers'][2]['name']
        clicks = data['totals']['cells'][2]['value']
        imp_label = data['headers'][3]['name']
        imp = data['totals']['cells'][3]['value']
        t_label = data['headers'][4]['name']
        t = data['totals']['cells'][4]['value']

        st.metric("TOTAL BALANCE", balance)
        card_1, card_2, card_3, card_4 = st.columns(4)
        card_1.metric(page_views_label, page_views)
        card_2.metric(clicks_label, clicks)
        card_3.metric(imp_label, imp, label_visibility='visible')
        card_4.metric(t_label, t, label_visibility='visible')

        style_metric_cards(border_left_color="orange", border_color='BLACK', background_color='rgba(237,235,230,0.7959558823529411)')
        st.markdown(
            f"""
            <style>
                div[data-testid="stMetric"],
                div[data-testid="metric-container"] {{
                    color:white;
                    background-image: linear-gradient(135deg, rgb(203, 17, 17) 0%, rgb(203, 17, 17) 23%,rgb(209, 42, 24) 23%, rgb(209, 42, 24) 37%,rgb(215, 67, 30) 37%, rgb(215, 67, 30) 40%,rgb(239, 168, 57) 40%, rgb(239, 168, 57) 41%,rgb(233, 143, 51) 41%, rgb(233, 143, 51) 44%,rgb(221, 92, 37) 44%, rgb(221, 92, 37) 54%,rgb(245, 193, 64) 54%, rgb(245, 193, 64) 66%,rgb(227, 118, 44) 66%, rgb(227, 118, 44) 100%);
                }}
            </style>
            """,
            unsafe_allow_html=True,
        )

        df = convert_to_dataframe(data)
        st.dataframe(df, use_container_width=True, hide_index=True)
    else:
        write("We do not have data for now ...")

# Display data fetched during initial load
if data:
    display_data(data, balance)

# Button to fetch data for selected dates
if st.button('Fetch Data'):
    with st.spinner('Fetching data...'):
        try:
            data, balance = main(start_date, end_date)
            display_data(data, balance)
        except Exception as e:
            st.error(f'Error fetching data: {e}')
