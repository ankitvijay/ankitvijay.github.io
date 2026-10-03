---
title: "My first major Open Source contribution"
date: "2019-04-26T20:44:44+10:00"
lastmod: "2019-06-28T08:34:20+10:00"
url: "/2019/04/26/my-first-major-open-source-contribution/"
slug: "my-first-major-open-source-contribution"
wp_id: 3966
category: ["asp-net-core", "net-core", "opem-source"]
tag: ["asp-net-core", "c", "net", "net-core", "open-source"]
summary: "Without a doubt Open Source is great. It has touched the lives of millions of developers and through them almost everyone living on this planet someway or the other. The magic of Open Source For all the power Open Source has given to developers, the sad reality is that only very few people are actually"
---

Without a doubt Open Source is great. It has touched the lives of millions of developers and through them almost everyone living on this planet someway or the other.

### The magic of Open Source

For all the power Open Source has given to developers, the sad reality is that only very few people are actually the contributors. Most of the devs just consume what a very few build, mostly in their own free time. I hate to admit, I’m also among those who enjoy using Open Source software, applications, packages but very rarely contribute. Until recently, my major contribution to GitHub was restricted to a few documentation updates, typos, minor code changes or raising issues on the repository. While it is not an excuse, one of the reasons, I have not been able to contribute to the Open Source as much as I would like is because I have mostly worked with enterprise customers in a closed environment which provides a very little opportunity to work beyond the usual tasks. This, however, changed a few days back.

### The Problem

Recently, we upgraded our work-in-progress application to ASP.NET Core 2.2. As part of the upgrade, I migrated our HealthChecks to the new out-of-the-box health check feature of ASP.NET Core 2.2. To read more about this feature, refer to this [link](https://docs.microsoft.com/en-us/aspnet/core/host-and-deploy/health-checks?view=aspnetcore-2.2). The [BeatPulse project](https://github.com/Xabaril/AspNetCore.Diagnostics.HealthChecks) on GitHub provides HealthCheck NuGet packages for many service providers such as SQL Server, Redis, Raven DB etc. which makes the integration nice and easy. For our application, I needed to integrate with RavenDB. However, the NuGet package had the following limitations:

- It did not allow a user to pass an array of connection strings/ URLs which is a must-have for configuring failover.
- Additionally, the implementation did not support Certificate Authentication, again a must-have of the production scenario. I went through the implementation and realized it is quite a simple fix.

### My Options

I had two options to go about this.

- **Option 1**: Raise an issue with the contributors and wait for this to be fixed someday. In the meantime, have my own implementation for our application. However, that would have meant an additional avoidable code in our repository which would need to be maintained. Also, if someone else from my organization needed that implementation, they would either copy from my code or create our own internal NuGet package. Again, waste of time and effort.
- **Option 2:** Submit a PR with the changes and wait for it to get merged in the mainline before leveraging it in my application. I was initially a bit sceptical about this. I was not sure how much time it would take to get my changes approved. So many times, this apprehension has made me and I’m sure many others like me take a shortcut (read “Lazy”) approach that is the Option 1.

### Solution

This time I decided to do what is right. I forked the repository, made the relevant changes and raised [this Pull Request](https://github.com/Xabaril/AspNetCore.Diagnostics.HealthChecks/pull/139) to fix the issue. To my surprise, I found the process very easy and straightforward. The repository owner [@unaizorrilla](https://github.com/unaizorrilla) was very prompt in his response. The entire process took less than a week and I was able to use the updated NuGet package in no time once the changes were merged. This experience was very heartening. Most importantly, it gave me an inner satisfaction that my code now will be used by hundreds of other developers and not just within my organization. If you have not yet contributed to Open Source, I encourage you all to look for the opportunities where you can contribute. Trust me, you will find plenty. 🙂

> Photo by [Brina Blum](https://unsplash.com/@brina_blum?utm_source=unsplash&utm_medium=referral&utm_content=creditCopyText) on [Unsplash](https://unsplash.com/search/photos/github?utm_source=unsplash&utm_medium=referral&utm_content=creditCopyText)
