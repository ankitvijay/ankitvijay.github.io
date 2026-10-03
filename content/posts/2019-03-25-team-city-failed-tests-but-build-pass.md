---
title: "Team City – Curious case of failed tests but passed build"
date: "2019-03-25T08:07:00+10:00"
lastmod: "2022-12-23T23:04:46+10:00"
url: "/2019/03/25/team-city-failed-tests-but-build-pass/"
slug: "team-city-failed-tests-but-build-pass"
wp_id: 3943
category: ["continuous-integration", "devops", "git", "integration-testing", "net-core", "team-city", "testing", "unit-testing"]
tag: ["devops", "integration-testing", "net", "net-core", "source-control", "teamcity", "testing", "unit-testing"]
summary: "Recently, I had written a post on how I managed bring down build pipeline for entire organization. While I was at fault during that time, Team City should take the blame for this one. Background I had recently created a CI/CD pipeline for our new .NET Core project. As part of the build pipeline, I"
---

Recently, I had written a post on how I managed bring down [build pipeline for entire organization.](/2019/02/15/when-i-brought-down-build-pipeline-for-entire-organization/) While I was at fault during that time, Team City should take the blame for this one.

### Background

I had recently created a CI/CD pipeline for our new .NET Core project. As part of the build pipeline, I had usual build steps to Build the solution, Run Unit Tests, Run Integration Tests, and then Deploy to Octopus.

### Team City dotnet CLI Plugin

As mentioned in my previous post on Team City, I have been try to avoid Team City plugins as much as possible and use scripts or command line instead. To run the Tests for my new project my first preference was to leverage “dotnet” command out of the box instead of using Team City dotnet plugin. However, **[dotnet test](https://docs.microsoft.com/en-us/dotnet/core/tools/dotnet-test?tabs=netcore21)** command does not take list of multiple projects *by default.* There are obviously way around this but I chose to go for Team City plug-in instead due to simplicity and ease of use. The configuration was simple and straightforward and I was up and running in minutes.

![](/wp-content/uploads/2019/03/image.png)

*Team City dotnet CLI plugin*

### Issue

Our CI/CD pipeline seem to be working as expected with no dramas. Once, the PR branch was approved, master branch build was trigger and on successful build, the solution would deploy to Octopus. On one fine day our QA reported a bug which should have ideally been caught by our integration tests. When I looked Team City build, I noticed that build was successful even when integration tests failed. That was weird in many ways and I double-checked the build configuration and verified that they were all set correctly. The “Execution step” for all the build steps was set to “If all previous steps finished successfully”. But still the build steps after the *failed* build step appear to be getting executed.

### Root Cause

One further digging, I found the root cause of the issue to be [this issue](https://github.com/JetBrains/teamcity-dotnet-plugin/issues/129) on Team City dotnet plugin. There were other devs who were also caught off-guard like me. As per one of the plugin contributors:

> It is original behavior. For most of runners a process returns non zero exit code which means that a running was not successful. For runners like NUnit, VSTest, dotnet test, msbuild /t:VSTest, dotnet vstest positive exit code just an amount of failed tests. See this [thread](https://youtrack.jetbrains.com/issue/TW-49018) for details

However, this explanation for me is not enough to NOT fix a wrong behavior/ bug in the plugin. The behavior is not intuitive and can lead to issues like mine and other developers.

If you want JetBrains to prioritize this issue you can vote [here](https://youtrack.jetbrains.com/issue/TW-55626).

### Workaround

One of the suggested workaround mentioned for this issue was to set “Execution Step” for the each build step as “Only if build status is successful”. But I did not like this solution as it means we are going away from *default* for no reason and we would need remember *yet another thing to change* from default every time we add a new build step.

I managed to solve to this issue with the slightly cleaner work-around by adding following “Failure Condition” to my Team City build configuration.

![image](https://user-images.githubusercontent.com/5988564/53308876-44dab080-38f0-11e9-9575-1657d0d60757.png)

This failure condition worked as build log messages contain text “Tests Failed” each time test build step failed.

Hope this tip helps you avoid making the same mistake and save few hours 🙂

Photo by [Harshal Desai](https://unsplash.com/@harshaldesai?utm_source=unsplash&utm_medium=referral&utm_content=creditCopyText) on [Unsplash](https://unsplash.com/s/photos/red-signal?utm_source=unsplash&utm_medium=referral&utm_content=creditCopyText)
