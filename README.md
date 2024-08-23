# Bike Sharing Analysis Dashboard

This is a Streamlit-based dashboard that provides insights and analysis on bike sharing data. The analysis covers various aspects such as hourly and daily distribution, correlation analysis, clustering analysis, and RFM (Recency, Frequency, Monetary) analysis.

## Author

- Name: Michael Natanael
- Email: mnatanael87@gmail.com

## Overview

The dashboard visualizes data from two datasets:
- `day_cleaned.xlsx`: Contains daily bike rental data.
- `hour_cleaned.xlsx`: Contains hourly bike rental data.

The main features of the dashboard include:
1. **Hourly and Daily Distribution of Bike Rentals**
2. **Correlation Analysis**
3. **Clustering Analysis**
4. **RFM Analysis**

## Features

### 1. Hourly and Daily Distribution of Bike Rentals

- **Season-wise Hourly Distribution**: Visualizes the hourly bike rental counts across different seasons.
- **Weekday-wise Hourly Distribution**: Shows the hourly rental patterns across different weekdays.
- **Season-wise Daily Distribution**: Displays the daily rental counts across different seasons.
- **Monthly Distribution**: Highlights the bike rental counts for each month.

### 2. Correlation Analysis

- **Correlation Matrix**: Shows the correlation between different features (e.g., temperature, humidity, windspeed) and the total bike rentals.

### 3. Clustering Analysis

- **Holiday vs. Non-Holiday Rentals**: Analyzes the bike rental counts on holidays compared to non-holidays.
- **Working Day vs. Non-Working Day Rentals**: Compares the rental counts on working days versus non-working days.

### 4. RFM Analysis

- **RFM for Registered Customers**: Analyzes the recency, frequency, and monetary value for registered customers.
- **RFM for Casual Customers**: Analyzes the same metrics for casual customers.

## Conclusion

Based on the analysis, the following key insights were derived:
1. The highest bike rentals occurred in the Fall season, particularly in June and September, on Thursdays, Fridays, and Saturdays, and between 17:00 - 18:00 hours.
2. Registered customers show a strong correlation (0.9) with the total bike rentals, while casual customers have a moderate correlation (0.6).

## How to Run the Dashboard

1. Clone the repository.
2. Install the necessary dependencies using `pip`:
   ```bash
   pip install -r requirements.txt

## Run steamlit app

```
cd dashboard
streamlit run dashboard.py
```
