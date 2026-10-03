---
title: "Override appSettings during development"
date: "2018-04-21T08:58:25+10:00"
lastmod: "2018-04-22T00:42:24+10:00"
url: "/2018/04/21/override-appsettings-during-development/"
slug: "override-appsettings-during-development"
wp_id: 3663
category: ["visual-studio"]
tag: ["c", "net", "source-control", "visual-studio"]
summary: "It is a fairly common scenario that during development the local machine configuration settings for different developers in are not same and it may not match with the default value in source control. One such example can be SQL server connection string. Some developers may have SQL Express installed, others may have a named instance"
---

It is a fairly common scenario that during development the local machine configuration settings for different developers in are not same and it may not match with the default value in source control.

One such example can be SQL server connection string. Some developers may have SQL Express installed, others may have a named instance on their local. However, the `web.config` or `app.config` can only have one value for this setting.

The way people (*at least “I” used to*)  handle this usually is to change the `config`values on the local machine during development but discard those changes at the time of commit. If accidentally, however you forget to change the setting back to original, then there is a  risk of breaking the build or code on other developer’s local machine.

## Override your appSettings

Recently, my colleague (thanks James!) showed me a nice little trick handle this.  I must say, I was bit embarrassed to not know this already.

You can override the key-value pairs defined under `appSettings` element of `config` by using the`file` attribute.

```xml
<appSettings file="localAppSettings.config">
   <add key="dbConnectionString" value="sourceControlConnectionString"/>
   <add key="someRandomApplicationSetting" value="sourceControlApplicationSetting"/>
</appSettings>
```

The file `localAppSettings.config` is not part of your source control. If your local settings match exactly as `web.config,`then you do not need to have this file on your local. Else, you can use this file to override ***only*** the settings that are different than `web.config`.

```xml
<appSettings>
  <add key="dbConnectionString" value="localMachineConnectionString"/>
</appSettings>
```

When you use the application settings in your code, you get following values:

|  |
| --- |
| **Key –> Value** |
| `dbConnectionString --> localMachineConnectionString` |
| `someRandomApplicationSetting --> sourceControlApplicationSetting` |

> **Important Note:** If you use `connectionStrings` element to store your data source connection string, then, you can use configSource attribute instead. The two attributes however, are not equivalent. You can read more about the difference [here](https://stackoverflow.com/questions/6940004/asp-net-web-config-configsource-vs-file-attributes#6940086).

Hope this nice little trick helps ease your development. 🙂
