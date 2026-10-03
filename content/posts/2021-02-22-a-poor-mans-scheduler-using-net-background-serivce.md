---
title: "A poor person’s scheduler using .NET Background service"
date: "2021-02-22T06:47:12+10:00"
lastmod: "2022-12-23T23:04:47+10:00"
url: "/2021/02/22/a-poor-mans-scheduler-using-net-background-serivce/"
slug: "a-poor-mans-scheduler-using-net-background-serivce"
wp_id: 143490
category: ["backgroundservice", "net-5", "net-core"]
tag: ["background-worker", "backgroundservice", "cron", "net", "net-5", "net-core", "recurring-job", "scheduler-service"]
summary: "This post explains how can create a simple scheduler using .NET BackgroundService without using external libraries or serverless functions."
featured_image: "/wp-content/uploads/2022/12/1e566-schedulerservice.jpg"
---

Running a job on a schedule is a common and essential requirement in programming. All the major technologies and programming languages give developers a way to run a scheduler service, and .NET is no different.

.NET has popular libraries such as TopSelf, Quartz, Hangfire etc. that you can use to run your scheduled jobs. If you are on the cloud, you can leverage serverless solutions such as Azure Function, AWS Lamda and Google Cloud Functions to schedule your jobs.

However, there are occasions where we may want to keep things simple and avoid any external dependency.

This post explains how you can create a scheduler service using .NET [BackgroundService](https://docs.microsoft.com/en-us/dotnet/api/microsoft.extensions.hosting.backgroundservice?view=dotnet-plat-ext-5.0).

## Source Code

You can follow [this GitHub repository](https://github.com/ankitvijay/SchedulerJobSample) for the source code of the sample application. I’m using the .NET 5 SDK for the sample, but the solution should also work with previous versions of the .NET Core.

Let us first start with creating a **Worker**project with the default template that contains a **BackgroundService**, as shown below:

```csharp
using System;
using System.Collections.Generic;
using System.Linq;
using System.Threading;
using System.Threading.Tasks;
using Microsoft.Extensions.Hosting;
using Microsoft.Extensions.Logging;

namespace SchedulerJobSample.Worker
{
    public class Worker : BackgroundService
    {
        private readonly ILogger<Worker> _logger;

        public Worker(ILogger<Worker> logger)
        {
            _logger = logger;
        }

        protected override async Task ExecuteAsync(CancellationToken stoppingToken)
        {
            while (!stoppingToken.IsCancellationRequested)
            {
                _logger.LogInformation("Worker running at: {time}", DateTimeOffset.Now);
                await Task.Delay(1000, stoppingToken);
            }
        }
    }
}
```

Running the application would return an output similar to below:

![](/wp-content/uploads/2022/12/97500-backgroundresponse.png)

*Default background Service*

Next, we will create a recurring task using the [CRON](https://cron.help/) expression. Here, I have used the popular open-source library [CRONOS](https://github.com/HangfireIO/Cronos) to parse the CRON expression. In the below code, we have scheduled our background service to run every one minute.

```csharp
using System;
using System.Threading;
using System.Threading.Tasks;
using Cronos;
using Microsoft.Extensions.Hosting;
using Microsoft.Extensions.Logging;

namespace SchedulerJobSample.Worker
{
    public class SchedulerService : BackgroundService
    {
        private readonly ILogger<SchedulerService> _logger;

        public SchedulerService(ILogger<SchedulerService> logger)
        {
            _logger = logger;
        }

        protected override async Task ExecuteAsync(CancellationToken stoppingToken)
        {
            while (!stoppingToken.IsCancellationRequested)
            {
                // Schedule the job every minute.
                await WaitForNextSchedule("* * * * *");
                _logger.LogInformation("Worker running at: {time}", DateTimeOffset.Now);
            }
        }

        private async Task WaitForNextSchedule(string cronExpression)
        {
            var parsedExp = CronExpression.Parse(cronExpression);
            var currentUtcTime = DateTimeOffset.UtcNow.UtcDateTime;
            var occurenceTime = parsedExp.GetNextOccurrence(currentUtcTime);

            var delay = occurenceTime.GetValueOrDefault() – currentUtcTime;
            _logger.LogInformation("The run is delayed for {delay}. Current time: {time}", delay, DateTimeOffset.Now);

            await Task.Delay(delay);
        }
    }
}
```

Here is the console output after the change:

![](/wp-content/uploads/2022/12/6dbc4-backgroundjobrunningeverymin.png)

*A background service running every one min.*

## Running Scheduler as a Scoped Service

The BackgroundService is a [Singleton service](https://docs.microsoft.com/en-us/dotnet/core/extensions/dependency-injection#service-lifetimes). However, it may not be an ideal place to execute our recurring job with a scheduler since we may have some scoped dependencies, such as a database repository. Injecting a scoped or transient dependency in Singleton service could lead to [Captive Dependency](/2020/03/17/net-core-and-di-beware-of-captive-dependency/). To fix this, we can invoke a [scoped service within a BackgroundService](https://docs.microsoft.com/en-us/aspnet/core/fundamentals/host/hosted-services?view=aspnetcore-5.0&tabs=visual-studio#consuming-a-scoped-service-in-a-background-task).

To create a scoped scheduler service, we first need to create a scoped service and our scheduler job logic.

```csharp
using System;
using System.Threading;
using System.Threading.Tasks;
using Microsoft.Extensions.Logging;

namespace SchedulerJobSample.Worker
{
    public interface IScopedSchedulerService
    {
        Task ExecuteAsync(CancellationToken cancellationToken);
    }

    public class ScopedSchedulerService : IScopedSchedulerService
    {
        private readonly ILogger<ScopedSchedulerService> _logger;

        public ScopedSchedulerService(ILogger<ScopedSchedulerService> logger)
        {
            _logger = logger;
        }

        public Task ExecuteAsync(CancellationToken cancellationToken)
        {
            _logger.LogInformation("Worker running at: {time}", DateTimeOffset.Now);

            return Task.CompletedTask;
        }
    }
}
```

Next, we update **BackgroundService** to inject **IServiceProvider** and resolve the scoped service created in the previous step.

```csharp
using System;
using System.Threading;
using System.Threading.Tasks;
using Cronos;
using Microsoft.Extensions.DependencyInjection;
using Microsoft.Extensions.Hosting;
using Microsoft.Extensions.Logging;

namespace SchedulerJobSample.Worker
{
    public class SchedulerService : BackgroundService
    {
        private readonly ILogger<SchedulerService> _logger;
        private readonly IServiceProvider _serviceProvider;

        public SchedulerService(ILogger<SchedulerService> logger, IServiceProvider serviceProvider)
        {
            _logger = logger;
            _serviceProvider = serviceProvider;
        }

        protected override async Task ExecuteAsync(CancellationToken stoppingToken)
        {
            while (!stoppingToken.IsCancellationRequested)
            {
                // Schedule the job every minute.
                await WaitForNextSchedule("* * * * *");

                using var scope = _serviceProvider.CreateScope();
                var scopedSchedulerService = scope.ServiceProvider.GetRequiredService<IScopedSchedulerService>();
                await scopedSchedulerService.ExecuteAsync(stoppingToken);
            }
        }

        private async Task WaitForNextSchedule(string cronExpression)
        {
            var parsedExp = CronExpression.Parse(cronExpression);
            var currentUtcTime = DateTimeOffset.UtcNow.UtcDateTime;
            var occurenceTime = parsedExp.GetNextOccurrence(currentUtcTime);

            var delay = occurenceTime.GetValueOrDefault() – currentUtcTime;
            _logger.LogInformation("The run is delayed for {delay}. Current time: {time}", delay, DateTimeOffset.Now);

            await Task.Delay(delay);
        }
    }
}
```

Last but not least, we have to register our newly created scoped service in Program.cs.

```csharp
 services.AddHostedService<SchedulerService>();
                    services.AddScoped<IScopedSchedulerService, ScopedSchedulerService>();
```

That’s it! We now have the flexibility to invoke a recurring job within a scope.

**A word of caution:** The above code works well as long as you only have a single instance of your worker. However, if your worker has more than one instances deployed, it would run the job multiple times. To avoid this, you could use techniques like a distributed lock. I will talk more about this in a separate post.

## Wrapping up

This post explains how you can create a simple scheduler service without using an external library or serverless functions. I hope you find it useful. 🙂

> Feature Photo by [Fabrizio Verrecchia](https://unsplash.com/@fabrizioverrecchia?utm_source=unsplash&utm_medium=referral&utm_content=creditCopyText) on [Unsplash](https://unsplash.com/s/photos/clock?utm_source=unsplash&utm_medium=referral&utm_content=creditCopyText)
