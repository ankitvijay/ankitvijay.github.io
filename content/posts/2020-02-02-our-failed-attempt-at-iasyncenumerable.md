---
title: "Our failed attempt at IAsyncEnumerable"
date: "2020-02-02T16:23:07+10:00"
lastmod: "2020-09-26T08:48:34+10:00"
url: "/2020/02/02/our-failed-attempt-at-iasyncenumerable/"
slug: "our-failed-attempt-at-iasyncenumerable"
wp_id: 4547
category: ["asp-net-core", "asp-net-core-3-1", "iasyncenumerable", "net-core", "net-core-2-2", "net-core-3-0"]
tag: ["asp-net-core", "asp-net-core-3-1", "async", "async-await", "c", "iasyncenumerable", "net", "net-core", "net-core-3-0"]
summary: "C# 8 introduced a great feature of async stream using IAsyncEnumerable. This post talks about potential pitfalls when not using it right."
---

I, like many others, usually write about my learning and success in my blog posts. But one of my colleagues made me realize that it is equally important to talk about your failures. So, here I’m talking about our failed attempt to migrate to IAsyncEnumerable.

### Background

With the release of .NET Core 3.1 and .NET Core 2.2 going out of support, we recently migrated one of our ASP.NET Core applications from .NET Core 2.2 to the latest and the greatest .NET Core 3.1.

.NET Core 3+ also comes up with many C# 8.0 language improvements. One of those improvements is [async stream](https://docs.microsoft.com/en-us/dotnet/csharp/tutorials/generate-consume-asynchronous-stream#async-streams-provide-a-better-way) or **IAsyncEnumerable**.

One of our API endpoints, “streamed” using IEnumerable. We felt there was an opportunity to use the latest C# 8 feature of the async stream using IAsyncEnumerable. We use Dapper to talk to our SQL. Here is an ultra-simplified version of our API and dapper query before our attempted migration to IAsyncEnumerable.

### Existing code

```csharp
    // Using Dapper;

    public async Task<IEnumerable<Item>> GetItems(int id)
    {
        var reader = await _connection.QueryMultipleAsync(getItemsSql,
           param: new
           {
               Id = id
           });

        var idFromDb = (await reader.ReadAsync<int?>().ConfigureAwait(false)).SingleOrDefault();
        if (idFromDb == null)
        {
           return null;
        }

        var items = await reader.ReadAsync<Item>(buffered: false).ConfigureAwait(false);

        return Stream(reader, items);
    }

    private IEnumerable<Item> Stream(SqlMapper.GridReader reader, IEnumerable<Item> items)
    {
        using (reader)
        {
            foreach (var item in items)
            {
                yield return item;
            }
        }
    }
```

```csharp
  public async Task<IActionResult> GetItems(int id)
  {
      var items = await _query.GetItems(id);
      return Ok(Stream(items);
  }

  private IEnumerable<ItemDto> Stream(IEnumerable<Item> items)
  {
      foreach (var item in items)
      {
          yield return GetItemDto(item);
      }
  }

  private static ItemDto GetItemDto(Item item)
  {
      return new ItemDto
      {
         //  Convert Item to ItemDto
      };
  }
```

As you can see in the above code, we do not *buffer* the result set returned from Dapper query in-memory and we return **Task&lt;IEnumerable&lt;ItemDto>** from the API.

### Updated Code

In order to convert the above code to use async stream, we started with converting the **IEnumerable** return type to **IAsyncEnumerable.** The updated code looked similar to below.

```csharp
    // Import Nuget package: System.Linq.Async

    public async Task<IAsyncEnumerable<Item>> GetItems(int id)
    {
        var reader = await _connection.QueryMultipleAsync(getItemsSql,
           param: new
           {
               Id = id
           });

        var idFromDb = (await reader.ReadAsync<int?>().ConfigureAwait(false)).SingleOrDefault();
        if (idFromDb == null)
        {
            return null;
        }

        var items = await reader.ReadAsync<Item>(buffered: false).ConfigureAwait(false);

        return Stream(reader, items);
    }

    private IAsyncEnumerable<Item> Stream(SqlMapper.GridReader reader, IEnumerable<Item> items)
    {
        using (reader)
        {
           await foreach (var item in items.ToAsyncEnumerable())
           {
               yield return item;
           }
        }
     }
```

```csharp
  public async Task<IActionResult> GetItems(int id)
  {
      var items = await _query.GetItems(id);
      return Ok(Stream(items);
  }

  private IAsyncEnumerable<ItemDto> Stream(IAsyncEnumerable<Item> items)
  {
      await foreach (var item in items)
      {
          yield return GetItemDto(item);
      }
  }

  private static ItemDto GetItemDto(Item item)
  {
      return new ItemDto
      {
         //  Convert Item to ItemDto
      };
  }
```

### The issues

With these minor changes to code, we thought we had won the battle converting our API into an **async stream**. But, unfortunately, we turned out to be wrong. There are primarily two issues with the above approach:

**Issue 1 – Dapper does not have support for IAsyncEnumerable**

The Dapper library currently does not support IAsyncEnumerable at the moment. There is a good [answer on StackOverflow](https://stackoverflow.com/questions/55536681/what-happens-with-returning-ienumerable-if-used-with-async-await-streaming-data/55538125#55538125) from @MarkGravell explaining the reason why this is the case at the moment. To convert the dapper query returned IAsyncEnumerable, we used the **ToAsyncEnumerable** from **System.Linq.Async** package. We wrongly assumed that ToAsyncEnumerable would magically convert the query into async. But it was a wrong assumption. I was corrected by @PanagiotisKanavos and @PauloMorgado on [Stack Overflow](https://stackoverflow.com/questions/59956623/using-iasyncenumerable-with-dapper).

Wrapping the query to returned IAsycEnumerable did nothing more than a fake async operation. It is still a CPU bound operation, and the code change makes it worse.

**Issue 2 – IAsyncEnumerable buffer limit**

While the first issue was enough for us to ditch **IAsyncEnumerable** untilthe Dapper library supports it, we soon realized that it was not the only issue. When we tried to test the API with around 50,000 records we received the following error:

‘AsyncEnumerableReader’ reached the configured maximum size of the buffer when enumerating a value of type ‘&lt;type>’. This limit is in place to prevent infinite streams of ‘IAsyncEnumerable&lt;>’ from continuing indefinitely. If this is not a programming mistake, consider ways to reduce the collection size, or consider manually converting ‘&lt;type>’ into a list rather than increasing the limit.

With 50,000 records, we had hit the buffer limit of number of records we can return with IAsyncEnumerable in ASP.NET Core. A property **[MvcOptions.MaxIAsyncEnumerableBufferLimit](https://docs.microsoft.com/en-us/dotnet/api/microsoft.aspnetcore.mvc.mvcoptions.maxiasyncenumerablebufferlimit?view=aspnetcore-3.1)** determines the buffer limit. By default, the limit is 8192. Since we were trying to return more than 8192 records we got the above error. We can update the buffer limit to the higher value by overriding **MaxIAsyncEnumerableBufferLimit** . However, this raised another question, why there is a buffer limit in the first place? Is that not what we were trying to avoid with **yield return**? The answer to this perhaps lies in these issues:

- [ASP.NET Core 3.0 doesn’t stream IAsyncEnumerable&lt;T> as chunk of data](https://github.com/dotnet/runtime/issues/30981)
- [Add support for asynchronously serializing IAsyncEnumerable&lt;T>](https://github.com/dotnet/runtime/issues/1570)

At the time of writing, there is no JSON serializer support for IAsyncEnumerable as yet. This results in buffering the response from the API instead of returning a response stream.

### Conclusion

Due to the above issues, we ended up reverting our changes to the original code. **IAsyncEnumerable** is a great feature and could solve world hunger in the future. But it is not ready for prime time yet, at least for our use case. Nevertheless, this whole exercise turned out to be a great learning experience for us. I hope this post would also help you to be aware of the pitfalls of jumping into the “new shining” feature such as IAsyncEnumerable without understanding it fully.

> Photo by [chuttersnap](https://unsplash.com/@chuttersnap?utm_source=unsplash&utm_medium=referral&utm_content=creditCopyText) on [Unsplash](https://unsplash.com/s/photos/fail?utm_source=unsplash&utm_medium=referral&utm_content=creditCopyText)
