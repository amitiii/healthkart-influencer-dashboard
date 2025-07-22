# Influenz – HealthKart Influencer Campaign Dashboard

A smart dashboard to track and visualize influencer marketing performance across platforms (Instagram, YouTube, Twitter) for HealthKart. Built using Streamlit.

![Dashboard Preview](https://healthkart-influencer-dashboard-lqdoavfgnpfqcxz4ugfksh.streamlit.app/#influenz-dashboard)

## 🚀 Features
- Upload & analyze influencer campaign data
- Track ROI & incremental ROAS
- Top influencers, personas & poor ROI detection
- Payout tracking with basis filters
- CSV exports and filters
- Clean UX built with Streamlit + Plotly

## 🛠️ Setup Instructions
Clone the repository:
```bash
git clone https://github.com/your-username/healthkart-influenz-dashboard.git
cd healthkart-influenz-dashboard
pip install -r requirements.txt
streamlit run app/dashboard.py
```

## 📁 Folder Structure
```
.
├── app/
│   └── dashboard.py
├── data/
│   ├── influencers.csv
│   ├── posts.csv
│   ├── payouts.csv
│   └── tracking_data.csv
├── requirements.txt
├── README.md
└── preview.png
```

## 📦 Deployment
You can deploy this dashboard using [Streamlit Cloud](https://streamlit.io/cloud).

In the Streamlit Cloud setup:
- Main file path: `app/dashboard.py`
- Branch: `main`

## 📊 Assumptions
- Revenue is from tracked users only
- Influencer payouts are based on post or order performance

---

Built with ❤️ by [Your Name]
