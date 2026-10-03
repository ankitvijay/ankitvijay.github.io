---
title: "When I brought down build-pipeline for entire organization"
date: "2019-02-15T07:42:14+10:00"
lastmod: "2019-02-15T07:56:07+10:00"
url: "/2019/02/15/when-i-brought-down-build-pipeline-for-entire-organization/"
slug: "when-i-brought-down-build-pipeline-for-entire-organization"
wp_id: 3877
category: ["continuous-delivery", "continuous-integration", "devops", "git", "team-city"]
tag: ["build", "ci-cd", "devops", "net", "source-control", "teamcity"]
summary: "December last year, last week before most of IT staff go on well-deserved vacation, when every team was trying to do one last deployment before code freeze, I brought down build-pipeline for almost every project in the company. Sounds scary? Here’s what happened. How it all started We are mostly a .NET shop and use"
---

December last year, last week before most of IT staff go on well-deserved vacation, when every team was trying to do one last deployment before code freeze, I brought down build-pipeline for almost every project in the company. Sounds scary? Here’s what happened.

## How it all started

We are mostly a .NET shop and use Team City for our builds. We have a number of Build Agents for running builds for our projects in Team City. A couple of days back before the incident we changed the repository name of our project. Subsequently, we updated the repo path in Team City for our project. After that, we did a dry run of the build and confirmed that it was all green.

## What caused the issue

However, once those changes were made, I noticed that few of our feature-branch builds, only on certain Build Agents started to fail with a weird error *Cannot find master branch.. something something*

I did a little bit of reading about the issue and it appeared to be a caching issue where Team City for some reason was not able to pick up the updated repository path name. It looked quite reasonable to clear relevant Team City cache variables. So, I went ahead and cleared some of the cache variables. After that, I ran my builds on all the Agents and everything was green again.

## The Chaos

Next day, when I reached the office, there was a choas. People were complaining about failing builds on Team City. Since I was the one who last touched the Team City configuration it was highly likely to be caused my changes.

We started digging deeper into the issue. We found out that the Team City “Nuget Plugin” was not working correctly and threw some weird errors for almost all the builds. So, the first thing we did is what every IT specialist does, try **restarting the Build Server and Build Agents** :). Unfortunately, this time it did not help. There was absolutely no help on the internet.

## The Fix

After several trials and errors, we finally managed to fix the major issue with NuGet Plugin.

Clearing the cache had somehow uninstalled NuGet plugin for all the NuGet Versions and Build Agents. To fix this, we had to manually stop Build Agent, reinstall the NuGet Version and start the Build Agent again. Then, repeat the process for all the required NuGet Versions (each project was using different version – may be the lastest one at the creation of build). To add to our pain, Team City Nuget plugin turned out to be case sensitive and for some mysterious reason, the case of one of the NuGet Version file was different from what Team City would have liked. Fortunately, we were able to resolve all the issues related to Nuget plugin.

Fixing the NuGet plugin issue fixed the build pipeline for most of our projects. But, few others were still failing because they had taken the dependency on NuGet packages cached on the Build Server. To fix we had to add the relevant NuGet source feed in the build steps.

## It was not over yet….

Just when I thought that all the issues were resolved and I could go home peacefully, life came full circle and we started getting the original error on my build.  At this point in time, there was no way I could take the same risk to clear the Team City cache.

So, I did some further digging and found out [this issue](https://github.com/GitTools/GitVersion/issues/912). Here is the summary of the issue:

We were using [GitVersion](https://gitversion.readthedocs.io/en/latest/) for [semantic](https://semver.org/) versioning for our builds. **GitVersion** needs access to master/develop branch to calculate the version number but Team City by default does not **fetch** the master branch (unless already fetched). To resolve this issue, all I had to do is to add a configuration parameter **numbers.git.fetchAllHeads=true.** Adding this parameter fixed the issue.

## Lessons Learnt

We had many lessons learnt from this incident. First and foremost, was to be careful when dealing with Team City cache. However, one thing key thing here was that all the builds which did not have a dependency on Team City plugins (like mine) did not have any issue. As an organization, we are moving more towards *scripting* the build steps as opposed to using plugins. This incident just validated our decision. For all the goodies Team City provide, I feel it still has a long way to go. While the other build management tools support YAML, configuring the builds through UI is still the preferred way for Team City. You cannot version control your build definition. Maybe as an organization, we need to start evaluating other options out there in the market.

## Final Thoughts

This incident made me realize how awesome our IT team is. There was no finger-pointing and everyone was rather focused on fixing the issue. I’m lucky to be working here. And we are expanding, so if you are interested in joining our team, please email me at vijayankit@outlook.com 🙂
