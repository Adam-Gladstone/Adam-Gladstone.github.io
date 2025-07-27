# -*- coding: utf-8 -*-

"""
ticker_data.py

Retrieve ticker data from yfinance

"""

import pandas as pd
import yfinance as yf


def get_value(info: dict, key: str):
    """
    Retrieve a value from a ticker info dictionary
    or None if the key doesn't exist
    """

    if info is not None:
        if key in info.keys():
            return info[key]

    return None


def get_items(symbol: str, fields: list) -> list:
    """
    Retrieve data from the corresponding fields for the specified ticker
    """

    items: list = [symbol]

    try:
        tk: dict = yf.Ticker(symbol)
        info: dict = tk.info

        for field in fields:
            items.append(get_value(info, field))
    # pylint: disable=broad-exception-caught
    except Exception:
        # pylint: enable=broad-exception-caught
        pass

    return items


def get_ticker_data(symbols: list, fields: list) -> pd.DataFrame:
    """
    Retrieve the specified fields from the input tickers
    """

    headers: list = ["Ticker"]
    for field in fields:
        headers.append(field)

    rows: list = []

    try:
        for symbol in symbols:
            rows.append(get_items(symbol, fields))

    # pylint: disable=broad-exception-caught
    except Exception:
        # pylint: enable=broad-exception-caught
        print("An error occured")

    df = pd.DataFrame(rows, columns=headers)

    return df


def get_ticker_weights(ticker_values: dict) -> pd.DataFrame:
    """
    Returns:
        ticker_weights
    """

    # Set up the structure
    rows: list = []
    headers: list = ["ticker", "weight"]

    # Calculate the portfolio value
    total_portfolio_value = sum(ticker_values.values())

    for ticker, value in ticker_values.items():
        weight = value / total_portfolio_value
        rows.append([ticker, weight])

    df = pd.DataFrame(rows, columns=headers)

    return df



# tickers = ['SAN.MC', 'BBVA.MC', 'REP.MC', 'MAP.MC', 'AENA.MC']
# fields = ["trailingPE", "forwardPE", "earningsGrowth", "trailingPegRatio"]
# print(yf.__version__)
# print(get_ticker_data(tickers, fields))
