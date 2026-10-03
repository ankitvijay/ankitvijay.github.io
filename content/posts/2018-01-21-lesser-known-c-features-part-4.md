---
title: "Lesser Known C# Features – Part 4"
date: "2018-01-21T17:05:18+10:00"
lastmod: "2022-12-23T23:04:46+10:00"
url: "/2018/01/21/lesser-known-c-features-part-4/"
slug: "lesser-known-c-features-part-4"
wp_id: 3535
category: ["net"]
tag: ["c", "net"]
summary: "This is Part 4 and most likely the last part of my series, lesser-known features of C#. The previous parts of this series are available here: Lesser known C# features – Part 1 Lesser known C# features – Part 2 Lesser known C# features – Part 3"
---

This is Part 4 and most likely the last part of my series, lesser-known features of C#. The previous parts of this series are available here:

- [Lesser known C# features – Part 1](/2018/01/08/lesser-known-c-features-part-1/)
- [Lesser known C# features – Part 2](/2018/01/11/lesser-known-c-features-part-2/)
- [Lesser known C# features – Part 3](/2018/01/14/lesser-known-c-features-part-3/)

## NumberStyles

It is fairly common to have a requirement to parse a numeric string which contains currency symbol, trailing spaces, parentheses etc. `NumberStyles` enum can help parse the numeric string which has these attributes.

Each numeric `type` like `int`, `decimal`, `float` etc have `Parse` and `TryParse` method overloads which takes the `NumberStyles` argument.

This enum is also decorated with `Flags` attribute which allows us to combine multiple values of the enum. In addition to this, we can use `NumberStyles` in combination with `NumberFormatInfo` to provide the culture-specific formatting while parsing the numeric string.

```csharp
using System;
using System.Globalization;

namespace NumberStylesExample
{
    public class Program
    {
        static void Main(string[] args)
        {
            // A Hexadecimal number with trailing and leading white spaces
            Console.WriteLine(int.Parse("   AbCDeF     ", NumberStyles.HexNumber |
                NumberStyles.AllowLeadingWhite | NumberStyles.AllowTrailingWhite));

            // A decimal number with -ve number defined within parentheses
            Console.WriteLine(Decimal.Parse("(10000.23)", NumberStyles.Float |
                NumberStyles.AllowParentheses));

            // A slightly complex example which shows how NumberStyles can be used
            // with TryParse method along with NumberFormatInfo.
            var numberFormatInfo = new NumberFormatInfo();
            numberFormatInfo.CurrencyDecimalSeparator = ",";
            numberFormatInfo.CurrencyGroupSeparator = ".";
            numberFormatInfo.CurrencySymbol = "£";
            Double.TryParse("£120500,56", NumberStyles.Float | NumberStyles.Currency,
                numberFormatInfo, out var result);
            Console.WriteLine(result);

            Console.Read();
        }
    }
}
```

The output of the above code is:

11259375
-10000.23
120500.56

## Environment.FailFast

`Environment.FailFast` immediately terminates the process and write the message to Windows Application Log. If this method is written in `try`/`finally` block then `Environment.FailFast` will prevent  the execution of `finally` block.

What is the use case of `FastFlow`? As per [Microsoft documentation:](https://docs.microsoft.com/en-us/dotnet/standard/design-guidelines/exception-throwing)

> **CONSIDER** terminating the process by calling `System.Environment.FailFast` (.NET Framework 2.0 feature) instead of throwing an exception if your code encounters a situation where it is unsafe for further execution.

```csharp
using System;

namespace FastFailExample
{
    public class Program
    {
        static void Main(string[] args)
        {
            try
            {
                // Some user code
                // .
                // .

                Environment.FailFast("End of world. Reboot!!!",
                    new Exception("Application terminated."));
            }
            finally
            {
                Console.WriteLine("This line is never be executed");
            }
        }
    }
}
```

Running the above code will immediately terminate the application and log application error in the event log. The `finally` block will be not executed.

Here is the Event log error:

![ApplicationError.PNG](/wp-content/uploads/2022/12/4725c-applicationerror.png)

## namespace alias

- **global alias**

Let us consider a scenario where we have a member name (e.g class, property, field etc.) with the same name as the namespace in a 3rd party library or a NuGet package we have imported into our project. How can we resolve this conflict in our code? That’s where [`global`namespace](https://docs.microsoft.com/en-us/dotnet/csharp/language-reference/keywords/global) alias can come to our rescue.

Consider a simple example where we have defined a class with the name `System` in our assembly.

```csharp
namespace GlobalNamespaceAliasExample
{
    public class System
    {
        public void Log(string message)
        {
            // Code to log
        }
    }
}
```

Now, the `System` namespace is also available in .NET Framework. What if we want to use the `System` namespace in the same class or in some other class within the same assembly? We can do this by prefixing the member in `System` namespace with `global` alias as shown below.

```csharp
namespace GlobalNameSpaceAliasExample
{
    public class System
    {
        public void Log(string message)
        {
            global::System.Console.WriteLine(message);
        }
    }
}
```

- **Extern alias**

Consider another example where two assemblies have the same namespace name. Let us call them `Assembly1` and `Assembly2`.  Each Assembly contains a class with common namespace `SameAssemblyName`.

`Assembly1`: **`SameNamespaceName`**.**`Class1`**

```csharp
using System;

namespace SameNamespaceName
{
    public class Class1
    {
        public static void MethodA()
        {
            var assemblyame = System.Reflection.Assembly.GetExecutingAssembly().GetName().Name;
            Console.WriteLine($"Assemble Name: {assemblyame}");
        }
    }
}
```

`Assembly2`: **`SameNamespaceName`**.**`Class2`**

```csharp
using System;

namespace SameNamespaceName
{
    public class Class2
    {
        public static void MethodB()
        {
            var assemblyame = System.Reflection.Assembly.GetExecutingAssembly().GetName().Name;
            Console.WriteLine($"Assemble Name: {assemblyame}");
        }
    }
}
```

Now, if our project refers to the above two assemblies then how can we refer to members in each assembly? The answer lies in `extern` `alias`.

Open solution explorer and select `Assembly1` in the References folder of the project which has the two assemblies referred. Next, open the assembly property window by pressing `F4` key. Change the alias of `Assembly1` from `global` to `assembly1` as shown in the screenshot below.

![ChangeAssemblyAlias](/wp-content/uploads/2022/12/66a0b-changeassemblyalias.png)

You can now add `extern alias assembly1` to the top of your class to call `Assembly1` with its alias.

Here is the full code:

```csharp
extern alias assembly1;

namespace NamespaceAliasExample
{
    public class Program
    {
        static void Main(string[] args)
        {
            assembly1::SameNamespaceName.Class1.MethodA();
            SameNamespaceName.Class2.MethodB();
        }
    }
}
```

The output of the above code is:

Assemble Name: Assembly1
Assemble Name: Assembly2

Hope you found tips in this series helpful. Please feel free to share your suggestions and keep the feedback coming 🙂
