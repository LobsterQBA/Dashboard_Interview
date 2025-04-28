import streamlit as st
import matplotlib.pyplot as plt
import numpy as np

# 标题
st.set_page_config(page_title="Magic School ROI Dashboard", layout="wide")
st.title("Magic School - China Go-to-Market ROI Tracker)")

# 侧边栏设置
st.sidebar.header("Adjust Your Assumptions")

# 用户输入
localization_cost = st.sidebar.number_input("Localization & Compliance Cost (\u00a5)", 2000000, step=100000)
cloud_cost = st.sidebar.number_input("Cloud Deployment Cost (\u00a5/year)", 500000, step=50000)
sales_team_cost = st.sidebar.number_input("Sales & Support Team Cost (\u00a5/year)", 2500000, step=100000)
price_per_school = st.sidebar.number_input("Price per School (\u00a5/year)", 30000, step=1000)
pilot_schools = st.sidebar.number_input("Number of Pilot Schools in Year 1", 30, step=5)
ltv_years = st.sidebar.slider("School Lifetime (Years)", 1.0, 5.0, 2.5, step=0.5)
renewal_rate = st.sidebar.slider("Renewal Rate (%)", 50, 100, 80, step=5)
cac_per_school = st.sidebar.number_input("Customer Acquisition Cost (\u00a5 per school)", 20000, step=1000)

# 计算值
first_year_investment = localization_cost + cloud_cost + sales_team_cost
first_year_revenue = pilot_schools * price_per_school
ltv_per_school = price_per_school * ltv_years * (renewal_rate / 100)
breakeven_schools = first_year_investment / ltv_per_school
ltv_cac_ratio = ltv_per_school / cac_per_school

# 分栏显示结果
col1, col2, col3 = st.columns(3)
col1.metric("\U0001f4c8 First-Year Investment", f"¥{first_year_investment:,.0f}")
col2.metric("\U0001f4b0 First-Year Revenue", f"¥{first_year_revenue:,.0f}")
col3.metric("\U0001f4cb Lifetime Value (LTV) per School", f"¥{ltv_per_school:,.0f}")

col4, col5, col6 = st.columns(3)
col4.metric("\U0001f4ca Breakeven Number of Schools", f"{breakeven_schools:.1f}")
col5.metric("\U0001f4c9 LTV/CAC Ratio", f"{ltv_cac_ratio:.2f}")

# 效益曲线 - 考虑不同年增长率效果
st.header("Profit Trajectories at Different Growth Rates")

years = np.arange(0, 6)
growth_rates = [30, 50, 80, 100]  # 测试的年增长率
fig, ax = plt.subplots(figsize=(12, 6))

for rate in growth_rates:
    annual_growth = 1 + (rate / 100)
    schools_projection = pilot_schools * (annual_growth ** years)
    revenue_projection = np.minimum(schools_projection, 1000) * price_per_school * (renewal_rate / 100)
    cost_projection = first_year_investment * (years==0) + cloud_cost * years
    profit_projection = revenue_projection.cumsum() - cost_projection
    ax.plot(years, profit_projection, marker='o', label=f"Growth {rate}%")

ax.axhline(0, color='gray', linestyle='--')
ax.set_xlabel("Years")
ax.set_ylabel("Cumulative Profit (\u00a5)")
ax.set_title("Profit Sensitivity Analysis by Growth Rate")
ax.legend()
ax.grid(True)
st.pyplot(fig)

# 分析评论
st.header("\U0001f4dd Strategic Insights")

if ltv_cac_ratio > 3:
    st.success("Healthy Unit Economics: LTV/CAC is strong.")
else:
    st.warning("Warning: LTV/CAC ratio below ideal standards.")

if pilot_schools >= breakeven_schools:
    st.success("Pilot size sufficient to reach break-even.")
else:
    st.info("Need to scale post-pilot to break even.")

