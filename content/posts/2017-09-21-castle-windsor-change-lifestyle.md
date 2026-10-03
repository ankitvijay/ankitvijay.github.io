---
title: "Castle Windsor: Change Lifestyle"
date: "2017-09-21T07:37:18+10:00"
lastmod: "2017-09-29T06:01:55+10:00"
url: "/2017/09/21/castle-windsor-change-lifestyle/"
slug: "castle-windsor-change-lifestyle"
wp_id: 2700
category: ["inversion-of-control"]
tag: ["castle-windsor", "dependency-injection", "di", "ioc", "net", "self-host"]
summary: "In my current project, we use Castle Winsdor for Dependency Injection. I must admit before this project I had never used or even heard of it. I have had some love-hate relationship with Castle Windsor , with more hate than love initially. However, over a period of time, I realized that Castle Windsor is probably"
---

In my current project, we use `Castle Winsdor` for Dependency Injection. I must admit before this project I had never used or even heard of it. I have had some love-hate relationship with `Castle Windsor` , with more hate than love initially. However, over a period of time, I realized that `Castle Windsor` is probably among the best IoC containers out there. It is extremely flexible and powerful.

Recently, I got stuck with up an issue where Integration Test Cases of our application started failing. It took me some time to find out the root cause of the issue.

## Why were Integration Test Cases failing?

We use [ASP.NET Web API self Host](https://code.msdn.microsoft.com/ASPNET-Web-API-Self-Host-30abca12) for our integration test cases and had shared code to register components to `WindsorContainer` . Few of these components were `PerWebRequest` lifestyle components. Web API Self Host did not like `PerWebRequest` lifestyle and started throwing `Internal Server Error (500)`

Of course, the easiest solution was to use separate code to register the containers for Integration test cases and register `PerWebRequest` components as `Singleton` in integration tests. However, that would mean that we would need to have two identical copies of the same code. It would be a maintenance headache. While searching for a solution I came across [this article](http://blog.ploeh.dk/2010/04/26/ChangingWindsorlifestylesafterthefact/) which talked about `IContributeComponentModelConstruction`.

`IContributeComponentModelConstruction` is the easiest way of extending and modifying Windsor container. You can implement this interface to override component lifestyle.

Here is the usage:

This file contains hidden or bidirectional Unicode text that may be interpreted or compiled differently than what appears below. To review, open the file in an editor that reveals hidden Unicode characters.
[Learn more about bidirectional Unicode characters](https://github.co/hiddenchars)

[Show hidden characters]({{ revealButtonHref }})

|  |  |
| --- | --- |
|  | public class PerWebRequestLifestyleOverrider : IContributeComponentModelConstruction |
|  | { |
|  | public void ProcessModel(IKernel kernel, ComponentModel model) |
|  | { |
|  | if (model.LifestyleType == LifestyleType.PerWebRequest) |
|  | { |
|  | model.LifestyleType = LifestyleType.Singleton; |
|  | } |
|  | } |
|  | } |
|  |  |

[view raw](https://gist.github.com/ankitvijay/3235edbd3991f19dbf735914185b5b9c/raw/478cbf5200cc247b0f87fb879b0ff301512c63f5/PerWebRequestLifestyleOverrider.cs)
[PerWebRequestLifestyleOverrider.cs](https://gist.github.com/ankitvijay/3235edbd3991f19dbf735914185b5b9c#file-perwebrequestlifestyleoverrider-cs)
hosted with ❤ by [GitHub](https://github.com)

Now, you can plug the above code to your container by simply adding to below line of code while registering your Windsor Container:

This file contains hidden or bidirectional Unicode text that may be interpreted or compiled differently than what appears below. To review, open the file in an editor that reveals hidden Unicode characters.
[Learn more about bidirectional Unicode characters](https://github.co/hiddenchars)

[Show hidden characters]({{ revealButtonHref }})

|  |  |
| --- | --- |
|  | var conatiner = new WindsorContainer(); |
|  | container.Kernel.ComponentModelBuilder.AddContributor(new PerWebRequestLifestyleOverrider()); |
|  | // Rest of your code |

[view raw](https://gist.github.com/ankitvijay/5bab96c40a2a2f33c34d2ac97cb3254f/raw/026d116d7cbe6c578f79777f262aeee0b1975dac/WindsorContainerRegistration.cs)
[WindsorContainerRegistration.cs](https://gist.github.com/ankitvijay/5bab96c40a2a2f33c34d2ac97cb3254f#file-windsorcontainerregistration-cs)
hosted with ❤ by [GitHub](https://github.com)

Hope this helps you to save some debugging effort 🙂
