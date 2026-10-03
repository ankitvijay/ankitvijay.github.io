---
title: "C# dynamic is evil, not your friend"
date: "2020-09-11T07:48:20+10:00"
lastmod: "2022-12-23T23:04:46+10:00"
url: "/2020/09/11/c-dynamic-is-an-evil-not-your-friend/"
slug: "c-dynamic-is-an-evil-not-your-friend"
wp_id: 5177
category: ["net-core"]
tag: ["c", "dynamic", "net", "net-core", "tip"]
summary: "This post gives you another reason why to stay away from C# dynamic. It turns the call-site into a late-bound leading to runtime issues."
---

Last year I wrote a blog post on an issue I faced with [C# dynamic](/2019/08/18/c-dynamic-a-friend-you-may-want-to-keep-a-distance/), where my one small mistake killed the IIS worker process, w3wp.exe. Recently, ignoring my own advice, I used **C# dynamic** at one of the places in my code. Not surprisingly found another interesting issue.

## Show me the code!

Here is the minimal reproducible example of the issue:

```csharp
class Program
{
    public static void Main()
    {
        dynamic data = new { SomeProperty = "ABC" };

        var response = IsTrue(data);
        if (response == "1")
        {
            Console.WriteLine("How can this compile?");
        }
    }

    private static bool IsTrue(object someData)
    {
        return true;
    }
}
```

## The issue

As you can see in the above code, method **IsTrue** returns a **bool**, but I’m still able to assign it to a **string**type. This code compiles successfully. At the runtime, however, it throws below exception:

Unhandled exception. CSharp.RuntimeBinder.RuntimeBinderException: Operator ‘==’ cannot be applied to operands of type ‘bool’ and ‘string’  … at CallSite.Target(Closure , CallSite , Object , String ) … at System.Dynamic.UpdateDelegates.UpdateAndExecute2[T0,T1,TRet](CallSite site, T0 arg0, T1 arg1)

At first glance, it just does not make sense. How can a return type of a static method not *inferred*by C# compiler? I reached out to the community on [StackOverflow](https://stackoverflow.com/questions/63784153/dynamic-passed-as-parameter-return-type-cannot-be-inferred) and [Twitter](https://twitter.com/davidfowl/status/1303080555475423232)to understand this little bit more.

Here is the response, I received from [Jon Skeet](https://stackoverflow.com/users/22656/jon-skeet):

> When you call a method with an argument of type dynamic, the call is dynamically bound – so the compiler treats the return type as dynamic too.
>
> There are some cases where the compiler *will* notice things that aren’t feasible, but generally when you use dynamic you lose a lot of compile-time type safety. I’m slightly surprised by the exact exception you received (and it’s not the exception I see) , but I’m not surprised that it compiled.

[David Fowler](https://twitter.com/davidfowl) on twitter also explained that dynamic turns the method call into a late-bound call.

<blockquote class="twitter-tweet" data-dnt="true" data-width="500"><p dir="ltr" lang="en">Dynamic infects the entire callsite turning everything into a late bound call</p>— David Fowler (@davidfowl) <a href="https://twitter.com/davidfowl/status/1303080555475423232?ref_src=twsrc%5Etfw">September 7, 2020</a></blockquote>

I also did a little bit reading and came across [this Microsoft](https://docs.microsoft.com/en-us/dotnet/csharp/programming-guide/types/using-type-dynamic#overload-resolution-with-arguments-of-type-dynamic) documentation where it explains that overload resolution for dynamic occurs at runtime instead of compile-time. However, this issue proved that the behavior is not limited to method overload alone.

## Final Words

The root cause of the issue which I came across here is no different to the [last time](/2019/08/18/c-dynamic-a-friend-you-may-want-to-keep-a-distance/). **dynamic is not static** :). C# dynamic defers the resolution and the problems that come along with it to the runtime.

The issue, yet again, proves why dynamic is terrible and how it can turn an innocent-looking code into a production nightmare.

[Don Syme](https://twitter.com/dsymetweets), the F# language designer, has this to say about dynamic and I could not agree more.

<blockquote class="twitter-tweet" data-dnt="true" data-width="500"><p dir="ltr" lang="en">– no expression form for generative list or sequence expressions (making HTML DSLs a mess among other things)<br/><br/>– dynamic is hell waiting to destroy your life</p>— Don Syme (@dsymetweets) <a href="https://twitter.com/dsymetweets/status/1294277715697311749?ref_src=twsrc%5Etfw">August 14, 2020</a></blockquote>
