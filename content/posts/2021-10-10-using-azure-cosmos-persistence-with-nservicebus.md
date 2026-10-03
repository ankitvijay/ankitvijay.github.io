---
title: "Using Azure Cosmos persistence with NServiceBus"
date: "2021-10-10T11:02:30+10:00"
lastmod: "2022-12-23T23:04:47+10:00"
url: "/2021/10/10/using-azure-cosmos-persistence-with-nservicebus/"
slug: "using-azure-cosmos-persistence-with-nservicebus"
wp_id: 257499
category: ["architecture-and-design", "cosmos-db", "event-driven-architecture", "microservices", "net-6"]
tag: ["c", "cosmos-db", "net", "net-6", "nservicebus", "servicebus"]
summary: "This post explains how you can use NServiceBus and Azure Cosmos DB persistence together for scalability and reliability."
---

## Introduction

NServiceBus has been a [well-known](https://particular.net/nservicebus) messaging and workflow solution for the .NET platform for over a decade. It offers reliability, maintainability, and scalability for distributed workflows. NServiceBus supports various queuing technology, aka transport, such as MSMQ, Azure Service Bus, Rabbit MQ, Amazon SQS, etc. In addition to this, it has support for datastore or persistence such as SQL, Cosmos DB, MongoDB, Raven DB, etc.

[Cosmos DB](https://azure.microsoft.com/en-au/services/cosmos-db/), on the other hand, is a fully managed No SQL database service on Azure. Cosmos DB is robust, and it is growing at a rapid pace. So much so that my 2-year old [post](https://ankitvijaydotin.wordpress.com/2019/11/13/azure-sql-to-cosmos-db/) on Cosmos DB has a lot of outdated information, and it needs a complete refresh.

This post will discuss how you can use these two world-class products to build your distributed system.

## Source Code

You can download the sample application that I will work on within this post from my [GitHub repository](https://github.com/ankitvijay/NServiceBus.CosmosOutbox.Samples).

The post assumes that you have a basic understanding of distributed systems, NServiceBus, and Cosmos DB. To run the solution on your local machine, you would need the following:

- [.NET 6](https://dotnet.microsoft.com/download/dotnet/6.0)
- [Azure Cosmos DB Emulator](https://docs.microsoft.com/en-us/azure/cosmos-db/local-emulator?tabs=ssl-netstd21)
- [NServiceBus Free Community License](https://particular.net/pricing)

## Architecture

As part of this exercise, we will build a new social platform called `Twitbook`(naming is hard). `Twitbook` is still in beta and only offers two features:

- It allows the author to create a new post
- People can comment on the post

We will offer these two features through API and save the data to Cosmos DB asynchronously using a background worker. We will also use the NServiceBus to make our distributed system reliable and scalable.

Here is the architecture.

![Twitbook architecture](https://ankitvijaydotin.wordpress.com/wp-content/uploads/2022/12/7ebfc-architecture-diagram.png)

*Twitbook Architecture*

## The solution structure

Our solution consists of the following three projects:

- **Api**: Api project receives a request from the client and sends the message to the service bus using NServiceBus. For simplicity and demo, we are using [NService Learning transport](https://docs.particular.net/transports/learning/) instead of real service bus. In the real world, we would use transport such as [Azure Service Bus](https://docs.particular.net/transports/azure-service-bus/).
- **Messages**: This project contains the commands and events that we will send or publish using NServiceBus.
- **Worker**: The worker receives a message from service bus, saves it to Cosmos and publishes the event when save is successful. The published event can be subscribed by different services downstream and use for purposes such as updating state of an external system, reporting, and so on.

![](https://ankitvijaydotin.wordpress.com/wp-content/uploads/2022/12/c0196-image.png)

*The solution structure*

## Building the sample

### Api Project – Setting up NServiceBus and Swagger

Let us start with creating the Web API. We will first add NServiceBus using `NServiceBus.Extensions.Hosting` nuget package.

This file contains hidden or bidirectional Unicode text that may be interpreted or compiled differently than what appears below. To review, open the file in an editor that reveals hidden Unicode characters.
[Learn more about bidirectional Unicode characters](https://github.co/hiddenchars)

[Show hidden characters]({{ revealButtonHref }})

|  |  |
| --- | --- |
|  | var builder = WebApplication.CreateBuilder(args); |
|  | builder.Host.UseNServiceBus(_ => |
|  | { |
|  | var endpointConfiguration = new EndpointConfiguration("Samples.Api"); |
|  | var transport = endpointConfiguration.UseTransport<LearningTransport>(); |
|  | var routing = transport.Routing(); |
|  | routing.RouteToEndpoint(Assembly.Load("Messages"), "Samples.Worker"); |
|  | endpointConfiguration.SendOnly(); |
|  | return endpointConfiguration; |
|  | }); |

[view raw](https://gist.github.com/ankitvijay/1fc69699146165517a7773f125d06504/raw/9861965a43c1df7d2f98a7d70dab3dbc3060471f/Program.cs)
[Program.cs](https://gist.github.com/ankitvijay/1fc69699146165517a7773f125d06504#file-program-cs)
hosted with ❤ by [GitHub](https://github.com)

API – Use NServiceBus

For API discovery, we will use Swagger.

This file contains hidden or bidirectional Unicode text that may be interpreted or compiled differently than what appears below. To review, open the file in an editor that reveals hidden Unicode characters.
[Learn more about bidirectional Unicode characters](https://github.co/hiddenchars)

[Show hidden characters]({{ revealButtonHref }})

|  |  |
| --- | --- |
|  | builder.Services.AddEndpointsApiExplorer(); |
|  | builder.Services.AddSwaggerGen(options => |
|  | { |
|  | options.SwaggerDoc("v1", new OpenApiInfo { Title = "Posts Api", Version = "v1" }); |
|  | }); |
|  |  |
|  | var app = builder.Build(); |
|  | . |
|  | . |
|  | app.UseHttpsRedirection() |
|  | .UseStaticFiles() |
|  | .UseSwagger() |
|  | .UseSwaggerUI(options => { options.SwaggerEndpoint("v1/swagger.json", "Posts Api"); }) |
|  | .UseRouting(); |

[view raw](https://gist.github.com/ankitvijay/a96065d32a15b1374d70d094fc6b2d84/raw/42f95d4ac603d872cbb07f508410214d6a0b6942/Program.cs)
[Program.cs](https://gist.github.com/ankitvijay/a96065d32a15b1374d70d094fc6b2d84#file-program-cs)
hosted with ❤ by [GitHub](https://github.com)

API – Set up Swagger

### Api Project – Create API endpoints

Next, we will add API endpoints to create a post and add comments to the post.

We are using the shiny new [minimal APIs](https://minimal-apis.github.io/) to develop our endpoints.

It is important to note that the endpoint will not create the post synchronously. It will put the **Command** on the bus and return **`Accepted`** to the client.

This file contains hidden or bidirectional Unicode text that may be interpreted or compiled differently than what appears below. To review, open the file in an editor that reveals hidden Unicode characters.
[Learn more about bidirectional Unicode characters](https://github.co/hiddenchars)

[Show hidden characters]({{ revealButtonHref }})

|  |  |
| --- | --- |
|  | app.MapPost("/create", async (IMessageSession messageSession, [FromBody] Post post) => |
|  | { |
|  | var addPostCommand = new Messages.AddPost(post.Title, post.Description, post.Author); |
|  | await messageSession.Send(addPostCommand); |
|  | return Results.Accepted(null, new { addPostCommand.PostId }); |
|  | }); |
|  |  |
|  | app.MapPost("/add-comment", async (IMessageSession messageSession, [FromBody] Comment comment) => |
|  | { |
|  | var addCommentCommand = new Messages.AddComment(comment.PostId, comment.Content, comment.CommentBy); |
|  | await messageSession.Send(addCommentCommand); |
|  | return Results.Accepted(null, new { addCommentCommand.CommentId }); |
|  | }); |
|  |  |
|  | app.Run(); |
|  |  |
|  | public record Post(string Title, string Description, string Author); |
|  | public record Comment(string PostId, string Content, string CommentBy); |

[view raw](https://gist.github.com/ankitvijay/374b1aff919ab362a46af20e5529361b/raw/6a99017750b9b1324b3d56a3890e1831a1290bea/Program.cs)
[Program.cs](https://gist.github.com/ankitvijay/374b1aff919ab362a46af20e5529361b#file-program-cs)
hosted with ❤ by [GitHub](https://github.com)

Create API endpoints

### Messages Project – Commands

The commands `AddPost` and `AddComment` inherit from an interface `IPostIdPartitionKey` . The interface contains a single property `PostId` which will be the partition key for **Post** and **Comment** documents in Cosmos DB. I will talk more about this later. But for now, here is how our messages look like:

This file contains hidden or bidirectional Unicode text that may be interpreted or compiled differently than what appears below. To review, open the file in an editor that reveals hidden Unicode characters.
[Learn more about bidirectional Unicode characters](https://github.co/hiddenchars)

[Show hidden characters]({{ revealButtonHref }})

|  |  |
| --- | --- |
|  | public interface IPostIdPartitionKey |
|  | { |
|  | string PostId { get; set; } |
|  | } |

[view raw](https://gist.github.com/ankitvijay/9a17ff86eb6f21ed8dbf98f487b84ca8/raw/76a34322d7f646bbe334491a9e60dd39a89ac897/1_IPostIdPartitionKey.cs)
[1_IPostIdPartitionKey.cs](https://gist.github.com/ankitvijay/9a17ff86eb6f21ed8dbf98f487b84ca8#file-1_ipostidpartitionkey-cs)
hosted with ❤ by [GitHub](https://github.com)

This file contains hidden or bidirectional Unicode text that may be interpreted or compiled differently than what appears below. To review, open the file in an editor that reveals hidden Unicode characters.
[Learn more about bidirectional Unicode characters](https://github.co/hiddenchars)

[Show hidden characters]({{ revealButtonHref }})

|  |  |
| --- | --- |
|  | public class AddPost : ICommand, IPostIdPartitionKey |
|  | { |
|  | public AddPost(string title, string description, string author) |
|  | { |
|  | Title = title; |
|  | Description = description; |
|  | Author = author; |
|  | PostId = Guid.NewGuid().ToString(); |
|  | } |
|  | public string PostId { get; set; } |
|  | public string Title { get; set; } |
|  | public string Description { get; set; } |
|  | public string Author { get; } |
|  | } |

[view raw](https://gist.github.com/ankitvijay/9a17ff86eb6f21ed8dbf98f487b84ca8/raw/76a34322d7f646bbe334491a9e60dd39a89ac897/2_AddPost.cs)
[2_AddPost.cs](https://gist.github.com/ankitvijay/9a17ff86eb6f21ed8dbf98f487b84ca8#file-2_addpost-cs)
hosted with ❤ by [GitHub](https://github.com)

This file contains hidden or bidirectional Unicode text that may be interpreted or compiled differently than what appears below. To review, open the file in an editor that reveals hidden Unicode characters.
[Learn more about bidirectional Unicode characters](https://github.co/hiddenchars)

[Show hidden characters]({{ revealButtonHref }})

|  |  |
| --- | --- |
|  | public class AddComment : ICommand, IPostIdPartitionKey |
|  | { |
|  | public AddComment(string postId, string content, string commentBy) |
|  | { |
|  | PostId = postId; |
|  | CommentId = Guid.NewGuid().ToString(); |
|  | Content = content; |
|  | CommentBy = commentBy; |
|  | } |
|  |  |
|  | public string CommentId { get; set; } |
|  | public string PostId { get; set; } |
|  | public string Content { get; set; } |
|  | public string CommentBy { get; set; } |
|  | } |

[view raw](https://gist.github.com/ankitvijay/9a17ff86eb6f21ed8dbf98f487b84ca8/raw/76a34322d7f646bbe334491a9e60dd39a89ac897/3_AddComment.cs)
[3_AddComment.cs](https://gist.github.com/ankitvijay/9a17ff86eb6f21ed8dbf98f487b84ca8#file-3_addcomment-cs)
hosted with ❤ by [GitHub](https://github.com)

NServiceBus Commands

## Cosmos DB Data structure

We will keep the original post and the associated comments of the post in separate JSON documents sharing the same partition key. It is because comments are unbonded collection and hierarchical data structure is better suited to save them. You can read more about design consideration when working with Cosmos DB [here](https://devblogs.microsoft.com/premier-developer/designing-a-cosmos-db-database/).

We will use `PostId` as our partition key in Cosmos.

### Worker Project – Domain

Before we go further, let us first look at how our domain objects that we save to Cosmos look.

This file contains hidden or bidirectional Unicode text that may be interpreted or compiled differently than what appears below. To review, open the file in an editor that reveals hidden Unicode characters.
[Learn more about bidirectional Unicode characters](https://github.co/hiddenchars)

[Show hidden characters]({{ revealButtonHref }})

|  |  |
| --- | --- |
|  | public class Post |
|  | { |
|  | public Post(string postId, |
|  | string title, |
|  | string description, |
|  | string author) |
|  | { |
|  | Id = postId; |
|  | PostId = postId; |
|  | Title = title; |
|  | Description = description; |
|  | Author = author; |
|  | LastUpdatedDate = DateTime.UtcNow; |
|  | CreatedDate = DateTime.UtcNow; |
|  | } |
|  |  |
|  | [JsonProperty("id")] public string Id { get; set; } |
|  | public string PostId { get; set; } |
|  | public string Title { get; set; } |
|  | public string Description { get; set; } |
|  | public string Author { get; set; } |
|  | public DateTime LastUpdatedDate { get; set; } |
|  | public DateTime CreatedDate { get; set; } |
|  | } |

[view raw](https://gist.github.com/ankitvijay/e5012529a0912c2ee36debdc033db9bf/raw/b9bdd45a79b75bdf643d549aa1b29c3c2ea597b7/1_Post.cs)
[1_Post.cs](https://gist.github.com/ankitvijay/e5012529a0912c2ee36debdc033db9bf#file-1_post-cs)
hosted with ❤ by [GitHub](https://github.com)

This file contains hidden or bidirectional Unicode text that may be interpreted or compiled differently than what appears below. To review, open the file in an editor that reveals hidden Unicode characters.
[Learn more about bidirectional Unicode characters](https://github.co/hiddenchars)

[Show hidden characters]({{ revealButtonHref }})

|  |  |
| --- | --- |
|  | public class Comment |
|  | { |
|  | public Comment(string postId, |
|  | string commentId, |
|  | string content, |
|  | string commentedBy) |
|  | { |
|  | Id = commentId; |
|  | PostId = postId; |
|  | Content = content; |
|  | CommentedBy = commentedBy; |
|  | CreatedDate = DateTime.UtcNow; |
|  | } |
|  |  |
|  | [JsonProperty("id")] public string Id { get; set; } |
|  | public string PostId { get; set; } |
|  | public string Content { get; set; } |
|  | public string CommentedBy { get; set; } |
|  | public DateTime CreatedDate { get; set; } |
|  | } |

[view raw](https://gist.github.com/ankitvijay/e5012529a0912c2ee36debdc033db9bf/raw/b9bdd45a79b75bdf643d549aa1b29c3c2ea597b7/2_Comment.cs)
[2_Comment.cs](https://gist.github.com/ankitvijay/e5012529a0912c2ee36debdc033db9bf#file-2_comment-cs)
hosted with ❤ by [GitHub](https://github.com)

Domain

As you can see, both `Post` and `Comment` domain objects have the property `PostId` that serves as a partition key in Cosmos.

### Worker Project – NServiceBus Behavior

We will create an NServiceBus behavior that will set the Cosmos DB partition key in the incoming message context in the NServiceBus pipeline. It is a crucial step to get the [Cosmos DB transaction batch](https://devblogs.microsoft.com/cosmosdb/introducing-transactionalbatch-in-the-net-sdk/) to work with the NServiceBus persistence session.

This file contains hidden or bidirectional Unicode text that may be interpreted or compiled differently than what appears below. To review, open the file in an editor that reveals hidden Unicode characters.
[Learn more about bidirectional Unicode characters](https://github.co/hiddenchars)

[Show hidden characters]({{ revealButtonHref }})

|  |  |
| --- | --- |
|  | public class PostIdAsPartitionKeyBehavior: Behavior<IIncomingLogicalMessageContext> |
|  | { |
|  | public override Task Invoke(IIncomingLogicalMessageContext context, Func<Task> next) |
|  | { |
|  | if (context.Message.Instance is IPostIdPartitionKey partitionKey) |
|  | { |
|  | var partitionKeyValue = partitionKey.PostId; |
|  | context.Extensions.Set(new PartitionKey(partitionKeyValue)); |
|  |  |
|  | return next(); |
|  | } |
|  |  |
|  | return next(); |
|  | } |
|  |  |
|  | public class Registration : RegisterStep |
|  | { |
|  | public Registration() : |
|  | base(nameof(PostIdAsPartitionKeyBehavior), |
|  | typeof(PostIdAsPartitionKeyBehavior), |
|  | "Determines the PartitionKey from the logical message", |
|  | b => new PostIdAsPartitionKeyBehavior()) |
|  | { |
|  | InsertBefore(nameof(LogicalOutboxBehavior)); |
|  | } |
|  | } |
|  | } |

[view raw](https://gist.github.com/ankitvijay/6f23605982693594e419c8653633b9b1/raw/d3fe70a2f6d52a291000235fc14906aa73d02b7b/PostIdAsPartitionKeyBehaviour.cs)
[PostIdAsPartitionKeyBehaviour.cs](https://gist.github.com/ankitvijay/6f23605982693594e419c8653633b9b1#file-postidaspartitionkeybehaviour-cs)
hosted with ❤ by [GitHub](https://github.com)

PostIdAsPartitionKeyBehaviour

The [NServiceBus Cosmos DB sample](https://github.com/Particular/docs.particular.net/blob/master/samples/cosmosdb/transactions/CosmosDB_2/Server/OrderIdAsPartitionKeyBehavior.cs) inspires the above code. If you are not familiar with NServiceBus behavior, please see this [post](https://docs.particular.net/nservicebus/pipeline/manipulate-with-behaviors).

Next, we will configure NServiceBus for our worker. We need to import `NServiceBus.Persistence.CosmosDB` nuget package along with usual `NServiceBus.Extensions.Hosting`

### Worker Project – NServiceBus Setup

This file contains hidden or bidirectional Unicode text that may be interpreted or compiled differently than what appears below. To review, open the file in an editor that reveals hidden Unicode characters.
[Learn more about bidirectional Unicode characters](https://github.co/hiddenchars)

[Show hidden characters]({{ revealButtonHref }})

|  |  |
| --- | --- |
|  | await Host.CreateDefaultBuilder(args) |
|  | .UseNServiceBus((_ => |
|  | { |
|  | var endpointConfiguration = new EndpointConfiguration("Samples.Worker"); |
|  | var transport = endpointConfiguration.UseTransport<LearningTransport>(); |
|  | transport.Transactions(TransportTransactionMode.SendsAtomicWithReceive); |
|  |  |
|  | endpointConfiguration.UsePersistence<CosmosPersistence>() |
|  | // Using Cosmos emulator |
|  | .CosmosClient(new CosmosClient( |
|  | "AccountEndpoint=https://localhost:8081/;AccountKey=C2y6yDjf5/R+ob0N8A7Cgv30VRDJIWEHLM+4QDU5DE2nQ9nDuVTqobD4b8mGGyPMbIZnqyMsEcaGQy67XIw/Jw==")) |
|  | .DatabaseName("Twitbook") |
|  | .DefaultContainer("Posts", "/PostId"); |
|  |  |
|  | endpointConfiguration.EnableOutbox(); |
|  |  |
|  | endpointConfiguration.Pipeline.Register(new PostIdAsPartitionKeyBehavior.Registration()); |
|  |  |
|  | endpointConfiguration.EnableInstallers(); |
|  | return endpointConfiguration; |
|  | })) |
|  | .Build() |
|  | .RunAsync(); |

[view raw](https://gist.github.com/ankitvijay/2e486b97c72f3de166ca1b304299c6a0/raw/c9fc41f9188ab517f52b23fdf52f61636f283d3f/Program.cs)
[Program.cs](https://gist.github.com/ankitvijay/2e486b97c72f3de166ca1b304299c6a0#file-program-cs)
hosted with ❤ by [GitHub](https://github.com)

Worker – Use NServiceBus

As you can see in the above code, there are three major points in this step up:

- We use NServiceBus Cosmos persistence. The Cosmos DB connection string points to the emulator for testing purposes. This allows us to use `CosmosPersistenceSession` in our handler.
- We have enabled NServiceBus [outbox](https://docs.particular.net/nservicebus/outbox/). Outbox pattern ensures  all message handlers are idempotent. It also gurantees atomic transaction distributed across the business data stored in Cosmos DB and the message queued from the message handler. Note that enabling the outbox will create outbox documents within Cosmos DB partition. The default time-to-live or TTL for these documents in 7 days.
- We register `PostIdAsPartitionKeyBehavior` that we created in the previous step in the NServiceBus pipeline.

### Worker Project – Message Handler

Next, we will consume the messages `AddPost` and `AddComent` sent in by the API in the worker handler.

Let us start with the handler for `AddPost`

This file contains hidden or bidirectional Unicode text that may be interpreted or compiled differently than what appears below. To review, open the file in an editor that reveals hidden Unicode characters.
[Learn more about bidirectional Unicode characters](https://github.co/hiddenchars)

[Show hidden characters]({{ revealButtonHref }})

|  |  |
| --- | --- |
|  | public class AddPostHandler : IHandleMessages<AddPost> |
|  | { |
|  | public async Task Handle(AddPost message, IMessageHandlerContext context) |
|  | { |
|  | var cosmosSession = context.SynchronizedStorageSession.CosmosPersistenceSession(); |
|  | var post = new Post(message.PostId, message.Title, message.Description, message.Author); |
|  | cosmosSession.Batch.CreateItem(post); |
|  | await context.Publish(new PostCreated |
|  | { |
|  | PostId = post.PostId, |
|  | Author = post.Author, |
|  | Description = post.Description, |
|  | Title = post.Title |
|  | }); |
|  | } |
|  | } |

[view raw](https://gist.github.com/ankitvijay/a2000958c3202b630ac929030ee29db4/raw/b8f91c688aeb9f4cfedb8e5a360c49ae1e00ad7d/AddPostHandler.cs)
[AddPostHandler.cs](https://gist.github.com/ankitvijay/a2000958c3202b630ac929030ee29db4#file-addposthandler-cs)
hosted with ❤ by [GitHub](https://github.com)

AddPostHandler.cs

`AddPostHandler` gets the Cosmos persistence session from the message handler context. We use Cosmos DB TransactionBatch to create a new **Post** in Cosmos and then publish `PostCreated` event to the Service Bus. NServiceBus outbox ensures that this operation is idempotent and the transaction is atomic.

Now, let us look at the handler for `AddComment` message.

This file contains hidden or bidirectional Unicode text that may be interpreted or compiled differently than what appears below. To review, open the file in an editor that reveals hidden Unicode characters.
[Learn more about bidirectional Unicode characters](https://github.co/hiddenchars)

[Show hidden characters]({{ revealButtonHref }})

|  |  |
| --- | --- |
|  | public class AddCommentHandler : IHandleMessages<AddComment> |
|  | { |
|  | public async Task Handle(AddComment message, IMessageHandlerContext context) |
|  | { |
|  | var cosmosSession = context.SynchronizedStorageSession.CosmosPersistenceSession(); |
|  | var postResource = await cosmosSession.Container.ReadItemAsync<Post>(message.PostId, |
|  | new PartitionKey(message.PostId)); |
|  |  |
|  | if (postResource == null) |
|  | { |
|  | throw new Exception( |
|  | $"Post {message.PostId} does not exist. Cannot add comment for the post that does not exist"); |
|  | } |
|  |  |
|  | postResource.Resource.LastUpdatedDate = DateTime.UtcNow; |
|  | cosmosSession.Batch.UpsertItem(postResource.Resource, new TransactionalBatchItemRequestOptions |
|  | { |
|  | IfMatchEtag = postResource.ETag |
|  | }); |
|  |  |
|  | var comment = new Comment(message.PostId, message.CommentId, message.Content, |
|  | message.CommentBy); |
|  | cosmosSession.Batch.CreateItem(comment); |
|  |  |
|  | await context.Publish(new CommentAdded |
|  | { |
|  | PostId = message.PostId, |
|  | CommentId = comment.Id, |
|  | Content = comment.Content, |
|  | CommentBy = comment.CommentedBy, |
|  | CreatedDate = comment.CreatedDate |
|  | }); |
|  | } |
|  | } |

[view raw](https://gist.github.com/ankitvijay/67bc9f5e10c69de0b3ea4203b21d1805/raw/8f6efad4a6e581ac69fde060f536d401ae47849c/AddCommentHandler.cs)
[AddCommentHandler.cs](https://gist.github.com/ankitvijay/67bc9f5e10c69de0b3ea4203b21d1805#file-addcommenthandler-cs)
hosted with ❤ by [GitHub](https://github.com)

AddCommentHandler.cs

The `AddCommentHandler` is slightly more involved.

- We first check if the parent post exists in Cosmos. It is possible that messages may come out of order and add comment request on the post is received before the post exists in the data store. If the post does not exist, we throw an exception. This allows the retry policy to kick-in and NServiceBus retries the message.
- We then update the `LastUpdatedDate` of the post. In the `UpsertItem` we check `Etag` of post that we are updating matches the one we retreive. Cosmos DB follows [Last Write Win](https://blog.odetocloud.com/2020/04/13/optimistic-concurrency-in-cosmosdb/) strategy. Setting `IfMatchETag` ensures the optimitic concurrency and prevents accidental overriding of the document.
- Next, we add the comment in the same transaction batch to ensure atomicity.
- Last, but not the least, we publish the `CommentAdded` event.

## Running the sample application

To run the sample application, we need to start Api and Worker projects. Let us create our first post by calling create post endpoint through Swagger.

![Add post endpoint](https://ankitvijaydotin.wordpress.com/wp-content/uploads/2022/12/29e9e-image-3.png)

*Create Post endpoint*

Next, we use generated `PostId` and add our first comment by calling add comment endpoint.

![](https://ankitvijaydotin.wordpress.com/wp-content/uploads/2022/12/c773d-image-4.png)

*Add comment endpoint*

This will save our post and comment to the Cosmos DB.

![](https://ankitvijaydotin.wordpress.com/wp-content/uploads/2022/12/ac3e5-image-7.png)

*Post document in Cosmos*

You will also notice a couple of outbox documents created by NServiceBus in Cosmos.

![](https://ankitvijaydotin.wordpress.com/wp-content/uploads/2022/12/1739f-image-6.png)

*Outbox document in Cosmos*

As mentioned earlier, the default **TTL** for the outbox document is seven days. It ensures that [no duplicate messages are reprocessed](https://stackoverflow.com/questions/68705343/the-significance-of-keeping-nservicebus-outbox-document-record-for-7-days-in-cos#68706511) within this time range.

## A word of caution

Enabling outbox with NServiceBus Cosmos persistence can lead to duplicate messages when the Cosmos DB RU limit is reached. It is an [open issue](https://github.com/Particular/NServiceBus.Persistence.CosmosDB/issues/170) with NServiceBus Cosmos DB SDK. As a workaround, you can increase your Cosmos DB RUs or switch to Cosmos DB Serverless. Alternatively, you can keep your handlers idempotent instead of relying on the outbox feature.

<blockquote class="twitter-tweet" data-dnt="true" data-width="500"><p dir="ltr" lang="en">Don't have much context at this point but it seems like something that would  need to be added to the persistence as transport cannot be slowed down. An alternative would be do perform idempotency check in the handlers rather than rely on the outbox feature.</p>— Sean Feldman (@sfeldman) <a href="https://twitter.com/sfeldman/status/1440115785419034625?ref_src=twsrc%5Etfw">September 21, 2021</a></blockquote>

## Wrapping Up

In this post, I have gone into detail about how you can use NServiceBus and Azure Cosmos DB together. I hope you find it helpful. If you have any further questions on this topic, please feel free to reach out to me on my [Twitter](https://twitter.com/vijayankit) handle or through the comments section below.
