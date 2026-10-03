---
title: "Tools and tricks that can help you code better and faster"
date: "2017-12-30T17:05:27+10:00"
lastmod: "2017-12-30T17:30:03+10:00"
url: "/2017/12/30/tools-and-tricks-that-can-help-you-code-better-and-faster/"
slug: "tools-and-tricks-that-can-help-you-code-better-and-faster"
wp_id: 3433
category: ["git", "productivity", "project", "unit-testing", "visual-studio"]
tag: ["c", "cmd", "cmder", "efficiency", "kdiff3", "net", "productivity", "source-control", "visual-studio", "visual-studio-2017", "visual-studio-code"]
summary: "Tools and tricks you can use along with Visual Studio to make your life easy as a developer:"
---

**Visual Studio**, without a doubt, is one of the most powerful IDE out there in the market. It is a great editor to build/ debug your projects. It offers built-in templates for a variety of projects.  It also has a great third-party plug-in support like ReSharper, Nunit, TSLint etc. Despite all these great features, Visual Studio does fall short in few places.

We still do not have a great Git support for Visual Studio, it is getting improved, but nowhere close to what we can do with git commands. The diff/ mergetool of Visual Studio is inferior to tools such KDiff3, Beyond Compare etc.  There is still no built-in console. The NPM, Gulp/ Grant support tools (Task Runner Explorer) experience is sub-par. The default test explorer window for unit testing leaves a lot to desire. Opening or reloading solution with a large number of projects can take a lot of time (though it has improved significantly with Visual Studio 2017). The 3rd party plugins like ReSharper have become the necessary evil. They help improve development experience but most of the time at the cost of performance.

These issues have prompted me to look for solutions beyond Visual Studio and that’s where I started exploring good old command-line and other free tools. Here are few tools and tricks I use along with Visual Studio to make my life easy as a developer:

## Cmder

Cmder is a console emulator for Windows. Cmder is a great alternative to Microsoft Command Prompt. It can be configured to use Command Shell (cmd.exe), bash or PowerShell. It is highly customizable with multiple tab windows, keyboard shortcuts, search option etc. If you use Git for your source control, then it can easily replace git bash. Cmder can be downloaded from [here](http://cmder.net/).

## Ditching Visual Studio Git plugin

- **Using Git from command-line (instead of Visual Studio)**

Visual Studio plugin for Git is good for some basic tasks like commit, change branch, push, pull etc. But not beyond that. Git provides an [extensive set of commands](https://git-scm.com/docs) which gives you a far more power and control. This has made me switch to the command-line completely.

- **SourceTree**

If you are not a big fan of command-line, Sourcetree can be your answer. Sourcetree is a free Git GUI which helps you interact with your Git repositories. It displays Git logs/ history in the form of a graph making it easy to visualize and manage Git repos. SourceTree also provides support for reviewing changeset, stash, cherry-pick/ switch branches etc. It can be downloaded from [here](http://https //www.sourcetreeapp.com/).

- **KDiff3 as default diff and merge tool**

Diff and merge are perhaps the two most important tasks while working on source control. And KDiff3 does a far better job than Visual Studio for this. It supports 3-way-merge,  char-by-char diff, ignore whitespace etc. Visual Studio default diff tool fails terribly when the files to be merged have different encoding. KDIff3 has built-in support for different encodings such as UTF-8, UTF-8 BOM, Unicode etc. KDiff3 can be downloaded from [here](https://sourceforge.net/projects/kdiff3/files/). You can use KDiff3 as default merge tool for git through the steps defined [here](http://jebaird.com/2013/07/08/setting-up-kdiff3-as-the-default-merge-tool-for-git-on-windows.html).

## Command-line to perform standard Visual Studio tasks

If your project is .NET Core then .NET Core has a rich set of CLI tools. You can use `dotnet` commands to create a new project, restore NuGet package, build, run unit tests etc. A full set of .NET Core commands is available [here](https://docs.microsoft.com/en-us/dotnet/core/tools/?tabs=netcore2x). The traditional .NET framework projects are tightly coupled with Visual Studio. But, you can still use a combination of different executables to get the desired outcome.

- **Nuget.exe to install and restore NuGet packages**

You can use `Nuget.exe` executable to install a new package or restore existing packages through the command-line. The executable can be downloaded from [here](https://www.nuget.org/downloads). Additionally, you can add the `Nuget.exe` folder path to the PATH environment variable. To add the folder path go to:

> Control Panel -> System and Security -> System -> Advanced system settings –> Environment Variables -> PATH

- **MSBuild to build your Visual Studio solution**

You can use `MSBuild` to build your solution directly from the command-line. MSBuild.exe for Visual Studio 2017 is present at the below location:

> C:\Program Files (x86)\Microsoft Visual Studio\2017\\MSBuild\15.0\Bin

Again, you can add this above folder path to the PATH environment variable. This way, the executables are available globally. You can combine nuget.exe and MSBuild.exe to restore NuGet package and build the Visual Studio solution (.sln) in a single command as follows:

`path\to\VisualStudioSolution\ nuget.exe restore && msbuild`

- **Run your unit tests and integration test cases from Console**

You can also run your unit test and integration test cases for different test adapters like MSTest, NUnit, and XUnit directly from the console.  For example, the MSTest adapter command-line options can be referred [here](https://msdn.microsoft.com/en-us/library/ms182489.aspx). The `MSTest.exe` location for Visual Studio 2017 is present at the below location:

> C:\Program Files (x86)\Microsoft Visual Studio\2017\\Common7\IDE

Similarly, you can download the latest NUnit.ConsoleRunner package from Nuget and then use executable to execute NUnit test cases.

`nuget install NUnit.ConsoleRunner -source nuget.org`

The documentation for Nunit3-Console can be referred [here](https://github.com/nunit/docs/wiki/Console-Runner).

## Visual Studio Code

Visual Studio code is a free, lightweight, cross-platform source code editor which can be used as an alternative to Visual Studio. You can build and debug .NET Core projects with Visual Studio Code with the help of plugin such as `ms-vscode.csharp`. There are hundreds of other plugins available that can help you develop your front-end code in TypeScript, Angular JS, React, Vue etc.

One of the major advantages of Visual Studio Code ***I find*** is that unlike Visual Studio, you can open your solution as “folder” just like windows explorer. That means when you check out another branch or merge a remote branch in Git, the entire solution is not reloaded. This can help save developers significant time and effort. Visual Studio Code also comes up with the built-in terminal. So, you do not need to go back and forth between the editor and console window.

Hope this post helps you increase your productivity and perhaps reduce some frustration while you develop great software. Please let me know your thoughts in the comments section below.
