---
title: "Azure SQL to Cosmos DB – Lesson Learnt"
date: "2019-11-13T07:53:12+10:00"
lastmod: "2020-02-26T07:47:46+10:00"
url: "/2019/11/13/azure-sql-to-cosmos-db/"
slug: "azure-sql-to-cosmos-db"
wp_id: 4305
category: ["architecture", "architecture-and-design", "azure-functions", "cosmos-db", "cosmos-sdk-v3", "event-driven-architecture", "sql"]
tag: ["architecture-and-design", "azure", "azure-functions", "c", "cosmonaunt", "cosmos-db", "event-driven-architecture", "net", "nservicebus", "sql"]
summary: "We are currently working on a greenfield project which involves building several microservices on Azure. One of our primary services had Azure SQL as its data source originally. But, midway during the development, we decided to switch Cosmos DB instead. One of the main motivations for this switch was that it was too hard to"
---

We are currently working on a greenfield project which involves building several microservices on Azure. One of our primary services had Azure SQL as its data source originally. But, midway during the development, we decided to switch Cosmos DB instead.

One of the main motivations for this switch was that it was too hard to ignore all goodness of a NoSQL DB over its SQL counterpart. We were able to get rid of a lot of Entity framework code, SQL creation and migration scripts, relational schema, and so on. Being on Azure, Cosmos DB came as a natural NoSQL choice for us.

But moving to Cosmos DB came with some downsides. SQL Server is old and boring but extremely reliable and mature. The most common problems like transactions, indexing, auditing, data migration, etc have been solved with SQL Server over and over. A quick internet search would give us answers to most of our questions.

Cosmos DB, on the other hand, is quite young. It is still a work in progress. Below are the few learnings we had as we migrated to Cosmos DB.

#### Cosmos DB SDK

Our development initially started when Cosmos DB SDK was still called `Microsoft.Azure.DocumentDB.Core` (Cosmos DB SDK v3 was not GA at that time). We did not find the SDK v2 very easy to consume. We had to write a lot of custom code to make it more palatable. We also considered using [Cosmonaut](https://github.com/Elfocrash/https://github.com/Elfocrash/Cosmonaut). Cosmonaut is a great library and wrapper around Cosmos DB SDK. It makes it very easy to interact with Cosmos DB APIs. For a small and mid-size project, I would recommend to give it a try.

However, Cosmonaut is also quite opinionated. And given v3 was around the corner we decided to stick with the Core SDK.

We have now switched over to v3 SDK and it is much easier to consume. There is still a scope of improvement but nevertheless, I think Microsoft is on the right path.

#### Emulator Support

Cosmos DB emulator only [supports Windows OS](https://feedback.azure.com/forums/263030-azure-cosmos-db/suggestions/18533509-add-documentdb-emulator-support-for-mac-os-x-and). This is a huge drawback for us since we also have developers on Mac OS and our build pipeline is on Linux. In addition to this, we found that the emulator does not behave the same as compared to “real” Cosmos DB in all the scenarios. As a result, developers have to build and run tests against the real Cosmos DB. This, of course, means more cost to the company.

#### No Datetime and DateTimeOffset type support

One of the most surprising limitations we can across with Cosmos DB was its [lack of support](https://docs.microsoft.com/en-us/azure/cosmos-db/working-with-dates) for `DateTime` and `DateTimeOffset` data type. It does not support localization of dates, which is probably one of the most basic requirements for any enterprise. As a workaround we need to store the dates in ISO 8601 UTC format as `string` following ISO 8601 (that is format  `YYYY-MM-DDThh:mm:ss.sssZ`)

#### No transaction support

Cosmos DB did not support transactions out-of-box until very recently. We had to write custom code using server-side store procedures to implement transaction. Fortunately, [.NET SDK v3.4](https://devblogs.microsoft.com/cosmosdb/whats-new-in-azure-cosmos-db-nov-2019/) changes that and we hope to migrate to the latest version soon.

#### No Outbox support

Our messaging infrastructure is built over [NServiceBus](https://particular.net/nservicebus). One of the great features of NServiceBus is [Outbox](https://docs.particular.net/nservicebus/outbox/). Unfortunately, there is no official support for Outbox with Cosmos DB. As a result, we had to roll our custom implementation of Outbox. This came at a cost of few sleepless nights for our Architect, Ivan to get it working right before our release 🙂

#### Cosmos DB is changing rapidly and documentation finds it difficult to keep pace

Cosmos DB is still maturing. And understandably, the Cosmos DB team is pushing in changes at a super rapid pace. The side effect of this is that documentation becomes out-of-date or incomplete very soon. For instance, recently, I stumbled into an issue with “Automatic” indexing. I raised it on [Stack Overflow](https://stackoverflow.com/questions/58703586/automatic-indexing-in-comos-db) only to find that “Automatic” property has been deprecated but docs are not yet updated to reflect the latest information.

#### Cost can shoot exponentially if you do not know what you are doing

Each read and write to Cosmos DB costs you [Request Unit](https://docs.microsoft.com/en-us/azure/cosmos-db/request-units) (or RU). If you are not careful, then your cost can shoot up exponentially.

Just for example, by default Cosmos DB indexes each item on the document. But, this can mean more write RUs. To reduce the RUs you can choose to index only the items you would need for your query. But, then it is extremely important to monitor your query performance. Small things like using `STARTSWITH` instead of `CONTAINS` in query can make a huge difference.

#### Change Feed support is basic

An [Event-Driven architecture](https://docs.microsoft.com/en-us/azure/architecture/guide/architecture-styles/event-driven) requires you to listen to an event and take appropriate action against that event. Cosmos DB support Events through [Change Feed](https://docs.microsoft.com/en-us/azure/cosmos-db/change-feed). Unfortunately, we found the Cosmos DB Change Feed support quite basic at the moment. For example, Change Feed does not tell you *what* has changed in the document. We were able to get around some of the limitations through custom code using Azure Functions [CosmosDBTrigger](https://docs.microsoft.com/en-us/azure/azure-functions/functions-bindings-cosmosdb-v2#trigger).

## Parting thoughts

Cosmos DB has its flaws. But things are changing at God’s speed. In spite of issues we encountered while moving to Cosmos DB, I strongly feel it is a step in the right direction. Cosmos DB will go strength to strength from here and I would definitely recommend it give it a try.

> Featured Photo by [Jeremy Thomas](https://unsplash.com/@jeremythomasphoto?utm_source=unsplash&utm_medium=referral&utm_content=creditCopyText) on [Unsplash](https://unsplash.com/s/photos/cosmos?utm_source=unsplash&utm_medium=referral&utm_content=creditCopyText)
