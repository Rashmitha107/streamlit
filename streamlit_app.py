import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import math

st.title("Data App Assignment, on June 20th")

st.write("### Input Data and Examples")
df = pd.read_csv("Superstore_Sales_utf8.csv", parse_dates=True)
st.dataframe(df)

# This bar chart will not have solid bars--but lines--because the detail data is being graphed independently
st.bar_chart(df, x="Category", y="Sales")

# Now let's do the same graph where we do the aggregation first in Pandas... (this results in a chart with solid bars)
st.dataframe(df.groupby("Category").sum())
# Using as_index=False here preserves the Category as a column.  If we exclude that, Category would become the datafram index and we would need to use x=None to tell bar_chart to use the index
st.bar_chart(df.groupby("Category", as_index=False).sum(), x="Category", y="Sales", color="#04f")

# Aggregating by time
# Here we ensure Order_Date is in datetime format, then set is as an index to our dataframe
df["Order_Date"] = pd.to_datetime(df["Order_Date"])
df.set_index('Order_Date', inplace=True)
# Here the Grouper is using our newly set index to group by Month ('M')
sales_by_month = df.filter(items=['Sales']).groupby(pd.Grouper(freq='M')).sum()

st.dataframe(sales_by_month)

# Here the grouped months are the index and automatically used for the x axis
st.line_chart(sales_by_month, y="Sales")

#st.write("## Your additions")   
# st.write("### (1) add a drop down for Category, addeddddd testinggggggggggggg for username (https://docs.streamlit.io/library/api-reference/widgets/st.selectbox)")
# st.write("### (2) add a multi-select for Sub_Category *in the selected Category (1)* (https://docs.streamlit.io/library/api-reference/widgets/st.multiselect)")
# st.write("### (3) show a line chart of sales for the selected items in (2)")
# st.write("### (4) show three metrics (https://docs.streamlit.io/library/api-reference/data/st.metric) for the selected items in (2): total sales, total profit, and overall profit margin (%)")
# st.write("### (5) use the delta option in the overall profit margin metric to show the difference between the overall average profit margin (all products across all categories)")


# (1) Dropdown for Category with placeholder
options = df['Category'].unique()
selected_category = st.selectbox(
    "Select a category from the below options",
    options=options,
    index=0
)

# Check if a category is selected
if selected_category:
    # Filter data based on selected category
    filtered_df = df[df['Category'] == selected_category]

    # (2) Multi-select for Sub_Category in the selected Category with placeholder
    sub_categories = filtered_df['Sub_Category'].unique()
    selected_sub_categories = st.multiselect(
        "Select sub-categories from the below options", 
        options=sub_categories, 
        default=[]
    )

    if selected_sub_categories:
        # Filter data based on selected sub-categories
        selected_df = filtered_df[filtered_df['Sub_Category'].isin(selected_sub_categories)]

        # (3) Line chart of sales for the selected items
        if not selected_df.empty:
            sales_by_month_sub = selected_df.groupby(pd.Grouper(freq='M')).sum()
            st.line_chart(sales_by_month_sub, y="Sales")

        # (4) Metrics for the selected items: total sales, total profit, and overall profit margin (%)
        if not selected_df.empty:
            total_sales = selected_df['Sales'].sum()
            total_profit = selected_df['Profit'].sum()
            profit_margin = (total_profit / total_sales) * 100 if total_sales > 0 else 0
            
            st.metric(label="Total Sales", value=f"${total_sales:,.2f}")
            st.metric(label="Total Profit", value=f"${total_profit:,.2f}")
            st.metric(label="Profit Margin", value=f"{profit_margin:.2f}%")

            # (5) Use the delta option in the overall profit margin metric to show the difference between the overall average profit margin (all products across all categories)
            overall_sales = df['Sales'].sum()
            overall_profit = df['Profit'].sum()
            overall_profit_margin = (overall_profit / overall_sales) * 100 if overall_sales > 0 else 0

            delta = profit_margin - overall_profit_margin

            st.metric(label="Overall Profit Margin", value=f"{profit_margin:.2f}%", delta=f"{delta:.2f}%")

            # Display the overall profit margin for reference
            st.write(f"Overall average profit margin (all products across all categories): {overall_profit_margin:.2f}%")
        else:
            st.write("No data available for the selected sub-categories.")
    else:
        st.write("Please select at least one sub-category.")
else:
    st.write("Please select a category.")