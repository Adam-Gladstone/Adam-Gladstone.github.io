---
title:  "Calling Python from C# using Python.NET"
seo_title: "Calling Python from C# using Python.NET"
seo_description: "This post provides a brief guide to using Python.NET in a C# desktop application to call Python functions."
layout: single
excerpt: "Recently, I've been using Python's __yfinance__ library to perform some simple portfolio analysis. Rather than using a Jupyter notebook to run the Python code and visualise the results, I thought it might be a nice idea to build a .NET desktop application using WinUI 3.0, XAML and C#. The application allows you to define a portfolio and manages the presentation of the results graphically. The underlying analysis is performed using Python. In order to call the Python code from C#, I use [Python.NET](https://github.com/pythonnet/pythonnet). The purpose of this blog post is to describe how to use Python.NET to call Python functions from a C# application. The complete application is available on github: (https://github.com/Adam-Gladstone/PortfolioManager)."
excerpt_separator: "<!--more-->"
categories: 
  - python-project 
tags:
  - Python 
  - yfinance 
  - WinUI 3.0
  - C#
---

### Introduction
Recently, I've been using Python's __yfinance__ library to perform some simple portfolio analysis. Rather than using a Jupyter notebook to run the Python code and visualise the results, I thought it might be a nice idea to build a .NET desktop application using WinUI 3.0, XAML and C#. The application allows you to define a portfolio and manages the presentation of the results graphically. The underlying analysis is performed using Python. In order to call the Python code from C#, I use [Python.NET](https://github.com/pythonnet/pythonnet). The purpose of this blog post is to describe how to use __Python.NET__ to call Python functions from a C# application. The complete application is available on github (https://github.com/Adam-Gladstone/PortfolioManager). 

![Portfolio Manager](https://adam-gladstone.github.io/assets/images/PortfolioAnalysisResults.png)

The main advantage of this approach is that it allows access to Python's extensive ecosystem from .NET. In this specific case, I wanted to build a simple portfolio management application while at the same time taking advantage of Python's __yfinance__ library to get the financial data I wanted and to use __pandas__ and __numpy__ to perform the calculations. I also wanted a slightly more real-world project using __Python.NET__. Information about this is somewhat limited and the examples are a little sketchy. 

#### Versions
We use the following versions:
- Python 3.12
- yfinance 0.2.54
- Python.NET 3.0.5

#### The Python API
To start off, I wrote a simple [portfolio analysis script](https://adam-gladstone.github.io/assets/images/portfolio_analysis.py). The script is based on a [portfolio management app](https://medium.com/python-in-plain-english/building-an-investment-portfolio-management-app-with-python-a68c2841f04b) written in Python. However, I refactored the main functionality in order to separate the calculations and analysis from the (graphical) presentation layer. This allowed me to call the Python functions from C# to obtain the data and then process the (converted) data in the C# application.

The API consists of four functions.

1. ```portfolio_returns(ticker_values, start_date, end_date)```
This function takes the user-supplied tickers (and values), start date and end date. The function computes the ticker weights and obtains the adjusted close prices (if available) for each ticker using the __yfinance__ library. The function returns a dictionary with the ticker weights, a DataFrame containing the individual ticker returns, and the overall portfolio returns.

2. ```perform_portfolio_analysis(data, ticker_weights, risk_free_rate)```
This function takes the portfolio returns DataFrame computed previously, the ticker weights, and a user-supplied risk free rate and uses this to calculate individual security returns, cumulative returns, volatility, and Sharpe Ratios. These are returned in a dictionary.

3. ```benchmark_returns(benchmark, start_date, end_date)```
This function obtains the benchmark data from __yfinance__ using the supplied parameters. It also returns a dictionary.

4. ```portfolio_vs_benchmark(port_returns, benchmark_returns, risk_free_rate)```
This function calculates the cumulative returns, annualized volatility, and Sharpe Ratios for both the portfolio and the benchmark using the data obtained in the previous functions. It provides a side-by-side comparison to assess the portfolio's performance relative to the benchmark.

These four functions define the API that is used by the .NET application.

#### The .NET Application
##### Prerequisites 
For the .NET application we first need to download and build Python.NET. The code is available from https://github.com/pythonnet/pythonnet. Once downloaded, open the solution file (```pythonnet.sln```), and select the __Python.Runtime__ as the startup project. Then right-click and build the debug version. If the build is successful the ```Python.Runtime.dll``` will be located in the pythonnet directory under \pythonnet\runtime\.

##### The PortfolioManager Application
Having built the ```Python.Runtime.dll```, we need to add it to the Portfolio Manager application. This is a WinUI 3.0 (C#/XAML) application which makes use of the [Windows Community Toolkit](https://github.com/CommunityToolkit/Windows) for dependency injection and the MVVM architecture. It also uses an Sqlite database to manage a collection of one or more portfolios.

Aside from the test framework (__PortfolioManager.Tests.MSTest__), the solution consists of two main projects: the __PortfolioManager__ and __PortfolioManager.Core__. The __PortfolioManager__ project deals with the application logic, user settings, the views and the view models. The reusable logic and data models are located in the __PortfolioManager.Core__ project. So we add the ```Python.Runtime.dll``` to the __Dependencies__ here under the __Assemblies__ node.

![Python.NET Runtime](https://adam-gladstone.github.io/assets/images/PythonNetRuntime.png)

##### The Python service
In the core library, we define a simple ```IPythonService``` interface that encapsulates the initialisation and the calls to the Python API.

``` 
public interface IPythonService
{
    void Initialize(string pythonDll);

    bool RunPortfolioAnalysis(PortfolioItem portfolio);
}
```

In the __PortfolioManager__ project, in the App.xaml.cs, we add the ```IPythonService``` to the list of services to be activated
```
...
services.AddSingleton<IPythonService, PythonService>();
```

Finally, we pass an instance of the ```IPythonService``` into the ```PortfolioDetailViewModel```. This view model manages the graphs output as a result of running the portfolio analysis. When the view is activated after clicking on the 'Run' button, the ```PythonService``` can be initialised and the view model can run the portfolio analysis based on the selected portfolio.

```
    public PortfolioDetailViewModel(IPythonService pythonService)
    {
        _pythonService = pythonService;

        var settings = App.GetService<SettingsViewModel>();

        var pythonDll = settings.PythonLibrary;
        _pythonService.Initialize(pythonDll);

		//...
    }
```

Initialisation of the ```PythonService``` consists of setting the path to the Python dll. This is configured via the application settings page. Additionally, we set up a couple of empty output streams to redirect any console output from the Python.Runtime.

#### Portfolio Analysis
The main function ```RunPortfolioAnalysis``` is called with the currently selected ```PortfolioItem```. The ```PortfolioItem``` contains the user supplied parameters which have been obtained from the UI.

![Portfolio Analysis Parameters](https://adam-gladstone.github.io/assets/images/PortfolioAnalysisParams.png)

The ```RunPortfolioAnalysis``` function loads the [portfolio_analysis.py](https://adam-gladstone.github.io/assets/images/portfolio_analysis.py) script and passes it to Python.NET, which creates a Python ```module``` object. The ```module``` object is used to access the script functions and variables. We use C#'s 'dynamic' keyword to delay the binding. We can see the available dynamically bound functions and parameters if we expand the ```module``` variable in the Watch window.

![Dynamic binding](https://adam-gladstone.github.io/assets/images/PortfolioAnalysisDynamicModule.png)

The portfolio analysis proceeds by calling the Python functions using the user-supplied parameters and any intermediate results. Once these have been appropriately converted they are copied into the portfolio item's data members. 
```
	...
	dynamic portfolioResults = module.portfolio_returns(tickers, startDate, endDate);

	var pyTickerWeights = new PyDict(portfolioResults["weights"]);

	portfolio.TickerWeights = Interop.Converters.ConvertTickerWeights(pyTickerWeights);
	...
```
In this snippet, the Python object ```pyTickerWeights``` is extracted from the dictionary returned from calling ```module.portfolio_returns```. The Python 'dict' is converted into a C# ```List<TickerWeight>```. The ```ConvertTickerWeights``` function just iterates over each ticker and obtains the corresponding weight. This is then assigned to the ```TickerWeights``` member of the portfolio item. The ```TickerWeights``` list is then used in a Pie Chart that displays the percentage allocation of tickers in the portfolio.

Once the analysis is complete, the ```PortfolioDetailViewModel``` initialises the ```PlotModel``` with the data from the portfolio item, which then updates the graph view as it is bound to the specific ```PlotModel```.

It is worth highlighting that the performance is quite slow. There seem to be two main aspects to this:
1. The initialisation of the Python engine seems to take some time, and perhaps this could be done once at startup.
2. The ```PortfolioDetailViewModel``` renders six graphs with different datasets serially. It seems to me that this might be better refactored to use C# asynchronous processing. 

I am currently investigating both these issues.

#### The interop layer
This layer provides facilities to convert between C# and Python types. Basic types (strings, ints, doubles etc.) are converted transparently. From C#, we use the ```.ToPython()``` extension method to convert to a Python object. And from Python, we use the ```.AsManagedObject(typeof(T))``` function to return a C# object which we can then cast. Converting from a pandas DataFrame or series can be somewhat more involved.

### Wrap-up
This blog post has described how to call Python functions from a C# desktop application using Python.NET. This arrangement (WinUI 3.0 C# front-end, Python.NET and Python) has the advantage of flexibility. The approach is quite generalisable. I could just as easily have created a TensorFlow model and called it from a C# application, if that had been my interest. On the other hand, the main disadvantage is the slow performance. This is an area that I am still currently investigating.

