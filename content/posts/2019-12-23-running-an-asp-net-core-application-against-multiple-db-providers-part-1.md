---
title: "Running an ASP.NET Core application against multiple DB providers – Part 1"
date: "2019-12-23T07:56:09+10:00"
lastmod: "2022-12-23T23:04:47+10:00"
url: "/2019/12/23/running-an-asp-net-core-application-against-multiple-db-providers-part-1/"
slug: "running-an-asp-net-core-application-against-multiple-db-providers-part-1"
wp_id: 4371
category: ["amazon-aurora", "architecture", "asp-net-core", "aws", "azure-sql-database", "net-core"]
tag: ["amazon-aurora", "asp-net-core", "azure", "azure-sql-database", "c", "dependency-injection", "mysql", "net", "net-core", "sql-server", "visual-studio"]
summary: "In my previous post, I had talked about how we to ported an existing repository code from Azure SQL to Amazon Aurora. This is a two-series post where I will throw a little bit more light on the intention behind it and what we were trying to achieve. Background We had a small ASP.NET Core solution"
---

In my previous [post](https://ankitvijaydotin.wordpress.com/2019/12/10/migrating-azure-sql-database-to-amazon-aurora/), I had talked about how we to ported an existing repository code from Azure SQL to Amazon Aurora.

This is a two-series post where I will throw a little bit more light on the intention behind it and what we were trying to achieve.

### Background

We had a small ASP.NET Core solution which had two primary components:

- ASP.NET Core Web API hosted on Azure Kubernetes Service (AKS)
- An Azure SQL Database based persistence layer

![](https://ankitvijaydotin.wordpress.com/wp-content/uploads/2022/12/8eaaf-image.png)

*Application solution structure*

However, we now had a new requirement to deploy the same little application to Amazon Web Server (AWS).

The persistence layer was required to be hosted on Amazon Aurora using MySQL. How we ported the persistence layer was explained in my previous post [here](https://ankitvijaydotin.wordpress.com/2019/12/10/migrating-azure-sql-database-to-amazon-aurora/).

An important thing to note here is that this exercise started as a PoC (Proof-of-Concept) and ended as a PoC. The actual implementation turned out to be a lot different due to organization Governance model, regional limitations, and cross-cutting concerns such as authentication, logging, build and deployment pipeline, etc. However, I feel the approach is still worth a mention and may be useful in many other use-cases.

### The Challenge

This new requirement brought up an interesting challenge for us, where, now the same code-base was required to be deployed twice to different cloud providers and with different database providers.

The aim of the POC was come with a solution which meets below goals:

- The solution needed to be simple and should not require major code refactoring.
- The developers should be able to easily develop and run the application across both SQL Server and MySQL.
- The developers should be able to run the integration tests across both the DB providers.

### The Solution

To achieve this, we came up with an idea of using an application settings to differentiate the deployment. The below diagram explains the proposed solution.

![](/wp-content/uploads/2019/12/Picture1.png)

*The proposed architecture*

> #### ***This exercise started as a PoC and ended as a PoC. The actual implementation turned out to be a lot different due to organization Governance model, regional limitations, and cross-cutting concerns such as authentication, logging, build and deployment pipeline, etc.***

#### Step 1: Project restructuring

We started with restructuring our code as below:

- The abstractions (repository interface) was moved into a separate project.
- The SQL server implementation which implemented the abstraction was moved into a separate project.
- A new MySQL server repository was introduced which again was an implementation of the interface.

![](/wp-content/uploads/2019/12/Picture2-1.png)

*The new solution structure*

#### Step 2: Add additional profile in launchSettings.json

To ensure we can run the application against both the DB providers during the development, we added a new profile for in launchSettings.json. The two profiles after the changes were:

- local-azure: To run the solution against Azure Sql implementation.
- local-aws: To run the solution against Amazon Aurora implementation.

Updated launchSettings.json looked similar to below:

This file contains hidden or bidirectional Unicode text that may be interpreted or compiled differently than what appears below. To review, open the file in an editor that reveals hidden Unicode characters.
[Learn more about bidirectional Unicode characters](https://github.co/hiddenchars)

[Show hidden characters]({{ revealButtonHref }})

|  |  |
| --- | --- |
|  | { |
|  | "$schema": "<http://json.schemastore.org/launchsettings.json&quot>;, |
|  | "profiles": { |
|  | "local-azure": { |
|  | "commandName": "Project", |
|  | "launchBrowser": true, |
|  | "launchUrl": "swagger", |
|  | "applicationUrl": "<https://localhost:5001;http://localhost:5000&quot>;, |
|  | "environmentVariables": { |
|  | "ASPNETCORE_ENVIRONMENT": "local-azure" |
|  | } |
|  | }, |
|  | "local-aws": { |
|  | "commandName": "Project", |
|  | "launchBrowser": true, |
|  | "launchUrl": "swagger", |
|  | "applicationUrl": "<https://localhost:5001;http://localhost:5000&quot>;, |
|  | "environmentVariables": { |
|  | "ASPNETCORE_ENVIRONMENT": "local-aws" |
|  | } |
|  | } |
|  | } |
|  | } |

[view raw](https://gist.github.com/ankitvijay/b3774b140ec71f7c526e1484bfd05d35/raw/7c65abd381023cb2e9b139a6b8e39e3c065c6fb9/launchsettings.json)
[launchsettings.json](https://gist.github.com/ankitvijay/b3774b140ec71f7c526e1484bfd05d35#file-launchsettings-json)
hosted with ❤ by [GitHub](https://github.com)

#### Step 3: Add a local application setting file for each profile/ deployment

Next, a local application settings file was added for both profiles, local-azure and local-aws. Each application settings file (**appsettings. local-azure.json** and **appsettings.local-aws.json**) had two settings:

- Deployment: Azure or AWS
- Connection String: A local connection string to connect to either SQL Server or MySQL.

This file contains hidden or bidirectional Unicode text that may be interpreted or compiled differently than what appears below. To review, open the file in an editor that reveals hidden Unicode characters.
[Learn more about bidirectional Unicode characters](https://github.co/hiddenchars)

[Show hidden characters]({{ revealButtonHref }})

|  |  |
| --- | --- |
|  | { |
|  | "Deployment": "Azure", |
|  | "ConnectionString": "Server=localhost,1436;Database=some-db-name;User Id=some=user;Password=very-secure-password;" |
|  | } |

[view raw](https://gist.github.com/ankitvijay/d489e47c3416318776166f88e1fe6401/raw/4144d6175d39728e5010174d7aa1739592c08aa7/appsettings.local-azure.json)
[appsettings.local-azure.json](https://gist.github.com/ankitvijay/d489e47c3416318776166f88e1fe6401#file-appsettings-local-azure-json)
hosted with ❤ by [GitHub](https://github.com)

#### Step 4: Updates to Startup.cs – Dependency Injection

Last, but not the least, the Startup.cs was updated to inject right dependencies based on the “Deployment” setting.

This file contains hidden or bidirectional Unicode text that may be interpreted or compiled differently than what appears below. To review, open the file in an editor that reveals hidden Unicode characters.
[Learn more about bidirectional Unicode characters](https://github.co/hiddenchars)

[Show hidden characters]({{ revealButtonHref }})

|  |  |
| --- | --- |
|  |  |
|  | public class Startup |
|  | { |
|  | private readonly IConfiguration _configuration; |
|  |  |
|  | public Startup(IConfiguration configuration) |
|  | { |
|  | _configuration = configuration; |
|  | } |
|  |  |
|  | public void ConfigureServices(IServiceCollection services) |
|  | { |
|  | var deployment = _configuration["Deployment"]; |
|  | var connectionString = _configuration["ConnectionString"]; |
|  |  |
|  | // Code removed for brevity |
|  |  |
|  | if (deployment == "Azure") |
|  | { |
|  | // Inject SQL Server dependency |
|  | } |
|  | else |
|  | { |
|  | // Inject MySQL dependency |
|  | } |
|  | } |
|  |  |
|  | // Code removed for brevity |
|  | } |

[view raw](https://gist.github.com/ankitvijay/51c24a04d6e71c6c0ac3313663098f7a/raw/1759c9c538e59fe78ffcecbfa5accf861e9ce851/Startup.cs)
[Startup.cs](https://gist.github.com/ankitvijay/51c24a04d6e71c6c0ac3313663098f7a#file-startup-cs)
hosted with ❤ by [GitHub](https://github.com)

As you can see in the above code, we chose which module/ DB provider to load at the run time using the deployment setting through the Dependency Injection.

To use the repository we needed to simply inject the **IRepository** interface and call the respective operation. (like Add, Update, Get, etc)

That’s it! This allowed us to develop and run the application across both the DB providers.

In my second and final series of this post, I will talk in the detail about our integration tests setup which arguably was little more than trivial.

> Photo by [Caleb Jones](https://unsplash.com/@gcalebjones?utm_source=unsplash&utm_medium=referral&utm_content=creditCopyText) on [Unsplash](https://unsplash.com/s/photos/road-fork?utm_source=unsplash&utm_medium=referral&utm_content=creditCopyText)
