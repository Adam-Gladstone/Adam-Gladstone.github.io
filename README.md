---
title: "About Me"
permalink: "/about/"
---

## About me
Hi. My name is Adam Gladstone. Welcome to my personal website. By profession, I am a [quantitative developer](https://www.linkedin.com/in/adam-gladstone-b6458b156/), but I also enjoy software development as a hobby. Things around software change really quickly, so there's always loads to learn, lots of new tools and some new approaches. So this website is just a collection of personal projects that reflect areas that I am interested in and technologies that I am learning about. 

## Current Interests
I mostly develop in C++ and C# but I also use Python and R depending on the project. I like to keep up with the latest enhancements in C++20, C++23 and now C++26. I regularly follow [Jason Turner](https://github.com/lefticus), [Marius Bancila](https://mariusbancila.ro/blog/), [CppStories](https://www.cppstories.com/). I am also interested in best practices, and tooling (for example Compiler Explorer, CMake, Asan, clang tidy etc). The main development environment I use is Visual Studio Community Edition 2022, but I also use VSCode for some types of projects.

I enjoy Windows Desktop Development. In the past I have used extensively both MFC and WTL for writing Windows applications. Mostly these just sat on top of COM components. These days, I prefer authoring components in C++/WinRT and consuming components in C# desktop applications (UWP or WinUI3) using XAML. More generally, I am interested in getting components written in one language to work with other components (i.e. software interoperability).

I have spent time in the past exploring Mobile Development targeting Android devices, and have produced a couple of quite functional apps (DietMonitor, which I use to keep a daily track of my weight, and Business Toolkit App, which is a simple Business English language learning quiz-based app targeting Spanish speakers). I am currently doing a lot of web development, using a basic stack - HTML, css, and javascript - for the front-end, and PHP8 for the back-end. I have also spent some time recently learning the symfony framework.

On the data analysis side, I like to use Excel, and especially PowerQuery for both ETL and EDA. I am currently learning DAX. If I need more analysis I use R and/or Python.

## I’m working on ...
In no particular order, the main projects that I am currently working on are:

- Office365 AddIns
This consists of two add-in projects: one for Excel and one for Word. Both connect to the R.NET library and allow R scripts to be run in Office365 applications. I am still spending time tweaking the Office365 AddIns, especially the [ExcelRAddIn](https://github.com/Adam-Gladstone/Office365AddIns). This has gone through a couple of updates and I am currently working on some changes to make evaluating R scripts easier from Excel.

- DietMonitorApp
This was my first attempt at a fully functional Android app and is itself based on an earlier Python application that runs on a desktop machine. The app is very simple. It monitors the progress of your diet. Just enter your weight each day and track your weight loss (or gain)! The app is now written in .NET MAUI (ported and updated from Xamarin Forms) and will be updated in the final quarter of 2026.

- Web Application Development
I've been doing some web (application) development recently. I have developed a couple of simple websites (https://www.inglesparapymes.com/, https://www.ianbellcomex.com/) using a basic HTML, css and javascript stack. More recently, I have also been experimenting with [WASM](https://adam-gladstone.github.io/software%20interoperability/web%20development/native%20c++%20code/Connecting-C++-to-JavaScript-using-WASM/) and with Blazor. In part, this is a continuation of the theme of Software Interoperability. In this particular case I wanted to be able to use a C++ library from a web browser using javascript. I am still investigating whether it is possible to use Blazor/C# with a C++ library. 

## I'm learning ...
- Mobile application development with XAML, .NET MAUI and C# on Windows 11 using Visual Studio 2022.
- WinRT (C++) for authoring COM-like components that can be consumed by UWP and WinUI applications. I have a couple of projects demonstrating these stacks: MediaCollectionWinUI and StatisticsViewer.
- Web Application Development using HTML, css, and javascript for the client-side and PHP8 (with symfony) for the server-side.
