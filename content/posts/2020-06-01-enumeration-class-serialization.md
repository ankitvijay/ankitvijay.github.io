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

This is the second post in the [S](https://ankitvijaydotin.wordpress.com/2020/06/12/series-enumeration-classes-ddd-and-beyond/)[eries: Enumeration classes – DDD and beyond](https://ankitvijaydotin.wordpress.com/2020/06/12/series-enumeration-classes-ddd-and-beyond/). If you have jumped here right in and are new to the Enumeration classes, I suggest going through the previous post first.

- Part 1: [Introduction to Enumeration Classes](https://ankitvijaydotin.wordpress.com/2020/05/21/introduction-enumeration-class/)
- Part 2: Enumeration class and JSON Serialization (this post)
- Part 3: [Enumeration class as query string parameter](https://ankitvijaydotin.wordpress.com/2020/06/14/enumeration-class-query-string/)
- Part 4: [Generating client code with NSwag for Enumeration class](https://ankitvijaydotin.wordpress.com/2020/07/12/enumeration-class-nswag/)
- Part 5: [Implementing Inheritance with Enumeration class](https://ankitvijaydotin.wordpress.com/2020/08/08/inheritance-enumeration-class/)

In part 1, I gave an introduction to Enumeration class and what problem it solves. In this and upcoming posts, I will explain how we can use Enumeration class for advanced scenarios. This post would cover how to we can serialize an Enumeration class.

A disclaimer before I go further:

While the Enumeration class is an excellent alternate to an Enum, it brings along a fair deal of complexity. Enumeration class solves specific-business scenarios and may not be fit for general purposes. Please evaluate if it suits your needs before adopting the Enumeration class.

## NuGet and source code

The Enumeration class and other dependent classes are available as the [NuGet packages](https://www.nuget.org/packages?q=ankitvijay). You can find the source code for the series at [this GitHub link](https://github.com/ankitvijay/Enumeration).

### Why serialize an Enumeration Class?

There can be a few reasons you may need to serialize and deserialize an Enumeration class, such as:

- Saving and retrieving your domain object in No-SQL DBs like Cosmos, Raven DB, etc.
- Using Enumeration class in the request body and response of a Web API.
- Publishing and retrieving an object with Enumeration class from a message bus.

Let us go back to our PaymentType example from our last post.

This file contains hidden or bidirectional Unicode text that may be interpreted or compiled differently than what appears below. To review, open the file in an editor that reveals hidden Unicode characters.
[Learn more about bidirectional Unicode characters](https://github.co/hiddenchars)

[Show hidden characters]({{ revealButtonHref }})

|  |  |
| --- | --- |
|  | public abstract class PaymentType : Enumeration |
|  | { |
|  | public static readonly PaymentType DebitCard = new DebitCardType(); |
|  |  |
|  | public static readonly PaymentType CreditCard = new CreditCardType(); |
|  |  |
|  | public abstract string Code { get; } |
|  |  |
|  | private PaymentType(int value, string name = null) : base(value, name) |
|  | { |
|  | } |
|  |  |
|  | private class DebitCardType : PaymentType |
|  | { |
|  | public DebitCardType() : base(0, "DebitCard") |
|  | { |
|  | } |
|  |  |
|  | public override string Code => "DC"; |
|  | } |
|  |  |
|  | private class CreditCardType : PaymentType |
|  | { |
|  | public CreditCardType() : base(1, "CreditCard") |
|  | { |
|  | } |
|  |  |
|  | public override string Code => "CC"; |
|  | } |
|  | } |

[view raw](https://gist.github.com/ankitvijay/bcc918e47fa82a3610aeef2e5df687fa/raw/901374688cfd0fb3ebe3f5ac21334398ef3bed21/PaymentType.cs)
[PaymentType.cs](https://gist.github.com/ankitvijay/bcc918e47fa82a3610aeef2e5df687fa#file-paymenttype-cs)
hosted with ❤ by [GitHub](https://github.com)

Unlike an Enum, **PaymentType**is a class with **static** **readonly**members. We would need a custom logic or converter to serialize it to JSON and deserialize it back.

### Version 1 – Using System.Text.Json

We can extend **System.Text.Json –>JsonConverter**of to serialize and deserialize an **Enumeration**class.

This file contains hidden or bidirectional Unicode text that may be interpreted or compiled differently than what appears below. To review, open the file in an editor that reveals hidden Unicode characters.
[Learn more about bidirectional Unicode characters](https://github.co/hiddenchars)

[Show hidden characters]({{ revealButtonHref }})

|  |  |
| --- | --- |
|  | // Import Nuget package System.Text.Json |
|  |  |
|  | public class EnumerationJsonConverter : JsonConverter<Enumeration> |
|  | { |
|  | private const string NameProperty = "Name"; |
|  |  |
|  | public override bool CanConvert(Type objectType) |
|  | { |
|  | return objectType.IsSubclassOf(typeof(Enumeration)); |
|  | } |
|  |  |
|  | public override Enumeration Read(ref Utf8JsonReader reader, Type typeToConvert, JsonSerializerOptions options) |
|  | { |
|  | switch (reader.TokenType) |
|  | { |
|  | case JsonTokenType.Number: |
|  | case JsonTokenType.String: |
|  | return GetEnumerationFromJson(reader.GetString(), typeToConvert); |
|  | case JsonTokenType.Null: |
|  | return null; |
|  | default: |
|  | throw new JsonException( |
|  | $"Unexpected token {reader.TokenType} when parsing the enumeration."); |
|  | } |
|  | } |
|  |  |
|  | public override void Write(Utf8JsonWriter writer, Enumeration value, JsonSerializerOptions options) |
|  | { |
|  | if (value is null) |
|  | { |
|  | writer.WriteNull(NameProperty); |
|  | } |
|  | else |
|  | { |
|  | var name = value.GetType().GetProperty(NameProperty, BindingFlags.Public | BindingFlags.Instance); |
|  | if (name == null) |
|  | { |
|  | throw new JsonException($"Error while writing JSON for {value}"); |
|  | } |
|  |  |
|  | writer.WriteStringValue(name.GetValue(value).ToString()); |
|  | } |
|  | } |
|  |  |
|  | private static Enumeration GetEnumerationFromJson(string nameOrValue, Type objectType) |
|  | { |
|  | try |
|  | { |
|  | object result = default; |
|  | var methodInfo = typeof(Enumeration).GetMethod( |
|  | nameof(Enumeration.TryGetFromValueOrName) |
|  | , BindingFlags.Static | BindingFlags.Public); |
|  |  |
|  | if (methodInfo == null) |
|  | { |
|  | throw new JsonException("Serialization is not supported"); |
|  | } |
|  |  |
|  | var genericMethod = methodInfo.MakeGenericMethod(objectType); |
|  |  |
|  | var arguments = new[] { nameOrValue, result }; |
|  |  |
|  | genericMethod.Invoke(null, arguments); |
|  | return arguments[1] as Enumeration; |
|  | } |
|  | catch (Exception ex) |
|  | { |
|  | throw new JsonException($"Error converting value '{nameOrValue}' to a enumeration.", ex); |
|  | } |
|  | } |
|  | } |

[view raw](https://gist.github.com/ankitvijay/365589a88a0442ae794a8a627e9023ec/raw/63540a843d9ad1dc83b1d030d9b9573836759163/JsonConverterVersion1.cs)
[JsonConverterVersion1.cs](https://gist.github.com/ankitvijay/365589a88a0442ae794a8a627e9023ec#file-jsonconverterversion1-cs)
hosted with ❤ by [GitHub](https://github.com)

### Version 2 – Using Newtonsoft.Json

Unfortunately, System.Text.Json has still not reached [feature parity](https://docs.microsoft.com/en-us/dotnet/standard/serialization/system-text-json-migrate-from-newtonsoft-how-to#table-of-differences-between-newtonsoftjson-and-systemtextjson) to **Newtonsoft.Json**. As a result, so often, we fall back to Newtonsoft.Json.

Here is the Newtonsoft.Json version of JsonConverter

This file contains hidden or bidirectional Unicode text that may be interpreted or compiled differently than what appears below. To review, open the file in an editor that reveals hidden Unicode characters.
[Learn more about bidirectional Unicode characters](https://github.co/hiddenchars)

[Show hidden characters]({{ revealButtonHref }})

|  |  |
| --- | --- |
|  | // Import Newtonsoft.Json |
|  |  |
|  | public class EnumerationJsonConverter : JsonConverter<Enumeration> |
|  | { |
|  | public override void WriteJson(JsonWriter writer, Enumeration value, JsonSerializer serializer) |
|  | { |
|  | if (value is null) |
|  | { |
|  | writer.WriteNull(); |
|  | } |
|  | else |
|  | { |
|  | writer.WriteValue(value.Name); |
|  | } |
|  | } |
|  |  |
|  | public override Enumeration ReadJson(JsonReader reader, |
|  | Type objectType, |
|  | Enumeration existingValue, |
|  | bool hasExistingValue, |
|  | JsonSerializer serializer) |
|  | { |
|  | return reader.TokenType switch |
|  | { |
|  | JsonToken.Integer => GetEnumerationFromJson(reader.Value.ToString(), objectType), |
|  | JsonToken.String => GetEnumerationFromJson(reader.Value.ToString(), objectType), |
|  | JsonToken.Null => null, |
|  |  |
|  | _ => throw new JsonSerializationException($"Unexpected token {reader.TokenType} when parsing an enumeration") |
|  | }; |
|  | } |
|  |  |
|  | private static Enumeration GetEnumerationFromJson(string nameOrValue, Type objectType) |
|  | { |
|  | try |
|  | { |
|  | object result = default; |
|  | var methodInfo = typeof(Enumeration).GetMethod( |
|  | nameof(Enumeration.TryGetFromValueOrName) |
|  | , BindingFlags.Static | BindingFlags.Public); |
|  |  |
|  | if (methodInfo == null) |
|  | { |
|  | throw new JsonSerializationException("Serialization is not supported"); |
|  | } |
|  |  |
|  | var genericMethod = methodInfo.MakeGenericMethod(objectType); |
|  |  |
|  | var arguments = new[] { nameOrValue, result }; |
|  |  |
|  | genericMethod.Invoke(null, arguments); |
|  | return arguments[1] as Enumeration; |
|  | } |
|  | catch (Exception ex) |
|  | { |
|  | throw new JsonSerializationException($"Error converting value '{nameOrValue}' to a enumeration.", ex); |
|  | } |
|  | } |
|  | } |

[view raw](https://gist.github.com/ankitvijay/1c909d72046e0dcc8b08f76a85cae2b0/raw/c321c0980c0a0a10e1ca0aacb8c524fea948feb5/JsonConverterVersion2.cs)
[JsonConverterVersion2.cs](https://gist.github.com/ankitvijay/1c909d72046e0dcc8b08f76a85cae2b0#file-jsonconverterversion2-cs)
hosted with ❤ by [GitHub](https://github.com)

### Usage

Let us consider a class **Transaction** with property **PaymentType**.

This file contains hidden or bidirectional Unicode text that may be interpreted or compiled differently than what appears below. To review, open the file in an editor that reveals hidden Unicode characters.
[Learn more about bidirectional Unicode characters](https://github.co/hiddenchars)

[Show hidden characters]({{ revealButtonHref }})

|  |  |
| --- | --- |
|  | public class Transaction |
|  | { |
|  | public double Amount { get; set; } |
|  |  |
|  | public PaymentType PaymentType { get; set; } |
|  | } |

[view raw](https://gist.github.com/ankitvijay/20939b9369101c259ca923cf8ec3fd3b/raw/f6dc999a2d9b431c08114b73f1d57591b6555c93/Transaction.cs)
[Transaction.cs](https://gist.github.com/ankitvijay/20939b9369101c259ca923cf8ec3fd3b#file-transaction-cs)
hosted with ❤ by [GitHub](https://github.com)

We can serialize and serialize the **Transaction**class using **EnumerationJsonConverter,**as shown in the below test:

This file contains hidden or bidirectional Unicode text that may be interpreted or compiled differently than what appears below. To review, open the file in an editor that reveals hidden Unicode characters.
[Learn more about bidirectional Unicode characters](https://github.co/hiddenchars)

[Show hidden characters]({{ revealButtonHref }})

|  |  |
| --- | --- |
|  | // Import System.Text.Json; |
|  |  |
|  | public class EnumerationJsonConverterTests |
|  | { |
|  | private readonly ITestOutputHelper _testOutputHelper; |
|  |  |
|  | public EnumerationJsonConverterTests(ITestOutputHelper testOutputHelper) |
|  | { |
|  | _testOutputHelper = testOutputHelper; |
|  | } |
|  |  |
|  | [Fact] |
|  | public void EnumerationIsSerializesAndDeserializesCorrectly() |
|  | { |
|  | var expected = new Transaction |
|  | { |
|  | Amount = 100, |
|  | PaymentType = PaymentType.CreditCard |
|  | }; |
|  |  |
|  | var json = JsonSerializer.Serialize(expected, |
|  | new JsonSerializerOptions |
|  | { |
|  | Converters = |
|  | { |
|  | new EnumerationJsonConverter() |
|  | } |
|  | }); |
|  |  |
|  | _testOutputHelper.WriteLine(json); |
|  |  |
|  | var actual= JsonSerializer.Deserialize<Transaction>(json, new JsonSerializerOptions() |
|  | { |
|  | Converters = { new EnumerationJsonConverter() } |
|  | }); |
|  |  |
|  | Assert.Equal(expected.Amount, actual.Amount); |
|  | Assert.Equal(expected.PaymentType, actual.PaymentType); |
|  | } |
|  | } |

[view raw](https://gist.github.com/ankitvijay/e7461410d1f50771beaf2184da7dc374/raw/071e989d3b8a719e5c34742871b172e4d87b9113/EnumerationJsonConverterTests.cs)
[EnumerationJsonConverterTests.cs](https://gist.github.com/ankitvijay/e7461410d1f50771beaf2184da7dc374#file-enumerationjsonconvertertests-cs)
hosted with ❤ by [GitHub](https://github.com)

Here is the JSON output:

This file contains hidden or bidirectional Unicode text that may be interpreted or compiled differently than what appears below. To review, open the file in an editor that reveals hidden Unicode characters.
[Learn more about bidirectional Unicode characters](https://github.co/hiddenchars)

[Show hidden characters]({{ revealButtonHref }})

|  |  |
| --- | --- |
|  | { |
|  | "Amount":100, |
|  | "PaymentType":"CreditCard" |
|  | } |

[view raw](https://gist.github.com/ankitvijay/8d10147083c9d144902e6a438d43ef83/raw/8d7ec27c0d92e6f4daa022d6f08031a588211dc8/output.json)
[output.json](https://gist.github.com/ankitvijay/8d10147083c9d144902e6a438d43ef83#file-output-json)
hosted with ❤ by [GitHub](https://github.com)

I hope you enjoyed this post and learning about how you can create a custom JSON converter to serialize an Enumeration class.
