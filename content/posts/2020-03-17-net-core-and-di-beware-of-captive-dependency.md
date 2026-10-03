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

Dependency Injection (DI) is one of the most important concepts in software engineering. We are no strangers to DI in the .NET world. Historically, the .NET framework had support for many IoC containers, such as [AutoFac](https://autofac.org/), [Castle Windsor](https://github.com/castleproject/Windsor/blob/master/docs/README.md), [Structure Map](https://structuremap.github.io/), [Unity](https://www.accusoft.com/resources/blog/dependency-injection-going-start-finish-unity-c/), etc. With the evolution of .NET Core, now ASP.NET Core comes up with a built-in IoC Container.

Before I proceed further, here is a quick recap of different lifetime services which comes with [ASP.NET Core Dependency Injection](https://docs.microsoft.com/en-us/aspnet/core/fundamentals/dependency-injection?view=aspnetcore-3.1):

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

```csharp
public class ScopedDependency
{
 public static int _counter = 0;
 public ScopedDependency()
 {
 ++_counter;
 }

 public int GetNextCounter()
 {
 return _counter;
 }
}
```

```csharp
public class SingletonDependency
{
    private readonly ScopedDependency scopedDepdendency;

    // Should this blow up??
    public SingletonDependency(ScopedDependency transitiveDependecy)
    {
        this.scopedDepdendency = transitiveDependecy;
    }

    public int GetNextCounter()
    {
        return scopedDepdendency.GetNextCounter();
    }
}
```

```csharp
public void ConfigureServices(IServiceCollection services)
{
    services.AddControllers();

    services.AddSingleton<SingletonDependency>();
    services.AddTransient<TransientDependency>();
}
```

As you can see in code, for every new request a when **ScopedDependency** is instantiated, you would expect the counter to increment by 1. Unfortunately, when you instantiate **SingletonDepedency**, it would hold on to a stale instance **ScopedDependency** which was created for the first-ever request.

In a complex architecture, captive dependency can lead to notorious runtime bugs which can very hard to identify and debug.

Even the IoC containers such as Autofac do not prevent developers from creating captive dependency and leave the responsibility to the developers. From the [documentation](https://docs.autofac.org/en/latest/lifetime/captive-dependencies.html):

> **Autofac does not necessarily prevent you from creating captive dependencies.** You may find times when you get a resolution exception because of the way a captive is set up, but you won’t always. Stopping captive dependencies is the responsibility of the developer.

## ASP.NET Core tries to solve this problem (but just partially)

ASP.NET Core default service container provides a way to deduct the captive dependency. However, it is an opt-in feature. To opt-in to this feature, you would need to set property **ValidateScopes** in **Program.cs** as shown below.

```csharp
public class Program
{
    public static void Main(string[] args)
    {
        CreateHostBuilder(args).Build().Run();
    }

    public static IHostBuilder CreateHostBuilder(string[] args) =>
        Host.CreateDefaultBuilder(args)
            .ConfigureWebHostDefaults(webBuilder =>
            {
                webBuilder.UseStartup<Startup>();
            })
        .UseDefaultServiceProvider((env, c) =>
        {
            if (env.HostingEnvironment.IsDevelopment())
            {
                c.ValidateScopes = true;
            }
        });
}
```

When you try to run your application now, you would receive an **InvalidOperationException**.

![](/wp-content/uploads/2020/03/Capture.jpg)

An important thing to note here is that validating scope at the **Startup**is a performance intensive operation. Hence, you may want only to set this property during development.

Also, this solution is not a silver bullet. As the name suggests, it only validates “Scoped” dependencies. This property does not work when you have **Transient**lifetime services.

## A real-world example

One of the real-world examples where this issue can bite you hard is when you try to use **Typed HttpClient** by registering your service through **AddHttpClient**. A Typed HttpClient has a transient lifetime. From the [documentation](https://docs.microsoft.com/en-us/dotnet/architecture/microservices/implement-resilient-applications/use-httpclientfactory-to-implement-resilient-http-requests)

> A Typed Client is, effectively, a transient object, meaning that a new instance is created each time one is needed and it will receive a new `HttpClient` instance each time it’s constructed. However, the `HttpMessageHandler` objects in the pool are the objects that are reused by multiple `HttpClient` instances.

Since, Typed Client is a transient object, using it in singleton service could lead to unexpected issues.

```csharp
public void ConfigureServices(IServiceCollection services)
{
    services.AddControllers();

    services.AddSingleton<SingletonService>();
    services.AddHttpClient<CatalogClient>();
}
```

```csharp
public class SingletonService
{
    // Warning: This is crime!!! – DO NOT DO THIS
   public SingletonService(CatalogClient catalogClient)
    {
        this.catalogClient = catalogClient;
    }

    public async Task<List<string>> GetCatalogs()
    {
        return await catalogClient.GetCatalogs();
    }
}
```

Of course, you easily fix this creating a [ClientFactory](https://josefottosson.se/you-are-probably-still-using-httpclient-wrong-and-it-is-destabilizing-your-software/).

```csharp
public void ConfigureServices(IServiceCollection services)
{
 services.AddSingleton<SingletonService>();
 services.AddSingleton<CatalogClientFactory>();
 services.AddHttpClient<CatalogClient>();
}
```

```csharp
public class CatalogClientFactory
{
    private readonly IServiceProvider serviceProvider;

    public CatalogClientFactory(IServiceProvider serviceProvider)
    {
        this.serviceProvider = serviceProvider;
    }

    public CatalogClient Create() => serviceProvider.GetService<CatalogClient>();
}
```

```csharp
public class SingletonService
{
    private readonly CatalogClientFactory catalogClientFactory;

    public SingletonService(CatalogClientFactory catalogClientFactory)
    {
        this.catalogClientFactory = catalogClientFactory;
    }

    public async Task<List<string>> GetCatalogs()
    {
        return await catalogClientFactory.Create().GetCatalogs();
    }
}
```

The problem, however, is that it is “one more thing” that you need to remember. There are no guard rails to stop a developer from using it wrongly.

## Conclusion

Please be extra careful when defining the lifetimes of your services. At this point in time, the ASP.NET Core default IoC container does not do a great job in preventing captive dependency issues. The captive dependency issues are hard to deduct and could lead to runtime errors. I hope that I’m able to highlight pitfalls of not configuring the lifetimes correctly.

[CodeProject](https://www.codeproject.com)
