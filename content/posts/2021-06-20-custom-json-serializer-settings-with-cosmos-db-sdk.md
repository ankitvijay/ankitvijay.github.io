---
title: "Custom JSON serialization with Azure Cosmos DB SDK"
date: "2021-06-20T09:14:10+10:00"
lastmod: "2021-06-21T07:19:09+10:00"
url: "/2021/06/20/custom-json-serializer-settings-with-cosmos-db-sdk/"
slug: "custom-json-serializer-settings-with-cosmos-db-sdk"
wp_id: 252467
category: ["architecture-and-design", "cosmos-db", "cosmos-sdk-v3", "json-serialization", "net-5"]
tag: ["azure", "cosmos-db", "cosmos-db-sdk-3", "json-serialization", "net", "newtonsoft", "system-text-json"]
summary: "This post explains how you can use custom JSON serializer settings with Cosmos DB using Newtonsoft JSON and System.Text.Json."
featured_image: "https://ankitvijaydotin.wordpress.com/wp-content/uploads/2022/12/261b2-twitter2.jpg"
---

## Background

Azure Cosmos DB SDK 3+ for SQL API replaced [Azure DocumentDB SDK](https://www.nuget.org/packages/Microsoft.Azure.DocumentDB/) a couple of years back. DocumentDB used Newtonsoft Json.NET for its serialization. However, with the growth of .NET Core and the introduction of shiny new System.Text.Json, the team wanted to reduce exposure to Newtonsoft. So the idea was in future, with CosmosDB SDK 4, System.Text.Json would replace Json.NET.

The unfortunate side-effect of this was that we do not have an easy way to supply custom JSON serializer settings. The SDK allows us to update a limited set of JSON settings such as `IgnoreNullValues`, `Intend` and `PropertyNamePolicy` through [CosmosSerializationOptions](https://github.com/Azure/azure-cosmos-dotnet-v3/blob/master/Microsoft.Azure.Cosmos/src/Serializer/CosmosSerializationOptions.cs). However, in the real world scenario, this is not always enough.

The [CosmosSerializer](https://github.com/Azure/azure-cosmos-dotnet-v3/blob/master/Microsoft.Azure.Cosmos/src/Serializer/CosmosSerializer.cs) class from the SDK is `abstract`and all its implementation, such as `CosmosJsonDotNetSerializer`, are `internal` `sealed`. I also raised [an issue](https://github.com/Azure/azure-cosmos-dotnet-v3/issues/1813) with the developer team to fix this limitation.

## CUSTOM JSON Serializer for Cosmos

Fix for this issue is easy, albeit ugly. We can create our own `CosmosJsonDotNetSerializer` inspired from Cosmos DB SDK as below:

This file contains hidden or bidirectional Unicode text that may be interpreted or compiled differently than what appears below. To review, open the file in an editor that reveals hidden Unicode characters.
[Learn more about bidirectional Unicode characters](https://github.co/hiddenchars)

[Show hidden characters]({{ revealButtonHref }})

|  |  |
| --- | --- |
|  | using System; |
|  | using System.IO; |
|  | using System.Text; |
|  | using Microsoft.Azure.Cosmos; |
|  | using Newtonsoft.Json; |
|  |  |
|  | /// <summary> |
|  | /// Azure Cosmos DB does not expose a default implementation of CosmosSerializer that is required to set the custom JSON serializer settings. |
|  | /// To fix this, we have to create our own implementation inspired internal implementation from SDK library. |
|  | /// <remarks> |
|  | /// See: <https://github.com/Azure/azure-cosmos-dotnet-v3/blob/master/Microsoft.Azure.Cosmos/src/Serializer/CosmosJsonDotNetSerializer.cs> |
|  | /// </remarks> |
|  | /// </summary> |
|  | public sealed class CosmosJsonDotNetSerializer : CosmosSerializer |
|  | { |
|  | private static readonly Encoding DefaultEncoding = new UTF8Encoding(false, true); |
|  | private readonly JsonSerializerSettings _serializerSettings; |
|  |  |
|  | /// <summary> |
|  | /// Create a serializer that uses the JSON.net serializer |
|  | /// </summary> |
|  | public CosmosJsonDotNetSerializer(JsonSerializerSettings jsonSerializerSettings) |
|  | { |
|  | _serializerSettings = jsonSerializerSettings ?? |
|  | throw new ArgumentNullException(nameof(jsonSerializerSettings)); |
|  | } |
|  |  |
|  | /// <summary> |
|  | /// Convert a Stream to the passed in type. |
|  | /// </summary> |
|  | /// <typeparam name="T">The type of object that should be deserialized</typeparam> |
|  | /// <param name="stream">An open stream that is readable that contains JSON</param> |
|  | /// <returns>The object representing the deserialized stream</returns> |
|  | public override T FromStream<T>(Stream stream) |
|  | { |
|  | using (stream) |
|  | { |
|  | if (typeof(Stream).IsAssignableFrom(typeof(T))) |
|  | { |
|  | return (T)(object)stream; |
|  | } |
|  |  |
|  | using (var sr = new StreamReader(stream)) |
|  | { |
|  | using (var jsonTextReader = new JsonTextReader(sr)) |
|  | { |
|  | var jsonSerializer = GetSerializer(); |
|  | return jsonSerializer.Deserialize<T>(jsonTextReader); |
|  | } |
|  | } |
|  | } |
|  | } |
|  |  |
|  | /// <summary> |
|  | /// Converts an object to a open readable stream |
|  | /// </summary> |
|  | /// <typeparam name="T">The type of object being serialized</typeparam> |
|  | /// <param name="input">The object to be serialized</param> |
|  | /// <returns>An open readable stream containing the JSON of the serialized object</returns> |
|  | public override Stream ToStream<T>(T input) |
|  | { |
|  | var streamPayload = new MemoryStream(); |
|  | using (var streamWriter = new StreamWriter(streamPayload, encoding: DefaultEncoding, bufferSize: 1024, leaveOpen: true)) |
|  | { |
|  | using (JsonWriter writer = new JsonTextWriter(streamWriter)) |
|  | { |
|  | writer.Formatting = Formatting.None; |
|  | var jsonSerializer = GetSerializer(); |
|  | jsonSerializer.Serialize(writer, input); |
|  | writer.Flush(); |
|  | streamWriter.Flush(); |
|  | } |
|  | } |
|  |  |
|  | streamPayload.Position = 0; |
|  | return streamPayload; |
|  | } |
|  |  |
|  | /// <summary> |
|  | /// JsonSerializer has hit a race conditions with custom settings that cause null reference exception. |
|  | /// To avoid the race condition a new JsonSerializer is created for each call |
|  | /// </summary> |
|  | private JsonSerializer GetSerializer() |
|  | { |
|  | return JsonSerializer.Create(_serializerSettings); |
|  | } |
|  | } |

[view raw](https://gist.github.com/ankitvijay/f0f243ec2477f87d96cd6faf4864da2c/raw/ef50ada3546b59d69c058966b1ae84f25bef2c6f/CosmosJsonDotNetSerializer.cs)
[CosmosJsonDotNetSerializer.cs](https://gist.github.com/ankitvijay/f0f243ec2477f87d96cd6faf4864da2c#file-cosmosjsondotnetserializer-cs)
hosted with ❤ by [GitHub](https://github.com)

As you can see in the above code `CosmosJsonDotNetSerializer` takes `JsonSerializerSettings` as a parameter in its Constructor.

This would allow us to create `CosmosClient` using `CosmosJsonDotNetSerializer` and pass our own `JsonSerializerSettings` as shown in the code snippet below:

This file contains hidden or bidirectional Unicode text that may be interpreted or compiled differently than what appears below. To review, open the file in an editor that reveals hidden Unicode characters.
[Learn more about bidirectional Unicode characters](https://github.co/hiddenchars)

[Show hidden characters]({{ revealButtonHref }})

|  |  |
| --- | --- |
|  | var cosmosClient = new CosmosClient("<cosmosDBConnectionString>", |
|  | new CosmosClientOptions |
|  | { |
|  | Serializer = new CosmosJsonDotNetSerializer(new JsonSerializerSettings |
|  | { |
|  | // Update your JSON Serializer Settings here. |
|  | TypeNameHandling = TypeNameHandling.Auto, |
|  | ReferenceLoopHandling = ReferenceLoopHandling.Error, |
|  | PreserveReferencesHandling = PreserveReferencesHandling.None, |
|  | ConstructorHandling = ConstructorHandling.AllowNonPublicDefaultConstructor |
|  | Converters = new JsonConverter[] |
|  | { |
|  | new StringEnumConverter() |
|  | } |
|  | }) |
|  | }); |

[view raw](https://gist.github.com/ankitvijay/a2abe13f411862443b95604bd90a37e0/raw/90380777e60e5bee9d207fda0d4ce666525ff997/CosmosClient.cs)
[CosmosClient.cs](https://gist.github.com/ankitvijay/a2abe13f411862443b95604bd90a37e0#file-cosmosclient-cs)
hosted with ❤ by [GitHub](https://github.com)

## BUT WAIT… THERE IS MORE

I raised a question to the Cosmos DB team sometime back if there is a way to use replace Json.NET with System.Text.Json. [Mark Brown](https://twitter.com/markjbrown), from the Cosmos DB team, responded that we can easily do that by extending `CosmosSerializer` like we did above.

<blockquote class="twitter-tweet" data-dnt="true" data-width="500"><p dir="ltr" lang="en"><a href="https://twitter.com/AzureCosmosDB?ref_src=twsrc%5Etfw">@AzureCosmosDB</a> trying to System.Text.Json instead of Newtonsoft with <a href="https://t.co/TkeBJwYYES">https://t.co/TkeBJwYYES</a>.Cosmos SDK v3+<br/>But it doesn't seem to support it. Am I missing something?</p>— Ankit Vijay (@vijayankit) <a href="https://twitter.com/vijayankit/status/1379556816862908420?ref_src=twsrc%5Etfw">April 6, 2021</a></blockquote>

Here is the System.Text.Json implementation of CosmosSerializer. The implementation is inspired by [Azure Cosmos Samples](https://github.com/Azure/azure-cosmos-dotnet-v3/blob/master/Microsoft.Azure.Cosmos.Samples/Usage/SystemTextJson/CosmosSystemTextJsonSerializer.cs).

This file contains hidden or bidirectional Unicode text that may be interpreted or compiled differently than what appears below. To review, open the file in an editor that reveals hidden Unicode characters.
[Learn more about bidirectional Unicode characters](https://github.co/hiddenchars)

[Show hidden characters]({{ revealButtonHref }})

|  |  |
| --- | --- |
|  | using System.IO; |
|  | using System.Text.Json; |
|  | using Azure.Core.Serialization; |
|  | using Microsoft.Azure.Cosmos; |
|  |  |
|  | /// <remarks> |
|  | // See: <https://github.com/Azure/azure-cosmos-dotnet-v3/blob/master/Microsoft.Azure.Cosmos.Samples/Usage/SystemTextJson/CosmosSystemTextJsonSerializer.cs> |
|  | /// </remarks> |
|  | public sealed class CosmosSystemTextJsonSerializer : CosmosSerializer |
|  | { |
|  | private readonly JsonObjectSerializer _systemTextJsonSerializer; |
|  |  |
|  | public CosmosSystemTextJsonSerializer(JsonSerializerOptions jsonSerializerOptions) |
|  | { |
|  | _systemTextJsonSerializer = new JsonObjectSerializer(jsonSerializerOptions); |
|  | } |
|  |  |
|  | public override T FromStream<T>(Stream stream) |
|  | { |
|  | if (stream.CanSeek && stream.Length == 0) |
|  | { |
|  | return default; |
|  | } |
|  |  |
|  | if (typeof(Stream).IsAssignableFrom(typeof(T))) |
|  | { |
|  | return (T) (object) stream; |
|  | } |
|  |  |
|  | using (stream) |
|  | { |
|  | return (T) _systemTextJsonSerializer.Deserialize(stream, typeof(T), default); |
|  | } |
|  | } |
|  |  |
|  | public override Stream ToStream<T>(T input) |
|  | { |
|  | var streamPayload = new MemoryStream(); |
|  | _systemTextJsonSerializer.Serialize(streamPayload, input, typeof(T), default); |
|  | streamPayload.Position = 0; |
|  | return streamPayload; |
|  | } |
|  | } |

[view raw](https://gist.github.com/ankitvijay/3946e9c807dd21306b19a9c42b85821e/raw/478faa6924204b4a275017e3be92a2cd7633e5e6/CosmosSystemTextJsonSerializer.cs)
[CosmosSystemTextJsonSerializer.cs](https://gist.github.com/ankitvijay/3946e9c807dd21306b19a9c42b85821e#file-cosmossystemtextjsonserializer-cs)
hosted with ❤ by [GitHub](https://github.com)

We can now use the serializer to create `CosmosClient` as below

This file contains hidden or bidirectional Unicode text that may be interpreted or compiled differently than what appears below. To review, open the file in an editor that reveals hidden Unicode characters.
[Learn more about bidirectional Unicode characters](https://github.co/hiddenchars)

[Show hidden characters]({{ revealButtonHref }})

|  |  |
| --- | --- |
|  | var cosmosClient = new CosmosClient("<cosmosDBConnectionString>", |
|  | new CosmosClientOptions |
|  | { |
|  | Serializer = new CosmosSystemTextJsonSerializer(new JsonSerializerOptions |
|  | { |
|  | // Update your JSON Serializer options here. |
|  | PropertyNamingPolicy = JsonNamingPolicy.CamelCase, |
|  | Converters = |
|  | { |
|  | new JsonStringEnumConverter() |
|  | }, |
|  | IgnoreNullValues = true, |
|  | IgnoreReadOnlyFields = true |
|  | }) |
|  | }); |

[view raw](https://gist.github.com/ankitvijay/b721a4207ab0a42e1f1a826612cd566a/raw/5605b1ff31189b7f2b01fc15829d62cfa15e668d/CosmosClient.cs)
[CosmosClient.cs](https://gist.github.com/ankitvijay/b721a4207ab0a42e1f1a826612cd566a#file-cosmosclient-cs)
hosted with ❤ by [GitHub](https://github.com)

## Wrapping Up

This post explains a workaround to create custom serializer settings using Json.NET and System.Text.Json when working with Cosmos DB. Hopefully, this workaround is short-lived and with the release of v4 we get this option out of the box.

> Feature Photo by [Greg Rakozy](https://unsplash.com/@grakozy?utm_source=unsplash&utm_medium=referral&utm_content=creditCopyText) on [Unsplash](https://unsplash.com/s/photos/cosmos?utm_source=unsplash&utm_medium=referral&utm_content=creditCopyText)
