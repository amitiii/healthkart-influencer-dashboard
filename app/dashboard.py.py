import streamlit as st
import pandas as pd
import plotly.express as px

# Page configuration
st.set_page_config(page_title="Influenz Dashboard", page_icon="📊", layout="wide")

# Title and styling
st.markdown("""
    <style>
        .main { background-color: #f8f9fa; }
        h1 { color: #004aad; }
        h2 { color: #13547a; }
        .stMetricValue { font-size: 24px !important; }
    </style>
""", unsafe_allow_html=True)

st.title("📊 Influenz – Influencer Campaign ROI Dashboard")
st.markdown("A smart analytics dashboard to monitor and optimize influencer marketing campaigns across platforms.")

# Load data with caching
@st.cache_data
def load_data():
    influencers = pd.read_csv("data/influencers.csv")
    posts = pd.read_csv("data/posts.csv")
    tracking = pd.read_csv("data/tracking_data.csv")
    payouts = pd.read_csv("data/payouts.csv")
    return influencers, posts, tracking, payouts

influencers, posts, tracking, payouts = load_data()

# Sidebar filters
st.sidebar.header("🔍 Filter Campaign Data")
platforms = st.sidebar.multiselect("Platform", influencers['platform'].unique(), default=influencers['platform'].unique())
categories = st.sidebar.multiselect("Category", influencers['category'].unique(), default=influencers['category'].unique())
products = st.sidebar.multiselect("Product", tracking['product'].unique(), default=tracking['product'].unique())

filtered_influencers = influencers[influencers['platform'].isin(platforms) & influencers['category'].isin(categories)]
filtered_tracking = tracking[
    tracking['influencer_id'].isin(filtered_influencers['influencer_id']) &
    tracking['product'].isin(products)
]
filtered_payouts = payouts[payouts['influencer_id'].isin(filtered_influencers['influencer_id'])]

# Tabs for layout
tab1, tab2, tab3, tab4 = st.tabs(["📈 Overview", "🏆 Top Influencers", "📣 Engagement", "💸 Payouts"])

# Overview Tab
with tab1:
    st.subheader("📊 Campaign Performance Summary")
    revenue = filtered_tracking['revenue'].sum()
    orders = filtered_tracking['orders'].sum()
    payout = filtered_payouts['total_payout'].sum()
    roi = round((revenue - payout) / payout, 2) if payout > 0 else 0

    kpi1, kpi2, kpi3, kpi4 = st.columns(4)
    kpi1.metric("Total Revenue", f"₹{revenue:,.0f}")
    kpi2.metric("Total Orders", orders)
    kpi3.metric("Total Payout", f"₹{payout:,.0f}")
    kpi4.metric("ROI", f"{roi}")

    st.markdown("---")
    st.markdown("### 📅 Revenue Trend")
    rev_trend = filtered_tracking.groupby("date")["revenue"].sum().reset_index()
    st.plotly_chart(px.line(rev_trend, x="date", y="revenue", title="Revenue Over Time"), use_container_width=True)

# Top Influencers Tab
with tab2:
    st.subheader("🏆 Top Influencers by Revenue")
    top_influencers = filtered_tracking.groupby("influencer_id")["revenue"].sum().reset_index().nlargest(10, "revenue")
    top_influencers = top_influencers.merge(influencers[['influencer_id', 'name']], on='influencer_id')
    st.plotly_chart(px.bar(top_influencers, x="name", y="revenue", title="Top 10 Influencers by Revenue", color="revenue", text_auto=True), use_container_width=True)

    st.markdown("---")
    st.subheader("📌 Influencer Performance Table")
    merged = filtered_tracking.merge(influencers, on="influencer_id")
    summary_table = merged.groupby(["name", "platform", "category"]).agg({
        "orders": "sum", "revenue": "sum"
    }).reset_index().sort_values(by="revenue", ascending=False)
    st.dataframe(summary_table, use_container_width=True)

# Engagement Tab
with tab3:
    st.subheader("📣 Post Engagement: Reach vs Likes")
    post_data = posts[posts['influencer_id'].isin(filtered_influencers['influencer_id'])]
    if not post_data.empty:
        fig = px.scatter(post_data, x='reach', y='likes', color='platform', size='comments',
                         hover_data=['caption'], title="Post Reach vs Likes")
        st.plotly_chart(fig, use_container_width=True)
    else:
        st.info("No post data available for selected filters.")

# Payouts Tab
with tab4:
    st.subheader("💸 Payout Tracking")
    enriched = filtered_payouts.merge(influencers[['influencer_id', 'name', 'platform']], on='influencer_id')
    st.dataframe(enriched, use_container_width=True)

    st.download_button("📥 Download Filtered Tracking Data", filtered_tracking.to_csv(index=False), "filtered_tracking.csv")

st.markdown("---")
st.caption("📍 Powered by Streamlit • HealthKart Internship Assignment • Developed by [Your Name]")