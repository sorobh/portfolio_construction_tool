#!/usr/bin/env python
# coding: utf-8

# In[12]:


import pandas as pd
import numpy as np
from openbb import obb
import matplotlib.pyplot as plt
import streamlit as st


# In[3]:


# Streamlit configuration
st.title("Portfolio Construction Tool")
st.sidebar.header("Asset Selection")


# In[ ]:


# Main guidance
st.markdown("""
This app allows you to analyze the performance of different asset classes on attributes like correlation, daily returns and volatility.

### How to Use:
1. Select the assets you want in your portfolio from the sidebar.
2. Choose a start date for historical data analysis.
3. Click the **Analyze** button to view charts and metrics.

""")


# In[4]:


obb.account.login(pat="OBB_PAT")


# In[6]:


# Function to convert data to DataFrame
def convert_to_dataframe(data):
    return data.to_dataframe()

# Function to fetch data based on selected assets and date
def fetch_data(asset, start_date):
    if asset == 'Gold':
        data = obb.etf.historical("GLD", start_date=start_date)
    elif asset == 'US Stock':
        data = obb.index.price.historical("NASDX", provider="fmp", start_date=start_date)
    elif asset == 'Bitcoin':
        data = obb.crypto.price.historical("BTC-USD", provider="fmp", start_date=start_date)
    else:
        return None  # No data for "None"
    return convert_to_dataframe(data)['close']


# In[7]:


# Sidebar inputs
assets = ['None', 'Gold', 'US Stock', 'Bitcoin']
asset_1 = st.sidebar.selectbox("Asset 1", assets)
asset_2 = st.sidebar.selectbox("Asset 2", assets)
asset_3 = st.sidebar.selectbox("Asset 3", assets)
start_date = st.sidebar.date_input("Start Date", pd.to_datetime('2020-01-01'))


# In[8]:


# Button to trigger analysis
if st.sidebar.button("Analyze"):
    # Fetch data
    data_dict = {}
    if asset_1 != "None":
        data_dict['Gold'] = fetch_data(asset_1, start_date)
    if asset_2 != "None":
        data_dict['US Stock'] = fetch_data(asset_2, start_date)
    if asset_3 != "None":
        data_dict['Bitcoin'] = fetch_data(asset_3, start_date)

    if not data_dict:
        st.warning("No assets selected for analysis.")
    else:
        # Combine data
        data_df = pd.DataFrame(data_dict)
        data_df = data_df.reindex(pd.date_range(start=data_df.index.min(), end=data_df.index.max(), freq='B'))
        data_df.dropna(inplace=True)

        # Analysis
        returns_df = data_df.pct_change().dropna()
        volatility_df = returns_df.std() * np.sqrt(252)
        correlation_matrix = returns_df.corr()

        # Display charts
        st.subheader("Correlation Matrix")
        st.write(correlation_matrix)
        
        st.subheader("Historical Price Data")
        st.line_chart(data_df)

        st.subheader("Daily Returns")
        st.line_chart(returns_df)

        st.subheader("Annualized Volatility")
        st.bar_chart(volatility_df)


# In[ ]:




