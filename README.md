# Stock Market Analysis Dashboard

## Authors
- Brent Young ([Brent-Young](https://github.com/Brent-Young))
- *Partner's name* ([partner-username])

## Project Description
This project is a Python application that analyzes historical stock market
data from the S&P 500 Kaggle dataset. Users can select one or more stocks
through a menu-driven interface and generate statistics and visualizations
for their selections. The application computes metrics such as daily and
cumulative returns, volatility, and moving averages, and compares
performance across multiple stocks. All data is stored locally in an SQLite
database for fast, repeatable queries. The goal is to make basic investment
research accessible through simple visual summaries.

## Project Outline/Plan

### Interface Plan
- Menu-driven command-line interface
- User selects stocks by ticker symbol and a date range
- User chooses which analysis or chart to generate
- Output shown as Matplotlib charts and printed summary tables
- Stretch goal: Streamlit web dashboard version

### Data Collection and Storage Plan (Author #1: [name])
- Dataset: S&P 500 stock data from Kaggle (daily open/high/low/close/volume)
- Clean raw CSVs with pandas (missing values, date parsing)
- Load cleaned data into an SQLite database indexed by ticker and date
- Include a loading script so the database can be rebuilt reproducibly

### Data Analysis and Visualization Plan (Author #2: [name])
- Compute daily returns, cumulative returns, and rolling volatility with pandas/NumPy
- Calculate 20/50-day moving averages for selected stocks
- Compute correlations between stocks
- Visualizations: price + moving-average line charts, return distribution plots, correlation heatmap
