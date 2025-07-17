import pandas as pd

# Load the sheet
df = pd.read_excel("kolkata air pollution open aq.xlsx", sheet_name='openaq (1)')

# Join the three columns per row into one string
full_rows = df.astype(str).apply(lambda row: ';'.join(row.dropna()), axis=1)

# Split each row by ';' and keep only valid rows (12 fields)
split_data = [row.split(";") for row in full_rows if len(row.split(";")) >= 12]

# Define correct column headers
columns = [
    "Country Code", "Empty1", "Location", "Source Name", "Latitude", 
    "Longitude", "Pollutant", "Source", "Unit", "Value", "Last Updated", "Country Label"
]

# Now create the DataFrame
clean_df = pd.DataFrame(split_data, columns=columns)

# Convert data types
clean_df["Value"] = pd.to_numeric(clean_df["Value"], errors="coerce")
clean_df["Last Updated"] = pd.to_datetime(clean_df["Last Updated"], errors="coerce")

# Let's check what I got finally!
print("Pollutants:", clean_df["Pollutant"].unique())
print("Locations:", clean_df["Location"].unique())
print(clean_df.head())

pm25_df = clean_df[clean_df["Pollutant"] == "PM2.5"].dropna(subset=["Value", "Last Updated"])
pm25_df["Month"] = pm25_df["Last Updated"].dt.to_period("M")

monthly_avg = pm25_df.groupby("Month")["Value"].mean().reset_index()
monthly_avg.columns = ["Month", "Average_PM2.5"]

import matplotlib.pyplot as plt

monthly_avg["Month"] = monthly_avg["Month"].astype(str)
plt.figure(figsize=(12, 6))
plt.plot(monthly_avg["Month"], monthly_avg["Average_PM2.5"], marker='o')
plt.xticks(rotation=45)
plt.title("Monthly Average PM2.5 Levels in Kolkata")
plt.xlabel("Month")
plt.ylabel("PM2.5 (µg/m³)")
plt.tight_layout()
plt.show()

# Average PM2.5 by location
location_avg = pm25_df.groupby("Location")["Value"].mean().sort_values()

# Plot bar chart
plt.figure(figsize=(10, 5))
location_avg.plot(kind='barh', color='coral')
plt.xlabel("Average PM2.5")
plt.title("Average PM2.5 Levels by Location in Kolkata")
plt.tight_layout()
plt.show()

# Group PM2.5 data by day of week and take average
pm25_df["Day"] = pm25_df["Last Updated"].dt.day_name()
day_avg = pm25_df.groupby("Day")["Value"].mean()
# Plotting average PM2.5 per day
plt.figure(figsize=(10, 5))
bars = day_avg.plot(kind='bar', color='skyblue')

plt.ylabel("Avg PM2.5")
plt.title("Average PM2.5 by Day of Week")
plt.xlabel("Day")
plt.xticks(rotation=45)
plt.tight_layout()
plt.show()

# Add year column
pm25_df["Year"] = pm25_df["Last Updated"].dt.year

# Compare 2019 vs 2020 vs 2021
yearly_avg = pm25_df.groupby("Year")["Value"].mean()

yearly_avg.plot(kind='bar', color='mediumseagreen')
plt.title("Average PM2.5 Levels by Year")
plt.ylabel("µg/m³")
plt.xlabel("Year")
plt.tight_layout()
plt.show()







