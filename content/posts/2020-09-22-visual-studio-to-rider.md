---
title: "Moving away from Visual Studio to JetBrains Rider"
date: "2020-09-22T12:08:56+10:00"
lastmod: "2020-10-04T19:16:29+10:00"
url: "/2020/09/22/visual-studio-to-rider/"
slug: "visual-studio-to-rider"
wp_id: 5197
category: ["jet-brains-rider", "productivity", "tooling", "visual-studio"]
tag: ["net", "productivity", "rider", "tooling", "visual-studio"]
summary: "The post describes JetBrains Rider as an alternate to Visual Studio and how Rider can help mitigate some of the Visual Studio pain-points."
---

### Visual Studio and ReSharper are great, but not together

Let me start by saying that I love Visual Studio. It is one of the best IDE out there especially if you are Microsoft shop. I have been developing on Visual Studio for over 12 years, and I have worked on every single version starting from Visual Studio 2003 to Visual Studio 2019. I never felt a need to look for an alternate for Visual Studio. Not that there was an alternate. 🙂

In the same breath, I love ReSharper. ReSharper again has been an essential tool which has made my development life easy over the years.

Unfortunately, it is the combination of ReSharper and Visual Studio that has not worked very well. The performance issues of Visual Studio and ReSharper are well known for years. But there has not been much improvement. [The post from JetBrains](https://blog.jetbrains.com/dotnet/2019/07/11/where-we-are-with-out-of-process-resharper/) gives some background of the issues with ReSharper on Visual Studio.

<blockquote class="twitter-tweet" data-dnt="true" data-width="500"><p dir="ltr" lang="en">I love <a href="https://twitter.com/VisualStudio?ref_src=twsrc%5Etfw">@VisualStudio</a>, I love <a href="https://twitter.com/resharper?ref_src=twsrc%5Etfw">@resharper</a>. Just don't together… Visual Studio 2019 with ReSharper has become unusable…  Can you guys please fix this?<br/><br/>– A frustrated dev</p>— Ankit Vijay (@vijayankit) <a href="https://twitter.com/vijayankit/status/1159591167769530370?ref_src=twsrc%5Etfw">August 8, 2019</a></blockquote>

### My tipping point

For the last year, I have been working with Visual Studio 2019 and ReSharper on a large solution where project count has gone over 130 projects over the previous few months. For those, you might be wondering why 130 odd-projects in a single solution? Well! It has its reasons, but, I will spare those details for some other time.

The performance of Visual Studio with ReSharper for the large solution was horrible. The Visual Studio UI hanged for mins before I could start coding. The build took very long to complete, and the tests took forever to run. From time to time, I ended up disabling the ReSharper only to enable it again. In addition to this, Git integration on Visual Studio left a lot to be desire. While the new Git tool filled some of the gaps, it was still very much work in progress. I raised [several issues](https://developercommunity.visualstudio.com/content/problem/1067609/visual-studio-sluggish-performace-and-freeze-issue.html) with the Visual Studio team, but unfortunately, none of it helped.

![](/wp-content/uploads/2022/12/9b0b6-visual-studio-performance-issue.png)

*100% CPU with Visual Studio was quite common*

All of these frustrations, coupled with the recommendations from my colleagues, made me look for an alternate and I decided to try Rider.

<blockquote class="twitter-tweet" data-dnt="true" data-width="500"><p dir="ltr" lang="en">Ditching <a href="https://twitter.com/VisualStudio?ref_src=twsrc%5Etfw">@VisualStudio</a> and testing waters with <a href="https://twitter.com/JetBrainsRider?ref_src=twsrc%5Etfw">@JetBrainsRider</a>  again. Let us see how it goes. Last time used <a href="https://twitter.com/JetBrainsRider?ref_src=twsrc%5Etfw">@JetBrainsRider</a> for 2 weeks before I went back to <a href="https://twitter.com/VisualStudio?ref_src=twsrc%5Etfw">@VisualStudio</a>. Will provide my feedback as I go along.</p>— Ankit Vijay (@vijayankit) <a href="https://twitter.com/vijayankit/status/1278133083443691520?ref_src=twsrc%5Etfw">July 1, 2020</a></blockquote>

### The learning curve

Now, my expectations with Rider were pretty low. Visual Studio has been around for over two decades, and I felt there was too much ground to cover for Rider. While I considered Rider to be a good alternate for Visual Studio for Mac. I wasn’t 100% sure about Rider when it came to Windows OS.

I was wrong about my assumptions. Rider turned-out to be much better than I imagine. I started Rider with a Visual Studio theme and key-mappings. It took a lot of friction out of using the new IDE. My editor screen and keyboard shortcuts worked the same as they were with Visual Studio.

![](/wp-content/uploads/2022/12/81201-visualstudiodarktheme.jpg)

*Visual Studio Dark Theme in Rider*

Initially, I still missed Visual Studio for about a couple of months. I would go back to Visual Studio almost every second day. However, I was also adamant about giving Rider a fair chance. And that turned out to be a right decision. A couple of months in I stopped missing Visual Studio. What also helped was JetBrains offer which automatically converted ReSharper Ultimate license to [dotNet Ultimate](https://www.jetbrains.com/dotnet/) license package which included Rider at no additional cost.

### Where Rider shines

Here are some of the Rider features which I liked the most:

- **Rider = IntelliJ IDEA + ReSharper** Rider comes with all the goodies of ReShaper without the performance tax. For the developers who cannot live without ReSharper, this can be huge.

![](/wp-content/uploads/2022/12/b06b2-dotnet-rider-is-intellij-plus-resharper.png)

*Rider = IntelliJ IDEA + ReSharper*

- **Faster build time**: Rider can improve the build time drastically as compared to Visual Studio by applying heuristics to only build the projects that need to be updated. It can be a real performance booster for large solutions.  This [post](https://blog.jetbrains.com/dotnet/2017/05/24/incremental-build-rider/) explains the incremental build feature in details.

Note: This feature was already available with ReSharper Build. So, if you are using ReSharper build instead of Visual Studio build management, then you might be already familiar with this.

- **Seamless external source debugging:** One of the features I liked about Rider was debugging external libraries/ nuget packages seamlessly like they are part of your code. And when you do not need to debug external source, you can turn off the feature.

![](/wp-content/uploads/2022/12/bc593-enableexternalsourcedebug-1.jpg)

*Enable external source debug option*

- **First-class support for Typescript/ Javascript debugging:** I always felt Typescript/Javascript received a stepchild treatment in Visual Studio. With Rider, Typescript has first-class debugging support. You can debug within the IDE without switching to browser dev-tools.

- **Better Unit test experience:** I have been a fan of ReSharper Unit test explorer window. And Rider only takes this forward. You can create multiple test window sessions and run only a subset of tests.

- **Great Git plugin:** It would be an understatement to say that Rider’s Git plugin is better than Visual Studio. It offers the code analysis even during the merge, which can be huge since you can fix compile-time error or remove unused references at the time of merge.

- **Handling of large solutions:** It is reasonable to expect that loading a large solution will take time. With Visual Studio, I encountered UI getting hanged several times during the project startup. Rider, on the other hand, handles it more gracefully. Like ReSharper, there is also an option to disable solution wide code analysis which can improve the load time.

- **Project Properties:** The project properties dialog in Rider supports the latest features of the new SDK project such as multi-target, setting language version, Nuget properties etc.

![](/wp-content/uploads/2022/12/4397d-projectfeatures.png)

*Project properties options in Rider*

- **Event Log, Terminal window, create gist etc.:** Rider comes up with an Event log window which the logs every event that happens with in the IDE. It also has a built-in Terminal and some excellent little features such create GitHub Gists from within the IDE. One other thing that impressed me was the ability to create custom “Run/Debug” templates. It offers much more than running a single project or “Multiple startup projects” option in Visual Studio.

### Rider is not perfect

It is not that Rider is perfect. In fact, far from it. It has its flaws. Here are some of the issues I have encountered with Rider.

- There were a couple of instances where UI froze, and I had to restart the Rider.

![](/wp-content/uploads/2022/12/c0f04-uifreezerider.png)

*Rider too does hang sometimes*

- The Unit test explorer windows had a bug where I found that testhost.exe was not released. In another instance, the test runner kept running even after the test run was complete.

<blockquote class="twitter-tweet" data-dnt="true" data-width="500"><p dir="ltr" lang="en"><a href="https://twitter.com/JetBrainsRider?ref_src=twsrc%5Etfw">@JetBrainsRider</a> <a href="https://twitter.com/maartenballiauw?ref_src=twsrc%5Etfw">@maartenballiauw</a> in the latest and a previous version of <a href="https://twitter.com/hashtag/rider?src=hash&amp;ref_src=twsrc%5Etfw">#rider</a>, the unit tests hangs and give below error.<br/><br/>The tests are running fine on the build server (and VS AFAIK). Any idea what could be causing it? I'm on v2.2.2 <a href="https://t.co/cBttTQbfHZ">pic.twitter.com/cBttTQbfHZ</a></p>— Ankit Vijay (@vijayankit) <a href="https://twitter.com/vijayankit/status/1305305137280286721?ref_src=twsrc%5Etfw">September 14, 2020</a></blockquote>

- The faster build time also comes up with some issues. Sometimes changing git branch could let code analysis go haywire, and the only workaround is to do a clean build.
- Deleting NuGet reference from the solution explorer does not work. You need to uninstall the NuGet reference manually.
- There is a subtle bug where you cannot open a second instance of Rider if one solution is already open. The only workaround that worked for me was to create a new solution or open an existing project from the same instance of Rider and then open it in a separate window.

Despite all these issues, I mostly had a positive experience with Rider. Rider, like Visual Studio, receives constant improvements and bug-fixes in the form of updates. I’m sure the JetBrains team is busy fixing these little defects.

**Wrapping Up**

The dominance of Visual Studio is there to stay. That said, Rider, in my opinion, is a serious competitor to the Visual Studio. I think this is the best thing that could happen to the dotnet community. It is good to have healthy competition which compels organizations to think out of the box and come with more innovative and creative ideas to make their product better.
