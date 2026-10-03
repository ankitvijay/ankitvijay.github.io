---
title: "C# dynamic – A friend you may want to keep a distance"
date: "2019-08-18T08:00:39+10:00"
lastmod: "2020-09-15T07:41:11+10:00"
url: "/2019/08/18/c-dynamic-a-friend-you-may-want-to-keep-a-distance/"
slug: "c-dynamic-a-friend-you-may-want-to-keep-a-distance"
wp_id: 4153
category: ["asp-net-core"]
tag: ["c", "debugging", "dynamic", "net"]
summary: "Recently, after one of my PRs which was merged to master, my teammates started complaining about a weird scenario. On some occasions, the ASP.NET Core app hosted inside the IIS worker process (w3wp.exe), would simply die without any exception/ warning. There were no clear retro-steps and it was difficult to pinpoint what was causing the"
---

Recently, after one of my PRs which was merged to master, my teammates started complaining about a weird scenario. On some occasions, the ASP.NET Core app hosted inside the IIS worker process (`w3wp.exe`), would simply die without any exception/ warning. There were no clear retro-steps and it was difficult to pinpoint what was causing the issue. It took me sometime to figure out the root cause of the issue and it turned out to be quite an interesting issue.

### Background

As part of my PR, I had added a new code to map a `Repository` `object`/ `entity` to a `Dto`. It was quite complex and a multi-level nested `entity`. I did not use the library such as `Automapper` to automatically map the entities. Why I chose to do mapping manually could be a discussion for another day. Anyways, the culprit code went something like this.

We had an `abstract` base class, let us call it `AbsractBaseRepository` and this class was derived by as many as 18 different child classes. Something similar to below:

```csharp
public abstract class SomeAbstractRepository
{
}

public class DerivedSomeRepository1 : SomeAbstractRepository
{
  public string SomeRandomProperty1 {get; set; }
  public string SomeRandomProperty2 {get; set; }
}

public class DerivedSomeRepository2 : SomeAbstractRepository
{
  public int SomeRandomProperty1 {get; set; }
  public int SomeRandomProperty2 {get; set; }
}

    .
    .
    .

public class DerivedSomeRepository18 : SomeAbstractRepository
{
  public double SomeRandomProperty1 {get; set; }
}
```

The `AbsractBaseRepository` was then used by one of the nested child `Repository` as below:

```csharp
public class NestedChildRepository
{

   .
   .
  public AbsractBaseRepository AbsractBaseRepository  {get; set; }
   .
   .

}
```

The `Dto` which was mapped from this `Repository` had a similar structure.

```csharp
public abstract class SomeAbstractDto
{
}

public class DerivedSomeDto1 : SomeAbstractDto
{
  public string SomeRandomProperty1 {get; set; }
  public string SomeRandomProperty2 {get; set; }
}

public class DerivedSomeDto2 : SomeAbstractDto
{
  public int SomeRandomProperty1 {get; set; }
  public int SomeRandomProperty2 {get; set; }
}

    .
    .
    .

public class DerivedSomeDto18 : SomeAbstractDto
{
  public double SomeRandomProperty1 {get; set; }
}
```

```csharp
public class NestedChildDto
{
   .
   .
  public AbsractBaseDto AbsractBaseDto  {get; set; }

   .
   .

}
```

Why and how we ended up with this structure is again out-of-scope of this post. To map the `Dto` from `Repository`, I tried to be a little bit smart/ lazy and used C# `dynamic` as below:

```csharp
public SomeAbstractDto ToDto(SomeAbstractRepository repository)
{
  if (repository == null) return null;

  return (SomeAbstractDto)ToDto((dynamic)repository);
}

public DerivedSomeDto1  ToDto(DerivedSomeRepository1 repository)
{
   return new DerivedSomeDto1
   {
      SomeRandomProperty1  = repository.SomeRandomProperty1,
      SomeRandomProperty2 = repository.SomeRandomProperty2
   }
}

    .
    .
    .

public DerivedSomeDto18  ToDto(DerivedSomeRepository18 repository)
{
   return new DerivedSomeDto18
   {
      SomeRandomProperty1  = repository.SomeRandomProperty1
   }
}
```

In the above code, casting the `repository` parameter to `dynamic` implicitly converted the base `repository` `object` to the derived `repository` and call the correct overload of `ToDto` method.

### The Issue

Unfortunately, I turned to be too smart for my own good. I missed the mappings for one of the derived `Repository` class. In a scenario where the missed derived `Repository` was present in the `entity`, the code execution fall-back to `base` class overload method, that is,  `ToDto(SomeAbstractRepository repository`). This resulted in an infinite loop causing the process to crash during debugging. Since there were as many as 18 derived `Repository` classes this was somehow missed in integration and unit tests as well. The easiest way to fix this was to simply add the mapping for the missed `Repository` class. However, it presented an additional risk, what if we add another derived `Repository` and we miss adding the mapping for that `Repository`? In that scenario, we would land up in a similar situation.

### The Fix

As a fix for this issue, I decided to go back to basics and use explicit conversion to map the `Repository` and `Dto`, even if it meant more lines of code. The explicit conversion helped us to identify the issue at the compile-time or in the worst case throw a clear exception at run-time instead of blowing the entire process without any exception at the run-time. The updated code looked something like below:

```csharp
public SomeAbstractDto ToDto(SomeAbstractRepository repository)
{
  if (repository == null) return null;

  case DerivedSomeDto1 derivedSomeDto1 :
    return ToDto(derivedSomeDto1);
    .
    .
    .
   case DerivedSomeDto18 derivedSomeDto18:
    return ToDto(derivedSomeDto18);
    default:
      throw InvalidOperationException("Operation not supported for given input");
}
```

#### Lessons Learnt

An important lesson which I learned while resolving this issue was to be extra cautious while using `dynamic`. For all the power `dynamic` brings, it comes at a cost. *Personally,* I try to avoid `dynamic` as much as possible and this issue just gave another reason why I would continue to do so.

Photo by [Lewis Ngugi](https://unsplash.com/@ngeshlew?utm_source=unsplash&utm_medium=referral&utm_content=creditCopyText) on [Unsplash](https://unsplash.com/search/photos/c%23-code?utm_source=unsplash&utm_medium=referral&utm_content=creditCopyText)
