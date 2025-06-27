---
title:  "Calling C++ functions from R using Rcpp"
seo_title: "Calling native C++ functions from R using the Rcpp package"
seo_description: "This post describes the steps to take to create an Rcpp package in RStudio which calls some native C++ functions. "
layout: single
excerpt: "If you are an R/RStudio user and you are learning C/C++ then this blog post may be interesting. Suppose that you've written a function in C/C++ (or even a whole program). You know how to run your code from the command line, passing in arguments and so on. However, this is not necessarily very convenient. Wouldn't it be nice to have your C/C++ functionality available in R? Well you can. In a few easy steps (using Rcpp) you can make your C/C++ functions available in R/RStudio. "
excerpt_separator: "<!--more-->"
categories: 
  - R-project 
tags:
  - R 
  - r-project 
  - rcpp 
  - cpp
  - cplusplus 
---

### Introduction
If you are an R/RStudio user and you are learning C/C++ then this blog post may be interesting. Suppose that you've written a function in C/C++ (or even a whole program). You know how to run your code from the command line, passing in arguments and so on. However, this is not necessarily very convenient. Wouldn't it be nice to have your C/C++ functionality available in R? Well you can. In a few easy steps (using Rcpp) you can make your C/C++ functions available in R/RStudio.

This blog post describes the steps required. I won't dwell too much on the technicalities. The details are covered elsewhere: [Rcpp](http://adv-r.had.co.nz/Rcpp.html). What I'm interested in here is __setting up an Rcpp package that can call C++ functions from R/RStudio__. 

This project is no more than a starting point. Later on, I may add bells-and-whistles. The complete __FinancialFunctions__ project is available on GitHub [FinancialFunctions](https://github.com/Adam-Gladstone/FinancialFunctions).

We'll start off by creating an Rcpp package. This will give us a framework that we can use to *drop in* the C++ code. Then, we will tweak the Rcpp code to call our C++ functions and build the package. For reference we are using the following versions:
* R version 4.4.1
* RStudio version 2024.04.2 (Build 764)
* RTools version 4.4

### 1. Creating an Rcpp package
Follow these steps to create an Rcpp package. 

First, make sure Rcpp is installed. If not, just run the following command in RStudio: ``install.packages("Rcpp")``

- Select File > New Project ...
- In the New Project Wizard dialog, select New Directory
- In the Project Type page, scroll down the list of project types and select 'R Package using Rcpp'.

![R Package using Rcpp](https://adam-gladstone.github.io/assets/images/Rcpp-project-type.png)

- In the 'Create R Package using Rcpp' page, fill in the Directory name. In this case it is __FinancialFunctions__.
- Press the Create Project button. A new RStudio session is started, and the project opens with a helpful __Read-and-delete-me__ file. 

Navigate to the \src directory and open the file __rcpp_hello_world.cpp__. Here there is a test C++ function called ``rcpp_hello_world()`` which we can call from R after we build the package.

![Rcpp Hello World](https://adam-gladstone.github.io/assets/images/Rcpp-hello-world.png)

- Select the menu: Build > Build binary package

If everything goes okay, we should see a message similar to this:

```
...
packaged installation of 'FinancialFunctions' as FinancialFunctions_1.0.zip
─  DONE (FinancialFunctions)
[1] "D:/TEMP/FinancialFunctions_1.0.zip"

Binary package written to D:/TEMP
```

Now we have built a fully functional Rcpp package. Open the zip-file and copy the contents into your R library directory (e.g. D:\R\R-4.4.1\library). Then, in RStudio, run the following script:

```
> library(FinancialFunctions)		# Load the package
> results <- rcpp_hello_world()		# Call the C++ function
> results							# Print the results
[[1]]
[1] "foo" "bar"

[[2]]
[1] 0 1
```

### 2. Adding C++ code
Now that we have a working skeleton, we can add our own C++ functions to the package.

Copy the two files [__FinancialFunctions.h__](https://adam-gladstone.github.io/assets/images/FinancialFunctions.h) and [__FinancialFunctions.cpp__](https://adam-gladstone.github.io/assets/images/FinancialFunctions.cpp) into the __\src__ directory.

There are two functions declared in the header file: ``price`` and ``ytm`` (yield-to-maturity).

The price function computes the present value of a stream of periodic cashflows using a single discount rate. The yield-to-maturity function computes the single rate of return implied by the periodic cashflows and the price (present value).

The price function takes a vector of times and a vector of cashflows (for a bond these are the coupons and the final principal repayment). In addition, the function takes a single rate, which is used to discount all the cashflows.

The yield-to-maturity function also takes a vector of times and a vector of cashflows (as above) and a (bond) price. From this, it iteratively determines the single rate at which the periodic stream of cashflows should be discounted to obtain the supplied price.

### 3. Connecting R with C++ using Rcpp
Delete the file __rcpp_hello_world.cpp__ as we no longer need the test function. Then copy the file [__rcpp_functions.cpp__](https://adam-gladstone.github.io/assets/images/rcpp_functions.cpp) into the __\src__ directory. This file contains the functions that we want to **export** from C++ to R using Rcpp.

At the top of the file, we include the main Rcpp header file. This is followed by the STL vector include and finally, we include the declarations of our functions in __FinancialFunctions.h__.

The code in __rcpp_functions.cpp__ declares an Rcpp function called ``bond_price``. Most importantly, it is preceded by the line ``// [[Rcpp::export]]``. This attribute indicates that the function should be **exported**, that is, made visible to R. As simple as that. Rcpp takes care of all the details. All we are concerned about is what parameters we are passed and how to call our function and get the results.

The ``bond_price`` function takes as its parameters two numeric vectors (the times and the cashflows), and a rate (a double). These are passed in from R. The function returns a double value, the calculated price. The Rcpp function looks like this.

``` 
// [[Rcpp::export]]
double bond_price(Rcpp::NumericVector times, Rcpp::NumericVector cashflows, double rate)
{
  std::vector<double> _times = Rcpp::as<std::vector<double>>(times);
  std::vector<double> _cashflows = Rcpp::as<std::vector<double>>(cashflows);
  
  double price = FinancialFunctions::Bonds::price(_times, _cashflows, rate);
 
  return price;
}
```

Inside the function, the Rcpp types ``NumericVector`` are converted to ``std::vector<double>``, which is what our function expects. 

Finally we call our function and return the result.

The Rcpp code for ``bond_ytm`` is very similar.

Everything is now ready to be built. 

- Select the menu: Build > Build binary package. 

Keep our fingers crossed that we have not made any mistakes. If everything goes okay, we should see a message similar to this:

```
Binary package written to D:/Development/Projects/R
```

Copy the contents of the zip file into your R library directory as previously, overwriting the initial version of the package.

In order to check that everything works as expected, run the following script.

```
library(FinancialFunctions)
# Example: a 3 year bond with a face value of $100 makes annual coupon 
# payments of 10%. The current interest rate (with annual compounding) is 9%.
times <- c(1, 2, 3)
cashflows <- c(10, 10, 110)
rate <- 0.09

# Calculate price and yield to maturity
price <- FinancialFunctions::bond_price(times, cashflows, rate)
ytm <- FinancialFunctions::bond_ytm(times, cashflows, price)

# Display the results
price
ytm
```

There should be no errors. We can check the results against the manual calculations in a spreadsheet if required.

### Wrap up.
That's all there is to it. We now have a working Rcpp package that calls C/C++ functions from R.

But that really is only the beginning. There's a lot more that can be done. For starters, we could improve the project design by isolating our code in a static library. We could also add some test cases, perhaps using a package like 'testthat'. Finally, we could add a couple more functions: perhaps bond duration and convexity calculations. I might look at how to do all this in a future article. The complete project is available on GitHub, [FinancialFunctions](https://github.com/Adam-Gladstone/FinancialFunctions).
