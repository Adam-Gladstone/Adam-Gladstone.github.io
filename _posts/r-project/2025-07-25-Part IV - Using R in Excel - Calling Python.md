---
title:  "Part IV - Using R in Excel - Calling Python"
seo_title: "Demonstrates using R in Excel via the ExcelRAddIn to call Python scripts. "
seo_description: "This post demonstrates using the ExcelRAddIn to call Python scripts via R. "
layout: single
excerpt: "This post describes using R to call Python scripts inside Excel. "
excerpt_separator: "<!--more-->"
categories: 
  - R-project 
tags:
  - R 
  - RStudio
  - r-project 
  - Office365 
  - Excel
  - ExcelRAddIn
  - Python
  - python-project
---

### Introduction
In the last post in this series I am going to look at calling Python from R. Even though Excel now provides a means of calling Python scripts directly, using the ```=PY()``` formula in a worksheet, there are still occasions when it is beneficial to call Python via R. For example, it turns out that importing ```yfinance``` produces a 'module not found' error using Excel's function. According to the documentation, ```yfinance``` is not one of the open source libraries that the Excel Python secure distribution supports. To get around this issue, we can use the R package [__Reticulate__](https://cran.r-project.org/web/packages/reticulate/index.html). This lets us load and run Python scripts from R. As we have seen in the previous parts of this series, the __ExcelRAddIn__ allows us to run R scripts from an Excel worksheet. And putting these two together is quite simple.

The workbook for this part of the series is: ["Part IV - R in Excel - Calling Python.xlsx"](https://adam-gladstone.github.io/assets/images/Part-IV-R-in-Excel-Calling-Python.xlsx). As before, the 'References' worksheet lists links to external references. The 'Libraries' worksheet loads additional (non-default) packages. In this demonstration, I use the 'reticulate' package and this is loaded here. The 'Datasets' worksheet contains the data referenced in the worksheets. In addition there are two auxilliary workksheets: Session Info and Setup. The Session Info retrieves information about the R environment and R version. The Setup worksheet performs some initialisation required for the reticulate package. First we point to the Python executable that we want to use. Next, we confirm the Python version is actually the one requested. Finally we set up a section that we can return to if there are errors from reticulate and Python itself. It is worth ensuring that these cells are evaluated correctly.

### Ticker Info
This worksheet requests some basic ticker info for a number of stocks. The first step is to load the script [ticker_data.py](https://adam-gladstone.github.io/assets/images/ticker_data.py) and ensure it compiles.

#### The Python script
The script consists of two main functions: ```get_ticker_data``` and ```get_ticker_weights```. 

```
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
```

```get_ticker_data``` takes a list of ticker symbols and a list of fields. The fields are the items we want to retrieve from yfinance's ticker info function. It uses the utility function ```get_value``` to retrieve the requested value or 0 if the key is not available. No doubt the Python script could be simplified and made more pythonic.

In the worksheet, we create a vector of tickers and a vector of fields, and then call the Python function.

![Ticker Info](https://adam-gladstone.github.io/assets/images/TickerInfo.png)

The result is a data frame with the values for the fields that we requested (if available).

#### Portfolio Weights
The second function ```get_ticker_weights```, simply computes the weights of a list of ticker symbols. The Python function requires that the input is a dictionary of symbols and their corresponding values. Therefore we create a ```ticker_list``` via R, since Reticulate converts R lists to Python dictionaries. The construction is somewhat mechanical and could certainly be improved just by changing the Python function inputs. With the ```ticker_list``` created we can call the Python function.

![Portfolio Weights](https://adam-gladstone.github.io/assets/images/PortfolioWeights.png)

This returns the portfolio weights which we can use to display graphically. From here, we could extend the Python code to compute portfolio returns for the tickers over a specified period. We could then compare the returns with a benchmark, and compute Sharpe ratios for the components.

### Wrap up
In this post we have seen how to call Python scripts from R using the Reticulate package. While the setup is not completely trivial, it is worth bearing in mind the advantages of this approach: from within Excel, we have access to both R and Python's extensive ecosystems, which in turn gives us a good deal of flexibility in creating solutions. And that concludes this series of posts on using R in Excel. I hope this has been useful.
