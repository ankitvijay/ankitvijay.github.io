---
title: ".NET Core and DI – Beware of Captive Dependency"
date: "2020-03-17T07:51:42+10:00"
lastmod: "2020-09-26T08:45:22+10:00"
url: "/2020/03/17/net-core-and-di-beware-of-captive-dependency/"
slug: "net-core-and-di-beware-of-captive-dependency"
wp_id: 4641
category: ["asp-net-core", "asp-net-core-3-1", "autofac", "captive-dependency", "net-core", "net-core-2-2", "net-core-3-0"]
tag: ["asp-net-core", "asp-net-core-3-1", "c", "captive-dependency", "dependency-injection", "net", "net-core", "net-core-3-0"]
summary: "The post explains captive dependency. It highlights the potential issues when you do not configure lifetime services correctly."
---

## Dependency Injection (DI) and IoC

Dependency Injection (DI) is one of the most important concepts in software engineering. We are no strangers to DI in the .NET world. Historically, the .NET framework had support for many IoC containers, such as [AutoFac](https://autofac.org/), [Castle Windsor](https://github.com/castleproject/Windsor/blob/master/docs/README.md), [Structure Map](https://structuremap.github.io/), [Unity](https://www.accusoft.com/resources/blog/dependency-injection-going-start-finish-unity-c/), etc. With the evolution of .NET Core, now ASP.NET Core comes up with a built-in IoC Container.

Before I proceed further, here is a quick recap of different lifetime services which comes with [ASP.NET Core Dependency Injection](https://docs.microsoft.com/en-us/aspnet/core/fundamentals/dependency-injection?view=aspnetcore-3.1):

### Transient

Transient lifetime services are created each time they’re requested from the service container. This lifetime works best for lightweight, stateless services.

### Scoped

Scoped lifetime services ([AddScoped](https://docs.microsoft.com/en-us/dotnet/api/microsoft.extensions.dependencyinjection.servicecollectionserviceextensions.addscoped)) are created once per client request (connection).

### Singleton

Singleton lifetime services ([AddSingleton](https://docs.microsoft.com/en-us/dotnet/api/microsoft.extensions.dependencyinjection.servicecollectionserviceextensions.addsingleton)) are created the first time they’re requested. Every subsequent request uses the same instance.

## I understand DI but what is a captive dependency?

The captive dependency issue perhaps is as old as Dependency Injection. Mark Seemann has defined [captive dependency](https://blog.ploeh.dk/2014/06/02/captive-dependency/) as follows:

> A Captive Dependency is a dependency with an incorrectly configured lifetime. It’s a typical and dangerous DI Container configuration error.

Let us consider a simple example:

- Consider a class **ScopedDependency** with a scoped lifetime.
- Consider a class **SingletonDependency** with singleton lifetime.

As per definition, **SingletonDependency** instance is created only once whereas a new **ScopedDependency** instance would be created for each request. What would happen if **SingletonDependency** takes a dependency on **ScopedDependency**?

This file contains hidden or bidirectional Unicode text that may be interpreted or compiled differently than what appears below. To review, open the file in an editor that reveals hidden Unicode characters.
[Learn more about bidirectional Unicode characters](https://github.co/hiddenchars)

[Show hidden characters]({{ revealButtonHref }})

|  |  |
| --- | --- |
|  | public class ScopedDependency |
|  | { |
|  | public static int _counter = 0; |
|  | public ScopedDependency() |
|  | { |
|  | ++_counter; |
|  | } |
|  |  |
|  | public int GetNextCounter() |
|  | { |
|  | return _counter; |
|  | } |
|  | } |

[view raw](https://gist.github.com/ankitvijay/52c7b4adf758aae464008d7dbeb4bcb5/raw/71f7b88e6fab1477857d955d3a59a1f936c499c5/ScopedDependency.cs)
[ScopedDependency.cs](https://gist.github.com/ankitvijay/52c7b4adf758aae464008d7dbeb4bcb5#file-scopeddependency-cs)
hosted with ❤ by [GitHub](https://github.com)

This file contains hidden or bidirectional Unicode text that may be interpreted or compiled differently than what appears below. To review, open the file in an editor that reveals hidden Unicode characters.
[Learn more about bidirectional Unicode characters](https://github.co/hiddenchars)

[Show hidden characters]({{ revealButtonHref }})

|  |  |
| --- | --- |
|  | public class SingletonDependency |
|  | { |
|  | private readonly ScopedDependency scopedDepdendency; |
|  |  |
|  | // Should this blow up?? |
|  | public SingletonDependency(ScopedDependency transitiveDependecy) |
|  | { |
|  | this.scopedDepdendency = transitiveDependecy; |
|  | } |
|  |  |
|  | public int GetNextCounter() |
|  | { |
|  | return scopedDepdendency.GetNextCounter(); |
|  | } |
|  | } |

[view raw](https://gist.github.com/ankitvijay/2ff079e425e14fa7a482fa54d331ecdd/raw/dad6e77ee85b211f9483d061ad5eb67b572a1e3f/SingletonDependency.cs)
[SingletonDependency.cs](https://gist.github.com/ankitvijay/2ff079e425e14fa7a482fa54d331ecdd#file-singletondependency-cs)
hosted with ❤ by [GitHub](https://github.com)

This file contains hidden or bidirectional Unicode text that may be interpreted or compiled differently than what appears below. To review, open the file in an editor that reveals hidden Unicode characters.
[Learn more about bidirectional Unicode characters](https://github.co/hiddenchars)

[Show hidden characters]({{ revealButtonHref }})

|  |  |
| --- | --- |
|  | public void ConfigureServices(IServiceCollection services) |
|  | { |
|  | services.AddControllers(); |
|  |  |
|  | services.AddSingleton<SingletonDependency>(); |
|  | services.AddTransient<TransientDependency>(); |
|  | } |

[view raw](https://gist.github.com/ankitvijay/619cc66aa3b79173dfb1a7c2009cc167/raw/ba7b3d2c84b0a71a6409c3ebdbdfd20d54e4618d/Startup.cs)
[Startup.cs](https://gist.github.com/ankitvijay/619cc66aa3b79173dfb1a7c2009cc167#file-startup-cs)
hosted with ❤ by [GitHub](https://github.com)

As you can see in code, for every new request a when **ScopedDependency** is instantiated, you would expect the counter to increment by 1. Unfortunately, when you instantiate **SingletonDepedency**, it would hold on to a stale instance **ScopedDependency** which was created for the first-ever request.

In a complex architecture, captive dependency can lead to notorious runtime bugs which can very hard to identify and debug.

Even the IoC containers such as Autofac do not prevent developers from creating captive dependency and leave the responsibility to the developers. From the [documentation](https://docs.autofac.org/en/latest/lifetime/captive-dependencies.html):

> **Autofac does not necessarily prevent you from creating captive dependencies.** You may find times when you get a resolution exception because of the way a captive is set up, but you won’t always. Stopping captive dependencies is the responsibility of the developer.

## ASP.NET Core tries to solve this problem (but just partially)

ASP.NET Core default service container provides a way to deduct the captive dependency. However, it is an opt-in feature. To opt-in to this feature, you would need to set property **ValidateScopes** in **Program.cs** as shown below.

This file contains hidden or bidirectional Unicode text that may be interpreted or compiled differently than what appears below. To review, open the file in an editor that reveals hidden Unicode characters.
[Learn more about bidirectional Unicode characters](https://github.co/hiddenchars)

[Show hidden characters]({{ revealButtonHref }})

|  |  |
| --- | --- |
|  | public class Program |
|  | { |
|  | public static void Main(string[] args) |
|  | { |
|  | CreateHostBuilder(args).Build().Run(); |
|  | } |
|  |  |
|  | public static IHostBuilder CreateHostBuilder(string[] args) => |
|  | Host.CreateDefaultBuilder(args) |
|  | .ConfigureWebHostDefaults(webBuilder => |
|  | { |
|  | webBuilder.UseStartup<Startup>(); |
|  | }) |
|  | .UseDefaultServiceProvider((env, c) => |
|  | { |
|  | if (env.HostingEnvironment.IsDevelopment()) |
|  | { |
|  | c.ValidateScopes = true; |
|  | } |
|  | }); |
|  | } |

[view raw](https://gist.github.com/ankitvijay/89fd6fe6018d133780d81823f945e1aa/raw/d90a38de23c75ea352bb4d23411158916ec62f14/Program.cs)
[Program.cs](https://gist.github.com/ankitvijay/89fd6fe6018d133780d81823f945e1aa#file-program-cs)
hosted with ❤ by [GitHub](https://github.com)

When you try to run your application now, you would receive an **InvalidOperationException**.

![](/wp-content/uploads/2020/03/Capture.jpg)

An important thing to note here is that validating scope at the **Startup**is a performance intensive operation. Hence, you may want only to set this property during development.

Also, this solution is not a silver bullet. As the name suggests, it only validates “Scoped” dependencies. This property does not work when you have **Transient**lifetime services.

## A real-world example

One of the real-world examples where this issue can bite you hard is when you try to use **Typed HttpClient** by registering your service through **AddHttpClient**. A Typed HttpClient has a transient lifetime. From the [documentation](https://docs.microsoft.com/en-us/dotnet/architecture/microservices/implement-resilient-applications/use-httpclientfactory-to-implement-resilient-http-requests)

> A Typed Client is, effectively, a transient object, meaning that a new instance is created each time one is needed and it will receive a new `HttpClient` instance each time it’s constructed. However, the `HttpMessageHandler` objects in the pool are the objects that are reused by multiple `HttpClient` instances.

Since, Typed Client is a transient object, using it in singleton service could lead to unexpected issues.

This file contains hidden or bidirectional Unicode text that may be interpreted or compiled differently than what appears below. To review, open the file in an editor that reveals hidden Unicode characters.
[Learn more about bidirectional Unicode characters](https://github.co/hiddenchars)

[Show hidden characters]({{ revealButtonHref }})

|  |  |
| --- | --- |
|  | public void ConfigureServices(IServiceCollection services) |
|  | { |
|  | services.AddControllers(); |
|  |  |
|  | services.AddSingleton<SingletonService>(); |
|  | services.AddHttpClient<CatalogClient>(); |
|  | } |

[view raw](https://gist.github.com/ankitvijay/287c2a8bc484205ec6e44ab2d27e43b5/raw/ce667452406814a74dd43e07552a79021c992ac1/1_Startup.cs)
[1_Startup.cs](https://gist.github.com/ankitvijay/287c2a8bc484205ec6e44ab2d27e43b5#file-1_startup-cs)
hosted with ❤ by [GitHub](https://github.com)

This file contains hidden or bidirectional Unicode text that may be interpreted or compiled differently than what appears below. To review, open the file in an editor that reveals hidden Unicode characters.
[Learn more about bidirectional Unicode characters](https://github.co/hiddenchars)

[Show hidden characters]({{ revealButtonHref }})

|  |  |
| --- | --- |
|  | public class SingletonService |
|  | { |
|  | // Warning: This is crime!!! – DO NOT DO THIS |
|  | public SingletonService(CatalogClient catalogClient) |
|  | { |
|  | this.catalogClient = catalogClient; |
|  | } |
|  |  |
|  | public async Task<List<string>> GetCatalogs() |
|  | { |
|  | return await catalogClient.GetCatalogs(); |
|  | } |
|  | } |

[view raw](https://gist.github.com/ankitvijay/287c2a8bc484205ec6e44ab2d27e43b5/raw/ce667452406814a74dd43e07552a79021c992ac1/2_SingletonService.cs)
[2_SingletonService.cs](https://gist.github.com/ankitvijay/287c2a8bc484205ec6e44ab2d27e43b5#file-2_singletonservice-cs)
hosted with ❤ by [GitHub](https://github.com)

Of course, you easily fix this creating a [ClientFactory](https://josefottosson.se/you-are-probably-still-using-httpclient-wrong-and-it-is-destabilizing-your-software/).

This file contains hidden or bidirectional Unicode text that may be interpreted or compiled differently than what appears below. To review, open the file in an editor that reveals hidden Unicode characters.
[Learn more about bidirectional Unicode characters](https://github.co/hiddenchars)

[Show hidden characters]({{ revealButtonHref }})

|  |  |
| --- | --- |
|  | public void ConfigureServices(IServiceCollection services) |
|  | { |
|  | services.AddSingleton<SingletonService>(); |
|  | services.AddSingleton<CatalogClientFactory>(); |
|  | services.AddHttpClient<CatalogClient>(); |
|  | } |

[view raw](https://gist.github.com/ankitvijay/9ed7ce02a3f54312d10991d989c5c421/raw/5ac56493161fffa3cc76cfe7e0212a7f64a83980/1_Startup.cs)
[1_Startup.cs](https://gist.github.com/ankitvijay/9ed7ce02a3f54312d10991d989c5c421#file-1_startup-cs)
hosted with ❤ by [GitHub](https://github.com)

This file contains hidden or bidirectional Unicode text that may be interpreted or compiled differently than what appears below. To review, open the file in an editor that reveals hidden Unicode characters.
[Learn more about bidirectional Unicode characters](https://github.co/hiddenchars)

[Show hidden characters]({{ revealButtonHref }})

|  |  |
| --- | --- |
|  | public class CatalogClientFactory |
|  | { |
|  | private readonly IServiceProvider serviceProvider; |
|  |  |
|  | public CatalogClientFactory(IServiceProvider serviceProvider) |
|  | { |
|  | this.serviceProvider = serviceProvider; |
|  | } |
|  |  |
|  | public CatalogClient Create() => serviceProvider.GetService<CatalogClient>(); |
|  | } |

[view raw](https://gist.github.com/ankitvijay/9ed7ce02a3f54312d10991d989c5c421/raw/5ac56493161fffa3cc76cfe7e0212a7f64a83980/2_CatalogClientFactory.cs)
[2_CatalogClientFactory.cs](https://gist.github.com/ankitvijay/9ed7ce02a3f54312d10991d989c5c421#file-2_catalogclientfactory-cs)
hosted with ❤ by [GitHub](https://github.com)

This file contains hidden or bidirectional Unicode text that may be interpreted or compiled differently than what appears below. To review, open the file in an editor that reveals hidden Unicode characters.
[Learn more about bidirectional Unicode characters](https://github.co/hiddenchars)

[Show hidden characters]({{ revealButtonHref }})

|  |  |
| --- | --- |
|  | public class SingletonService |
|  | { |
|  | private readonly CatalogClientFactory catalogClientFactory; |
|  |  |
|  | public SingletonService(CatalogClientFactory catalogClientFactory) |
|  | { |
|  | this.catalogClientFactory = catalogClientFactory; |
|  | } |
|  |  |
|  | public async Task<List<string>> GetCatalogs() |
|  | { |
|  | return await catalogClientFactory.Create().GetCatalogs(); |
|  | } |
|  | } |

[view raw](https://gist.github.com/ankitvijay/9ed7ce02a3f54312d10991d989c5c421/raw/5ac56493161fffa3cc76cfe7e0212a7f64a83980/3_SingletonService.cs)
[3_SingletonService.cs](https://gist.github.com/ankitvijay/9ed7ce02a3f54312d10991d989c5c421#file-3_singletonservice-cs)
hosted with ❤ by [GitHub](https://github.com)

The problem, however, is that it is “one more thing” that you need to remember. There are no guard rails to stop a developer from using it wrongly.

## Conclusion

Please be extra careful when defining the lifetimes of your services. At this point in time, the ASP.NET Core default IoC container does not do a great job in preventing captive dependency issues. The captive dependency issues are hard to deduct and could lead to runtime errors. I hope that I’m able to highlight pitfalls of not configuring the lifetimes correctly.

[CodeProject](https://www.codeproject.com)
