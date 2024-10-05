import urllib

import matplotlib.image as mpimg
import matplotlib.pyplot as plt
import pandas as pd
import seaborn as sns
import streamlit as st
from babel.numbers import format_currency
from fungsi import BrazilMapPlotter, DataAnalyzer

# sns.set(style="dark")
# st.set_option("deprecation.showPyplotGlobalUse", False)

# Dataset
datetime_cols = [
    "order_approved_at",
    "order_delivered_carrier_date",
    "order_delivered_customer_date",
    "order_estimated_delivery_date",
    "order_purchase_timestamp",
    "shipping_limit_date",
]

all_df = pd.read_csv("https://raw.githubusercontent.com/HiiGER/submission_dicoding/refs/heads/master/all_data.csv")
all_df.sort_values(by="order_approved_at", inplace=True)
all_df.reset_index(inplace=True)

# Geolocation Dataset
geolocation = pd.read_csv("https://raw.githubusercontent.com/HiiGER/submission_dicoding/refs/heads/master/geolocation.csv")
data = geolocation.drop_duplicates(subset="customer_unique_id")

for col in datetime_cols:
    all_df[col] = pd.to_datetime(all_df[col])

min_date = all_df["order_approved_at"].min()
max_date = all_df["order_approved_at"].max()

# Sidebar
with st.sidebar:
    # Title
    st.title("Angger Tirta")
    st.title("Tetalen Mukti")

    # Logo Image
    st.image(
        "https://github.com/HiiGER/submission_dicoding/blob/master/dashboard/images.png?raw=true"
    )

    # Date Range
    start_date, end_date = st.date_input(
        label="Select Date Range",
        value=[min_date, max_date],
        min_value=min_date,
        max_value=max_date,
    )

    st.caption("Copyright (C) Angger tirta T.M 2024")


# Main
main_df = all_df[
    (all_df["order_approved_at"] >= str(start_date))
    & (all_df["order_approved_at"] <= str(end_date))
]

function = DataAnalyzer(main_df)
map_plot = BrazilMapPlotter(data, plt, mpimg, urllib, st)

daily_orders_df = function.create_daily_orders_df()
sum_order_items_df = function.create_sum_order_items_df()
state, most_common_state = function.create_bystate_df()
order_status, common_status = function.create_order_status()

# Title
st.header("E-Commerce Dashboard")

# Daily Orders
st.subheader("Daily Orders")

col1, col2 = st.columns(2)

with col1:
    total_order = daily_orders_df["order_count"].sum()
    st.markdown(f"Total Pembelian: **{total_order}**")

with col2:
    total_revenue = format_currency(
        daily_orders_df["revenue"].sum(), "IDR", locale="id_ID"
    )
    st.markdown(f"Total Pendapatan : **{total_revenue}**")

fig, ax = plt.subplots(figsize=(12, 6))
ax.plot(
    daily_orders_df["order_approved_at"],
    daily_orders_df["order_count"],
    marker="o",
    linewidth=2,
    color="#90CAF9",
)
ax.tick_params(axis="x", rotation=45)
ax.tick_params(axis="y", labelsize=15)
st.pyplot(fig)

# Order Items
st.subheader(" ")
st.subheader(" ")
st.subheader("Order Items")
col1, col2 = st.columns(2)

with col1:
    total_items = sum_order_items_df["product_count"].sum()
    st.markdown(f"Total jumah barang: **{total_items}**")

with col2:
    avg_items = sum_order_items_df["product_count"].mean()
    st.markdown(f"Average : **{avg_items}**")

fig, ax = plt.subplots(nrows=1, ncols=2, figsize=(45, 25))

colors = ["#068DA9", "#D3D3D3", "#D3D3D3", "#D3D3D3", "#D3D3D3"]

sns.barplot(
    x="product_count",
    y="product_category_name_english",
    data=sum_order_items_df.head(5),
    palette=colors,
    ax=ax[0],
)
ax[0].set_ylabel(None)
ax[0].set_xlabel("Number of Sales", fontsize=30)
ax[0].set_title("Produk paling banyak terjual", loc="center", fontsize=50)
ax[0].tick_params(axis="y", labelsize=35)
ax[0].tick_params(axis="x", labelsize=30)

sns.barplot(
    x="product_count",
    y="product_category_name_english",
    data=sum_order_items_df.sort_values(by="product_count", ascending=True).head(5),
    palette=colors,
    ax=ax[1],
)
ax[1].set_ylabel(None)
ax[1].set_xlabel("Number of Sales", fontsize=30)
ax[1].invert_xaxis()
ax[1].yaxis.set_label_position("right")
ax[1].yaxis.tick_right()
ax[1].set_title("Produk paling sedikit terjual", loc="center", fontsize=50)
ax[1].tick_params(axis="y", labelsize=35)
ax[1].tick_params(axis="x", labelsize=30)

st.pyplot(fig)


st.subheader(" ")
st.subheader(" ")
st.subheader("Demographic")
most_common_state = state.customer_state.value_counts().index[0]
st.markdown(f"Most Common State: **{most_common_state}**")

fig, ax = plt.subplots(figsize=(12, 6))
sns.barplot(
    x=state.customer_state.value_counts().index,
    y=state.customer_count.values,
    data=state,
    palette=[
        "#068DA9" if score == most_common_state else "#D3D3D3"
        for score in state.customer_state.value_counts().index
    ],
)

plt.title("Number customers from State", fontsize=15)
plt.xlabel("State")
plt.ylabel("Number of Customers")
plt.xticks(fontsize=12)
fig.tight_layout()  # Add this line to ensure the layout is tight
st.pyplot(fig)  # This line is already correct

st.caption("Copyright (C) Angger tirta T.M 2024")
