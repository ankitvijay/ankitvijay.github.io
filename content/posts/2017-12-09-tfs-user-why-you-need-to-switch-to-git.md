---
title: "TFS User – Why you need to switch to Git"
date: "2017-12-09T21:59:17+10:00"
lastmod: "2019-02-15T09:58:13+10:00"
url: "/2017/12/09/tfs-user-why-you-need-to-switch-to-git/"
slug: "tfs-user-why-you-need-to-switch-to-git"
wp_id: 3348
category: ["continuous-delivery", "continuous-integration", "devops", "git", "visual-studio"]
tag: ["cd", "ci", "net", "source-control", "tfs"]
summary: "Not too long ago, TFS and SVN were the only source control I had used. I had a very little experience of distributed source controls like Git. So when I got an opportunity to work on Git on a large scale project for the first time, I had my doubts. But, it did not take"
---

Not too long ago, TFS and SVN were the only source control I had used. I had a very little experience of distributed source controls like Git. So when I got an opportunity to work on Git on a large scale project for the first time, I had my doubts***.*** But, it did not take me long to realize that why Git so much better than TFS. So, many technical issues we had in our projects were really the limitation of TFS. But due to that limitation, our team ended up spending hundreds of man-hours. ***If only***we had someone to tell us or convince us to use Git as our source control, the life would have been so better. :)Even today there are people and teams who have only used TFS as source control due to different reasons. Through this post, I intend to reach out to those individuals/ teams and explain why Git is so much better than TFS.

**It’s not easy to look TFS beyond Visual Studio**

TFS and Visual Studio are complementary to each other. TFS works great as long as you are working in its ***limitation***and using it within Visual Studio. But, have you tried to check-in through a command line? Or have you tried to use TFS beyond Visual Studio editor? Well, then you would know the experience is less than ideal. What you can do with TFS is mostly limited to what Visual Studio has to offer.

Git, on the other hand, has a rich console support. The Git commands give you full control of source control. Visual Studio also has a Git plugin. But, once you start using Git commands you would probably never go back to the plugin. It also means that you are free to use any editor, even Notepad++ to code. But, you will still get same rich experience with your source control.

**Branching in TFS is scary**

Any long time TFS user would know what I’m talking about. Branching in TFS is dreaded. I have worked with folks who would anything to avoid creating a TFS branch. In fact, the branching in TFS is usually done only when you are working with multiple releases in parallel. The reason is, TFS creates a separate physical copy of your repository when you create a branch. That means each branch takes additional space on your local disk. This leads to one interesting problem. People tend to merge less often while using TFS. Hence, when you eventually merge you branches it can be a real mess, sometimes a project in itself.

Branching in GIT is not a physical copy but a **pointer to commit**. It is extremely cheap, lightweight and fast. In fact, as per [Git-flow](https://jeffkreeftmeijer.com/git-flow/), you create a branch for every feature (or story) you work on. Within your feature branch, you can check-in as many times as you like and then ***merge***onto the mainline branch

**Check-in in TFS can be scary and that makes Continuous Integration/Delivery difficult**

Consider this scenario, you are working in a large team, say 50 members.  And your team is following a ***good practice***of gated check-ins to ensure code quality and standards are met before they get checked-in. If each member of your team *checks-in* at least once in a day and if one gated check-in takes 15 mins, then it means that you may have to wait for hours together to get your changes checked-in. Worst still, if your check-in gets failed due to a merge issue then you need to queue your check-in all over again and wait again!!!

One way to prevent this issue is to check-in less frequently. But, then it also means that you either keep unsaved changes on your local machine or create ugly shelvesets. The longer you wait for your changes to commit, the size of merge conflict also increases.

In Git, one can create a separate branch for each feature you are working on. Additionally, you first ***commit changes*** to your local branch and then ***push*** it to the remote. Once, you are done with your changes you can ***merge***your changes to the mainline branch by raising a ***pull-request*** (PR). This makes Git ideal for large teams and Continous Integration/ Delivery.

**Conclusion**

I have just highlighted few points why Git is superior to TFS. Please try it out yourself first hand and if you like it try to convince your team to make a switch. One of the easiest ways you can learn more about Git is by contributing to an open source project of your choice on [Github](https://github.com/). It can be a bit intimidating at first, but I’m sure you won’t regret it. 🙂
