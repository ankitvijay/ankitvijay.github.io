---
title: "Lesser known C# features – Part 2"
date: "2018-01-11T01:33:56+10:00"
lastmod: "2022-12-23T23:04:46+10:00"
url: "/2018/01/11/lesser-known-c-features-part-2/"
slug: "lesser-known-c-features-part-2"
wp_id: 3479
category: ["net"]
tag: ["c", "net"]
summary: "This is Part 2 of the series, lesser-known features of C# language. I would suggest you to go through Part 1 if you have not already."
---

This is Part 2 of the series, lesser-known features of C# language. I would suggest you to go through [Part 1](https://ankitvijaydotin.wordpress.com/2018/01/08/lesser-known-c-features-part-1/) if you have not already.

## ObsoleteAttribute

From my experience, `Obsolete` attribute is more of ***lesser used*** than ***lesser known***. As the name suggests, this attribute is used for marking elements such methods, properties, classes etc as deprecated. This attribute can be used when you are working on a class library or a NuGet package which used by internal or external users and you want your users to no longer use an old version of class/ method/ property.  This gives time to your users to make changes in their code without breaking their application. For example, consider the below `Logger` class

This file contains hidden or bidirectional Unicode text that may be interpreted or compiled differently than what appears below. To review, open the file in an editor that reveals hidden Unicode characters.
[Learn more about bidirectional Unicode characters](https://github.co/hiddenchars)

[Show hidden characters]({{ revealButtonHref }})

|  |  |
| --- | --- |
|  | public static class Logger |
|  | { |
|  | public static void Log(string message, |
|  | [CallerFilePath] string sourceFilePath = "", |
|  | [CallerLineNumber] int sourceLineNumber = 0, |
|  | [CallerMemberName] string callerMemberName = "") |
|  | { |
|  | Log($"[Message]: {message}; [Source File Path]: {sourceFilePath}; " + |
|  | $"[Source Line Number]: {sourceLineNumber}; [Caller Member Name]: {callerMemberName}; "); |
|  | } |
|  |  |
|  | [Obsolete("This method is will be removed in the future. Use Log(string message) instead.")] |
|  | public static void Log(string message, string callerMemberName) |
|  | { |
|  | Log($"[Message]: {message}; [Caller Member Name]: {callerMemberName}; "); |
|  | } |
|  |  |
|  | private static void Log(string message) |
|  | { |
|  | Debug.WriteLine(message); |
|  | } |
|  | } |

[view raw](https://gist.github.com/ankitvijay/3b97e87690fc928d38feb2379678d958/raw/19011b2c8579f42e0a6454d71e01c8850b2747cd/ObsoleteAttributeExample)
 [ObsoleteAttributeExample](https://gist.github.com/ankitvijay/3b97e87690fc928d38feb2379678d958#file-obsoleteattributeexample)
hosted with ❤ by [GitHub](https://github.com)

In the above code, one of the overloads of the `Log` method is marked as `Obsolete`. When a caller invokes this method, it gets the below warning:

![ObsoleteAttributeExample](https://ankitvijaydotin.wordpress.com/wp-content/uploads/2022/12/1026f-obsoleteattributeexample.png)

Additionally, if the calling project treats “[warning as error](http://dailydotnettips.com/2016/03/04/avoid-code-warnings-being-missed-or-ignored-treating-warnings-as-errors-in-visual-studio/)” then the developers will get compile time error when they try to use this method. This will force the user calling the logger method to either update the code to use the new implementation of Log method or disable the warning explicitly.

![ObsoleteAttributeExampleDisableWarning.png](https://ankitvijaydotin.wordpress.com/wp-content/uploads/2022/12/cf110-obsoleteattributeexampledisablewarning.png)

## char.GetUnicodeCategory

Type `char` has a number of helper methods like `IsDigit`, `IsLetter`, `IsLower` etc. In addition to this, `char` also exposes a method called `GetUnicodeCategory` which returns enum `UnicodeCategory`.

As per [unicode.org](http://unicode.org/standard/WhatIsUnicode.html#After)

> The Unicode Standard provides a unique number for every character, no matter what platform, device, application or language.

The `UnicodeCategory` categorizes the input character into category such as `CurrencySymbol`, `ClosePunctuation`, `LineSeparator`, `LowercaseLetter` etc. This information may be useful for different scenarios like when you need to validate a user input string. Example:

This file contains hidden or bidirectional Unicode text that may be interpreted or compiled differently than what appears below. To review, open the file in an editor that reveals hidden Unicode characters.
[Learn more about bidirectional Unicode characters](https://github.co/hiddenchars)

[Show hidden characters]({{ revealButtonHref }})

|  |  |
| --- | --- |
|  | using System; |
|  |  |
|  | namespace GetUnicodeCategoryExample |
|  | { |
|  | class Program |
|  | { |
|  | static void Main(string[] args) |
|  | { |
|  | var sampleString = @"1aB%$^()-"; |
|  | for (int i = 0; i < sampleString.Length; i++) |
|  | { |
|  | Console.WriteLine($"[Char]: {sampleString[i]};" + |
|  | $" [UnicodeCategory]: {char.GetUnicodeCategory(sampleString[i])}"); // or char.GetUnicodeCategory(sampleString, i) |
|  | } |
|  |  |
|  | Console.Read(); |
|  | } |
|  | } |
|  | } |

[view raw](https://gist.github.com/ankitvijay/ade183f68709dc9250e02c144f89286e/raw/1acb2404d359bf8bde86f5949fa645341698fd73/GetUnicodeCategoryExample)
 [GetUnicodeCategoryExample](https://gist.github.com/ankitvijay/ade183f68709dc9250e02c144f89286e#file-getunicodecategoryexample)
hosted with ❤ by [GitHub](https://github.com)

The output of the above code is:

[Char]: 1; [UnicodeCategory]: DecimalDigitNumber
[Char]: a; [UnicodeCategory]: LowercaseLetter
[Char]: B; [UnicodeCategory]: UppercaseLetter
[Char]: %; [UnicodeCategory]: OtherPunctuation
[Char]: $; [UnicodeCategory]: CurrencySymbol
[Char]: ^; [UnicodeCategory]: ModifierSymbol
[Char]: (; [UnicodeCategory]: OpenPunctuation
[Char]: ); [UnicodeCategory]: ClosePunctuation
[Char]: -; [UnicodeCategory]: DashPunctuation

## ConditionalAttribute

You might be already aware of conditional preprocessor directives like `#if`, `#elif`, `#endif.` Preprocessors directive help in doing a conditional compilation.

`ConditionalAttribute` provides an elegant and clean alternative to the directives. Consider the slight variation of `Logger` class in the example below. We now have an additional method called `DebugLog` with `ConditionalAttrbute`.

This file contains hidden or bidirectional Unicode text that may be interpreted or compiled differently than what appears below. To review, open the file in an editor that reveals hidden Unicode characters.
[Learn more about bidirectional Unicode characters](https://github.co/hiddenchars)

[Show hidden characters]({{ revealButtonHref }})

|  |  |
| --- | --- |
|  | using System.Diagnostics; |
|  | using System.Runtime.CompilerServices; |
|  |  |
|  | namespace ConditionalAttributeExample |
|  | { |
|  | public static class Logger |
|  | { |
|  | public static void Log(string message, |
|  | [CallerFilePath] string sourceFilePath = "", |
|  | [CallerLineNumber] int sourceLineNumber = 0, |
|  | [CallerMemberName] string callerMemberName = "") |
|  | { |
|  | Log($"[Message]: {message}; [Source File Path]: {sourceFilePath}; " + |
|  | $"[Source Line Number]: {sourceLineNumber}; [Caller Member Name]: {callerMemberName}; "); |
|  | } |
|  |  |
|  | [Conditional("DEBUG")] |
|  | public static void DebugLog(string message, [CallerMemberName] string callerMemberName = "") |
|  | { |
|  | Log($"[Message]: {message}; [Caller Member Name]: {callerMemberName};"); |
|  | } |
|  |  |
|  | private static void Log(string message) |
|  | { |
|  | Debug.WriteLine(message); |
|  | } |
|  | } |
|  | } |

[view raw](https://gist.github.com/ankitvijay/84471e98d7cd7468e2ee7663790773eb/raw/cf060f81dfd55573c22f2e1f6564046be0ff486c/Logger.cs)
 [Logger.cs](https://gist.github.com/ankitvijay/84471e98d7cd7468e2ee7663790773eb#file-logger-cs)
hosted with ❤ by [GitHub](https://github.com)

This file contains hidden or bidirectional Unicode text that may be interpreted or compiled differently than what appears below. To review, open the file in an editor that reveals hidden Unicode characters.
[Learn more about bidirectional Unicode characters](https://github.co/hiddenchars)

[Show hidden characters]({{ revealButtonHref }})

|  |  |
| --- | --- |
|  | namespace ConditionalAttributeExample |
|  | { |
|  | class Program |
|  | { |
|  | static void Main(string[] args) |
|  | { |
|  | Logger.DebugLog("Member Start"); |
|  |  |
|  | // Perform operation |
|  | Logger.Log("Testing logging inside Main() method"); |
|  |  |
|  | Logger.DebugLog("Member End"); |
|  | } |
|  | } |
|  | } |

[view raw](https://gist.github.com/ankitvijay/84471e98d7cd7468e2ee7663790773eb/raw/cf060f81dfd55573c22f2e1f6564046be0ff486c/Main.cs)
 [Main.cs](https://gist.github.com/ankitvijay/84471e98d7cd7468e2ee7663790773eb#file-main-cs)
hosted with ❤ by [GitHub](https://github.com)

The output of the above code is self-explanatory. The `DebugLog` method will only be executed when we are running this code in **Debug** mode/ configuration. With the help of`ConditionalAttribute`, however, our `Main` method remains free of the preprocessor or ugly `if` `else` conditions.

Please note that you can also define your own conditional compilation symbols under **Project Properties -> Build** as shown in the figure below:

![CustomCompilationSymbol.PNG](https://ankitvijaydotin.wordpress.com/wp-content/uploads/2022/12/1dc4b-customcompilationsymbol.png)

> Note: The conditional attribute and preprocessor directives are not the same. as mentioned in one of the answers of [this MSDN post](https://social.msdn.microsoft.com/Forums/vstudio/en-US/e459c267-bcdf-4666-89a3-3d9b51a73ae8/c-preprocessor-directives-vs-the-conditional-attribute?forum=csharpgeneral). With conditional attribute, the method is still part of the assembly. However, with preprocessor directive the piece of code is not visible to assembly itself (when the condition is false).

Hope these tips help you write better code and improving your programming skills. Please share your view and feedback in the comments section below.

Thank you for taking time to read this post. Part 3 is on the way soon! 🙂
