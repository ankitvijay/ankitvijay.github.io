---
title: "Lesser known C# features – Part 3"
date: "2018-01-14T09:47:26+10:00"
lastmod: "2022-12-23T23:04:46+10:00"
url: "/2018/01/14/lesser-known-c-features-part-3/"
slug: "lesser-known-c-features-part-3"
wp_id: 3503
category: ["net"]
tag: ["c", "net"]
summary: "This is Part 3 of my series, lesser-known features of C#. The previous parts of this series are available here: Lesser known C# features – Part 1 Lesser known C# – feature – Part 2"
---

This is Part 3 of my series, lesser-known features of C#. The previous parts of this series are available here:

- [Lesser known C# features – Part 1](/2018/01/08/lesser-known-c-features-part-1/)
- [Lesser known C# – feature – Part 2](/2018/01/11/lesser-known-c-features-part-2/)

Before we delve into the features, I would like to talk about one of the feedback I have received for my previous posts. Many readers have pointed out that the features I talked about are .NET framework features. These features are available in other CLR languages and not limited to C#. I would like to clarify that I started this series with language C# in mind. My intention was to just keep the discussion to C# specific features. However, it is just a coincidence that all the features I talked till now are language independent. I have tried to change that in Part 3.

## using static

`using static` has been there for a while now. But, I think this feature has not received enough love it deserves from the developers. `using static` was introduced in C# 6.0.

As per the [Microsoft docs](https://docs.microsoft.com/en-us/dotnet/csharp/language-reference/keywords/using-static):

> The `using static` directive designates a type whose static members you can access without specifying a type name

Consider the example of `Logger` class we have been working on in the previous posts. Here is the static `Logger` class:

```csharp
using System.Diagnostics;
using System.Runtime.CompilerServices;

namespace staticUsingExample
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

        [Conditional("DEBUG")]
        public static void DebugLog(string message, [CallerMemberName] string callerMemberName = "")
        {
            Log($"[Message]: {message}; [Caller Member Name]: {callerMemberName};");
        }

        private static void Log(string message)
        {
           Debug.WriteLine(message);
        }
    }
}
```

The `Log` method, due to its nature may be called quite a few times from a class. Prior to C# 6.0, we would end up having `Logger.Log` call number of times in a single class. Instead, you can use `using static` as below:

```csharp
using static staticUsingExample.Logger;

namespace staticUsingExample
{
    class Program
    {
        static void Main(string[] args)
        {
            DebugLog("Member Start");

            // Execute method
            Log("Testing logging inside Main() method");

            DebugLog("Member End");
        }
    }
}
```

This helps to make your code cleaner and easier to understand.

However, I would suggest not to go overboard withthis. I ***personally*** use this feature only in the scenarios where the `static` method ***appears*** to be an extension of a class. This can be subjective and opinion-based.

I have also found `using static` to be better suited than using [extension methods](https://docs.microsoft.com/en-us/dotnet/csharp/programming-guide/classes-and-structs/extension-methods) on few occasions. Consider a hypothetical example, you have a helper method that takes `string id` as an input and validates the parameter`id`.

```csharp
namespace staticUsingExample
{
 public static class IdValidationHelper
 {
 public static bool IsValid(string id)
 {
 bool isValid = false;

 // Validate id

 return isValid;
 }
 }
}
```

Now, let us say you need to call this method across the project. This can potentially make your code-base polluted with a call similar to `IdValidationHelper.IsValid(id)`.

One of the ways you can look to work around this is by using extension methods. This would help you make a call similar to `id.IsValid()` making your code easier to understand. However, it also means that `IsValid` method is now available for any type of string even if it is not an `id`.

![Extension Method Issue](/wp-content/uploads/2022/12/07c76-extensionmethodissue.png)

This is where `using static` can come handy. You no longer, need to prefix the method with the class name and at the same point of time, you no longer need to use an extension method in a wrong context.

One may argue that you can still pass a non-id string argument to the helper method. However, I feel it is still better than exposing the method on the type `string` since, logically, it is not a part of `string` type like `IsEmpty` or other similar extension methods.

## Evaluating boolean expressions without short-circuit

We have all used operators `&&` and `||` to evaluate boolean expressions. These operators do a [short-circuit evaluation](https://en.wikipedia.org/wiki/Short-circuit_evaluation). That is, if the first expression gives a conclusive result then the second expression is not evaluated. Consider this example:

```csharp
using System;

namespace ShortCircuitExample
{
    public class Program
    {
        static void Main(string[] args)
        {
            if (IsStoreOpen() && NeedGrocery())
            {
                Console.WriteLine("Go to store");
            }
            else
            {
                Console.WriteLine("Stay at home");
            }

            Console.Read();
        }

        private static bool NeedGrocery()
        {
            Console.WriteLine("Need grocery");
            return false;
        }

        private static bool IsStoreOpen()
        {
            Console.WriteLine("Is store open");
            return false;
        }
    }
}
```

The output of the above code is:

Is store open
Stay at home

`NeedGrocery` method is not called because the first expression returns `false`. Hence, the second expression is not evaluated.

However, what if you want to evaluate second expression irrespective of result of first expression? You can do this by using `&` and `|` operators. These operators do a non-short circuit evaluation.

Let us change the above code to use`&` operator instead of `&&`.

```csharp
using System;

namespace NonShortCircuitExample
{
    public class Program
    {
        static void Main(string[] args)
        {
            if (IsStoreOpen() & NeedGrocery())
            {
                Console.WriteLine("Go to store");
            }
            else
            {
                Console.WriteLine("Stay at home");
            }

            Console.Read();
        }

        private static bool NeedGrocery()
        {
            Console.WriteLine("Need grocery");
            return false;
        }

        private static bool IsStoreOpen()
        {
            Console.WriteLine("Is store open");
            return false;
        }
    }
}
```

The output of the above code is:

Is store open
Need grocery
Stay at home

I’m not sure of any real-world example of where you would use a non-short circuit operator.  Maybe, while writing unit tests if you need to evaluate both the expressions for code coverage or for some other reason.  Maybe for debugging.  However, it is there in case you need it 🙂

As always, I look forward to hearing your feedback.
