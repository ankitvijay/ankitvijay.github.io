---
title: "Override appSettings during development – .NET Core"
date: "2018-12-28T08:13:31+10:00"
lastmod: "2022-12-23T23:04:46+10:00"
url: "/2018/12/28/override-appsettings-during-development-net-core/"
slug: "override-appsettings-during-development-net-core"
wp_id: 3839
category: ["asp-net-core", "git", "net-core", "visual-studio"]
tag: ["appsettings", "asp-net-core", "configuration", "net", "net-core", "source-control"]
summary: "Sometime back, I had written about how to override appSettings during development in traditional ASP.NET application. Recently, we started development of a ASP.NET Core application and had a similar challenge. Our developers work on different operating systems (Windows and Mac). They have different local connection strings and application settings. We had a same problem as"
---

Sometime back, I had written about [how to override appSettings](/2018/04/21/override-appsettings-during-development/) during development in traditional ASP.NET application.

Recently, we started development of a ASP.NET Core application and had a similar challenge. Our developers work on different operating systems (Windows and Mac). They have different local connection strings and application settings. We had a same problem as earlier: How do we ensure that we do not store developer specific app settings/ connection string in source control.

Configuration in ASP.NET Core is quite [advance and extensible](https://docs.microsoft.com/en-us/aspnet/core/fundamentals/configuration/?view=aspnetcore-2.2) as compared to traditional ASP.NET Framework. We have multiple ways to solve this problem. From the documentation:

> App configuration in ASP.NET Core is based on key-value pairs established by *configuration providers*. Configuration providers read configuration data into key-value pairs from a variety of configuration sources:
>
> - Azure Key Vault
> - Command-line arguments
> - Custom providers (installed or created)
> - Directory files
> - Environment variables
> - In-memory .NET objects
> - Settings files

Also, ASP.NET Core offers following [two recommended](https://docs.microsoft.com/en-us/aspnet/core/security/app-secrets?view=aspnetcore-2.2&tabs=windows) ways to store app secrets during development:

- Environment variables
- Secret Manager

One of the issue, with the above two approaches is that the settings are stored outside the IDE. Also, since these settings override the `appSettings.json file` it can cause confusion while debugging as the developer may not realize that settings are being overridden.

## Our Approach

For our project we were looking for the simplest possible solution without any additional overhead. The easiest possible solution us for was to use `appSettings.Developement.json` file to store local settings and exclude it from source control by adding to `.gitignore` (we use Git).

However, we already have a separate “`Dev`” environment where we first deploy our application before pushing to `Test` and `Live` environments. Using the default `Developement` environment for the purpose of storing the local settings could have confused the developers.

As a result, we ended up adding a new **`appSettings.Local.json`** file to the project. This setting file was then added to `.gitignore` to exclude this file from source control.

<https://gist.github.com/ankitvijay/21b45c70e00846d5ce738005fae0372b.js>

Here is a sample `appSettings.Local.json`

<https://gist.github.com/ankitvijay/8d86bdc4bf62b95fa4e16601fd970813.js>

We then, changed our `launchsettings.json` and updated `ASPNETCORE_ENVIRONMENT` to point to `Local` instead of `Development`

Last but not the least, we updated `Startup.json` to use developer exception page while doing development.

<https://gist.github.com/ankitvijay/368ea6031ed1d31c9c907f9d8fe2f009.js>

That’s it! This approach helped us to keep all our settings in one place (within our IDE) and it turned out to be a pretty neat solution to our problem.

Hope you find this tip useful. Please share your thoughts in comments section below.
