---
title: "Edit csproj Project file programatically"
date: "2016-09-09T04:34:29+00:00"
lastmod: "2017-09-29T06:25:19+10:00"
url: "/2016/09/09/edit-csproj-project-file-programatically/"
slug: "edit-csproj-project-file-programatically"
wp_id: 1082
category: ["project"]
tag: ["csproj", "visual-studio"]
summary: "In my current engagement, we have more than 80 projects in a solution (don’t ask me why :)). Recently, as per quality guidelines, we needed to make few changes to each project. For example: Treat warnings as errors, enable code analysis for each project, sign assembly etc."
---

In my current engagement, we have more than 80 projects in a solution (don’t ask me why :)). Recently, as per quality guidelines, we needed to make few changes to each project.
For example:  Treat warnings as errors, enable code analysis for each project, sign assembly etc.

I realized doing it manually can take me entire day so I spent few mins to create a small script in C# to save my time. Here is the code snippet:

This file contains hidden or bidirectional Unicode text that may be interpreted or compiled differently than what appears below. To review, open the file in an editor that reveals hidden Unicode characters.
[Learn more about bidirectional Unicode characters](https://github.co/hiddenchars)

[Show hidden characters]({{ revealButtonHref }})

|  |  |
| --- | --- |
|  | using System.Collections.Generic; |
|  | using System.Linq; |
|  | using Microsoft.Build.Evaluation; |
|  |  |
|  | class Program |
|  | { |
|  | static void Main(string[] args) |
|  | { |
|  | var projectList = new List<string>() |
|  | { |
|  | // Your Project file paths |
|  | }; |
|  | foreach (var project in projectList) |
|  | { |
|  | var projectCollection = new ProjectCollection(); |
|  | var proj = projectCollection.LoadProject(project); |
|  | // Select Debug configuration |
|  | var debugPropertyGroup = |
|  | proj.Xml.PropertyGroups.First( |
|  | e => e.Condition == " '$(Configuration)|$(Platform)' == 'Debug|AnyCPU' "); |
|  | debugPropertyGroup.SetProperty("TreatWarningsAsErrors", "true"); |
|  | debugPropertyGroup.SetProperty("RunCodeAnalysis", "true"); |
|  | // Select Release configuration |
|  | var releasePropertyGroup = |
|  | proj.Xml.PropertyGroups.First( |
|  | e => e.Condition == " '$(Configuration)|$(Platform)' == 'Release|AnyCPU' "); |
|  | releasePropertyGroup.SetProperty("TreatWarningsAsErrors", "true"); |
|  | releasePropertyGroup.SetProperty("RunCodeAnalysis", "true"); |
|  | //Sign assembly with a with strong name key |
|  | proj.SetProperty("SignAssembly", "true"); |
|  | proj.SetProperty("AssemblyOriginatorKeyFile", "test.pfx"); |
|  | //Save |
|  | proj.Save(); |
|  | } |
|  | } |
|  | } |

[view raw](https://gist.github.com/ankitvijay/0d8003f244fb4e9bcd6cd91717f34eab/raw/96ab9a8969b1482d0a548dc395f0f9d8b0033475/EditCsProj.cs)
[EditCsProj.cs](https://gist.github.com/ankitvijay/0d8003f244fb4e9bcd6cd91717f34eab#file-editcsproj-cs)
hosted with ❤ by [GitHub](https://github.com)

Hope it helps save some time for some of you 🙂

**Update:** I have created a command line utility for the solution and added it to [GitHub](https://github.com/ankitvijay/ankitvijay-ParseCsProject-). This utility accepts different set arguments to based on operations required to be performed. Please refer to `ReadMe.md` in GitHub for more details.
