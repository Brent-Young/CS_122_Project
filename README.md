# Stock Market Analysis Dashboard

## Authors
- Brent Young ([Brent-Young](https://github.com/Brent-Young))

## Project Description
This project is a Python application that analyzes historical stock market
data from the S&P 500 Kaggle dataset. Users can select one or more stocks
through a menu-driven interface and generate statistics and visualizations
for their selections. The application computes metrics such as daily and
cumulative returns, volatility, and moving averages, and compares
performance across multiple stocks. All data is loaded from a local CSV file
into a pandas DataFrame for fast, repeatable queries. The goal is to make basic investment
research accessible through simple visual summaries.

## Project Outline/Plan

### Interface Plan
- Flask web interface served locally and embedded in a Jupyter notebook
- User selects one or more stocks by ticker symbol from a dropdown list
- User chooses which analysis or chart to generate via buttons
- Output shown as Matplotlib charts and summary tables rendered in the browser

### Data Collection and Storage Plan
- Dataset: S&P 500 stock data from Kaggle (daily open/high/low/close/volume)
- Clean raw CSV with pandas (drop missing values, parse dates, sort by ticker and date)
- Data loaded directly into a pandas DataFrame for fast, repeatable queries

### Data Analysis and Visualization Plan
- Compute daily returns, cumulative returns, and rolling volatility with pandas/NumPy
- Calculate 20/50-day moving averages for selected stocks
- Compute correlations between stocks
- Visualizations: price + moving-average line charts, return distribution plots, correlation heatmap
