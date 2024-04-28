---
title:  "Office365 AddIns for R (Part III)"
seo_title: "The latest updates and enhancements to the ExcelRAddIn for Office365"
seo_description: "This post describes the latest updates and enhancements to the ExcelRAddIn. "
layout: single
excerpt: "A while back, I introduced the __ExcelRAddIn__ ([Office365 AddIns for R (Part I)](https://adam-gladstone.github.io/Office365AddIns-for-R-part-I/)). This is an Office365 AddIn that allows you to evaluate an R-script from within Excel and use the results. This blog-post describes some of the recent updates to the ExcelRAddIn. "
excerpt_separator: "<!--more-->"
categories: 
  - R-project 
tags:
  - R 
  - r-project 
  - Office365 
  - Excel 
---

### Introduction
A while back, I introduced the __ExcelRAddIn__ ([Office365 AddIns for R (Part I)](https://adam-gladstone.github.io/Office365AddIns-for-R-part-I/)). This is an Office365 AddIn that allows you to evaluate an R-script from within Excel and use the results. This blog-post describes some of the recent updates to the ExcelRAddIn. I focus on two specific areas. Firstly, I describe some ease of use features. Then I describe the function wrappers.

#### Ease of use features.
* As a convenience, users can now specify packages to load when the add-in is initialised. This is available from the Settings button on the R Tools AddIn ribbon.

![R Environment Settings](https://adam-gladstone.github.io/assets/images/r-environment-settings.png)

In the previous version, packages were loaded by executing the R-script `library(<package-name>)`. In this version, default package loading takes place on the first call to `RScript.Evaluate(...)`, so the first time any R-script is evaluated, there may be a slight delay depending on which and how many packages are loaded. Any issues with the package loading are reported to the R Environment AddIn panel (see below). 

![Default Package Loading](https://adam-gladstone.github.io/assets/images/default-package-loading.png)

* In the previous version, the three functions (`CreateVector`, `CreateMatrix`, and `CreateDataFrame`) which are used to pass data from Excel to R, used a final parameter 'Type'. This indicated the corresponding R-type (which can be 'character', 'complex', 'integer', 'logical', or 'numeric'). This is now optional; the R-type is determined from the data, if possible. This makes it somewhat easier to create objects to pass to R from Excel. For example, given an Excel table called 'GalapagosData' (from the [faraway dataset](https://rdrr.io/cran/faraway/)), we can create a data frame simply by passing in a name ("gala"), the data and the headers:

![CreateDataFrame](https://adam-gladstone.github.io/assets/images/create-data-frame.png)

* Two generic calls have been added: `RScript.Params` and `RScript.Function`. `RScript.Params` returns a list of parameters for the requested function and `RScript.Function` evaluates the specified function, possibly using some or all of the parameters retrieved from the call to `RScript.Params`.

![RScript.Params](https://adam-gladstone.github.io/assets/images/rscript-params.png)

* Some additional functions for querying models (i.e. objects returned from calls to 'lm', 'glm' etc) have been added: 
	`Model.Results` outputs a list of results from the model. 
	`Model.Result` outputs the result obtained from one item of the list of model results. Optionally, the result can be formatted as a data frame. This is somewhat more convenient than having to evaluate scripts of the form `'model name'$coeffcients`, etc.
	`Model.Accuracy` returns a number of statistics relating to measures of model accuracy.

![Model accuracy measures from 'forecast'](https://adam-gladstone.github.io/assets/images/model-accuracy.png)

#### Wrapper functions.
One of the motivations for updating the __ExcelRAddIn__ was to provide an improved experience when using more complex R functions in an Excel worksheet. The idea was to avoid building up a script by providing wrapper functions that can handle the variety of parameters passed to the underlying R functions. The option of using a script is always available. However, for a complex function like `auto.arima` (which can take up to 35 parameters) or `glm`, it is easier to setup a parameter dictionary with the appropriately named parameters and their values (as shown below)

![Logistic Regression Params](https://adam-gladstone.github.io/assets/images/glm-params.png)

rather than creating a script, for example: `logModel = glm(Purchase~Income+Age+ZipCode, data = purchase, family = binomial(link='logit'))`

This also makes it easier to see the effects of any updates to model parameters. As described above, the parameter names and their default values can be retrieved by using the `RScript.Params` function.

At the moment, wrapper functions have been provided for a number of the functions in the [__forecast__ library](https://cran.r-project.org/web/packages/forecast/forecast.pdf) and for the following two 'workhorse' functions:
* Regression.LM		- Fit a linear model to the data
* Regression.GLM	- Fit a generalised linear model to the data

A spreadsheet with examples based on the underlying packages can be downloaded from here: [Forecast.xlsx](https://adam-gladstone.github.io/assets/images/Forecast.xlsx).

### Wrap-up
In this blog-post I have described two sets of enhancements to the __ExcelRAddIn__. Firstly some ease of use features were described. Secondly, I outlined some function wrappers that provide an improved user experience when using complex R functions in Excel. I am still working on improving the default ('summary') output display of results. Overall, the __ExcelRAddIn__ seeks to provide access to R functionality from inside Excel in a way that is somewhat more flexible than the existing Data Analysis Toolpak. 
