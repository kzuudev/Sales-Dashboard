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
display_office_supplies_sales_per_year = pd.read_sql_query(office_supplies_sales_year, conn)
print("Total sales of Office Supplies Per Year", "\n", display_office_supplies_sales_per_year, "\n")

office_supplies_sales_month = "SELECT strftime('%m', Order_Date) AS Month, SUM(Sales) AS TotalSalesPerMonth FROM superstore_sales WHERE Category = 'Office Supplies' GROUP BY Month ORDER BY Month"
display_furniture_sales_per_month = pd.read_sql_query(office_supplies_sales_month, conn)
print("Total sales of Office Supplies Per Month", "\n", display_furniture_sales_per_month, "\n")


# -- Analyze the sales of Furniture per year and months
furniture_sales_year = "SELECT strftime('%Y', Order_Date) AS Year, SUM(Sales) AS TotalSalesPerYear FROM superstore_sales WHERE Category = 'Furniture' GROUP BY Year ORDER BY Year"
display_furniture_sales_per_year = pd.read_sql_query(furniture_sales_year, conn)
print("Total sales of Furniture Per Year", "\n", display_furniture_sales_per_year, "\n")

furniture_sales_month = "SELECT strftime('%m', Order_Date) AS Month, SUM(Sales) AS TotalSalesPerMonth FROM superstore_sales WHERE Category = 'Furniture' GROUP BY Month ORDER BY Month"
display_furniture_sales_per_month = pd.read_sql_query(furniture_sales_month, conn)
print("Total sales of Furniture Per Month", "\n", display_furniture_sales_per_month, "\n")

# -- Analyze the sales of Technology per year and months
technology_sales_year = "SELECT strftime('%Y', Order_Date) AS Year, SUM(Sales) AS TotalSalesPerYear FROM superstore_sales WHERE Category = 'Technology' GROUP BY Year ORDER BY Year"
display_technology_sales_per_year = pd.read_sql_query(technology_sales_year, conn)
print("Total sales of Technology Per Year", "\n", display_technology_sales_per_year, "\n")

furniture_sales_month = "SELECT strftime('%m', Order_Date) AS Month, SUM(Sales) AS TotalSalesPerMonth FROM superstore_sales WHERE Category = 'Technology' GROUP BY Month ORDER BY Month"
display_technology_sales_per_month = pd.read_sql_query(furniture_sales_month, conn)
print("Total sales of Technology Per Month", "\n", display_technology_sales_per_month, "\n")


# Analyzing which products generate high sales but low profit

# -- Analyze the dataset first by querying it
high_sales_low_profit_products_data = "SELECT Product_Name, SUM(Sales) AS TotalProductSales, SUM(Profit) AS TotalProductProfit From superstore_sales GROUP BY Product_Name ORDER BY TotalProductProfit"
display_high_sales_low_profit_products = pd.read_sql_query(high_sales_low_profit_products_data, conn)
print(display_high_sales_low_profit_products)

# -- Apply Business Logic to query the product that has high sales but low profit using Python
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







# Create Visualizations
# result.plot(kind="bar", x="Category", y="TotalSales")
# plt.show()
