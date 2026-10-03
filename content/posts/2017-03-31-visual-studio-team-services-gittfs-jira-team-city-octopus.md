---
title: "Visual Studio Team Services = Git/TFS + JIRA + Team City + Octopus"
date: "2017-03-31T08:38:21+05:30"
lastmod: "2019-02-15T09:57:14+10:00"
url: "/2017/03/31/visual-studio-team-services-gittfs-jira-team-city-octopus/"
slug: "visual-studio-team-services-gittfs-jira-team-city-octopus"
wp_id: 1839
category: ["devops", "visual-studio-team-services"]
tag: ["jira", "net", "octopus", "visual-studio", "vsts"]
summary: "Warning: The content of this post is highly opinionated. Please exercise caution. 🙂 A bit of Background Back in 2012-13, the term Dev-Ops was unheard of in my team. We were still living in dark ages where a developer would developed the code, then write unit test cases more to get the code coverage look good"
---

> Warning: The content of this post is highly opinionated. Please exercise caution. 🙂

## A bit of Background

Back in 2012-13, the term Dev-Ops was unheard of in my team. We were still living in dark ages where a developer would developed the code, then write unit test cases more to get the code coverage look good than to actually “test” the code. The code would then go through a review and queued for check-in. Some magic which the developer never really cared about would then tell us if the code was successfully checked-in or it failed. That magic was TFS XAML  build. The build was managed by a dedicated team and we never felt it was part of development process. After the end of ~~sprint~~ iteration a huge code base would then go to the test team and they would start testing the code based on their test cases and log bugs to the dev team. More often than not a developer would talk to tester only during that phase. This resulted in 100s of bugs in a big team. Few of these bugs would be invalid due lack of understanding of requirements, few others would be basic bugs which should have been handled by the developer in the first place. All the requirements, tasks, bugs, issues etc were logged in TFS. But, there was no dashboard. So, every developer and dev lead had to be expert in excel to track the items more effectively. It is said **Ignorance is bliss**, and same was true for us. We were happy in our shell, delivering code in this fashion and never felt need of change.

During the similar time-frame, I got an opportunity to work in a customer location. This is when I got a rude shock. The customer used tools which I had not heard before. They used [confluence](https://www.atlassian.com/software/confluence) to collaborate, [JIRA](https://www.atlassian.com/software/jira) to track work items, [Team City](https://www.jetbrains.com/teamcity/) for build and a source control that was not TFS :). Suddenly, I realized that development was more than just writing code. I fell in love with these tools immediately. I realized there is more in the world than TFS.

However, there was still one big pain point with all these tools and application. We were using just too many tools and plugins – TortotiseSVN, JIRA, Team City, some other tool for deployment etc. Each one of these tools looked different and they worked differently.

## Visual Studio Team Services

Microsoft was late to join the party and TFS was surely lagging the features that Agile projects and modern development practices demand. In 2013, Microsoft introduced [Visual Studio Online](https://msdn.microsoft.com/en-us/magazine/dn519923.aspx) (VSO). At the time of launch VSO appeared to be nothing more than TFS on cloud. However, Microsoft started adding more and more features to VSO. Many of these features were “inspired” from competitive tools. Over a period of time, VSO was aptly renamed to Visual Studio Team Services (VSTS). Today, VSTS has become one stop for all our development.

VSTS has solved one big problem of fragmentation. Its features today are on-par if not more with JIRA, Team City and Octupus.  With VSTS as a user you do not need multiple accounts,  your single account will give you access to everything you need for software development. Additionally, VSTS now offers full support for more and more non-Microsoft services. That means, you are first class citizen irrespective of your editor, source control (TFVC,  Git) and technology. If you do not want to use VSTS for everything, you still have a choice to choose what you want. For example, you can choose Octopus over VSTS Release Management and push package from VSTS build to Octopus directly. It works seamlessly.

To know more about features of VSTS [go here](https://www.visualstudio.com/team-services/features/). What tools do you use for your development?
