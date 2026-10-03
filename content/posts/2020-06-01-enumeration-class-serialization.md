---
title: "Enumeration class and JSON Serialization"
date: "2020-06-01T07:08:05+10:00"
lastmod: "2022-12-23T23:04:47+10:00"
url: "/2020/06/01/enumeration-class-serialization/"
slug: "enumeration-class-serialization"
wp_id: 4947
category: ["ddd", "domain-driven-design", "enumeration-class", "json-serialization", "net-core"]
tag: ["c", "ddd", "domain-driven-design", "enumeration", "json", "jsonconverter", "net", "net-core", "newtonsoft", "serialization", "system-text-json"]
summary: "In this post, I will explain how we can serialize an Enumeration class using a custom JSON Converter for both System.Text.Json and Newtonsoft.Json."
---

This is the second post in the [S](/2020/06/12/series-enumeration-classes-ddd-and-beyond/)[eries: Enumeration classes – DDD and beyond](/2020/06/12/series-enumeration-classes-ddd-and-beyond/). If you have jumped here right in and are new to the Enumeration classes, I suggest going through the previous post first.

- Part 1: [Introduction to Enumeration Classes](/2020/05/21/introduction-enumeration-class/)
- Part 2: Enumeration class and JSON Serialization (this post)
- Part 3: [Enumeration class as query string parameter](/2020/06/14/enumeration-class-query-string/)
- Part 4: [Generating client code with NSwag for Enumeration class](/2020/07/12/enumeration-class-nswag/)
- Part 5: [Implementing Inheritance with Enumeration class](/2020/08/08/inheritance-enumeration-class/)

In part 1, I gave an introduction to Enumeration class and what problem it solves. In this and upcoming posts, I will explain how we can use Enumeration class for advanced scenarios. This post would cover how to we can serialize an Enumeration class.

A disclaimer before I go further:

While the Enumeration class is an excellent alternate to an Enum, it brings along a fair deal of complexity. Enumeration class solves specific-business scenarios and may not be fit for general purposes. Please evaluate if it suits your needs before adopting the Enumeration class.

## NuGet and source code

The Enumeration class and other dependent classes are available as the [NuGet packages](https://www.nuget.org/packages?q=ankitvijay). You can find the source code for the series at [this GitHub link](https://github.com/ankitvijay/Enumeration).

### Why serialize an Enumeration Class?

There can be a few reasons you may need to serialize and deserialize an Enumeration class, such as:

- Saving and retrieving your domain object in No-SQL DBs like Cosmos, Raven DB, etc.
- Using Enumeration class in the request body and response of a Web API.
- Publishing and retrieving an object with Enumeration class from a message bus.

Let us go back to our PaymentType example from our last post.

```csharp
public abstract class PaymentType : Enumeration
{
    public static readonly PaymentType DebitCard = new DebitCardType();

    public static readonly PaymentType CreditCard = new CreditCardType();

    public abstract string Code { get; }

    private PaymentType(int value, string name = null) : base(value, name)
    {
    }

    private class DebitCardType : PaymentType
    {
        public DebitCardType() : base(0, "DebitCard")
        {
        }

        public override string Code => "DC";
    }

    private class CreditCardType : PaymentType
    {
        public CreditCardType() : base(1, "CreditCard")
        {
        }

        public override string Code => "CC";
    }
}
```

Unlike an Enum, **PaymentType**is a class with **static** **readonly**members. We would need a custom logic or converter to serialize it to JSON and deserialize it back.

### Version 1 – Using System.Text.Json

We can extend **System.Text.Json –>JsonConverter**of to serialize and deserialize an **Enumeration**class.

```csharp
// Import Nuget package System.Text.Json

public class EnumerationJsonConverter : JsonConverter<Enumeration>
{
    private const string NameProperty = "Name";

    public override bool CanConvert(Type objectType)
    {
        return objectType.IsSubclassOf(typeof(Enumeration));
    }

    public override Enumeration Read(ref Utf8JsonReader reader, Type typeToConvert, JsonSerializerOptions options)
    {
        switch (reader.TokenType)
        {
            case JsonTokenType.Number:
            case JsonTokenType.String:
                return GetEnumerationFromJson(reader.GetString(), typeToConvert);
            case JsonTokenType.Null:
                return null;
            default:
                throw new JsonException(
                    $"Unexpected token {reader.TokenType} when parsing the enumeration.");
        }
    }

    public override void Write(Utf8JsonWriter writer, Enumeration value, JsonSerializerOptions options)
    {
        if (value is null)
        {
            writer.WriteNull(NameProperty);
        }
        else
        {
            var name = value.GetType().GetProperty(NameProperty, BindingFlags.Public | BindingFlags.Instance);
            if (name == null)
            {
                throw new JsonException($"Error while writing JSON for {value}");
            }

            writer.WriteStringValue(name.GetValue(value).ToString());
        }
    }

    private static Enumeration GetEnumerationFromJson(string nameOrValue, Type objectType)
    {
        try
        {
            object result = default;
            var methodInfo = typeof(Enumeration).GetMethod(
                nameof(Enumeration.TryGetFromValueOrName)
                , BindingFlags.Static | BindingFlags.Public);

            if (methodInfo == null)
            {
                throw new JsonException("Serialization is not supported");
            }

            var genericMethod = methodInfo.MakeGenericMethod(objectType);

            var arguments = new[] { nameOrValue, result };

            genericMethod.Invoke(null, arguments);
            return arguments[1] as Enumeration;
        }
        catch (Exception ex)
        {
            throw new JsonException($"Error converting value '{nameOrValue}' to a enumeration.", ex);
        }
    }
}
```

### Version 2 – Using Newtonsoft.Json

Unfortunately, System.Text.Json has still not reached [feature parity](https://docs.microsoft.com/en-us/dotnet/standard/serialization/system-text-json-migrate-from-newtonsoft-how-to#table-of-differences-between-newtonsoftjson-and-systemtextjson) to **Newtonsoft.Json**. As a result, so often, we fall back to Newtonsoft.Json.

Here is the Newtonsoft.Json version of JsonConverter

```csharp
// Import Newtonsoft.Json

public class EnumerationJsonConverter : JsonConverter<Enumeration>
{
    public override void WriteJson(JsonWriter writer, Enumeration value, JsonSerializer serializer)
    {
        if (value is null)
        {
            writer.WriteNull();
        }
        else
        {
            writer.WriteValue(value.Name);
        }
    }

    public override Enumeration ReadJson(JsonReader reader,
        Type objectType,
        Enumeration existingValue,
        bool hasExistingValue,
        JsonSerializer serializer)
    {
        return reader.TokenType switch
        {
            JsonToken.Integer => GetEnumerationFromJson(reader.Value.ToString(), objectType),
            JsonToken.String => GetEnumerationFromJson(reader.Value.ToString(), objectType),
            JsonToken.Null => null,

            _ => throw new JsonSerializationException($"Unexpected token {reader.TokenType} when parsing an enumeration")
        };
    }

    private static Enumeration GetEnumerationFromJson(string nameOrValue, Type objectType)
    {
        try
        {
            object result = default;
            var methodInfo = typeof(Enumeration).GetMethod(
                nameof(Enumeration.TryGetFromValueOrName)
                , BindingFlags.Static | BindingFlags.Public);

            if (methodInfo == null)
            {
                throw new JsonSerializationException("Serialization is not supported");
            }

            var genericMethod = methodInfo.MakeGenericMethod(objectType);

            var arguments = new[] { nameOrValue, result };

            genericMethod.Invoke(null, arguments);
            return arguments[1] as Enumeration;
        }
        catch (Exception ex)
        {
            throw new JsonSerializationException($"Error converting value '{nameOrValue}' to a enumeration.", ex);
        }
    }
}
```

### Usage

Let us consider a class **Transaction** with property **PaymentType**.

```csharp
public class Transaction
{
    public double Amount { get; set; }

    public PaymentType PaymentType { get; set; }
}
```

We can serialize and serialize the **Transaction**class using **EnumerationJsonConverter,**as shown in the below test:

```csharp
// Import System.Text.Json;

public class EnumerationJsonConverterTests
{
    private readonly ITestOutputHelper _testOutputHelper;

    public EnumerationJsonConverterTests(ITestOutputHelper testOutputHelper)
    {
        _testOutputHelper = testOutputHelper;
    }

    [Fact]
    public void EnumerationIsSerializesAndDeserializesCorrectly()
    {
        var expected = new Transaction
        {
            Amount = 100,
            PaymentType = PaymentType.CreditCard
        };

        var json = JsonSerializer.Serialize(expected,
            new JsonSerializerOptions
            {
                Converters =
                {
                    new EnumerationJsonConverter()
                }
            });

        _testOutputHelper.WriteLine(json);

        var actual= JsonSerializer.Deserialize<Transaction>(json, new JsonSerializerOptions()
        {
            Converters = { new EnumerationJsonConverter() }
        });

        Assert.Equal(expected.Amount, actual.Amount);
        Assert.Equal(expected.PaymentType, actual.PaymentType);
    }
}
```

Here is the JSON output:

```json
{
  "Amount":100,
  "PaymentType":"CreditCard"
}
```

I hope you enjoyed this post and learning about how you can create a custom JSON converter to serialize an Enumeration class.
