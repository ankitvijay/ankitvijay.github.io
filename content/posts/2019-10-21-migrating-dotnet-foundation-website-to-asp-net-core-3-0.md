---
title: "Migrating Dotnet Foundation website to ASP.NET Core 3.0"
date: "2019-10-21T07:49:07+10:00"
lastmod: "2020-09-15T07:40:25+10:00"
url: "/2019/10/21/migrating-dotnet-foundation-website-to-asp-net-core-3-0/"
slug: "migrating-dotnet-foundation-website-to-asp-net-core-3-0"
wp_id: 4240
category: ["asp-net-core", "azure-app-service", "net-core", "net-core-2-2", "net-core-3-0"]
tag: ["asp-net-core", "migration", "net", "net-core-2-2", "net-core-3-0", "upgrade"]
summary: "I recently migrated the Dotnet Foundation website, https://dotnetfoundation.org/ to ASP.NET Core 3.0. The site was initially built on ASP.NET Core 2.1 and I found this as a good learning opportunity. Migrating from ASP.NET Core 2.1 to 2.2 I had initially raised PR to migrate from ASP.NET Core 2.1 to 2.2 instead of directly going to"
---

I recently migrated the Dotnet Foundation website, <https://dotnetfoundation.org/> to ASP.NET Core 3.0. The site was initially built on ASP.NET Core 2.1 and I found this as a good learning opportunity.

### Migrating from ASP.NET Core 2.1 to  2.2

I had initially raised PR to migrate from ASP.NET Core 2.1 to 2.2 instead of directly going to ASP.NET 3.0. The reason I chose to not migrate to ASP.NET Core 3.0 directly was that `dotnetfondation.org` is hosted on Azure App service and at the time of writing ASP.NET Core 3.0 is not available for Azure App Service. As per the [documentation](https://docs.microsoft.com/en-us/aspnet/core/migration/22-to-30?view=aspnetcore-3.0&tabs=visual-studio#aspnet-core-30-not-currently-available-for-azure-app-service):

> ## ASP.NET Core 3.0 not currently available for Azure App Service
>
> We hope to make this available soon. Until ASP.NET Core 3.0 is available on Azure App Service, follow the instructions at [Deploy ASP.NET Core preview release to Azure App Service](https://docs.microsoft.com/en-us/aspnet/core/host-and-deploy/azure-apps/index?view=aspnetcore-3.0#deploy-aspnet-core-preview-release-to-azure-app-service).

Migrating to ASP.NET Core 2.1 did not turn out to be too tricky and [Microsoft documentation](https://docs.microsoft.com/en-us/aspnet/core/migration/21-to-22?view=aspnetcore-3.0&tabs=visual-studio) helped to seamlessly migrate to ASP.NET Core 2.2.

Here are the [PR](https://github.com/dotnet-foundation/dotnetfoundation-website/pull/101) and [diff](https://github.com/dotnet-foundation/dotnetfoundation-website/pull/101/commits/6c6cfc7b9c14049633e0d9dda3217a6dd3db3c62) of my initial attempt at migration. However, @jongalloway suggested to migrate to ASP.NET Core 3.0 directly and he would do then do a self-contained deployment. So, I decided to migrate the application to ASP.NET Core 3.0 as per his suggestion.

<blockquote class="twitter-tweet" data-dnt="true" data-width="500"><p dir="ltr" lang="en">Replied… are you up for updating this to 3.0 and I'll handle the self contained deployment to Azure?</p>— Jon Galloway (@jongalloway) <a href="https://twitter.com/jongalloway/status/1181042570018734080?ref_src=twsrc%5Etfw">October 7, 2019</a></blockquote>

### Migrating from ASP.NET Core 2.2 to  3.0

Migrating from ASP.NET Core 2.2 to 3.0 required slightly more work since ASP.NET Core 3.0 is a major release. But again, the [Microsoft documentation](https://docs.microsoft.com/en-us/aspnet/core/migration/22-to-30?view=aspnetcore-3.0&tabs=visual-studio#aspnet-core-30-not-currently-available-for-azure-app-service) came to the rescue. Here is my [PR](https://github.com/dotnet-foundation/dotnetfoundation-website/pull/107) for migration to ASP.NET Core 3.0.

Below are the list of the changes I went through to complete the migration. Note that the diff you see here is from my commit to upgrading to ASP.NET Core 2.2 to 3.0:

**Pre-requisite: Upgrade to Visual Studio 2019 to version 16.3 or greater**

As a first step, I downloaded .NET Core 3.0 SDK from [here](https://dotnet.microsoft.com/download/dotnet-core/3.0). I also had to update Visual Studio 2019 to the latest version as .NET Core 3.0 needs [version 16.3 or greater](https://devblogs.microsoft.com/visualstudio/dot-net-core-support-in-visual-studio-2019-version-16-3/).

**U****pgrade to** **netcoreapp3.0**

Once I was on the latest version of Visual Studio, I started with the most obvious change. That is, updating the `TargetFramework` in the `csproj` file to  `netcoreapp3.0`. In addition to this, I removed `AspNetCoreHostingModel` element which was added  during `ASP.NET Core 2.2` upgrade. This element can be removed because projects default to in-process hosting model in ASP.NET Core 3.0. From the [documentation](https://docs.microsoft.com/en-us/aspnet/core/migration/22-to-30?view=aspnetcore-3.0&tabs=visual-studio#in-process-hosting-model):

> Projects default to the [in-process hosting model](https://docs.microsoft.com/en-us/aspnet/core/host-and-deploy/aspnet-core-module?view=aspnetcore-3.0#in-process-hosting-model) in ASP.NET Core 3.0 or later. You may optionally remove the `<AspNetCoreHostingModel>` property in the project file if its value is `InProcess`.

![Update to netcore3.0](/wp-content/uploads/2022/12/af646-csproj-1426460620-1571547477400.png)

*Replace netcoreapp2.2 to netcoreapp3.0 and removed AspNetCoreHostingModel*

**Upgrade all the** **NuGet** **packages to the latest version and remove obsolete packages**

Updating the `Targetframework` led to several build errors. I then upgraded all `NuGet` packages to the latest version and removed `obsolete` packages such as  `Microsoft.AspNetCore.App`.

Note that realistically I needed to only update the packages which were impacted due to .NET Core 3.0 upgrade. But instead of worrying about what to upgrade, I decided to upgrade all the packages. I found upgrading all packages to be less daunting even if it meant that there could be more breaking changes.

![Nuget](/wp-content/uploads/2022/12/af3a0-nuget-1.png)

*Upgrade NuGet packages and remove obsolete packages*

**Replace IHostingEnvironment to IWebHostEnvironment and add Microsoft.Extensions.Hosting**

With .NET Core 3.0. `IHostingEnvironment` has been deprecated in favor of `IWebHostEnviroment`. Also, extension methods such as `IHostEnvironment`,  `IsDevelopment` etc now available in `Microsoft.Extensions.Hosting`. See this GitHub [announcement](https://github.com/aspnet/AspNetCore/issues/7749) for additional information.

Hence next, I replaced `IHostingEnvironent` with `IWebHostEnvironment` and added a reference to `Microsoft.Extensions.Hosting` wherever applicable.

![](/wp-content/uploads/2022/12/5ed1e-iwebhostingenvironment2-620350882-1571608265363.png)

*Add package Micorosft.Extensions.Hosting and replace IHostingEnvironment with IWebHostEnvironment*

**Update to Routing and MVC controllers**

Next, I made the following changes with respect to routing.

- Introduced `app.UseRouting` in `Startup.cs`. This is required to be added in after `UseStaticFiles` . See: [Migrate Startup.Configure](https://docs.microsoft.com/en-us/aspnet/core/migration/22-to-30?view=aspnetcore-3.0&tabs=visual-studio#migrate-startupconfigure) for details
- Replaced `UseMvc` with `UseEndpoints`. Mapping of controllers and `RazorPages` now takes place inside `UseEndpoint` .
- Replaced `MapRoute` with `MapControllerRoute` inside `UseEndpoint`. See: [MVC controllers](http:// https://docs.microsoft.com/en-us/aspnet/core/migration/22-to-30?view=aspnetcore-3.0&tabs=visual-studio#mvc-controllers)
- Introduced `endpoint.MapRazorPages` inside `UseEndpoint`. See [MVC service registration](https://docs.microsoft.com/en-us/aspnet/core/migration/22-to-30?view=aspnetcore-3.0&tabs=visual-studio#mvc-service-registration)

![](/wp-content/uploads/2022/12/37df6-userouting-4-4149386746-1571603968201.png)

*Add UseRouting, replace UseMvc with UseEndpints, add MapRazorPages*

![ControllerRouting](/wp-content/uploads/2022/12/7d794-controllerrouting-1.png)

*Replace MapRoute with MapControllerRoute*

**Remove SetCompatibilityVersion**

With .NET Core 3.0, `SetCompatiblityVersion` is no longer required. According to [documentation](https://docs.microsoft.com/en-us/aspnet/core/mvc/compatibility-version?view=aspnetcore-3.0):

> The [SetCompatibilityVersion](https://docs.microsoft.com/dotnet/api/microsoft.extensions.dependencyinjection.mvccoremvcbuilderextensions.setcompatibilityversion) method is a no-op for ASP.NET Core 3.0 apps. That is, calling `SetCompatibilityVersion` with any value of [CompatibilityVersion](https://docs.microsoft.com/dotnet/api/microsoft.aspnetcore.mvc.compatibilityversion) has no impact on the application.

Hence, the method call was removed.

![RemoveSetCompatibilityVersion](/wp-content/uploads/2022/12/18a55-removesetcompatibilityversion.png)

*Remove SetCompatiblityVersion*

### Conclusion

The migration exercise of ASP.NET Core 2.2 to 3.0 was not too much work. The Microsoft documentation is quite comprehensive and provides all the information you would need to migrate your app to the latest and the greatest. I now cannot wait to migrate our enterprise applications to .NET Core 3.0.

> Feature Photo by [Amber Walker](https://unsplash.com/@artwalker?utm_source=unsplash&utm_medium=referral&utm_content=creditCopyText) on [Unsplash](https://unsplash.com/s/photos/migrate?utm_source=unsplash&utm_medium=referral&utm_content=creditCopyText)
