---
title: "Visual Studio 2017 – The best IDE ever"
date: "2017-03-08T07:43:33+05:30"
lastmod: "2017-10-02T11:14:31+10:00"
url: "/2017/03/08/visual-studio-2017-the-best-ide-ever/"
slug: "visual-studio-2017-the-best-ide-ever"
wp_id: 1508
category: ["visual-studio"]
tag: ["c", "net", "visual-studio", "visual-studio-2017"]
summary: "Visual Studio 2017 was launched with much fan fare yesterday (March 7, 2017). I started exploring Visual Studio 2017 from RC and I must say, after using VS 2017 I felt I was earlier leaving in stone age. It is so much better. In short the Visual Studio 2017 is equivalent to following: VS 2017"
---

Visual Studio 2017 was launched with much fan fare yesterday (March 7, 2017). I started exploring Visual Studio 2017 from RC and I must say, after using VS 2017 I felt I was earlier leaving in stone age. It is so much better.

In short the Visual Studio 2017 is equivalent to following:

> **VS 2017** =  **VS 2015** + Loads of **3rd party plugins** (like NChrunch, few ReSharper features etc.)+ **Improved** tooling, performance, experience, productivity etc.

Below, I have tried to highlight major features in Visual Studio 2017. This is not an exhaustive list but only few features which has helped ***me*** to improve my productivity significantly.

# Faster Installation – Choose your workload

The first thing that you will notice while starting Visual Studio is that you got to chose what you want. Are you just a web developer? No worries, you only install just web workload. In fact, you can even chose what individual component you want to install within that workload. That means, lesser space, faster install time.

![01-VS Installer](https://ankitvijaydotin.wordpress.com/wp-content/uploads/2017/03/01-vs-installer.png)

Visual Studio 2017 installer

# Faster Load Time – Increase Productivity

One of the major pain-points with previous version of VS was that it used to taken an eternity to load a solution with lot of projects. You could actually launch your VS go for coffee, come back and it would still be loading. But, VS 2017 actually loads these project very fast. So, you no longer need to go to coffee, just open the project and start coding and leave home early 🙂

From my own experience, my solution contained around 92 projects. Opening them in Visual Studio 2015 could take anywhere between 2 to 3 minutes or even more. Sometimes, it would hang and I would need to start all over again. Worst still, if you had ReSharper installed like me, I could go for lunch along with coffee and come back before it loads.

![VS 2015 - Preparing solution1](https://ankitvijaydotin.wordpress.com/wp-content/uploads/2017/03/vs-2015-preparing-solution11.png)

VS 2015 – Preparing Solution (You can go for a coffee)

With VS 2017, the same solution opens in less than 30 seconds. No more coffee breaks!

# C# 7.0 Support

Visual Studio 2017 comes with C# 7.0. C# 7.0 has introduce lot of new features like Tuples, Switch Case improvements, Pattern Matching, Local Functions, etc.

```csharp
// Example of tuple feature of C# 7.0
public (int sum, int difference) GetSumAndDiffernce(int a, int b)
{
       return (a + b, a - b);
}
```

You can get more details on C# 7.0 [here](https://blogs.msdn.microsoft.com/dotnet/2016/08/24/whats-new-in-csharp-7-0/).

# Live Unit Testing

If you have used NChrunch, probably you would know what I’m talking about. Visual Studio 2017 brings in the support for live unit testing. VS 2017 runs unit test cases in background as you write your code. It means you simply write code and you will get an instant feedback on what unit test cases are failing or passing due to your change. Ideal for TDD. Makes your smarter and increase your productivity.

To enable Live Unit Testing in your solution go to Test -> Live Unit Testing -> Start

![03-Live Unit Testing](https://ankitvijaydotin.wordpress.com/wp-content/uploads/2017/03/03-live-unit-testing2.png)

Start Live Unit Testing

![06-Live Unit test Example](https://ankitvijaydotin.wordpress.com/wp-content/uploads/2017/03/06-live-unit-test-example.png)

Example of Live Unit Testing

```
Important Note: If you are using a .NET Core project. Then you are out of your luck. .NET Core does not support Live Unit Testing currently.
You will get following error in output window:
"Live Unit Testing does not yet support .NET Core"
```

# Improvements in .NET Core Tooling

Back in VS 2015 days, .NET Core tooling was still in preview. If you were early adopters of .NET Core you would know what a pain it was. With VS 2017 the tooling has come out of preview and moved to 1.0. In addition to this you have MS Build support.

Once, you open an existing .NET Core project written in Visual Studio 2015 is “One-way upgrade” dialog as shown below. On clicking OK it will migrate your existing VS project to a newer version automatically.

![02-Project Upgrade1.PNG](https://ankitvijaydotin.wordpress.com/wp-content/uploads/2017/03/02-project-upgrade1.png)

.NET Core One-way upgrade

Why this upgrade? This is because, VS 2017 no longer supports project.json and xproj. It is replaced by csproj. The csproj itself is no longer complicated as earlier. You can edit csproj file and add/ remove references without unloading the project. The csproj file also supports intellisense.

![05-Edit CSProj.PNG](https://ankitvijaydotin.wordpress.com/wp-content/uploads/2017/03/05-edit-csproj.png)

Simplified csproj file with intellisense

## Docker Support

Vs 2017 supports containers out of the box. While creating a new project you get an option to enable Docker Support.

![04-Enable Docker](https://ankitvijaydotin.wordpress.com/wp-content/uploads/2017/03/04-enable-docker.png)

Enable Docker Support

```
Important Note: Before you enable Docker Support in your project, make sure you have Docker installed in your machine.

Else, your build will fail with error: "Microsoft.DotNet.Docker.CommandLineClientException: Unable to run 'docker-compose'. Verify that Docker for Windows is installed and running locally."

If you do not have the tools, you can enable Docker support later as well.
```

There are many other features which I have not listed down here. For the complete list please refer to [VS 2017 release notes](https://www.visualstudio.com/en-us/news/releasenotes/vs2017-relnotes).

Happy Coding!!!

#
