import os
import tkinter as tk
from tkinter import ttk, messagebox
import pandas as pd
import numpy as np
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg

DATA_PATH = os.path.join(os.path.dirname(__file__), 'all_stocks_5yr.csv')


def load_data():
    df = pd.read_csv(DATA_PATH, parse_dates=['date'])
    df = df.dropna()
    df = df.sort_values(['Name', 'date'])
    return df


class StockApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Stock Market Analysis Dashboard")
        self.root.geometry("1100x700")

        self.df = load_data()
        self.all_tickers = sorted(self.df['Name'].unique())

        self._build_ui()

    def _build_ui(self):
        # Left control panel
        ctrl = tk.Frame(self.root, width=220, bg="#2b2b2b")
        ctrl.pack(side=tk.LEFT, fill=tk.Y, padx=0, pady=0)
        ctrl.pack_propagate(False)

        tk.Label(ctrl, text="Stock Dashboard", bg="#2b2b2b", fg="white",
                 font=("Helvetica", 14, "bold")).pack(pady=(20, 5))

        tk.Label(ctrl, text="Enter tickers (comma-separated):", bg="#2b2b2b",
                 fg="#aaaaaa", wraplength=190).pack(pady=(10, 2))

        self.ticker_entry = tk.Entry(ctrl, font=("Helvetica", 11))
        self.ticker_entry.insert(0, "AAPL, GOOGL, MSFT")
        self.ticker_entry.pack(padx=10, fill=tk.X)

        tk.Label(ctrl, text="Analysis:", bg="#2b2b2b", fg="#aaaaaa").pack(pady=(15, 2))

        btn_style = {"bg": "#4a90d9", "fg": "white", "font": ("Helvetica", 10),
                     "relief": tk.FLAT, "cursor": "hand2", "pady": 6}

        tk.Button(ctrl, text="Cumulative Returns", command=self.plot_cumulative,
                  **btn_style).pack(fill=tk.X, padx=10, pady=3)
        tk.Button(ctrl, text="Moving Averages", command=self.plot_moving_avg,
                  **btn_style).pack(fill=tk.X, padx=10, pady=3)
        tk.Button(ctrl, text="Volatility", command=self.plot_volatility,
                  **btn_style).pack(fill=tk.X, padx=10, pady=3)
        tk.Button(ctrl, text="Correlation Heatmap", command=self.plot_correlation,
                  **btn_style).pack(fill=tk.X, padx=10, pady=3)
        tk.Button(ctrl, text="Summary Statistics", command=self.show_summary,
                  **btn_style).pack(fill=tk.X, padx=10, pady=3)

        # Right chart area
        self.chart_frame = tk.Frame(self.root, bg="white")
        self.chart_frame.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True)

        self.canvas = None
        self._show_welcome()

    def _show_welcome(self):
        fig, ax = plt.subplots(figsize=(8, 5))
        ax.text(0.5, 0.5, "Select tickers and an analysis\nto get started",
                ha='center', va='center', fontsize=14, color='gray',
                transform=ax.transAxes)
        ax.axis('off')
        self._draw(fig)

    def _get_tickers(self):
        raw = self.ticker_entry.get()
        tickers = [t.strip().upper() for t in raw.split(',') if t.strip()]
        missing = [t for t in tickers if t not in self.all_tickers]
        if missing:
            messagebox.showwarning("Unknown tickers", f"Not found in dataset: {', '.join(missing)}")
            tickers = [t for t in tickers if t in self.all_tickers]
        return tickers

    def _get_data(self, tickers):
        data = self.df[self.df['Name'].isin(tickers)].copy()
        data['daily_return'] = data.groupby('Name')['close'].pct_change()
        return data

    def _draw(self, fig):
        if self.canvas:
            self.canvas.get_tk_widget().destroy()
        self.canvas = FigureCanvasTkAgg(fig, master=self.chart_frame)
        self.canvas.draw()
        self.canvas.get_tk_widget().pack(fill=tk.BOTH, expand=True)
        plt.close(fig)

    def plot_cumulative(self):
        tickers = self._get_tickers()
        if not tickers:
            return
        data = self._get_data(tickers)
        data['cumulative_return'] = data.groupby('Name')['daily_return'].transform(
            lambda x: (1 + x).cumprod() - 1)

        fig, ax = plt.subplots(figsize=(8, 5))
        for ticker in tickers:
            s = data[data['Name'] == ticker]
            ax.plot(s['date'], s['cumulative_return'], label=ticker)
        ax.set_title('Cumulative Returns')
        ax.set_ylabel('Return')
        ax.legend()
        fig.tight_layout()
        self._draw(fig)

    def plot_moving_avg(self):
        tickers = self._get_tickers()
        if not tickers:
            return
        data = self._get_data(tickers)
        data['ma20'] = data.groupby('Name')['close'].transform(lambda x: x.rolling(20).mean())
        data['ma50'] = data.groupby('Name')['close'].transform(lambda x: x.rolling(50).mean())

        fig, axes = plt.subplots(len(tickers), 1, figsize=(8, 4 * len(tickers)), squeeze=False)
        for i, ticker in enumerate(tickers):
            s = data[data['Name'] == ticker]
            ax = axes[i][0]
            ax.plot(s['date'], s['close'], label='Close', alpha=0.6)
            ax.plot(s['date'], s['ma20'], label='20-day MA')
            ax.plot(s['date'], s['ma50'], label='50-day MA')
            ax.set_title(f'{ticker} — Moving Averages')
            ax.legend()
        fig.tight_layout()
        self._draw(fig)

    def plot_volatility(self):
        tickers = self._get_tickers()
        if not tickers:
            return
        data = self._get_data(tickers)
        data['volatility'] = data.groupby('Name')['daily_return'].transform(
            lambda x: x.rolling(30).std())

        fig, ax = plt.subplots(figsize=(8, 5))
        for ticker in tickers:
            s = data[data['Name'] == ticker]
            ax.plot(s['date'], s['volatility'], label=ticker)
        ax.set_title('30-Day Rolling Volatility')
        ax.set_ylabel('Std Dev of Daily Returns')
        ax.legend()
        fig.tight_layout()
        self._draw(fig)

    def plot_correlation(self):
        tickers = self._get_tickers()
        if not tickers:
            return
        data = self._get_data(tickers)
        pivot = data.pivot_table(index='date', columns='Name', values='daily_return')
        corr = pivot.corr()

        fig, ax = plt.subplots(figsize=(6, 5))
        im = ax.imshow(corr.values, cmap='coolwarm', vmin=-1, vmax=1)
        plt.colorbar(im, ax=ax)
        ax.set_xticks(range(len(tickers)))
        ax.set_yticks(range(len(tickers)))
        ax.set_xticklabels(tickers)
        ax.set_yticklabels(tickers)
        for i in range(len(tickers)):
            for j in range(len(tickers)):
                ax.text(j, i, f'{corr.iloc[i, j]:.2f}', ha='center', va='center')
        ax.set_title('Return Correlation Heatmap')
        fig.tight_layout()
        self._draw(fig)

    def show_summary(self):
        tickers = self._get_tickers()
        if not tickers:
            return
        data = self._get_data(tickers)
        summary = data.groupby('Name')['daily_return'].agg(
            Mean_Return='mean',
            Volatility='std',
            Total_Return=lambda x: (1 + x).prod() - 1
        ).round(4)

        fig, ax = plt.subplots(figsize=(7, 3))
        ax.axis('off')
        table = ax.table(
            cellText=summary.reset_index().values,
            colLabels=['Ticker'] + list(summary.columns),
            cellLoc='center',
            loc='center'
        )
        table.auto_set_font_size(False)
        table.set_fontsize(11)
        table.scale(1.2, 2)
        ax.set_title('Summary Statistics', pad=20)
        fig.tight_layout()
        self._draw(fig)


if __name__ == '__main__':
    root = tk.Tk()
    app = StockApp(root)
    root.mainloop()
