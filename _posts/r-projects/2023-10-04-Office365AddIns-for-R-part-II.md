---
title:  "Office365 AddIns for R (Part II)"
seo_title: "Evaluate R scripts directly in an Office365 Word document and display the results inline."
seo_description: "This Office365 AddIn for Word allows you to evaluate an R script in a Word document and present the results inline."
layout: single
excerpt: "In the previous post [Office365 AddIns for R (Part I)](https://adam-gladstone.github.io/Office365AddIns-for-R-part-I/), I introduced the __ExcelRAddIn__. In this post I would like to describe the __RScriptAddIn__ for Word."
excerpt_separator: "<!--more-->"
categories: 
  - R-project
tags:
  - R 
  - r-project 
  - Office365 
  - Word
---

### Introduction
In the previous post [Office365 AddIns for R (Part I)](https://adam-gladstone.github.io/Office365AddIns-for-R-part-I/), I introduced the __ExcelRAddIn__. In this post I would like to describe the __RScriptAddIn__ for Word. This allows you to run an R script 'inline' from within a Word document. I read [R-bloggers](http://www.R-bloggers.com) regularly and I thought this add-in might be useful. In this post I will run through a simple demo.

#### RScriptAddIn
Imagine a situation where you want to write a document explaining how to use some feature of R, for example the F-test. You open Word and begin writing; you write the equations as usual:

![F test](https://adam-gladstone.github.io/assets/images/f-test-doc.png)

and then you get to the section 'Compute the F-test in R'. You write the corresponding R script in the document. The RScriptAddIn allows you to execute the script inline and to see the results. 

Select the script, and from the Add-Ins menu select the Run Script button. The script is evaluated (assuming the path has been set up correctly - if not use the settings for this purpose) and the data is added to the R environment.

![Run script 1](https://adam-gladstone.github.io/assets/images/run-script-1.png)

You continue writing the document and executing the R script.

![Run script 2](https://adam-gladstone.github.io/assets/images/run-script-2.png)

One caveat here is that the F-test results are returned in an un-summarized form, and in this case there doesn't seem to be an easy way to coerce the result to a data frame for improved tabular display. Therefore you may need to format this yourself.

![Formatted output](https://adam-gladstone.github.io/assets/images/manual-format.png)

I am looking for a way to improve this.

### Wrap-up
As in the previous post, I want to reiterate that the projects are still in an 'alpha' stage, meaning you will need to download the project [Office365Addins](https://github.com/Adam-Gladstone/Office365AddIns), build the Visual Studio solution, and install or run it directly from Visual Studio.



