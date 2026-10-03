---
title: "Lesser known C# features – Part 1"
date: "2018-01-08T07:19:58+10:00"
lastmod: "2018-01-25T00:45:55+10:00"
url: "/2018/01/08/lesser-known-c-features-part-1/"
slug: "lesser-known-c-features-part-1"
wp_id: 3461
category: ["net"]
tag: ["c", "net"]
summary: "Language C# has become very powerful and mature over the years. As with any other language, C# also has few features which are used lesser than others. These are useful but often forgotten features. Through a series of blog post, I want to talk to about these lesser known/used features of C#. This is Part 1 of the series."
---

Language C#  has become very powerful and mature over the years. As with any other language, C# also has few features which are used lesser than others. These are useful but often forgotten features. Through a series of blog post, I want to talk to about these lesser known/used features of C#. This is **Part 1** of the series.

## Debugger Attributes

Debugger attributes help developers to customize output in the debugger window. These attributes are available in the `System.Diagnostics` namespace.

- `DebuggerDisplay`

`DebuggerDisplay` attribute controls how a  type or member is displayed in the debugger windows. For example, consider the below class with `DebuggerDisplay` attribute.

```csharp
[DebuggerDisplay("Name of employee is {FirstName} {Surname} and his department is {Department}")]
public class Employee
{
    public string FirstName { get; set; }

    public string Surname { get; set; }

    public string Department { get; set; }
}
```

When you debug code, you would see a message as shown below:

![DebuggerDisplay.png](/wp-content/uploads/2022/12/61d95-debuggerdisplay.png)

- **`DebuggerBrowsable`**

DebuggerBrowser attribute can be used to further control how the properties and fields appear in the debugger window. This attribute takes `DebuggerBrowserState` enum, which defines  states: `Never`, `Collapsed` and `RootHidden`

```csharp
public class Employee
{
    [DebuggerBrowsable(DebuggerBrowsableState.Collapsed)]
    public string FirstName { get; set; }

    [DebuggerBrowsable(DebuggerBrowsableState.Never)]
    public string Surname { get; set; }

    [DebuggerBrowsable(DebuggerBrowsableState.RootHidden)]
    public List<string> Reportees { get; set; }
}
```

The debug window output for above code would appear as below:

![DebuggerBrowsableExample.png](/wp-content/uploads/2022/12/0064a-debuggerbrowsableexample.png)

Other useful attributes available under this namespace are

- **`DebuggerHidden`**
- **`DebuggerNonUserCode`**
- `DebuggerStepperBoundary`
- `DebuggerStepThrough`
- `​DebuggerTypeProxy`
- **`DebuggerVisualizer`**

You can refer to the `System.Diagnostics` namespace to know more about these attributes.

## **CallerInfo Attributes**

As the name suggests, these attributes help to track information of a caller. There are three types of CallerInfo attributes available:

- **`CallerMemberName` –**Gives the name of the caller (eg. method or property name).

- **`CallerFilePath` –** Gives the fill path at the time of compilation of the source file that contains the caller.

- **`CallerLineNumber` –**Gives the line number at which a method (caller) was called in the source file.

<https://gist.github.com/ankitvijay/2400c1ebb26d3de3523c682d6d1a65c8#file-logger-cs>

<https://gist.github.com/ankitvijay/2400c1ebb26d3de3523c682d6d1a65c8#file-logger-cs>

These attributes are available in the `System.Runtime.CompilerServices` namespace.

Example, consider a class that logs message from the caller. While logging the message, we would like to get additional information about the method name, source line number etc. It is very tedious to pass this information for each message that needs to be logged. Instead, we can use Caller Info attributes to obtain the information.

```csharp
using System.Diagnostics;
using System.Runtime.CompilerServices;

namespace CallerInfoExample
{
  public static class Logger
  {
      public static void Log(string message,
                               [CallerFilePath] string sourceFilePath = "",
                               [CallerLineNumber] int sourceLineNumber = 0,
                               [CallerMemberName] string callerMemberName = "")
      {
          Log($"[Message]: {message}; [Source File Path]: {sourceFilePath}; " +
            $"[Source Line Number]: {sourceLineNumber}; [Caller Member Name]: {callerMemberName}; ");
      }

      private static void Log(string message)
      {
          Debug.WriteLine(message);
      }
  }
}
```

```csharp
namespace CallerInfoExample
{
    class Program
    {
        static void Main(string[] args)
        {
            Logger.Log("Testing logging inside Main() method");
        }
    }
}
```

When we call `Logger.Log` from `Main` method, all we need to pass is the log message and rest of the information is obtained through CallerInfo attributes.

The output of above code snippet is:

> [Message]: Testing logging inside Main() method; [Source File Path]: DriveLabel:\Full-Source-File-Path\Program.cs; [Source Line Number]: 7; [Caller Member Name]: Main;

`CallerMemberInfo` attribute is also used with `INotifyProperyChanged`  interface. This attributes helps you to keep your code clean as you no longer need to explicitly pass the property name that gets change. You can read more about the usage [here](https://docs.microsoft.com/en-gb/dotnet/api/system.componentmodel.inotifypropertychanged?view=netframework-4.7.1).

Hope these tips would help you write better code. Stay tuned for more. 🙂

Also, please share any other lesser known C# features you have been using that you would like me to talk about in this series.
