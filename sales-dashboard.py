# Prepare The Tools (matplotlib and pandas)
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import sqlite3

# Load and Read the CSV
df = pd.read_csv("superstore_dataset.csv")
print(df.head())

# -- current shape of the data (rows and columns)
print("Initial shape of the dataset: ", df.shape)

# -- columns of dataframe
print("Initial columns of the dataset: ", df.columns)

# -- dataframe information
print(df.info)

# -- check null values in dataframe
print(df.isnull().sum())

# -- print data types of each cell
print(df.dtypes)

# Create SQL Database and Insert Data

# -- Creation of database and connection
conn = sqlite3.connect("superstore.db")

# -- Creation of table named "superstore_sales"
df.to_sql("superstore_sales", conn, if_exists="replace", index=False)

# query the total sales of each category
query = "SELECT Category, SUM(Sales) AS TotalSales FROM superstore_sales GROUP BY Category"
result = pd.read_sql_query(query, conn)
print(result.head())




# Analyze Trends

# -- Analyze the sales of Office Supplies per year and months
office_supplies_sales_year = "SELECT strftime('%Y', Order_Date) AS Year, SUM(Sales) AS TotalSalesPerYear FROM superstore_sales WHERE Category = 'Office Supplies' GROUP BY Year ORDER BY Year"
df_office_supplies_sales_per_year = pd.read_sql_query(office_supplies_sales_year, conn)
print("Total sales of Office Supplies Per Year", "\n", df_office_supplies_sales_per_year, "\n")

office_supplies_sales_month = "SELECT strftime('%m', Order_Date) AS Month, SUM(Sales) AS TotalSalesPerMonth FROM superstore_sales WHERE Category = 'Office Supplies' GROUP BY Month ORDER BY Month"
df_furniture_sales_per_month = pd.read_sql_query(office_supplies_sales_month, conn)
print("Total sales of Office Supplies Per Month", "\n", df_furniture_sales_per_month, "\n")


# -- Analyze the sales of Furniture per year and months
furniture_sales_year = "SELECT strftime('%Y', Order_Date) AS Year, SUM(Sales) AS TotalSalesPerYear FROM superstore_sales WHERE Category = 'Furniture' GROUP BY Year ORDER BY Year"
df_furniture_sales_per_year = pd.read_sql_query(furniture_sales_year, conn)
print("Total sales of Furniture Per Year", "\n", df_furniture_sales_per_year, "\n")

furniture_sales_month = "SELECT strftime('%m', Order_Date) AS Month, SUM(Sales) AS TotalSalesPerMonth FROM superstore_sales WHERE Category = 'Furniture' GROUP BY Month ORDER BY Month"
df_furniture_sales_per_month = pd.read_sql_query(furniture_sales_month, conn)
print("Total sales of Furniture Per Month", "\n", df_furniture_sales_per_month, "\n")

# -- Analyze the sales of Technology per year and months
technology_sales_year = "SELECT strftime('%Y', Order_Date) AS Year, SUM(Sales) AS TotalSalesPerYear FROM superstore_sales WHERE Category = 'Technology' GROUP BY Year ORDER BY Year"
df_technology_sales_per_year = pd.read_sql_query(technology_sales_year, conn)
print("Total sales of Technology Per Year", "\n", df_technology_sales_per_year, "\n")

furniture_sales_month = "SELECT strftime('%m', Order_Date) AS Month, SUM(Sales) AS TotalSalesPerMonth FROM superstore_sales WHERE Category = 'Technology' GROUP BY Month ORDER BY Month"
df_technology_sales_per_month = pd.read_sql_query(furniture_sales_month, conn)
print("Total sales of Technology Per Month", "\n", df_technology_sales_per_month, "\n")


# Analyzing which products generate high sales but low profit

# -- Analyze the dataset first by querying it
high_sales_low_profit_products_data = "SELECT Product_Name, SUM(Sales) AS TotalProductSales, SUM(Profit) AS TotalProductProfit From superstore_sales GROUP BY Product_Name ORDER BY TotalProductProfit"
df_high_sales_low_profit_products = pd.read_sql_query(high_sales_low_profit_products_data, conn)
print(df_high_sales_low_profit_products)

# -- Apply Business Logic to query the product that has high sales but low profit
high_sales = 400
low_profit = 300

cols_to_show = [
    "Product_Name",
    "Sales",
    "Profit",
    "flag_high_sales_low_profit"
]

df["flag_high_sales_low_profit"] = (
    (df["Sales"] > high_sales) &
    (df["Profit"] < low_profit)
)

high_sales_low_profit_products = (
    df[df["flag_high_sales_low_profit"]]
        .sort_values(by=["Sales", "Profit"], ascending=[False, True])
)

print("\nAnalyzing which products generate high sales but low profit")
print(high_sales_low_profit_products[cols_to_show])


# Analyze which discount ranges hurt profitability the most

# -- Filtering and querying the dataset first based on discount range
print("\n")
discount_ranges_profit_data = """
SELECT
    CASE
        WHEN Discount = 0 THEN 'No Discount'
        WHEN Discount > 0 AND Discount <= 0.10 THEN 'Low (0–10%)'
        WHEN Discount > 0.10 AND Discount <= 0.30 THEN 'Medium (10–30%)'
        WHEN Discount > 0.30 AND Discount <= 0.50 THEN 'High (30–50%)'
        ELSE 'Very High (>50%)'
    END AS discount_range,
    SUM(Sales) AS total_sales,
    SUM(Profit) AS total_profit,
    COUNT(*) AS order_count
FROM superstore_sales
GROUP BY discount_range
ORDER BY discount_range;
"""

df_discount_ranges_profit = pd.read_sql_query(discount_ranges_profit_data, conn)
print(df_discount_ranges_profit)

# -- Apply Business Logic for Measure profit impact and Compare profit margin
df_discount_ranges_profit['profit_margin'] = (df_discount_ranges_profit['total_profit'] / df_discount_ranges_profit['total_sales'])
profit_margin = df_discount_ranges_profit[['discount_range', 'profit_margin']]

print("\nAnalyzing which discount ranges hurt profitability the most")
print(profit_margin)

print("\n")

# Analyze which regions have high order volume but low average order value (where are we getting many orders, but each order is small)
high_order_volume_low_avg_value = "SELECT Region, SUM(Sales) AS TotalRegionSales, SUM(Profit) AS TotalRegionProfit, COUNT(DISTINCT Order_ID) AS OrderCount, SUM(Sales) / COUNT(DISTINCT Order_ID) AS AverageOrderValue, SUM(Sales) / SUM(Profit) AS ProfitMargin From superstore_sales GROUP BY Region ORDER BY TotalRegionProfit"
df_high_order_volume_low_avg_value = pd.read_sql_query(high_order_volume_low_avg_value, conn)
print(df_high_order_volume_low_avg_value)


# Apply Business logic for flagging high volume / low AOV Regions
avg_orders = df_high_order_volume_low_avg_value['OrderCount'].mean()
avg_aov = df_high_order_volume_low_avg_value['AverageOrderValue'].mean()

df_high_order_volume_low_avg_value['region_flag'] = df_high_order_volume_low_avg_value.apply(
    lambda x: 'High Order Volume / Low Order Value'
    if x['OrderCount'] > avg_orders and x['AverageOrderValue'] < avg_aov
    else 'Normal',
    axis=1
)

print(df_high_order_volume_low_avg_value[['Region', 'region_flag']])




# Analyze which customers are frequent buyers but have declining spend over time (which customers buy often, but are spending less money each time as time goes on?)
frequent_buyers_less_money_ot = "SELECT Customer_ID, strftime('%Y-%m', Order_Date) AS order_month, SUM(Sales) monthly_spend, COUNT(DISTINCT Order_ID) AS monthly_orders FROM superstore_sales GROUP BY Customer_ID, order_month"
df_frequent_buyers_less_money_ot = pd.read_sql_query(frequent_buyers_less_money_ot, conn)
print(df_frequent_buyers_less_money_ot)

# Apply Business logic for high total order count
avg_customer_order = df_frequent_buyers_less_money_ot['monthly_orders'].mean()

df_frequent_buyers_less_money_ot['order_volume_flag'] = df_frequent_buyers_less_money_ot.apply(
    lambda x: 'High Total Order'
    if x['monthly_orders'] > avg_customer_order
    else 'Low Total Order',
    axis=1
)

print(df_frequent_buyers_less_money_ot[['Customer_ID', 'monthly_orders', 'monthly_spend', 'order_volume_flag']])


# Create Visualizations
# result.plot(kind="bar", x="Category", y="TotalSales")
# plt.show()

# plt.scatter(df_high_order_volume_low_avg_value['OrderCount'], df_high_order_volume_low_avg_value['AverageOrderValue'])
# plt.xlabel("Order Count")
# plt.ylabel("Average Order Value")
# plt.title('Order Volume vs AOV by Region')
#
# for i, region in enumerate(df_high_order_volume_low_avg_value['Region']):
#     plt.text(df_high_order_volume_low_avg_value['OrderCount'][i], df_high_order_volume_low_avg_value['AverageOrderValue'][i], region)
#
#
# plt.show()