---
title: "Gotchas with switch expression"
date: "2021-09-04T07:59:21+10:00"
lastmod: "2021-09-04T10:16:10+10:00"
url: "/2021/09/04/c-gotchas-with-switch-expression/"
slug: "c-gotchas-with-switch-expression"
wp_id: 257463
category: ["net"]
tag: ["c", "net", "rosyln", "switch-case", "switch-expression", "tips-tricks", "visual-studio"]
summary: "This post talks about a bug in Rider and Roslyn analyzers when we refactor the switch-case to switch expression with Nullable default type."
featured_image: "https://ankitvijaydotin.wordpress.com/wp-content/uploads/2022/12/51f6d-csharp.png"
---

## Introduction

I use JetBrains Rider for my development and usually refactor my code as per the tips from Rider (or ReSharper if you are using Visual Studio). One of the tips that Rider suggests is to replace the traditional switch-case statements with a relatively new [C# feature](https://docs.microsoft.com/en-us/dotnet/csharp/language-reference/operators/switch-expression), switch expression. Here is the screenshot of the suggestion:

![](https://ankitvijaydotin.wordpress.com/wp-content/uploads/2022/12/96cf8-image.png?w=1024&h=476)

*Rider suggestion to convert switch-case to switch expression*

If you are a Visual Studio user, then Roslyn analyzer gives the same refactoring suggestion.

![Roslyn Analyzer screenshot for switch expression](https://ankitvijaydotin.wordpress.com/wp-content/uploads/2022/12/d7f2d-roslyn.jpg)

*Roslyn Analyzer refactoring suggestion*

Most of the time, the refracting suggestion does not have any side-effect, and the code works as before.

## Switch Expression refactoring may introduce a bug

Consider the below simple code:

```
Console.WriteLine("Is Null? " + (GetBoolean("Nah") == null));
enum Boolean
{
    Yes,
    No
}
static Boolean? GetBoolean(string boolString)
{
    switch (boolString)
    {
        case "Yes":
            return Boolean.Yes;
        case "No":
            return Boolean.No;
        default:
            return default;
    }
}
```

The method **`GetBoolean`** takes a string and returns a nullable enum. When the parameter `boolString` does not match any case, it returns `default`. That means when we pass parameter value as `Nah` the method returns `null` , and the output of the above code would be `true`

If we refactor the above code as per Rider or Visual Studio suggestion, the code would look as below:

```
static Boolean? GetBoolean(string boolString)
{
    return boolString switch
    {
        "Yes" => Boolean.Yes,
        "No" => Boolean.No,
         _ => default
     };
}
```

At first glance, the above code appears correct, and we would expect it to return `null` when we pass the parameter value as `Nah` as in the previous code snippet.

However, the method returns `Yes` instead. And the output of the code changes to `false`

## Why does this happen?

I landed into this issue very recently, and luckily, a failed test helped me discover this bug. I raised this question on Twitter

<blockquote class="twitter-tweet" data-dnt="true" data-width="500"><p dir="ltr" lang="en">C# trivia. What would be the output of this?<a href="https://t.co/VlrUqQ8kA2">https://t.co/VlrUqQ8kA2</a><a href="https://twitter.com/resharper?ref_src=twsrc%5Etfw">@resharper</a> suggests converting switch/case to switch expression. Should it be fair to assume that we should get the same result? 🙂<br/><br/>cc: <a href="https://twitter.com/buhakmeh?ref_src=twsrc%5Etfw">@buhakmeh</a> <a href="https://twitter.com/davidfowl?ref_src=twsrc%5Etfw">@davidfowl</a> <br/>Happy to hear your thoughts. <a href="https://t.co/bWRUw1QAqh">pic.twitter.com/bWRUw1QAqh</a></p>— Ankit Vijay (@vijayankit) <a href="https://twitter.com/vijayankit/status/1430707964029988869?ref_src=twsrc%5Etfw">August 26, 2021</a></blockquote>

The reason we see this behaviour is because, with switch expression, the first “case” does not return a `Boolean?` but `Boolean` instead. As a result, it infers the `default` as a default `Boolean` which is `Yes` leading to this bug.

@citizenmatt (Matt Ellis) sumps it up pretty nicely in his tweet

<blockquote class="twitter-tweet" data-dnt="true" data-width="500"><p dir="ltr" lang="en">Great example! The target typed `default` keyword is different in each scenario. With the switch statement, it's "target typed" to the return keyword, which is nullable. In the switch expression, it's target typed to the results of the previous arms of the switch, which is not.</p>— Matt Ellis (@citizenmatt) <a href="https://twitter.com/citizenmatt/status/1430824939448422401?ref_src=twsrc%5Etfw">August 26, 2021</a></blockquote>

Matt Ellis (from JetBrains) and David Kean (from Visual Studio) were kind enough to raise a bug to fix this in the future release.

<blockquote class="twitter-tweet" data-dnt="true" data-width="500"><p dir="ltr" lang="en">So we get different semantics with different code. We need to adjust our inspection for cases like these. I've created an issue you can vote for and track, etc. <a href="https://t.co/EEdMNUjCUH">https://t.co/EEdMNUjCUH</a></p>— Matt Ellis (@citizenmatt) <a href="https://twitter.com/citizenmatt/status/1430825197884649472?ref_src=twsrc%5Etfw">August 26, 2021</a></blockquote>

<blockquote class="twitter-tweet" data-dnt="true" data-width="500"><p dir="ltr" lang="en">Nice one! Filed <a href="https://t.co/2FB4uSV6fp">https://t.co/2FB4uSV6fp</a></p>— David Kean (@davkean) <a href="https://twitter.com/davkean/status/1431064303637958659?ref_src=twsrc%5Etfw">August 27, 2021</a></blockquote>

## fixing the switch expression

To fix this issue, we can typecast the first case of switch expression as `Boolean?`.

```
static Boolean? GetBoolean(string boolString)
{
    return boolString switch
    {
        "Yes" => (Boolean?)Boolean.Yes,
        "No" => Boolean.No,
         _ => default
     };
}
```

Alternatively, we can return the default as `null` instead.

```
static Boolean? GetBoolean(string boolString)
{
    return boolString switch
    {
        "Yes" => Boolean.Yes,
        "No" => Boolean.No,
         _ => null
     };
}
```

Personally, I went for the second approach as I find it cleaner.

## Wrapping Up

This whole exercise was a great learning exercise for me. It shows that we need to be careful when dealing with `default` type in C# especially when using it with switch expression. Hope you also find this useful.
