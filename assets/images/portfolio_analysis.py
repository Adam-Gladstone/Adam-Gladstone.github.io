"""
portfolio_analysis.py

This script is based on: 'Building an Investment Portfolio Management App with Python' by Luís Fernando Torres
(https://medium.com/python-in-plain-english/building-an-investment-portfolio-management-app-with-python-a68c2841f04b)

It has been refactored in order to separate the analysis (and calculations) functions from 
the presentation of the results (graphs) in a jupyter notebook (portfolio_analysis.ipynb).
The portfolio_analysis.py functions are used in the PortfolioManager (C#/WinUI) application.

[X] flake8  - E501 line too long (multiple)
[X] black   - passed
"""

# Pandas & NumPy
import pandas as pd
import numpy as np

# yfinance to retrieve financial data
import yfinance as yf

import warnings

warnings.filterwarnings("ignore")


def portfolio_returns(ticker_values: dict, start_date: str, end_date: str) -> dict:
    """
    Returns:
        "weights" (ticker_weights),
        "data" (dataframe),
        "portfolio returns" (returns)
    """
    # Get ticker data with yfinance
    df: pd.DataFrame = yf.download(
        tickers=list(ticker_values.keys()), start=start_date, end=end_date, auto_adjust=False
    )

    # Check if there is data available in the given date range
    if isinstance(df.columns, pd.MultiIndex):
        missing_data_tickers = []
        for ticker in ticker_values.keys():
            first_valid_index = df["Adj Close"][ticker].first_valid_index()
            if (
                first_valid_index is None
                or first_valid_index.strftime("%Y-%m-%d") > start_date
            ):
                missing_data_tickers.append(ticker)

        if missing_data_tickers:
            raise ValueError(
                f"No data available for the following tickers starting from {start_date}: {', '.join(missing_data_tickers)}"
            )
            return
    else:
        # For a single ticker, simply check the first valid index
        first_valid_index = df["Adj Close"].first_valid_index()
        if (
            first_valid_index is None
            or first_valid_index.strftime("%Y-%m-%d") > start_date
        ):
            raise ValueError(
                f"No data available for the ticker starting from {start_date}"
            )
            return

    # Calculate the portfolio value
    total_portfolio_value = sum(ticker_values.values())

    # Calculate the weights for each security in the portfolio
    ticker_weights = {
        ticker: value / total_portfolio_value for ticker, value in ticker_values.items()
    }

    # Check if dataframe has MultiIndex columns
    if isinstance(df.columns, pd.MultiIndex):
        df = df["Adj Close"].fillna(
            df["Close"]
        )  # If 'Adjusted Close' is not available, use 'Close'

    # Check if there is more than one security in the portfolio
    if len(ticker_weights) > 1:
        weights = list(ticker_weights.values())  # Obtain weights
        weighted_returns = df.pct_change().mul(
            weights, axis=1
        )  # Computed weighted returns
        port_returns = weighted_returns.sum(
            axis=1
        )  # Sum weighted returns to build portfolio returns
    # If there is only one security in the portfolio...
    else:
        df = df["Adj Close"].fillna(
            df["Close"]
        )  # Obtain 'Adjusted Close'. If not available, use 'Close'
        port_returns = df.pct_change()  # Computing returns without weights

    results = {"weights": ticker_weights, "data": df, "portfolio returns": port_returns}

    return results


def perform_portfolio_analysis(
    df: pd.DataFrame, ticker_weights: dict, risk_free_rate: float
) -> dict:
    """
    This function takes historical stock data and the weights of the securities in the portfolio,
    It calculates individual security returns, cumulative returns, volatility, and Sharpe Ratios.

    Parameters:
    - df (pd.DataFrame): DataFrame containing historical stock data with securities as columns.
    - tickers_weights (dict): A dictionary where keys are ticker symbols (str) and values are their
        respective weights (float)in the portfolio.

    Returns:
        "individual cumulative returns" (individual_cumsum),
        "individual volatility" (individual_vol),
        "individual Sharpe ratio"  (individual_sharpe),

    Notes:
    """

    # DataFrame and Series
    individual_cumsum = pd.DataFrame()
    individual_vol = pd.Series(dtype=float)
    individual_sharpe = pd.Series(dtype=float)

    # Loop through tickers and weights in the tickers_weights dictionary
    for ticker, weight in ticker_weights.items():
        if ticker in df.columns:  # Check that the tickers are available
            individual_returns = df[
                ticker
            ].pct_change()  # Compute individual daily returns for each ticker

            individual_cumsum[ticker] = (
                (1 + individual_returns).cumprod() - 1
            ) * 100  # Compute cumulative returns over the period for each ticker

            vol = (
                individual_returns.std() * np.sqrt(252)
            ) * 100  # Compute annualized volatility
            individual_vol[ticker] = vol  # Add annualized volatility for each ticker
            individual_excess_returns = (
                individual_returns - risk_free_rate / 252
            )  # Compute the excess returns
            sharpe = (
                individual_excess_returns.mean()
                / individual_returns.std()
                * np.sqrt(252)
            ).round(
                2
            )  # Compute the Sharpe Ratio
            individual_sharpe[ticker] = sharpe  # Add the Sharpe Ratio for each ticker

    results = {
        "individual cumulative returns": individual_cumsum,
        "individual volatility": individual_vol,
        "individual Sharpe ratio": individual_sharpe,
    }

    return results


def benchmark_returns(benchmark: str, start_date: str, end_date: str) -> dict:

    # Obtain benchmark data with yfinance
    benchmark_df = yf.download(benchmark, start=start_date, end=end_date, auto_adjust=False)

    # Obtain 'Adjusted Close'. If not available, use 'Close'.
    benchmark_df = benchmark_df["Adj Close"].fillna(benchmark_df["Close"])

    # Compute benchmark returns
    benchmark_returns = benchmark_df.pct_change()

    results = {"benchmark returns": benchmark_returns}

    return results


def portfolio_vs_benchmark(
    port_returns: pd.Series, benchmark_returns: pd.Series, risk_free_rate: float
) -> dict:
    """
    This function calculates and displays the cumulative returns, annualized volatility, and Sharpe Ratios
    for both the portfolio and the benchmark. It provides a side-by-side comparison to assess the portfolio's
    performance relative to the benchmark.

    Parameters:
    - port_returns (pd.Series): A Pandas Series containing the daily returns of the portfolio.
    - benchmark_returns (pd.Series): A Pandas Series containing the daily returns of the benchmark.

    Returns:
        "portfolio cumulative returns": portfolio_cumsum,
        "benchmark cumulative returns": benchmark_cumsum,
        "portfolio volatility": port_vol,
        "benchmark volatility": benchmark_vol,
        "excess portfolio returns": excess_port_returns,
        "portfolio sharpe ratio": port_sharpe,
        "excess benchmark returns": excess_benchmark_returns,
        "benchmark sharpe ratio": benchmark_sharpe,
    """

    # Compute the cumulative returns for the portfolio and the benchmark
    portfolio_cumsum = (((1 + port_returns).cumprod() - 1) * 100).round(2)
    benchmark_cumsum = (((1 + benchmark_returns).cumprod() - 1) * 100).round(2)

    # Compute the annualized volatility for the portfolio and the benchmark
    port_vol = ((port_returns.std() * np.sqrt(252)) * 100).round(2)
    benchmark_vol = ((benchmark_returns.std() * np.sqrt(252)) * 100).round(2)

    # Compute the Sharpe Ratio for the portfolio and the benchmark
    excess_port_returns = port_returns - risk_free_rate / 252
    port_sharpe = (
        excess_port_returns.mean() / port_returns.std() * np.sqrt(252)
    ).round(2)
    excess_benchmark_returns = benchmark_returns - risk_free_rate / 252
    benchmark_sharpe = (
        excess_benchmark_returns.mean() / benchmark_returns.std() * np.sqrt(252)
    ).round(2)

    results = {
        "portfolio cumulative returns": portfolio_cumsum,
        "benchmark cumulative returns": benchmark_cumsum,
        "portfolio volatility": port_vol,
        "benchmark volatility": benchmark_vol,
        "excess portfolio returns": excess_port_returns,
        "portfolio sharpe ratio": port_sharpe,
        "excess benchmark returns": excess_benchmark_returns,
        "benchmark sharpe ratio": benchmark_sharpe,
    }

    return results


"""
tickers = {
    'SAB.MC' : (1000.0),
    'FER.MC' : (750.0),
    'ITX.MC' : (250.0),
    'MEL.MC' : (2000.0)
}

start: str = '2020-02-18'
end: str = '2025-02-18'
risk_free_rate: float = 0.0125

portfolio_results = portfolio_returns(tickers, start, end)
benchmark_results = benchmark_returns('^IBEX', start, end)

port_returns = portfolio_results['portfolio returns']
benchmark_returns = benchmark_results['benchmark returns']

comparative_results = portfolio_vs_benchmark(port_returns, benchmark_returns, risk_free_rate)
print(comparative_results)

df = portfolio_results['data']
ticker_weights = portfolio_results['weights']
analysis_results = perform_portfolio_analysis(df, ticker_weights, risk_free_rate)
print(analysis_results)
"""
