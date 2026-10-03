---
title: "NuGet packages – Our Standards and Defaults"
date: "2020-03-29T15:10:41+10:00"
lastmod: "2020-09-15T07:29:36+10:00"
url: "/2020/03/29/nuget-packages-our-standards-and-defaults/"
slug: "nuget-packages-our-standards-and-defaults"
wp_id: 4675
category: ["net-core", "nuget"]
tag: ["net", "net-core", "nuget"]
summary: "This posts talks about some of the standards and practices we use for our internal NuGet packages in our organization."
---

NuGet, the popular package manager for .NET, has been around since 2010. Over the years, its usage has grown exponentially. With the evolution of [.NET Standard class library](https://docs.microsoft.com/en-us/nuget/quickstart/create-and-publish-a-package-using-visual-studio?tabs=netcore-cli) creating a NuGet package is as easy as pie. You no longer need to define a separate nuspec file. NuGet package properties can be defined within the project files.

As part of our work, we create several NuGet packages for our internal teams. We need to provide a consistent experience for all our NuGet packages. To maintain consistency, we have defined a template that every NuGet package needs to derive from.

### Some common NuGet properties

Here are some of the properties we set to standardize our Nuget packages.

- `PackageTags` – Each Nuget package we create has one or more package tags. Our team name is one of the mandatory package tags. The package tags help to group the set of packages that are usually used in conjunction with each other. The package tags help with the discoverability of Nuget packages. An end-user can search by a package tag within Visual Studio or at our organization’s ProGet server.

- `PublishRepositoryUrl` – Setting this property to `true` allows the user to locate the source of NuGet package.

- `Authors` – `Authors` property is set to our team name. It helps anyone within the organization to know the creator of the Nuget package and reach out to the right person if they have any questions.

- `Description` – We use this field to clearly define the purpose of the NuGet package. This field provides an introduction to the NuGet package and how it can be consumed.

- `GenerateDocumentationFile` – Setting this property is set to `true` allows us to export the comments on all public access modifiers such as class, method, properties, etc. When this property is set, `dotnet build` also displays a warning if a comment on any type or member is missing. In addition to this, by “Treating warnings as errors” we ensure these warnings are turned into compile-time errors such as below. This way, we ensure every single type or member which can be consumed is documented.

error CS1591: Missing XML comment for publicly visible type or member ‘TypeName’

- `AllowedOutputExtensionsInPackageBuildOutputFolder`: Setting this property to `$(AllowedOutputExtensionsInPackageBuildOutputFolder);.pdb`
  allows us to include the`.pdb` files along with NuGet package.

### Other stuff

- **SourceLink**: Along with the above properties, we enable Source Link to our Nuget packages. Source Link allows users to step into the source code of the NuGet package. You can find more information on Source Link [here](https://github.com/dotnet/sourcelink).

- **Versioning**: Even though our NuGet packages are for internal distribution, we are still very disciplined with our versioning. We use [semver](https://semver.org/) through [GitVersion](https://gitversion.net/docs/more-info/version-increments) to version our packages. We increment the major, minor and patch versions through commit messages. We also try to keep our packages backward compatible as much as possible and introduce a breaking change only when necessary.

- **Directory.Build.props**: I must admit did not know about [Directory.Build.props](https://docs.microsoft.com/en-us/visualstudio/msbuild/customize-your-build?view=vs-2019) until very recently before my colleague, Werner suggested to use it. Directory.Build.props file allows us to customize the build. We can add a new property to every project in the solution by defining it in a single file with this name in the root folder. All the common Nuget properties within the solution can be added to the Directory.Build.props file. This helps us to avoid repetition and maintain consistency.

- **NuGetReferenceSwitcher:** [NugetReferenceSwitcher](https://github.com/RicoSuter/NuGetReferenceSwitcher) is a Visual Studio extension that allows us to switch between project reference and NuGet. This helps us to view the Nuget source code and allows us to develop as if NuGet package is part of our solution.

These are some of the standards and practices we use for our NuGet packages. Hope you find this useful. 🙂

> Photo by [Brandable Box](https://unsplash.com/@brandablebox?utm_source=unsplash&utm_medium=referral&utm_content=creditCopyText) on [Unsplash](https://unsplash.com/s/photos/package?utm_source=unsplash&utm_medium=referral&utm_content=creditCopyText)
