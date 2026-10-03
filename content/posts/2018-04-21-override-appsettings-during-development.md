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

One such example can be SQL server connection string. Some developers may have SQL Express installed, others may have a named instance on their local. However, the `web.config` or `app.config` can only have one value for this setting.

The way people (*at least “I” used to*)  handle this usually is to change the `config`values on the local machine during development but discard those changes at the time of commit. If accidentally, however you forget to change the setting back to original, then there is a  risk of breaking the build or code on other developer’s local machine.

## Override your appSettings

Recently, my colleague (thanks James!) showed me a nice little trick handle this.  I must say, I was bit embarrassed to not know this already.

You can override the key-value pairs defined under `appSettings` element of `config` by using the`file` attribute.

This file contains hidden or bidirectional Unicode text that may be interpreted or compiled differently than what appears below. To review, open the file in an editor that reveals hidden Unicode characters.
[Learn more about bidirectional Unicode characters](https://github.co/hiddenchars)

[Show hidden characters]({{ revealButtonHref }})

|  |  |
| --- | --- |
|  | <appSettings file="localAppSettings.config"> |
|  | <add key="dbConnectionString" value="sourceControlConnectionString"/> |
|  | <add key="someRandomApplicationSetting" value="sourceControlApplicationSetting"/> |
|  | </appSettings> |

[view raw](https://gist.github.com/ankitvijay/e7f5ce6b2ea4299679ffa4b39c9f4e8a/raw/0e33c370dcd566c517e668deda1c74aa94f2826e/web.config)
 [web.config](https://gist.github.com/ankitvijay/e7f5ce6b2ea4299679ffa4b39c9f4e8a#file-web-config)
hosted with ❤ by [GitHub](https://github.com)

The file `localAppSettings.config` is not part of your source control. If your local settings match exactly as `web.config,`then you do not need to have this file on your local. Else, you can use this file to override ***only*** the settings that are different than `web.config`.

This file contains hidden or bidirectional Unicode text that may be interpreted or compiled differently than what appears below. To review, open the file in an editor that reveals hidden Unicode characters.
[Learn more about bidirectional Unicode characters](https://github.co/hiddenchars)

[Show hidden characters]({{ revealButtonHref }})

|  |  |
| --- | --- |
|  | <appSettings> |
|  | <add key="dbConnectionString" value="localMachineConnectionString"/> |
|  | </appSettings> |

[view raw](https://gist.github.com/ankitvijay/1e57a39926b0ab2b5657383650692578/raw/45613ea286ceecac34cf71c4de76f22a7b37ca60/localAppSettings.config)
 [localAppSettings.config](https://gist.github.com/ankitvijay/1e57a39926b0ab2b5657383650692578#file-localappsettings-config)
hosted with ❤ by [GitHub](https://github.com)

When you use the application settings in your code, you get following values:

|  |
| --- |
| **Key –> Value** |
| `dbConnectionString --> localMachineConnectionString` |
| `someRandomApplicationSetting --> sourceControlApplicationSetting` |

> **Important Note:** If you use `connectionStrings` element to store your data source connection string, then, you can use configSource attribute instead. The two attributes however, are not equivalent. You can read more about the difference [here](https://stackoverflow.com/questions/6940004/asp-net-web-config-configsource-vs-file-attributes#6940086).

Hope this nice little trick helps ease your development. 🙂
