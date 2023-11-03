---
title: "About Me"
permalink: "/about/"
---

## About me
Hi. My name is Adam Gladstone. Welcome to my personal website. By profession, I am a [quantitative developer](https://www.linkedin.com/in/adam-gladstone-b6458b156/), but I also enjoy software development as a hobby. Things around software change really quickly, so there's always loads to learn, lots of new tools and some new approaches. So this website is just a collection of personal projects that reflect areas that I am interested in and technologies that I am learning about. 

## Current Interests
I mostly develop in C++ and C# but I also use Python and R depending on the project. I like to keep up with the latest enhancements in C++20 and C++23. I regularly follow [Jason Turner](https://github.com/lefticus), [Marius Bancila](https://mariusbancila.ro/blog/), [CppStories](https://www.cppstories.com/) and [Modernes C++](https://www.modernescpp.com/index.php/blog/). I am also interested in best practices, and tooling (for example Compiler Explorer, CMake, Asan, clang tidy etc). The main development environment I use is Visual Studio Community Edition 2022, but I also use VSCode for some types of projects.

I enjoy Windows Desktop Development. In the past I have used extensively both MFC and WTL for writing Windows applications. Mostly these just sat on top of COM components. These days, I prefer to authoring components in C++/WinRT and consuming components in C# desktop applications (UWP or WinUI3) using XAML. More generally, I am interested in getting components written in one language to work with other components (i.e. software interoperability).

I am currently exploring Mobile Development (mainly targeting Android devices). I am in the process of porting a DietMonitor app written with Xamarin.Forms to .NET MAUI. One of the 'promises' of .NET MAUI is the ability to write a single UI targeting both Windows desktop and mobile devices. This sounds good but I'm not convinced.

On the data analysis side, I use like to use Excel, and especially PowerQuery for both ETL and EDA. I am currently learning DAX. If I need more analysis I use R and/or Python.

## I’m working on ...
In no particular order, the main projects that I am currently working on are:

- Office365 AddIns  
This consists of two add-in projects: one for Excel and one for Word. Both connect to the R.NET library and allow R scripts to be run in Office365 applications.

- DietMonitorApp  
This was my first attempt at a fully functional Android app and is itself based on an earlier Python application that runs on a desktop machine. The app is very simple. It monitors the progress of your diet. Just enter your weight each day and track your weight loss (or gain)! I am currently porting the app to .NET MAUI.

- FIXTools
These are a complicated collection of tools. The project comprises a C# code generator that takes [Financial Information eXchange](https://en.wikipedia.org/wiki/Financial_Information_eXchange) `FIX.xml` specifications as input and generates a C++ constexpr FIX header library. The project demonstrates how this can be incorporated in various simple tools that 'decode' FIX messages.

- StatisticsLibrary  
I developed a small C++ library of statistical functions (mean, var, sd, ...), statistical tests (t-test, z-test, F-test ...) and some basic time-series analysis. This was used as the basis for my book on __Software Interoperability__. I am looking to extend the library with more advanced analyses (e.g. pca and lda), when I have the time.

- NaturalLanguageProcessing  
A long-standing C# project that tests ideas in natural language parsing. I am currently waiting to implement micro-grammars and chains.

## I'm learning ...
- Mobile application development with XAML, .NET MAUI and C# on Windows 11 using Visual Studio 2022.
- WinRT (C++) for authoring COM-like components that can be consumed by UWP and WinUI applications. I have a couple of projects demonstrating these stacks: MediaCollectionWinUI and StatisticsViewer.



