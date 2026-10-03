---
title: "Updating Cosmos DB document schema"
date: "2021-07-18T09:44:35+10:00"
lastmod: "2022-12-23T23:04:46+10:00"
url: "/2021/07/18/update-schema-cosmos-db/"
slug: "update-schema-cosmos-db"
wp_id: 257398
category: ["architecture-and-design", "cosmos-db", "cosmos-sdk-v3", "net-core", "nosql", "raven"]
tag: ["azure", "cosmos-db", "migration", "net", "nosql", "raven", "schema"]
summary: "This post explains the pain-points of updating schema in NoSQL and how you can update Cosmos DB schema using custom JSON serializer."
featured_image: "https://ankitvijaydotin.wordpress.com/wp-content/uploads/2022/12/ab732-updateschema-2.jpg"
---

## NoSQL vs SQL schema

NoSQL gives us the flexibility of dynamic schema. Hence, we often call it schemaless. SQL, on the other hand, has a rigid data model with a pre-defined schema. The tooling around SQL is quite mature. In the .NET world, there are hundreds of options to migrate schema, such as [Entity Framework](https://docs.microsoft.com/en-us/ef/core/managing-schemas/migrations/?tabs=dotnet-core-cli), [DbUp](https://dbup.github.io/), [fluentmigrator](https://github.com/fluentmigrator/fluentmigrator), and the list goes on.

## Schemaless or schema pain?

NoSQL databases such as Cosmos DB are fun to work with during development when we do not have any workload in production. The schema is usually exposed as a POCO, and we can simply add or delete a property to update the data model.

However, once we move to production, updating schema can become a pain. The flexibility of dynamic schema starts biting us back hard. And we realize that maybe NoSQL is not as flexible as we thought.

## Backward compatibility with NoSQL

When working with RavenDB or Cosmos DB, we often end up with **Obsolete** properties that we cannot remove since old documents may still have those properties. The problem gets worse as the application matures. We need to deal with additional complexity and null properties throughout the application. Here is an example of how an entity may look like just after a few schema changes.

This file contains hidden or bidirectional Unicode text that may be interpreted or compiled differently than what appears below. To review, open the file in an editor that reveals hidden Unicode characters.
[Learn more about bidirectional Unicode characters](https://github.co/hiddenchars)

[Show hidden characters]({{ revealButtonHref }})

|  |  |
| --- | --- |
|  | public class Order |
|  | { |
|  | [JsonProperty("id")] |
|  | public string Id { get; set; } |
|  |  |
|  | [Obsolete("Order name is obsolete, use Name instead")] |
|  | public string OrderName { get; set; } |
|  |  |
|  | [Obsolete("HasShipped is obsolete, set OrderStatus as Shipped Instead")] |
|  | public bool HasShipped { get; set; } |
|  |  |
|  | public string Name { get; set; } |
|  |  |
|  | public OrderStatus Status { get; set; } |
|  | } |
|  |  |
|  | public enum OrderStatus |
|  | { |
|  | Started, |
|  | Processed, |
|  | Shipped, |
|  | Completed |
|  | } |

[view raw](https://gist.github.com/ankitvijay/9f0ca084a22b58e6c2b4514b71e180c8/raw/9046e77c75cabf4916322b4f05cf0f9b4484d520/Order.cs)
[Order.cs](https://gist.github.com/ankitvijay/9f0ca084a22b58e6c2b4514b71e180c8#file-order-cs)
hosted with ❤ by [GitHub](https://github.com)

We need to deal with these obsolete properties throughout the code, and code becomes messy and hard to maintain.

Raven DB gives us the ability to update to schema through [events](https://ravendb.net/docs/article-page/4.2/migration/client-api/session/how-to/subscribe-to-events#onafterconversiontodocument). Unfortunately, we do not have such an option with Cosmos DB SDK. Let us take the above example to see how the **Order**document could evolve over a period in a real-world application.

This file contains hidden or bidirectional Unicode text that may be interpreted or compiled differently than what appears below. To review, open the file in an editor that reveals hidden Unicode characters.
[Learn more about bidirectional Unicode characters](https://github.co/hiddenchars)

[Show hidden characters]({{ revealButtonHref }})

|  |  |
| --- | --- |
|  | public class OrderV1 |
|  | { |
|  | [JsonProperty("id")] |
|  | public string Id { get; set; } |
|  |  |
|  | public string OrderName { get; set; } |
|  |  |
|  | public bool HasShipped { get; set; } |
|  | } |

[view raw](https://gist.github.com/ankitvijay/c7e516463650dac527880801ffeef794/raw/3361186508c23a36a16ffc01be2c04da8b492bf3/OrderV1.cs)
[OrderV1.cs](https://gist.github.com/ankitvijay/c7e516463650dac527880801ffeef794#file-orderv1-cs)
hosted with ❤ by [GitHub](https://github.com)

This file contains hidden or bidirectional Unicode text that may be interpreted or compiled differently than what appears below. To review, open the file in an editor that reveals hidden Unicode characters.
[Learn more about bidirectional Unicode characters](https://github.co/hiddenchars)

[Show hidden characters]({{ revealButtonHref }})

|  |  |
| --- | --- |
|  | public class OrderV2 |
|  | { |
|  | [JsonProperty("id")] |
|  | public string Id { get; set; } |
|  |  |
|  | // OrderName renamed to Name |
|  | public string Name { get; set; } |
|  |  |
|  | public bool HasShipped { get; set; } |
|  | } |

[view raw](https://gist.github.com/ankitvijay/c7e516463650dac527880801ffeef794/raw/3361186508c23a36a16ffc01be2c04da8b492bf3/OrderV2.cs)
[OrderV2.cs](https://gist.github.com/ankitvijay/c7e516463650dac527880801ffeef794#file-orderv2-cs)
hosted with ❤ by [GitHub](https://github.com)

This file contains hidden or bidirectional Unicode text that may be interpreted or compiled differently than what appears below. To review, open the file in an editor that reveals hidden Unicode characters.
[Learn more about bidirectional Unicode characters](https://github.co/hiddenchars)

[Show hidden characters]({{ revealButtonHref }})

|  |  |
| --- | --- |
|  | public class OrderV3 |
|  | { |
|  | [JsonProperty("id")] |
|  | public string Id { get; set; } |
|  |  |
|  | public string Name { get; set; } |
|  |  |
|  | // Introduced OrderStatus instead of HasShipped |
|  | public OrderStatus OrderStatus { get; set; } |
|  | } |
|  |  |
|  | public enum OrderStatus |
|  | { |
|  | Started, |
|  | Processed, |
|  | Shipped, |
|  | Completed |
|  | } |

[view raw](https://gist.github.com/ankitvijay/c7e516463650dac527880801ffeef794/raw/3361186508c23a36a16ffc01be2c04da8b492bf3/OrderV3.cs)
[OrderV3.cs](https://gist.github.com/ankitvijay/c7e516463650dac527880801ffeef794#file-orderv3-cs)
hosted with ❤ by [GitHub](https://github.com)

## Updating Cosmos Schema to the latest Version

Ideally, we would only like to deal with **OrderV3**in the entire code base without worrying about the documents stored in the older schema version.

We can achieve this by manipulating the raw JSON before reading it from Cosmos DB. [Cosmos DB trigger](https://docs.microsoft.com/en-us/azure/cosmos-db/how-to-use-stored-procedures-triggers-udfs#pre-triggers) is one way to accomplish this. However, triggers and stored procedures only support javascript at the time of writing. Moving the business logic outside of .NET or C# may not be the first choice for many teams.

## Custom JSON Serializer to Update Cosmos schema

[In my previous post](https://ankitvijaydotin.wordpress.com/2021/06/20/custom-json-serializer-settings-with-cosmos-db-sdk/), I talked about creating a custom JSON serializer with Cosmos DB SDK. We can use the same approach to update documents with the old schema version before it is loaded through Cosmos DB SDK.

We start by introducing a property called schema version in Cosmos Document. The schema version is an integer property that we increment for each schema change.

This file contains hidden or bidirectional Unicode text that may be interpreted or compiled differently than what appears below. To review, open the file in an editor that reveals hidden Unicode characters.
[Learn more about bidirectional Unicode characters](https://github.co/hiddenchars)

[Show hidden characters]({{ revealButtonHref }})

|  |  |
| --- | --- |
|  | public class Order |
|  | { |
|  | [JsonProperty("id")] |
|  | public string Id { get; set; } |
|  |  |
|  | public string Name { get; set; } |
|  |  |
|  | public OrderStatus OrderStatus { get; set; } |
|  |  |
|  | public int SchemaVersion {get; set;} |
|  | } |
|  |  |
|  | public enum OrderStatus |
|  | { |
|  | Started, |
|  | Processed, |
|  | Shipped, |
|  | Completed |
|  | } |

[view raw](https://gist.github.com/ankitvijay/348b1117ef165582d5e596ee24f2b50a/raw/f66c8e4afe6eaecfd2e9b5bc179576ec8b51209d/Order.cs)
[Order.cs](https://gist.github.com/ankitvijay/348b1117ef165582d5e596ee24f2b50a#file-order-cs)
hosted with ❤ by [GitHub](https://github.com)

Next, we update [**CosmosJsonDotNetSerializer**](https://gist.github.com/ankitvijay/f0f243ec2477f87d96cd6faf4864da2c#file-cosmosjsondotnetserializer-cs) from [the previous pos](https://ankitvijaydotin.wordpress.com/2021/06/20/custom-json-serializer-settings-with-cosmos-db-sdk/)t by manipulating raw JSON of older documents to the latest schema version.

This file contains hidden or bidirectional Unicode text that may be interpreted or compiled differently than what appears below. To review, open the file in an editor that reveals hidden Unicode characters.
[Learn more about bidirectional Unicode characters](https://github.co/hiddenchars)

[Show hidden characters]({{ revealButtonHref }})

|  |  |
| --- | --- |
|  | // Code removed for bravity |
|  | public sealed class CosmosJsonDotNetSerializer : CosmosSerializer |
|  | { |
|  | // Code removed for bravity |
|  |  |
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
|  | return UpdateSchemaVersionToCurrent<T>(jsonSerializer.Deserialize<JObject>(jsonTextReader)); |
|  | } |
|  | } |
|  | } |
|  | } |
|  |  |
|  | private T UpdateSchemaVersionToCurrent<T>(JObject jObject) |
|  | { |
|  | const int currentSchemaVersion = 3; |
|  | var schemaVersion = jObject["SchemaVersion"].Value<int>(); |
|  |  |
|  | for (var i = schemaVersion; i < currentSchemaVersion; i++) |
|  | { |
|  | switch (i) |
|  | { |
|  | case 1: |
|  | jObject["Name"] = jObject["OrderName"]; |
|  | jObject["OrderName"] = null; |
|  | break; |
|  |  |
|  | case 2: |
|  | var hasShipped = jObject["HasShipped"].Value<bool>(); |
|  | if (hasShipped) |
|  | { |
|  | jObject["OrderStatus"] = (int)OrderStatus.Shipped; |
|  | } |
|  | else |
|  | { |
|  | jObject["OrderStatus"] = (int)OrderStatus.Processed; |
|  | } |
|  | break; |
|  | } |
|  | } |
|  |  |
|  | jObject["SchemaVersion"] = currentSchemaVersion; |
|  | return jObject.ToObject<T>(); |
|  | } |
|  |  |
|  | // Code removed for bravity |
|  | } |

[view raw](https://gist.github.com/ankitvijay/11aadc546c9de4e4ea8de907940a9e59/raw/981d9cdb1403cf860f05fee2c809e3234710a292/CosmosJsonDotNetSerializer.cs)
[CosmosJsonDotNetSerializer.cs](https://gist.github.com/ankitvijay/11aadc546c9de4e4ea8de907940a9e59#file-cosmosjsondotnetserializer-cs)
hosted with ❤ by [GitHub](https://github.com)

As you can see in the above code, we call the **UpdateSchemaVersionToCurrent**method before deserializing the stream returned from Cosmos. In this method, we update the JSON Object of the document to the latest schema version.

This way, we always deal with the latest Order entity throughout the code, and when we save the entity back to Cosmos, it is persisted with the latest schema version.

## We can take it further

We can run the schema migration as a separate process, for example, in an Azure function where we load a document of an older schema version, convert it to the latest version and save it back to the Cosmos.

This process can be equivalent to migration scripts that we run for SQL schema.

## **Wrapping Up**

Dealing with the older schema versions is not so trivial with NoSQL databases. However, I hope this post gives you some insights into how you can achieve this with Cosmos.

> Photo by [Markus Winkler](https://unsplash.com/@markuswinkler?utm_source=unsplash&utm_medium=referral&utm_content=creditCopyText) on [Unsplash](https://unsplash.com/s/photos/update?utm_source=unsplash&utm_medium=referral&utm_content=creditCopyText)
