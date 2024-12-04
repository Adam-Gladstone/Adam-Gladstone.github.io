---
title:  "Python in Excel via Reticulate"
seo_title: "Calling a Python script from Excel using the R package Reticulate"
seo_description: "This post describes a particular use-case for Python in Excel and how it was solved using the R package Reticulate (version 1.39.0). "
layout: single
excerpt: "This post describes a particular use-case for Python in Excel and how it was solved using the R package [Reticulate 1.39.0](https://cran.r-project.org/web/packages/reticulate/index.html) along with the [ExcelRAddIn](https://github.com/Adam-Gladstone/Office365AddIns).A while back I read an interesting post on LinkedIn that identified a number of criteria that might be useful when selecting stocks for a portfolio.. "
excerpt_separator: "<!--more-->"
categories: 
  - R-project 
tags:
  - R 
  - r-project 
  - Python 
  - Excel 
---

### Introduction
This post describes a particular use-case for Python in Excel and how it was solved using the R package [Reticulate 1.39.0](https://cran.r-project.org/web/packages/reticulate/index.html) along with the [ExcelRAddIn](https://github.com/Adam-Gladstone/Office365AddIns).

A while back I read an interesting post on LinkedIn that identified a number of criteria that might be useful when selecting stocks for a portfolio. The specific criteria are: 
- Trailing PE < 25
- Forward PE < 15
- EPS Growth > 15%
- PEG Ratio < 1.2
- Market Cap < $5bn

The criteria were suggested from an article about [Peter Lynch](https://www.linkedin.com/pulse/title-timeless-wisdom-peter-lynch-invest-what-you-know-pushkar-raj-c5zlc/).

So I thought it would be a nice idea to get these indicators for a small portfolio of tech giant stocks and display the results in Excel using conditional formatting to determine if the stock selection is consistent with the desired criteria. The end result for this portfolio looks as follows: 

![Portfolio values and indicators](https://adam-gladstone.github.io/assets/images/final-result.PNG)

#### Python script
With the exception of 'Market Cap', the indicators are not available as part of Excel's 'Stock' data type. It took some time to figure out where the data could be sourced, and then some further experimentation around how best to get hold of the data. It turned out that the easiest approach was to use the Python library __yfinance__ to retrieve the ticker info, and from this select the indicators of interest. I wrote a short Python script to do this.

```
"""
equity_financials_alt.py
"""

import pandas as pd
import yfinance as yf


def get_value(info: dict, key: str) -> float:
    """Retrieve a value from the dictionary or 0 if it doesn't exist"""
    if key in info.keys():
        return info[key]
    return float(0.0)


def get_key_indicators(ticker: str) -> list:
    """Retrieve key indicators for ticker"""

    tk: dict = yf.Ticker(ticker)
    info: dict = tk.info

    indicators: list = [
        ticker,
        get_value(info, "trailingPE"),
        get_value(info, "forwardPE"),
        get_value(info, "earningsGrowth"),
        get_value(info, "pegRatio"),
        get_value(info, "marketCap"),
    ]

    return indicators


def get_all_indicators(tickers: list) -> pd.DataFrame:
    """Retrieve all indicators as a data frame"""

    rows: list = []
    headers: list = [
        "ticker",
        "trailingPE",
        "forwardPE",
        "earningsGrowth",
        "pegRatio",
        "marketCap",
    ]

    for ticker in tickers:
        rows.append(get_key_indicators(ticker))

    df = pd.DataFrame(rows, columns=headers)
    return df

```

The script consists of two functions: ```get_key_indicators``` takes a single ticker and requests all the ticker info. It then selects the indicators of interest and returns a list. It uses the utility function ```get_value``` to retrieve the requested value or 0 if the key is not available. The second function ```get_all_indicators``` calls the function above for each of the input tickers and returns a data frame. No doubt the Python script could be simplified and made more __pythonic__.

In fact, the initial version of the script saved the data frame to a `csv` file. Then, on the Excel side, it used a PowerQuery import to get the data from the `csv` file into a table. This seemed clumsy and I wanted a simpler, more direct, solution [^1]. 

This is where the R package Reticulate came to the rescue. It provides functionality to load and run Python scripts via R. The ExcelRAddIn allows you to run R scripts from an Excel worksheet. Putting the two together was simple.

#### Using Reticulate in Excel
Using Reticulate in Excel via the ExcelRAddIn was simple and consists of the following steps.

A. Load the reticulate library.
B. Tell reticulate where to find the Python version. The second parameter determines whether the requested copy of Python is required or not. 

![Loading Reticulate](https://adam-gladstone.github.io/assets/images/startup-reticulate.PNG)

If we are doing this routinely, it is useful to add Reticulate to the libraries that are loaded at startup.

![Reticulate environment](https://adam-gladstone.github.io/assets/images/env-reticulate.PNG)

C. Load the Python script, and check it compiles ok. For this we just evaluate the following R script in Excel: `source_python("D:/Development/Projects/Python/FinancialData/equity_financials_alt.py")`

D. Create an R vector of tickers for the indicators that we want.

![Create R vector](https://adam-gladstone.github.io/assets/images/tickers-vector.PNG)

E. Finally call the 'get_all_indicators' function, passing it the vector of tickers. 

![Retrieve the indicators](https://adam-gladstone.github.io/assets/images/all-indicators.PNG)

The result is a data frame with the values we want. We can then apply the conditional formatting to highlight the values that are consistent with the criteria. Using these criteria, we can see that the selected stocks are not consistent with the desired criteria (particularly the Trailing PE and the Forward PE). The amount of red indicating, at a glance, that almost none of the stocks fulfill the required criteria.

### Wrap-up
This post has described how to use the R package Reticulate to execute a Python script from Excel and retrieve the results. The Excel workbook can be downloaded from here:

[Call Python from R in Excel.xlsx](https://adam-gladstone.github.io/assets/images/Call-Python-from-R-in-Excel.xlsx).

The Python script can be downloaded from here: 
[equity_financials_alt.py](https://adam-gladstone.github.io/assets/images/equity_financials_alt.py). 

This use-case is quite particular (obtaining specific financial data from __yfinance__). However, the approach is more widely useful. On the other hand, there are a number of alternative approaches (web-scraping, using different finance libraries, and even using Python in Excel) that may be more appropriate. 


[^1]: I think it should have been possible to use Excel's Python function [PY=](https://support.microsoft.com/en-us/office/get-started-with-python-in-excel-a33fbcbe-065b-41d3-82cf-23d05397f53d). But it turns out that importing __yfinance__ produces a 'module not found' error. According to the documentation __yfinance__ is not one of the open source libraries that the Excel Python secure distribution [supports](https://support.microsoft.com/en-us/office/open-source-libraries-and-python-in-excel-c817c897-41db-40a1-b9f3-d5ffe6d1bf3e).
