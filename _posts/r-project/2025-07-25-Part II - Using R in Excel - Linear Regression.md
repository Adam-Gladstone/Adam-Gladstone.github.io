---
title:  "Part II - Using R in Excel - Linear Regression"
seo_title: "Demonstrates using R in Excel via the ExcelRAddIn to perform linear regression. "
seo_description: "This post demonstrates using the ExcelRAddIn to perform linear regression. "
layout: single
excerpt: "If you have ever wanted to use R's workhorse lm(...) function in an Excel worksheet, then this post may be of interest to you. "
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
---

### Introduction
In the [first part](https://adam-gladstone.github.io/r-project/Part-I-Using-R-in-Excel-Descriptive-Statistics/) of this series, I looked at using R in Excel to obtain descriptive statistics. In this second part of the series I am going to look at using R in Excel to perform linear regression, specifically using the ```lm()``` [function](https://www.rdocumentation.org/packages/stats/versions/3.6.2/topics/lm). ```lm()``` is a real workhorse function. It can be used to carry out both single and multiple regression and different types of analysis of variance. For this demonstration I will only focus on single and multiple regression.

The workbook for this part of the series is: ["Part II - R in Excel - Linear Regression.xlsx"](https://adam-gladstone.github.io/assets/images/Part-II-R-in-Excel-Linear-Regression.xlsx). As before, the 'References' worksheet lists links to external references. The 'Libraries' worksheet loads additional (non-default) packages. In this demonstration, I use the ```datarium``` and ```broom``` packages. The 'Datasets' worksheet contains the data referenced in the worksheets.

### The Data
The dataset is the marketing dataset from the ```datarium``` package. It consists of a data frame containing the impact of three advertising medias (youtube, facebook and newspaper) on sales. Data are the advertising budget in thousands of dollars along with the sales. The advertising experiment has been repeated 200 times. The dataset is described [here](https://search.r-project.org/CRAN/refmans/datarium/html/marketing.html).

![Marketing Dataset](https://adam-gladstone.github.io/assets/images/MarketingDataset.png)

If the dataset is not available, check that the ```datarium``` library is loaded by going to the Libraries worksheet and evaluating:

```=RScript.Evaluate(library(datarium), TRUE)```

### Simple Linear Regression
In the Simple Linear Regression worksheet we create a simple linear model. 

```smodel <- lm(sales ~ youtube, data = marketing)```

As we did in the first part of this series, we unpack the 'smodel'. Mostly this is simply a question of evaluating the corresponding R objects, for example the residuals and the coefficients. We also request the 95% confidence intervals for the coefficients.

![Residuals and Coefficients](https://adam-gladstone.github.io/assets/images/ResidualsAndCoefficients.png)

At this point, we can compare the results to the Summary Output provided by the Analysis ToolPak's regression function (including the 95% confidence intervals).

It's worth emphasising that the output that is returned to Excel via the add-in is not 'formatted' as it is in R/RStudio. If we call ```summary(smodel)``` in R we are presented with a familiar tabular output summarising the main features of the model. However, what is returned to Excel via the add-in is more basic. So it is worth spending some time looking at this. We can see from the add-in environment, that the ```smodel_summary``` is a list of 11 items. To use this we need to unpack some of the individual list items.

![Model Summary](https://adam-gladstone.github.io/assets/images/ModelSummaryList.png)

Here we can see the actual call made and the details of the model including the statistics (```sigma```, ```r-squared``` and so on). It needs some extra work to unpack the summary data from the model residuals in order to produce a tabular output.

```as.data.frame(as.array(summary(smodel$residuals)))```

This formula summarises the model residuals and coerces the data into an array first (to get the names) and then as a data frame. We perform a similar operation to get the coefficients into a tabular format.

With all the data available in this form, and with a little effort, we can now construct a summary output similar to R.

![Summary Output](https://adam-gladstone.github.io/assets/images/SummaryOutput.png)

### Multiple Linear Regression
The next worksheet demonstrates multiple linear regression using the same marketing data. This is similar to the previous worksheet and illustrates how to extract relevant values from the returned model data.

However, in this case we make use of the package ```broom```. This can help [tidy up](https://cran.r-project.org/web/packages/broom/vignettes/broom.html) the output data.

![Tidy Output](https://adam-gladstone.github.io/assets/images/TidyOutput.png)

In previous examples, we have extracted model results by concatenating the returned model name with labels from the model. To make it easier to retrieve results, the add-in provides some additional functions for querying models: ```Model.Results``` outputs a list of results from the model. ```Model.Result``` outputs the result obtained from one item of the list of model results. Optionally, the result can be formatted as a data frame. This is somewhat more convenient than having to evaluate scripts of the form ```model name'$coeffcients```, etc. By extracting the model data and the summary, we can construct an output that is similar to that provided by R.

### Logistic Regression
The final example demonstrates logistic regression. At this point you might be thinking that this massaging and extracting output data is not entirely satisfactory. It's a lot of work and it can be quite brittle (if the cell references change, for example). Furthermore, as the models become more complicated (see [Part III in the series](https://adam-gladstone.github.io/r-project/Part-III-Using-R-in-Excel-Forecasting/)) this approach potentially becomes messier. To mitigate this, the add-in provides a couple of wrapper functions around regression. These help with both the setup and the output of more complex models.

![Regression.GLM](https://adam-gladstone.github.io/assets/images/RegressionGLM.png)

The model inputs are specified as a block of parameters, and the function ```Regression.GLM``` is used instead of the R script equivalent using ```glm```. The model outputs can be 'queried' using the ```Model.Results``` and the ```Model.Result``` formulas. However, even with this, it takes some effort to output a summary similar to the one provided by R.

### Wrap Up
In this post, we have looked at how to use R in Excel to perform linear regression, and we have spent some time demonstrating how to extract the different components from the model data. This will be useful in the next two parts of this series.
