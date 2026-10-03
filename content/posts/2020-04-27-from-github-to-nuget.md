---
title: "From GitHub to NuGet"
date: "2020-04-27T07:50:37+10:00"
lastmod: "2022-12-23T23:04:47+10:00"
url: "/2020/04/27/from-github-to-nuget/"
slug: "from-github-to-nuget"
wp_id: 4804
category: ["asp-net-core", "asp-net-core-3-1", "continuous-delivery", "continuous-integration", "devops", "github", "net-core", "nuget", "open-source"]
tag: ["asp-net-core", "branching-model", "github", "github-actions", "github-flow", "net", "nuget"]
summary: "This post talks about my journey to publish ASP.NET Core Middleware as a Nuget Package from GitHub repository through GitHub Actions."
---

I have been [contributing to open source](/2019/10/21/migrating-dotnet-foundation-website-to-asp-net-core-3-0/) for quite some time. However, with some exceptions, most of these contributions had been small, intending to solve a particular problem at my workplace. In addition to this, none of my previous contributions went beyond a public repository on my GitHub account. But I was keen to change that and a small vacation during Covid-19 turned out to be perfect timing.

## My first package on nuget.org

Stay-at-home vacation during Covid-19 allowed me to do something I wanted to for a long time, that is, developing a NuGet package that can be used by hundreds of developers across the globe. In this post I have described my journey from creating a repository in GitHub to publishing the package on Nuget.org. I hope this encourages some of you to do something beyond your usual work. 🙂

### The selection criteria

What to build turned out to be a task in itself. Here are some of the things I was looking to achieve from this entire exercise:

- The project should be small and simple that I could complete within 8-10 person-hours. I had no intention of spending my entire vacation on this 🙂
- There should not be any dependency on a 3rd party library.
- Despite being simple, it should solve some “real” developer problems.
- The project should tick all the boxes of a “typical” open source project such as a GitHub repository, unit/ integration tests, an automated build pipeline, and the ability to publish the package to NuGet.
- It should come with the documentation/ instructions on how the Nuget package can be consumed.
- It should be easy to maintain and accept contributions from the community.
- Last, but not the least it should provide a template for several other NuGet packages which I may publish in the future. 🙂

### The problem statement

With the above points in mind, I decided to create a middleware that returns an exception as a JSON response for an ASP.NET Core Web API. This is a problem I have faced several times at my workplace. The default ASP.NET Core template comes up with the middleware, **UseDeveloperExceptionPage**, which returns the exception in the form of HTML or plain text. However, many times this is not sufficient and developers want to consume a JSON response instead. I could not find an official or well-received 3rd-party package that solves this problem at present.

### GitHub Repository

As a first step, I created an empty repository. After several attempts, I settled for the name [**DeveloperExceptionJsonResponse**](https://github.com/ankitvijay/DeveloperExceptionJsonResponse)for my GitHub repo and eventually the NuGet package (Naming is [hard](https://martinfowler.com/bliki/TwoHardThings.html)).

Next, I used [gitignore.io](https://www.gitignore.io/) to create a .gitignore file for my repository. If you have not heard of this gitignore.io, it is a great tool to auto-generate the gitignore files for your projects.

To start with, I decided to go with [GitHub Flow](http://scottchacon.com/2011/08/31/github-flow.html) as my branching strategy with a master branch “always deployable”. I did, however, soon realize that this may not work very well for my scenario. I will talk more about this in the coming sections.

### Branch Protection

Even though I was the only developer, I refrained from working on master. I added branch protection rules under GitHub settings to prevent pushing the commits directly to the master.

![](/wp-content/uploads/2020/04/image-8.png)

*Figure: Branch protection rules*

I, then created my [first issue](https://github.com/ankitvijay/DeveloperExceptionJsonResponse/issues?q=is%3Aissue+is%3Aclosed) and feature branch on GitHub to setup the project and CI build pipeline.

### NuGet Account

I signed up at [nuget.org](https://www.nuget.org/) to publish my NuGet package. To publish the NuGet package to Nuget.org we need an API Key. The API key is a token that identifies a user to the NuGet gallery. I generated the API key from my newly created NuGet account.

![](/wp-content/uploads/2020/04/image-9.png)

*Figure: API Key management for nuget.org*

The API key is a secret and should not be shared publicly. GitHub provides an ability to [store secrets](https://help.github.com/en/actions/configuring-and-managing-workflows/creating-and-storing-encrypted-secrets) such as this under the Settings –> Secrets section which is where I ended up storing the key. The secrets can be accessed from the GitHub Action workflow as secure environment variables.

### CI build Pipeline using GitHub Actions

The next step was to build a CI pipeline for the repository. I have quite some experience building the CI/CD pipeline on Azure DevOps but in this case I chose to try [GitHub Actions](https://help.github.com/en/actions), as I felt that it may provide seamless integration with the GitHub repository. And I was not wrong.

My GitHub Action workflow executes the following steps:

- **Versioning**: Needless to say but a Nuget package requires versioning. I chose [GitVersion](https://gitversion.net/docs) to achieve [Semantic Versioning](https://semver.org/) on the project primarily because of the familiarity and experience of using it in my organization. The GitHub Action to use GitVersion can be found [here](https://github.com/GitTools/actions).

**Tip**: When using GitVersion Action ensure that you have **Gitversion.yml**file in your source code to avoid unexpected issues. The documentation does not do a great job of explaining that. To configure additional options, refer to the [source code](https://github.com/GitTools/actions/blob/master/gitversion/execute/action.yml).

- **Set up .NET Core**: I used the official GitHub [setup-dotnet Action](https://github.com/actions/setup-dotnet) to set up the [dotnet cli](https://github.com/dotnet/cli) environment. This action allowed me to use **dotnet** commands such as restore, build, test, pack, and nuget push.

- **Publish NuGet package**: Pushing the package to NuGet.org was trivial. I used conditional steps to push the package only when the pull request is merged to the master. The API key was read from the GitHub secrets key-vault.

My CI workflow is available [here](https://github.com/ankitvijay/DeveloperExceptionJsonResponse/tree/master/.github/workflows).

I wanted to **control** when to push a new version to nuget.org. Unfortunately, one of the limitations of GitHub Action currently is the ability to [manually trigger](https://github.community/t5/GitHub-Actions/GitHub-Actions-Manual-Trigger-Approvals/td-p/31504) a workflow. It is one of the highest voted feature requests. There are some [hacks and workarounds](https://stackoverflow.com/questions/5a8933155/manual-workflow-triggers-in-github-actions) available to achieve this but I did not spend much time exploring those options. In the longer term, I may switch to a [Trunk-based development](https://trunkbaseddevelopment.com/) where I can have more control over my releases.

## Next steps

There some enhancements I’m looking to work on next as and when I have some spare time.

- Ability to support multiple target frameworks. Currently, the package only supports .NET Core 3.1.
- Change the branching strategy, have separate release branches.
- Enhance GitHub actions, add features such as tagging, code coverage, code analysis, etc.
- Release the major version of the NuGet package.

## Conclusion

Publishing the NuGet package for my open source project was a unique experience. It was quite different from publishing NuGet packages for internal projects in my organization where we have more control. I intend to take these learnings and do similar projects in the future. I also hope that I was able to encourage some of you to take the first step into the world of open source and start working on your pet projects.

Source code: <https://github.com/ankitvijay/DeveloperExceptionJsonResponse>

NuGet package: <https://www.nuget.org/packages/DeveloperExceptionJsonResponse/>

Documentation: <https://ankitvijay.github.io/DeveloperExceptionJsonResponse/>

Please use the NuGet package and raise an [issue](https://github.com/ankitvijay/DeveloperExceptionJsonResponse/issues) to report a bug or feature-request. Contributions are welcome :).
