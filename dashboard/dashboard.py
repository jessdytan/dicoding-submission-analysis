import matplotlib.pyplot as plt
import pandas as pd
import numpy as np
import streamlit as st 
import seaborn as sns
import plotly.express as px
import sys
from pathlib import Path

dir = Path(__file__).absolute()
sys.path.append(str(dir.parent.parent))

# load file
path_to_file = 'main_data.csv'

# Load datasets
@st.cache_data
def load_data():
    data = pd.read_csv(path_to_file)
    return data

df = load_data()

# Dashboard title
st.title("📊 E-Commerce Dashboard")
st.sidebar.header("Filters Data")

# Filter date range
df['order_purchase_timestamp'] = pd.to_datetime(df['order_purchase_timestamp'])

# Sidebar date range selection
date_range = st.sidebar.date_input(
    "Select Date Range", 
    [df['order_purchase_timestamp'].min().date(), df['order_purchase_timestamp'].max().date()]
)

# Ensure the selection returns a tuple (start_date, end_date)
if isinstance(date_range, tuple):
    start_date, end_date = date_range
    # Filter data based on selected date range
    filtered_orders = df[(df['order_purchase_timestamp'] >= pd.Timestamp(start_date)) &
                     (df['order_purchase_timestamp'] <= pd.Timestamp(end_date))]
    
    st.write(f"Showing data from {start_date} to {end_date}")
    st.dataframe(filtered_orders)
else:
    st.write("Please select a valid date range.")

# Section 1: Sales Trend
df_sales_trend = filtered_orders.groupby(filtered_orders['order_purchase_timestamp'].dt.to_period('M')).size()
df_sales_trend.index = df_sales_trend.index.strftime('%Y-%m')

st.subheader("📈 Sales Trend Over Time")

# Create a figure
fig, ax = plt.subplots(figsize=(10, 5))
sns.lineplot(x=df_sales_trend.index.astype(str), y=df_sales_trend.values, ax=ax)

# Set labels and title
ax.set_xlabel("Month")
ax.set_xticklabels(df_sales_trend.index, rotation=45, ha='right')
ax.set_ylabel("Total Orders")
ax.set_title("Monthly Sales Trend")

# Show the plot
st.pyplot(fig)

# Section 2: Top Product Categories
st.subheader("🏆 Top 10 Product Categories")
popular_categories = filtered_orders['product_category_name_english'].value_counts().head(10).reset_index()

# Pastikan warna sesuai
colors = ['#1f77b4'] + ['#aec7e8'] * (len(popular_categories) - 1)

# Visualisasi dengan barplot
fig, ax = plt.subplots(figsize=(10, 5))  # Ubah ukuran dari (102, 5) ke (10, 5)
sns.barplot(x=popular_categories.iloc[:, 1], y=popular_categories.iloc[:, 0], palette=colors)

ax.set_title("Top 10 Kategori Produk Paling Diminati")
ax.set_xlabel("Jumlah Produk Terjual")
ax.set_ylabel("Kategori Produk")

st.pyplot(fig)

# Section 3: Payment Method Distribution
st.subheader("💳 Payment Methods Distribution")
colors = ["#4e79a7", "#f28e2b", "#e15759", "#76b7b2"]

# Hitung jumlah masing-masing metode pembayaran
payment_counts = filtered_orders['payment_type'].value_counts().reset_index()
payment_counts.columns = ['payment_type', 'count']  # Rename kolom agar lebih jelas

# Gunakan plotly express untuk membuat pie chart
fig = px.pie(payment_counts, 
             names='payment_type', 
             values='count', 
             color=colors)  # Warna gradasi biru

# Tampilkan di Streamlit
st.plotly_chart(fig)

# Section 4: Shipping Time Analysis
st.subheader("🚚 Delivery Time Analysis")
filtered_orders['delivery_time'] = (pd.to_datetime(filtered_orders['order_delivered_customer_date']) - pd.to_datetime(filtered_orders['order_purchase_timestamp'])).dt.days
fig, ax = plt.subplots()
sns.histplot(filtered_orders['delivery_time'].dropna(), bins=30, kde=True, color='blue', ax=ax)
ax.set_title("Distribution of Delivery Time")
st.pyplot(fig)

# Section 5: Customer Group Based on Payment Value
st.subheader("🔢 Customer Group Based on the Payment Value")
filtered_orders['customer_segment'] = pd.qcut(filtered_orders['payment_value'], q=4, labels=["Bronze", "Silver", "Gold", "Platinum"])
grouped_data = filtered_orders.groupby("customer_segment")["payment_value"].mean()

st.bar_chart(grouped_data)
 


st.markdown("---")

st.caption('Copyright JDY (c) 2025. All rights reserved.')