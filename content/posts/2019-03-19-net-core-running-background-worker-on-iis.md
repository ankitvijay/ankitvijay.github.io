---
title: ".NET Core – Running Background Worker on IIS"
date: "2019-03-19T08:09:15+10:00"
lastmod: "2019-03-19T09:24:35+10:00"
url: "/2019/03/19/net-core-running-background-worker-on-iis/"
slug: "net-core-running-background-worker-on-iis"
wp_id: 3932
category: ["asp-net-core", "devops", "net-core"]
tag: ["asp-net-core", "background-worker", "devops", "iis", "net", "net-core", "net-core-2-1", "net-core-2-2", "octopus"]
summary: "One of the crucial pieces of the new solution that I’m working on is RabbitMQ. For those who have never heard of RabbitMQ, it is one of the most widely used open source message broker. Since our solution is hosted on-premise, RabbitMQ was one of the most natural fit for us. Our entire solution architecture"
---

One of the crucial pieces of the new solution that I’m working on is [RabbitMQ](https://www.rabbitmq.com/). For those who have never heard of RabbitMQ, it is one of the most widely used open source message broker. Since our solution is hosted on-premise, RabbitMQ was one of the most natural fit for us. Our entire solution architecture is built on .NET Core 2.1 and recently migrated to .NET Core 2.2. To run the RabbitMQ we had 3 options:

- Run RabbitMQ as a traditional .NET Framework “Windows Service”
- Run RabbitMQ as a .NET Core “Windows Service”
- Host RabbitMQ on IIS as a .NET Core application

Creating a .NET Framework based Windows Service was a known beast, as we have done it hundred times. However, since our entire solution was based on .NET Core, it was a step backward. As a result, we started exploring option 2, that is running RabbitMQ as a .NET Core based Windows Service. Our solution was largely inspired (read “Copied”) from Steve Gordan’s post on “[Running a .NET Core Generic Host App as a Windows Service](https://www.stevejgordon.co.uk/running-net-core-generic-host-applications-as-a-windows-service)“

Based on his post, we configured the solution to run as console application during development, and then as windows service at the time of deployment. However, we did not find deploying the windows service on .NET Core as simple as we initially thought. We had to modify project file to add `RunTimeIdentifier` or [RID](https://docs.microsoft.com/en-us/dotnet/core/rid-catalog). RID is OS and architecture specific. It is a different string based on OS, Version, Architecture. We did not want OS specific dependencies in our solution. In addition to this, a Windows-service also come up with its own set of complexities. It is difficult to debug and monitor as compared to a web hosted-service.

This is where we looked into the third option: Host the Background Worker on IIS. Hosting the Background Worker on IIS meant that we were able to deploy our Background Worker same as we would deploy a web app. Instead of using a “Generic Host” we were able to use default “Web Host”. There was less custom code. It was easier to debug and monitor. In addition to this, we were also able to leverage [.NET Core Health Checks](https://al-hardy.blog/2017/04/17/asp-net-core-health-checking/).

To run the background worker on the IIS, we had to tweak IIS settings to keep it always up and running. Here is the PowerShell script which we run on Octopus to update the IIS settings.

This file contains hidden or bidirectional Unicode text that may be interpreted or compiled differently than what appears below. To review, open the file in an editor that reveals hidden Unicode characters.
[Learn more about bidirectional Unicode characters](https://github.co/hiddenchars)

[Show hidden characters]({{ revealButtonHref }})

|  |  |
| --- | --- |
|  | ## IIS WebAdmin Module |
|  | Import-Module WebAdministration |
|  |  |
|  | $AppPoolInstance = Get-Item IIS:\AppPools\$AppPool |
|  |  |
|  | Write-Output "Set Site PreLoadEnabled to true" |
|  | Set-ItemProperty IIS:\Sites\$Site -name applicationDefaults.preloadEnabled -value True |
|  |  |
|  | Write-Output "Set Recycling.periodicRestart.time = 0" |
|  | $AppPoolInstance.Recycling.periodicRestart.time = [TimeSpan]::Parse("0"); |
|  | $AppPoolInstance | Set-Item |
|  |  |
|  | Write-Output "Set App Pool start up mode to AlwaysRunning" |
|  | $AppPoolInstance.startMode = "alwaysrunning" |
|  |  |
|  | Write-Output "Disable App Pool Idle Timeout" |
|  | $AppPoolInstance.processModel.idleTimeout = [TimeSpan]::FromMinutes(0) |
|  | $AppPoolInstance | Set-Item |
|  |  |
|  | if ($appPoolStatus -ne "Started") { |
|  | Write-Output "Starting App Pool" |
|  | Start-WebAppPool $AppPool |
|  | } else { |
|  | Write-Output "Restarting App Pool" |
|  | Restart-WebAppPool $AppPool |
|  | } |

[view raw](https://gist.github.com/ankitvijay/9dd0aef6450a30d34516e0642d5e30b5/raw/4e04d6127251b9fef763d9c6fed62ac1835739f7/AlwaysOn.ps)
[AlwaysOn.ps](https://gist.github.com/ankitvijay/9dd0aef6450a30d34516e0642d5e30b5#file-alwayson-ps)
hosted with ❤ by [GitHub](https://github.com)

Hope you find this useful. 🙂
