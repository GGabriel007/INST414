import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from tabulate import tabulate  # Import tabulate for better table display

# Load dataset
file_path = "Metro_zhvi_uc_sfrcondo_tier_0.33_0.67_sm_sa_month.csv"
df = pd.read_csv(file_path)

# Rename columns for better readability 
df.rename(columns={"RegionName": "City", "StateName": "State"}, inplace=True)

# Convert the dataset from wide format to long format
df_long = df.melt(id_vars=["City", "State", "SizeRank"], var_name="Date", value_name="HousePrice")

# Convert Date column to datetime format
df_long["Date"] = pd.to_datetime(df_long["Date"], errors='coerce')  # Ensures parsing without crashing

# Drop missing values 
df_long.dropna(inplace=True)

df_long["HousePrice"] = pd.to_numeric(df_long["HousePrice"], errors="coerce")

# Compute correlation matrix before dropping "SizeRank"
correlation_matrix = df_long.select_dtypes(include=[np.number]).corr()

# Display correlation table 
print(correlation_matrix)

# Drop unnecessary columns AFTER correlation analysis
df.drop(columns=["RegionID", "RegionType"], inplace=True)

# Price Distribution 
plt.figure(figsize=(8, 5))
sns.histplot(df_long["HousePrice"], bins=50, kde=True)
plt.title("Distribution of House Prices")
plt.xlabel("House Price")
plt.ylabel("Frequency")
plt.xscale("log")
plt.show()

# Geographic Price Trends (Bar Chart)
plt.figure(figsize=(10, 6))
pivot_table = df_long.groupby("City")["HousePrice"].mean().sort_values(ascending=False)
top_cities = pivot_table.head(30)  # Select top 30 cities

sns.barplot(x=top_cities.values, y=top_cities.index, hue=top_cities.index, dodge=False, legend=False, palette="coolwarm")
plt.title("Top 30 Cities with Highest Average House Prices")
plt.xlabel("House Price")
plt.ylabel("City")
plt.show()

print("\nCleaned Data Sample:")
print(tabulate(df_long.head(), headers='keys', tablefmt='fancy_grid'))
