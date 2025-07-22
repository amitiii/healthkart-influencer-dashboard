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

# Sidebar filters
platforms = st.sidebar.multiselect("Platform", influencers['platform'].unique(), default=influencers['platform'].unique())
categories = st.sidebar.multiselect("Category", influencers['category'].unique(), default=influencers['category'].unique())
products = st.sidebar.multiselect("Product", tracking['product'].unique(), default=tracking['product'].unique())

filtered_influencers = influencers[influencers['platform'].isin(platforms) & influencers['category'].isin(categories)]
filtered_tracking = tracking[
    tracking['influencer_id'].isin(filtered_influencers['influencer_id']) &
    tracking['product'].isin(products)
]
filtered_payouts = payouts[payouts['influencer_id'].isin(filtered_influencers['influencer_id'])]

# KPI metrics
st.subheader("📈 Campaign Overview")
revenue = filtered_tracking['revenue'].sum()
orders = filtered_tracking['orders'].sum()
payout = filtered_payouts['total_payout'].sum()
roi = round((revenue - payout) / payout, 2) if payout > 0 else 0

col1, col2, col3, col4 = st.columns(4)
col1.metric("Total Revenue", f"₹{revenue:,.0f}")
col2.metric("Orders", orders)
col3.metric("Payout", f"₹{payout:,.0f}")
col4.metric("ROI", f"{roi}")

# Revenue trend
st.subheader("📅 Revenue Trend")
rev_trend = filtered_tracking.groupby("date")["revenue"].sum().reset_index()
st.plotly_chart(px.line(rev_trend, x="date", y="revenue", title="Revenue Over Time"), use_container_width=True)

# Top influencers by revenue
st.subheader("🏆 Top Influencers by Revenue")
top_influencers = filtered_tracking.groupby("influencer_id")["revenue"].sum().reset_index().nlargest(10, "revenue")
top_influencers = top_influencers.merge(influencers[['influencer_id', 'name']], on='influencer_id')
st.plotly_chart(px.bar(top_influencers, x="name", y="revenue", title="Top 10 Influencers by Revenue"), use_container_width=True)

# Posts scatter
st.subheader("📣 Posts: Reach vs Likes")
post_data = posts[posts['influencer_id'].isin(filtered_influencers['influencer_id'])]
fig = px.scatter(post_data, x='reach', y='likes', color='platform', size='comments', hover_data=['caption'])
st.plotly_chart(fig, use_container_width=True)

# Payout table
st.subheader("💸 Payout Tracking Table")
st.dataframe(filtered_payouts.merge(influencers[['influencer_id', 'name']], on='influencer_id'))

# Export button
st.download_button("📥 Export Filtered Tracking Data", filtered_tracking.to_csv(index=False), "filtered_tracking.csv")
