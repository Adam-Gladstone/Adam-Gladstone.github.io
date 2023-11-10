---
title:  "Consume a C++/WinRT component in a C# desktop application"
layout: single
excerpt: "I have a function called 'GetDescriptiveStatistics' that takes some data and returns summary statistics. The function is written in C++, and I want to call it and display the results in a Windows desktop application. This post describes how to do this."
excerpt_separator: "<!--more-->"
categories: 
  - Software Interoperability
tags:
  - cpp 
  - cppwinrt
  - winrt
  - midl
  - csharp
  - winui3
  - xaml
---

### Introduction
I have a function called 'GetDescriptiveStatistics' that takes some data and returns summary statistics. The thing is, the function is written in C++ (using STL and Boost), and I want to call it and display the results in a Windows desktop application written in C# using XAML and WinUI3.0.

![StatisticsViewerWinUI](https://adam-gladstone.github.io/assets/images/StatisticsViewer.png)

If you know how to do this, you can stop reading here and take a beach break. If not, this post describes the steps to take to write a WinRT (Windows Runtime) Component that exposes the 'GetDescriptiveStatistics' functionality, generate a C# projection (interop), and finally consume it in a C# desktop application allowing me to bind the results to a WinUI3.0 ListView. 

### Why would you want to do this? 
Based on the __Microsoft Learn__ article [Windows Runtime components with C++/WinRT](https://learn.microsoft.com/en-us/windows/uwp/winrt-components/create-a-windows-runtime-component-in-cppwinrt) there are three main reasons for building a Windows Runtime component in C++/WinRT.
1. To enjoy the performance advantage of C++ in complex or computationally intensive operations.
2. To reuse standard C++ code that's already written and tested.
3. To expose Win32 functionality to a Universal Windows Platform (UWP) app written in, for example, C#.

In this particular case, it is the second and third reasons that interested me. In the past, you could 'connect' a native C++ codebase to .NET by creating a COM wrapper component (perhaps using ATL/MFC), or you could create a custom managed wrapper using C++/CLI. The approach adopted here (as well as the older approach) is demonstrated in the suite [SoftwareInteroperability](https://github.com/Adam-Gladstone/SoftwareInteroperability) under the three projects: __StatisticsLibrary__, __StatisticsLibraryWRC__, and __StatisticsLibraryProjection__.

### Stages

#### 1. Build a static library
The first stage is to build the C++ code into a Universal Windows C++ static library project.

![StatisticsLibrary Property Pages](https://adam-gladstone.github.io/assets/images/StatisticsLibraryPropPages.png)

This is really a convenience. It allows us to keep the native C++ code separate from the C++/WinRT code. And this means we can write C++ unit tests directly against this library without having to worry about the details of WinRT types. The resulting __StatisticsLibrary__ consists of some basic statistical functions (descriptive statistics and linear regression) and statistical tests (T-test, F-test and ANOVA). The `StatisticsLibrary.h` file contains the declaration of the function 'GetDescriptiveStatistics' as follows:

![GetDescriptiveStatistics](https://adam-gladstone.github.io/assets/images/GetDescriptiveStatistics.png)

The function takes some data and optionally a list of keys corresponding to the summary statistics that you want to get. If it is empty, the function returns all the summary statistics (mean, median, standard deviation, variance and so on). The summary statistics are returned as a set of key-value pairs.

#### 2. Create a Windows Runtime Component
The next stage is to create a __StatisticsLibraryWRC__ project using the 'Windows Runtime Component (C++/WinRT)' Visual Studio project template. This project references the __StatisticsLibrary__ static library. The __StatisticsLibraryWRC__ is the interop layer. Here we need to do two things.

Firstly we need to define the API layer. The API is specified using IDL [MIDL3.0](https://docs.microsoft.com/en-us/uwp/midl-3/intro). The one we are interested in is defined in the `Statistics.idl` file under the `Components` folder. The API defines the name 'DescriptiveStatistics' and the WinRT types. The WinRT types we select correspond closely to the native C++ types. For the data parameter we pass in an `IVector<Double>`, and optionally an `IVector<String>` for the keys. For the return type we choose to use `IMap<String, Double>`. 

![StatisticsLibraryWRC](https://adam-gladstone.github.io/assets/images/StatisticsLibraryWRC.png)

With the IDL complete, we can build the project. This will fail, but the `cppwinrt.exe` will usefully generate stubs for the API defined by the IDL. We can take this stub code from the generated `.h` and `.cpp` files and copy it to the project source location. Then we can write the implementation code. This simply forwards the call `DescriptiveStatistics` to the native C++ function `GetDescriptiveStatistics` and deals with the returned results.

The second main task in the interop layer is to write code to perform any conversions from C++ (STL) types to WinRT/C++ types (and vice-versa). The two functions in the `Conversions` namespace perform the conversion from `IVector<double>` to a `std::vector<double>` and `ResultsToMap` converts a `std::unordered_map<std::string, double>` to an `IMap<hstring, double>`. 

![StatisticsLibraryWRC Implementation](https://adam-gladstone.github.io/assets/images/StatisticsLibraryWRC-Impl.png)

At this point, we can build the complete Windows Runtime Component.

#### 3. Create a C# projection
The next stage is to create a project that we use to generate a C# projection based on our C++/WinRT component. For this we create __StatisticsLibraryProjection__. This is a C# class library project targeting .NET 6.0. We need to add the `Microsoft.Windows.CsWinRT` package to the project using the NuGet package manager. And we need to add a project reference to the __StatisticsLibraryWRC__ project. The screenshot below shows the project dependencies.

![StatisticsLibraryProjection](https://adam-gladstone.github.io/assets/images/StatisticsLibraryProjection.png)

We get rid of the boilerplate `Class1.cs` file and we add a NuGet spec (`.nuspec`) file to the __StatisticsLibraryProjection__ project under a 'nuget' folder. The `.nuspec` file is a standard XML file renamed `StatisticsLibraryProjection.nuspec`. The `.nuspec` file contains the metadata and targets required by NuGet. Finally, we configure the `StatisticsLibraryProjection.csproj` file to generate the NuGet package for the correct target(s) and in the right directory. These properties specify the NuspecFile and the directory to generate the NuGet package. This is more fully described in the article [Generate a C# projection ...](https://learn.microsoft.com/en-gb/windows/apps/develop/platform/csharp-winrt/net-projection-from-cppwinrt-component)

After the project is built, the component WinMD and the implementation assembly (`StatisticsLibraryWRC.winmd` and `StatisticsLibraryWRC.dll`), the projection source files, and the projection assembly (`StatisticsLibraryProjection.dll`), will all be generated under the **_build** output directory. You'll also be able to see the generated NuGet package, `StatisticsLibraryWRC.0.1.0-prerelease.nupkg`, under the `\StatisticsLibraryProjection\nuget` folder.

#### 4. Consume the Windows Runtime Component in C#
Now we are ready to use the NuGet package in a C# .NET 6 application. We simply add a reference to the package to the __StatisticsViewerWinUI__ project using the NuGet package manager (ensuring that the package sources are correctly set).

![StatisticsViewerWinUI Solution](https://adam-gladstone.github.io/assets/images/StatisticsViewerWinUI-Solution.png)

The __StatisticsViewerWinUI__ project is based on the Visual Studio project template for C# 'Blank App, Packaged (WinUI 3 in Desktop)'. The application consists of a single main view (defined in `MainPage.xaml`). This contains the menus and the list view controls. The ListView on the right handles displaying the results returned from the call to 'GetDescriptiveStatistics' as shown below.

![StatisticsViewerWinUI](https://adam-gladstone.github.io/assets/images/StatisticsViewer.png)

At this point it would be really nice to say, 'well, we can set the XAML ListView ItemsSource property to bind directly to the DescriptiveStatistics results. After all, via the projection, they are being returned as an `IDictionary<string, double>`'. Unfortunately, I couldn't get this to work. The ListView binding seems to require an `ObservableCollection<...>`. Therefore, in the `MainViewModel.cs` we declare a `Results` property that sets/gets an observable collection of `ResultStatistics`, as follows:

![ObservableCollection](https://adam-gladstone.github.io/assets/images/Results-ObservableCollection.png)

In the XAML we configure the ListView `ItemsSource` to bind to this collection. Additionally, the ListView `HeaderTemplate` is specified as having two columns and the ListView `ItemTemplate` is defined as consisting of a `ResultStatistic` item which in turn exposes properties to get the name and value.

![ListView Control](https://adam-gladstone.github.io/assets/images/ListViewControl.png)

In the `MainViewModel.cs` we define a function `PopulateResults` which takes the `IDictionary<string, double>` returned from the call to `DescriptiveStatistics` and iteratively creates `ResultStatistic` items from this. These are then notified to the `ObservableCollection<>` which updates the ListView using the `ItemTemplate` defined in the `MainPage.xaml`. The result is that we can populate the ListView (relatively) easily. A number of the other classes in the __StatisticsLibrary__ return their results in this form, so we don't need to do anything else.

And that is all there is to it. We have successfully connected native C++ code to .NET via C++/WinRT, and consumed the Windows Runtime Component in a C# Windows desktop application.

### Wrap up
So why is this useful? Well apart from solving the original problem, it provides a generalizable stack. I can wrap (high-performance) C++ code using WinRT types in order to create an interop component, generate a C# projection, distribute the component alongside the projection assembly as a NuGet package and finally consume the NuGet package from a .NET application.

### References
[Windows Runtime components with C++/WinRT](https://learn.microsoft.com/en-us/windows/uwp/winrt-components/create-a-windows-runtime-component-in-cppwinrt)

[Generate a C# projection from a C++/WinRT component, distribute as a NuGet for .NET apps](https://learn.microsoft.com/en-gb/windows/apps/develop/platform/csharp-winrt/net-projection-from-cppwinrt-component)

