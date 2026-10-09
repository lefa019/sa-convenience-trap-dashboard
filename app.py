import streamlit as st
import plotly.express as px
import plotly.graph_objects as gg
from plotly.subplots import make_subplots
import numpy as np
import pandas as pd
from scipy.stats import linregress

# Page Configuration
st.set_page_config(
    page_title="SA Retail Convenience Trap Dashboard",
    page_icon="📊",
    layout="wide"
)

# Title & Header
st.title(" Analysis of SA Retail Convenience Trap")
st.markdown("**Author:** Richard Baloyi | *Interactive Research & Analytics Dashboard*")
st.markdown("---")

# ---------------------------------------------------------
# Sidebar Controls
# ---------------------------------------------------------
st.sidebar.header("Dashboard Controls")
annual_cost_input = st.sidebar.slider(
    "Annual Household Convenience Cost (R)", 
    min_value=1000, 
    max_value=10000, 
    value=2500, 
    step=250
)
investment_return = st.sidebar.slider(
    "Assumed Annual Investment Return (%)", 
    min_value=4.0, 
    max_value=15.0, 
    value=8.0, 
    step=0.5
) / 100.0

# ---------------------------------------------------------
# Data Preparation
# ---------------------------------------------------------
years = np.array([2018, 2019, 2020, 2021, 2022, 2023, 2024, 2025, 2026])

# Row 1 Layout
col1, col2, col3 = st.columns(3)

# Panel 1: Convenience vs Physical Activity
with col1:
    st.subheader("1. Convenience vs Physical Activity")
    delivery = np.array([10, 28, 75, 160, 280, 420, 580, 750, 920])
    tiktok = np.array([5, 35, 120, 280, 450, 620, 780, 850, 910])
    ai_usage = np.array([2, 8, 25, 65, 140, 260, 420, 580, 720])
    activity = np.array([100, 94, 87, 79, 73, 68, 64, 61, 58])

    fig1 = make_subplots(specs=[[{"secondary_y": True}]])
    fig1.add_trace(gg.Scatter(x=years, y=delivery, name="Food Delivery", mode="lines+markers"), secondary_y=False)
    fig1.add_trace(gg.Scatter(x=years, y=tiktok, name="TikTok Usage", mode="lines+markers"), secondary_y=False)
    fig1.add_trace(gg.Scatter(x=years, y=ai_usage, name="AI Adoption", mode="lines+markers"), secondary_y=False)
    fig1.add_trace(gg.Scatter(x=years, y=activity, name="Physical Activity (%)", mode="lines+markers", line=dict(dash='dash', color='red')), secondary_y=True)

    fig1.update_xaxes(title_text="Year")
    fig1.update_yaxes(title_text="Usage Index", secondary_y=False)
    fig1.update_yaxes(title_text="Physical Activity Level (%)", secondary_y=True)
    fig1.update_layout(height=400, margin=dict(l=20, r=20, t=30, b=20), legend=dict(orientation="h", y=-0.2))
    st.plotly_chart(fig1, use_container_width=True)

# Panel 2: Cost Leakage Breakdown
with col2:
    st.subheader("2. Household Cost Leakage")
    categories = ['Airtime Surcharges', 'Food Delivery', 'Streaming Premiums', 'Gated Estate Levies', 'Other']
    costs = [1200, 1800, 850, 2400, 650]
    
    fig2 = px.pie(names=categories, values=costs, hole=0.4, color_discrete_sequence=px.colors.qualitative.Pastel)
    fig2.update_layout(height=400, margin=dict(l=20, r=20, t=30, b=20))
    st.plotly_chart(fig2, use_container_width=True)

# Panel 3: Pre- vs Post-Convenience Behaviour
with col3:
    st.subheader("3. Behavioral Shift Profile")
    behaviours = ['Walking Dist (min)', 'Daily Steps', 'Research Time (min)', 'Screen Time (hr)']
    pre = [250, 8500, 450, 2.5]
    post = [80, 5200, 120, 9.6]

    df3 = pd.DataFrame({'Behavior': behaviours, 'Pre-Convenience': pre, 'Post-Convenience': post})
    fig3 = px.bar(df3, x='Behavior', y=['Pre-Convenience', 'Post-Convenience'], barmode='group')
    fig3.update_layout(height=400, margin=dict(l=20, r=20, t=30, b=20), legend=dict(orientation="h", y=-0.2))
    st.plotly_chart(fig3, use_container_width=True)

st.markdown("---")

# Row 2 Layout
col4, col5, col6 = st.columns(3)

# Panel 4: Compounding Cost over 10 Years
with col4:
    st.subheader("4. 10-Year Compounding Opportunity Cost")
    years_4 = np.arange(0, 11)
    cumulative = years_4 * annual_cost_input
    investment = [annual_cost_input * (((1 + investment_return)**y) - 1) / investment_return for y in years_4]

    fig4 = gg.Figure()
    fig4.add_trace(gg.Scatter(x=years_4, y=cumulative, name="Spent on Convenience", mode="lines+markers"))
    fig4.add_trace(gg.Scatter(x=years_4, y=investment, name=f"Invested ({int(investment_return*100)}%)", mode="lines+markers"))
    fig4.update_xaxes(title_text="Years")
    fig4.update_yaxes(title_text="Amount (R)")
    fig4.update_layout(height=400, margin=dict(l=20, r=20, t=30, b=20), legend=dict(orientation="h", y=-0.2))
    st.plotly_chart(fig4, use_container_width=True)

# Panel 5: Service Lock-in Heatmap
with col5:
    st.subheader("5. Service Dependence & Lock-in Heatmap")
    services = ['Food Delivery', 'Spaza Airtime', 'Social Media', 'AI Tools', 'Gated Estates', 'Streaming']
    metrics = ['Dependence', 'Retention', 'Revenue Model']
    data = [
        [9, 8, 7, 6, 5, 4],
        [9, 7, 8, 5, 6, 7],
        [8, 9, 6, 4, 5, 8]
    ]

    fig5 = px.imshow(data, x=services, y=metrics, color_continuous_scale="YlOrRd", text_auto=True)
    fig5.update_layout(height=400, margin=dict(l=20, r=20, t=30, b=20))
    st.plotly_chart(fig5, use_container_width=True)

# Panel 6: Delivery Growth vs Obesity Prevalence
with col6:
    st.subheader("6. Delivery Volume vs Obesity Rate")
    delivery_volume = np.array([10, 25, 80, 180, 320, 480, 650, 820, 950])
    obesity_rate = np.array([22, 23, 25, 27, 29, 31, 33, 35, 37])

    slope, intercept, r_value, _, _ = linregress(delivery_volume, obesity_rate)
    trend_line = slope * delivery_volume + intercept

    fig6 = gg.Figure()
    fig6.add_trace(gg.Scatter(x=delivery_volume, y=obesity_rate, mode='markers+text', text=years, textposition="top center", name='Urban Data Points'))
    fig6.add_trace(gg.Scatter(x=delivery_volume, y=trend_line, mode='lines', name=f'Trend Line (R² = {r_value**2:.3f})'))
    fig6.update_xaxes(title_text="Delivery Volume Index")
    fig6.update_yaxes(title_text="Obesity Rate (%)")
    fig6.update_layout(height=400, margin=dict(l=20, r=20, t=30, b=20), legend=dict(orientation="h", y=-0.2))
    st.plotly_chart(fig6, use_container_width=True)
