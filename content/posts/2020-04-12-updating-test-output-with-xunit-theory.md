---
title: "Writing better tests with xUnit Theory"
date: "2020-04-12T08:55:36+10:00"
lastmod: "2022-12-23T23:04:47+10:00"
url: "/2020/04/12/updating-test-output-with-xunit-theory/"
slug: "updating-test-output-with-xunit-theory"
wp_id: 4727
category: ["testing", "unit-testing", "xunit", "xunit-fact", "xunit-theory"]
tag: ["c", "net", "xunit", "xunit-fact", "xunit-theory"]
summary: "This post describes some of the pain-points of xUnit Theory and how we can write more descriptive tests by overriding the test output."
---

[xUnit](https://xunit.net/) needs no introduction. It is a free, open-source unit testing tool for .NET which has been around for years. It is also a great alternate to [MSTest](https://github.com/Microsoft/testfx-docs)and [NUnit](https://nunit.org/documentation/).

**xUnit Theory** is a great way of writing data-driven tests. It provides a simple and easy way to write repetitive tests through attributes such as **InlineData, MemberData, and ClassData.**

For this post, I have assumed that you are already aware of xUnitTheoryand I’m going talk to a little bit more about how we can write better descriptive tests using MemberData.

### Example

Let us consider a simple example. We have a class called ****AnimalRepository**** with a method **Find.**

```csharp
public class AnimalRepository
{
    private readonly List<string> _animals = new List<string>()
        {
            "TIGER",
            "LION",
            "DOG",
            "CAT",
            "COW",
            "PIG"
        };
    public string Find(SearchCriteria searchCriteria)
    {
        if (searchCriteria == null)
        {
            throw new ArgumentNullException(nameof(searchCriteria));
        }

        return _animals.FirstOrDefault(e => e.Contains(searchCriteria.SearchTerm,
            searchCriteria.IgnoreCase ? StringComparison.OrdinalIgnoreCase : StringComparison.Ordinal));
    }
}
```

```csharp
public class SearchCriteria
{
    public SearchCriteria(string searchTerm, bool ignoreCase = false)
    {
        SearchTerm = searchTerm ?? throw new ArgumentNullException(nameof(searchTerm));
        IgnoreCase = ignoreCase;
    }

    public string SearchTerm { get; }

    public bool IgnoreCase { get; }
}
```

The above code is self-explanatory. As you can see, the **Find**method allows a user to search for an animal name from the in-memory list of animals. Let’s say, we now need to unit test the **Find**method of class **AnimalRepository.**

### Version 1

The code below shows how a typical test for the **Find** method would like using **XUnit** theory.

```csharp
public class AnimalRepositoryTests
{
    [Theory]
    [MemberData(nameof(GetFindAnimalData))]
    public void FindReturnsCorrectResult(SearchCriteria searchCriteria, string expectedResult)
    {
        var repository = new AnimalRepository();

        // Act
        var result = repository.Find(searchCriteria);

        // Assert
        Assert.Equal(expectedResult, result);
    }

    public static IEnumerable<object[]> GetFindAnimalData()
    {
        yield return new object[]
        {
                new SearchCriteria("FOX"),
                null
        };

        yield return new object[]
        {
                new SearchCriteria("dog", true),
                "DOG"
        };

        yield return new object[]
        {
                new SearchCriteria("IG"),
                "TIGER"
        };
    }
}
```

As you can see the xUnit Theory provides a simple consistent way to create a single test with different test data sources.

The above code, however, has some drawbacks when compared to a **xUnit Fact.** Here are some of the cons:

- Unlike **Fact**where we have different tests each scenario, the tests here are no longer descriptive. In the above approach, it is not always possible for a new developer to easily understand what scenario we are trying to test.
- On running the tests through Visual Studio Test Explorer or ReSharper or even **dotnet test** command, the test output is not so easy to understand.

![Figure 1: Version 1 - ReSharper Test Result window](/wp-content/uploads/2022/12/ecb2c-image.png "Figure 1: Version 1 - ReSharper Test Result window")

*Figure 1: Version 1 – ReSharper Test Result window*

![Figure 2:  Version 1 - "dotnet test --verbosity normal" test output](/wp-content/uploads/2022/12/65f23-image-2.png "Figure 2:  Version 1 - \"dotnet test --verbosity normal\" test output")

*Figure 2: Version 1 – “ dotnet test –verbosity normal ” test output*

- If we have a huge test dataset, then it is difficult to relate the test data with the corresponding test output especially when the test fails for one or more test data.

### Version 2

We first start with an **abstract** class **TestSource**.

```csharp
public abstract class TestSource
{
    public string TestName { get; }

    protected TestSource(string testName)
    {
        TestName = testName;
    }

    public override string ToString()
    {
        return TestName.ToString();
    }
}
```

As you can see in the code above, the **TestSource constructor**takes the **testName** as input parameter and overrides the **ToString()**method to return **TestName**.

The test output rendered by xUnit Theory can be updated by overriding the ToString() method on the data object.

Next, we update our **AnimalRespositoryTests** class as below.

```csharp
  public class AnimalRepositoryTestSource : TestSource
  {
      public AnimalRepositoryTestSource(SearchCriteria searchCriteria, string expectedResult, [CallerMemberName]string testName = null)
          : base(testName)
      {
          SearchCriteria = searchCriteria;
          ExpectedResult = expectedResult;
      }

      public SearchCriteria SearchCriteria { get; }
      public string ExpectedResult { get; }
  }
```

```csharp
public class AnimalRepositoryTests
{
    [Theory]
    [MemberData(nameof(GetFindAnimalData))]
    public void FindReturnsCorrectResult(AnimalRepositoryTestSource testData)
    {
        var repository = new AnimalRepository();

        // Act
        var result = repository.Find(testData.SearchCriteria);

        // Assert
        Assert.Equal(testData.ExpectedResult, result);
    }

    public static IEnumerable<object[]> GetFindAnimalData()
    {
        yield return WhenSearchTermDoesNotExist();
        yield return WhenIgnoreCaseIsSetToTrue();
        yield return WhenSearchTermIsPartialMatch();
    }

    private static object[] WhenSearchTermDoesNotExist()
    {
        return new object[]
        {
            new AnimalRepositoryTestSource(new SearchCriteria("FOX"), null)
        };
    }

    private static object[] WhenIgnoreCaseIsSetToTrue()
    {
        return new object[]
        {
            new AnimalRepositoryTestSource(new SearchCriteria("dog", true), "DOG")
        };
    }
    private static object[] WhenSearchTermIsPartialMatch()
    {
        return new object[]
        {
            new AnimalRepositoryTestSource(new SearchCriteria("IG", true), "TIGER")
        };
    }

}
```

Few things to highlight in above code:

- We create a class **AnimalRepositoryTestSource** which inherits from **TestSource.**Typically this class would remain in the same file as **AnimalRepositoryTests**.
- **AnimalRepositoryTestSource**constructor takes the parameters required for our test data in Version 1 along with the [CallerMethodName](https://docs.microsoft.com/en-us/dotnet/api/system.runtime.compilerservices.callermembernameattribute?view=netframework-4.8) which gives us the method name of “caller to the method”. I have talked more about **CallerMethodName** in one of my [previous posts](/2018/01/08/lesser-known-c-features-part-1/)**.**
- Test data in **GetFindAnimalData** method is divided into separate methods. Each method name clearly describes **what** we are trying to test.
- The methods create an instance of **AnimalRepositoryTestSource** by passing the relevant test data as parameters in its constructor.
- **FindReturnsCorrectResult** is updated to accept **AnimalRepositoryTestSource** object.

That’s it! With the above code changes, our test output would look much simpler and more descriptive.

![Figure 3: Version 2 - ReSharper Test Result window](/wp-content/uploads/2022/12/53d5f-image-6.png "Figure 3: Version 2 - ReSharper Test Result window")

*Figure 3: Version 2 – ReSharper Test Result window*

![Figure 2: Version 2 - "dotnet test --verbosity normal" test output](/wp-content/uploads/2022/12/6c69c-image-4.png "Figure 2: Version 2 - \"dotnet test --verbosity normal\" test output")

*Figure 4: Version 2 – “ dotnet test –verbosity normal ” test output*

I hope you find this tip useful for your tests written with xUnit Theory. 🙂

The source code of the code samples in this blog is available on GitHub [here](https://github.com/ankitvijay/xUnitMemberDataExample).

> Feature Photo by [Samia Liamani](https://unsplash.com/@mialiamani?utm_source=unsplash&utm_medium=referral&utm_content=creditCopyText) on [Unsplash](https://unsplash.com/s/photos/unit-test?utm_source=unsplash&utm_medium=referral&utm_content=creditCopyText)

[CodeProject](https://www.codeproject.com)
