---
title: "Passing correlation id across requests"
date: "2020-11-24T22:30:17+10:00"
lastmod: "2020-11-25T08:42:45+10:00"
url: "/2020/11/24/passing-correlation-id-across-requests/"
slug: "passing-correlation-id-across-requests"
wp_id: 49920
category: ["architecture", "asp-net-core", "corelation-id", "event-driven-architecture", "microservices", "net-core"]
tag: ["asp-net-core", "correlation-id", "logging", "net", "net-core", "serilog", "tracking"]
summary: "This post describes importance of passing a single correlation id across requests in microservices and how we an achieve this in .NET."
featured_image: "/wp-content/uploads/2022/12/4c2c8-zach-lucero-x_x3rppdbii-unsplash-e1606222303198.jpg"
---

Over the past few years, the software world has evolved rapidly. Microservices and Event-Driven Architecture are no longer buzzwords. They have become a new default. Microservices, being loosely coupled enable teams to develop faster and independently.

Unfortunately, for all the goodness that microservices bring, it also comes at a cost. Instead of one single monolith, we now need to deal with multiple services. A request from a client may go through numerous service boundaries, making it hard to track and find a bug in production. Hence, each service must log every request/ event in consistently and homogenously to make it easy to trace. This could be achieve this is by adding a correlation id to every log from different services.

In the next section, I will talk about how we can achieve this in .NET.

### The code – Passing correlation id to logs

The **CorrelationIdContext**class below helps us to set and get the correlation id for a given request.

```csharp
public class CorrelationIdContext
{
    private static readonly AsyncLocal<string> _correlationId = new AsyncLocal<string>();

    public static void SetCorrelationId(string correlationId)
    {
        if (string.IsNullOrWhiteSpace(correlationId)
        {
            throw new ArgumentException("Correlation Id cannot be null or empty", nameof(correlationId));
        }

        if (!string.IsNullOrWhiteSpace(_correlationId.Value))
        {
            throw new InvalidOperationException("Correlation Id is already set for the context");
        }

        _correlationId.Value = correlationId;
    }

    public static string GetCorrelationId()
    {
        return _correlationId.Value;
    }
}
```

Let us deep-dive into the code little more. The **_correlationId**is a private [AsyncLocal](https://docs.microsoft.com/en-us/dotnet/api/system.threading.asynclocal-1?view=net-5.0)variable. AsyncLocal has been around since .NET Framework 4.6. AsyncLocal can help us store ambient data that is local to an asynchronous control flow. That is, AsyncLocal can persist a value across an asynchronous flow.

We can call **CorrelationIdContext.SetCorrelationId** to set the Correlation id for “request context” at the start of the request in ASP.NET Core or while subscribing to message/event from a message bus.

Note: It is essential to reiterate that **CorrelationIdContext**usage is not limited to ASP.NET Core. We can also use it in serverless, hosted service, background worker, etc., albeit, with caution.

In ASP.NET Core, we can create a middleware to set the correlation id at the start of the request.

```csharp
public class CorrelationIdMiddleware
{
    private readonly RequestDelegate _next;

    public CorrelationIdMiddleware(RequestDelegate next)
    {
        _next = next;
    }

    public async Task Invoke(HttpContext context)
    {
        context.Request.Headers.TryGetValue("correlation-id", out var correlationIds);

        var correlationId = correlationIds.FirstOrDefault() ?? Guid.NewGuid().ToString();

        CorrelationContext.SetCorrelationId(correlationId);

        // Serilog
        using (LogContext.PushProperty("correlation-id", correlationId))
        {
            await _next.Invoke(context);
        }
    }
}
```

```csharp
public class Startup
{
    public virtual void ConfigureServices(IServiceCollection services)
    {
       // Code removed for brevity
    }

    public void Configure(IApplicationBuilder app)
    {
        // Add Middleware at start of the reqeust
        app.UseMiddleware<CorrelationIdMiddleware>();

        app.UseRouting();

        app.UseEndpoints(endpoints => endpoints.MapControllers());
    }
}
```

As you can see from the above code, we try to read the correlation id from the request header. If it is missing, we create a new correlation id and set it in CorrelationContext**.**Next, we enrich our logs by pushing the correlation to [Serilog LogContext](https://github.com/serilog/serilog/wiki/Enrichment#the-logcontext).

We can access the correlation id anywhere in the request context by calling **CorrelationIdContext .GetCorrelationId**.

To pass the correlation id to any downstream service, we can set default request header to the HttpClient.

```csharp
public class Startup
{
    public virtual void ConfigureServices(IServiceCollection services)
    {
       services.AddHttpClient<IMyServiceClient, MyServiceClient>((serviceProvider, client) =>
            {
                client.BaseAddress = customerCoreServiceOptions.BaseUri;
                client.DefaultRequestHeaders.Add("correlation-id",
                                                 CorrelationIdContext.GetCorrelationId() ??
                                                 Guid.NewGuid().ToString());
            });
    }

    public void Configure(IApplicationBuilder app)
    {
      // Code removed for brevity
    }
}
```

### Wrapping Up

Tracing a request in a distributed environment is essential to find bugs in production. In real-world, we may have systems written in a variety of frameworks/ languages within an organization. However, still, it is crucial to have the same standard across the heterogeneous services. Having a one standard across the organization can remove ambiguity and help us pinpoint the faulty service.
