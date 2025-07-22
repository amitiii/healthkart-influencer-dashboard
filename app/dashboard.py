import streamlit as st
import pandas as pd
import plotly.express as px

st.set_page_config(page_title="Influenz Dashboard", layout="wide")
st.title("📊 Influenz - Influencer Campaign ROI Dashboard")

@st.cache_data
def load_data():
    influencers = pd.read_csv("data/influencers.csv")
    posts = pd.read_csv("data/posts.csv")
    tracking = pd.read_csv("data/tracking_data.csv")
    payouts = pd.read_csv("data/payouts.csv")
    return influencers, posts, tracking, payouts

influencers, posts, tracking, payouts = load_data()

# Filters
platforms = st.sidebar.multiselect("Platform", influencers['platform'].unique(), default=influencers['platform'].unique())
filtered_influencers = influencers[influencers['platform'].isin(platforms)]
filtered_tracking = tracking[tracking['influencer_id'].isin(filtered_influencers['influencer_id'])]

# KPIs
st.subheader("📈 Campaign Overview")
revenue = filtered_tracking['revenue'].sum()
orders = filtered_tracking['orders'].sum()
payout = payouts['total_payout'].sum()
roi = round((revenue - payout) / payout, 2) if payout > 0 else 0

col1, col2, col3, col4 = st.columns(4)
col1.metric("Total Revenue", f"₹{revenue:,.0f}")
col2.metric("Orders", orders)
col3.metric("Payout", f"₹{payout:,.0f}")
col4.metric("ROI", f"{roi}")

# Charts
st.subheader("📅 Revenue Trend")
rev_trend = filtered_tracking.groupby("date")["revenue"].sum().reset_index()
st.plotly_chart(px.line(rev_trend, x="date", y="revenue", title="Revenue Over Time")), us
