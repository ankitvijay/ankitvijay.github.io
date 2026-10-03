---
title: "Sending message from Azure Functions to NServiceBus receiver"
date: "2019-09-22T09:01:23+10:00"
lastmod: "2020-02-26T07:48:16+10:00"
url: "/2019/09/22/azure-functions-sender-nservicebus-receiver/"
slug: "azure-functions-sender-nservicebus-receiver"
wp_id: 4208
category: ["architecture", "architecture-and-design", "azure-functions", "azure-service-bus", "event-driven-architecture", "nservicebus"]
tag: ["architecture-and-design", "azure", "azure-functions", "azure-service-bus", "event-driven-architecture", "net", "nservicebus"]
summary: "NServiceBus is one of the most widely used service bus in .NET World. It offers features like high performance, scalability, automatic retries, auditing and so-on. NService has an out-of-box support for MSMQ, RabbitMQ, Sql Server, Azure Service Bus, etc. Our organization uses NServiceBus for messaging and workflow. We use Azure Service Bus in test/production and"
---

`NServiceBus`is one of the most widely used service bus in .NET World. It offers features like high performance, scalability, automatic retries, auditing and so-on. `NService` has an out-of-box support for MSMQ, RabbitMQ, Sql Server, Azure Service Bus, etc.

Our organization uses `NServiceBus` for messaging and workflow. We use Azure Service Bus in test/production and `RabbitMQ` on `docker` while doing the development on local. `NServiceBus` provides a nice wrapper over two different message brokers and hides their underlying differences and complexities.

#### Azure Functions and NServiceBus

Recently, I had an opportunity to work on Azure Functions. My task was to create simple a Time-triggered Azure function which queues a message to Azure Service Bus. The Service Bus message would then be consumed by one of the workers to process the message. The worker was configured to use NServiceBus to get all the goodness that comes along with it.

Unfortunately, on the Azure function (publisher/sender) side I could not find an official support for `NServiceBus`. I did stumble on [this](https://github.com/tmasternak/NServiceBus.Functions) proof-of-concept which demonstrated the integration between `NServiceBus` and Azure Function. But, since there was no official NuGet package, I decided to use native Azure Service Bus [binding](https://docs.microsoft.com/en-us/azure/azure-functions/functions-bindings-service-bus) for Azure Functions. Here is the sample code of my initial implementation:

This file contains hidden or bidirectional Unicode text that may be interpreted or compiled differently than what appears below. To review, open the file in an editor that reveals hidden Unicode characters.
[Learn more about bidirectional Unicode characters](https://github.co/hiddenchars)

[Show hidden characters]({{ revealButtonHref }})

|  |  |
| --- | --- |
|  | using System; |
|  | using Microsoft.Azure.WebJobs; |
|  | using Microsoft.Extensions.Logging; |
|  |  |
|  | namespace DemoNServiceBusSubscriberAndAzureFunctionPublisher |
|  | { |
|  | public static class TimerTriggerAzureFunction |
|  | { |
|  | [FunctionName("QueueMessageToWorker")] |
|  | public static void Run([TimerTrigger("0 */5 * * * *")]TimerInfo myTimer, |
|  | [ServiceBus("%AzureServiceBusQueue%", Connection = "AzureServiceBusConnectionString")] |
|  | ICollector<ExecuteSomeCommand> collectors, |
|  | ILogger log) |
|  | { |
|  | collectors.Add(new ExecuteSomeCommand(Guid.NewGuid().ToString())); |
|  | } |
|  | } |
|  |  |
|  | public class ExecuteSomeCommand |
|  | { |
|  | public ExecuteSomeCommand(string id) |
|  | { |
|  | Id = id; |
|  | } |
|  |  |
|  | public string Id { get; } |
|  | } |
|  | } |

[view raw](https://gist.github.com/ankitvijay/0ba925e99710f83fc8b997e12e37660b/raw/2fcbdf0dfe6bae6699cace3a86e757e9c7aad23c/TimerTriggerAzureFunction.cs)
[TimerTriggerAzureFunction.cs](https://gist.github.com/ankitvijay/0ba925e99710f83fc8b997e12e37660b#file-timertriggerazurefunction-cs)
hosted with ❤ by [GitHub](https://github.com)

#### The Issue

My worker built upon `NServiceBus` was not able to subscribe to messages published via Azure Function. I could see message in the message queue, but for some reason my `CommandHandler` on the worker could not handle the message.

#### Root Cause of the issue

To invoke the correct message handler `NServiceBus` needs to map the transport message to a message type. In this scenario, the message queued on Azure Service Bus by the Azure Function did not carry the mapping information. As a result, the `CommandHandler` on the worker could not process the message. From the [documentation](https://docs.particular.net/nservicebus/messaging/message-type-detection):

> In order to invoke the correct message handlers for incoming messages, NServiceBus must be able to map the incoming transport message to a [message type](https://docs.particular.net/nservicebus/messaging/messages-events-commands).
>
>  Source: <https://docs.particular.net/nservicebus/messaging/message-type-detection>

#### The Fix

It turned out to be quite straight forward and simple fix. I needed to supply the mapping information with my publish `Command`. `NServiceBus` documentation defines the mapping rules as follows:

> 1. If the message contains the [`NServiceBus.EnclosedMessageTypes` header](https://docs.particular.net/nservicebus/messaging/headers#serialization-headers-nservicebus-enclosedmessagetypes), the header value is used to find the message type. The header value must contain at least the [FullName](https://docs.microsoft.com/en-us/dotnet/api/system.type.fullname) of the message type but can also contain the [AssemblyQualifiedName](https://docs.microsoft.com/en-us/dotnet/api/system.type.assemblyqualifiedname). NServiceBus uses the AssemblyQualifiedName when emitting messages.
>
> 2. If the header is missing, serializers can optionally infer the message type based on the message payload.
>
> Source: <https://docs.particular.net/nservicebus/messaging/message-type-detection>

To fix the issue, I chose to simply serialize the `Command` and add the typing information along with the message. Here is the modified sample code:

This file contains hidden or bidirectional Unicode text that may be interpreted or compiled differently than what appears below. To review, open the file in an editor that reveals hidden Unicode characters.
[Learn more about bidirectional Unicode characters](https://github.co/hiddenchars)

[Show hidden characters]({{ revealButtonHref }})

|  |  |
| --- | --- |
|  | using System; |
|  | using Microsoft.Azure.WebJobs; |
|  | using Microsoft.Extensions.Logging; |
|  | using Newtonsoft.Json; |
|  |  |
|  | namespace DemoNServiceBusSubscriberAndAzureFunctionPublisher |
|  | { |
|  | public static class TimerTriggerAzureFunction |
|  | { |
|  | [FunctionName("QueueMessageToWorker")] |
|  | public static void Run([TimerTrigger("0 */5 * * * *")]TimerInfo myTimer, |
|  | [ServiceBus("%AzureServiceBusQueue%", Connection = "AzureServiceBusConnectionString")] |
|  | ICollector<string> collectors, |
|  | ILogger log) |
|  | { |
|  | collectors.Add(Serialize(new ExecuteSomeCommand(Guid.NewGuid().ToString()))); |
|  | } |
|  |  |
|  | private static string Serialize(ExecuteSomeCommand command) |
|  | { |
|  | return JsonConvert.SerializeObject(command, new JsonSerializerSettings |
|  | { |
|  | TypeNameHandling = TypeNameHandling.All |
|  | }); |
|  | } |
|  | } |
|  |  |
|  | public class ExecuteSomeCommand |
|  | { |
|  | public ExecuteSomeCommand(string id) |
|  | { |
|  | Id = id; |
|  | } |
|  |  |
|  | public string Id { get; } |
|  | } |
|  | } |

[view raw](https://gist.github.com/ankitvijay/684e078d745dfbdab56a3d5df7104090/raw/24f23ddaceee92eff086bc8ea4891506a095496a/TimerTriggerAzureFunction.cs)
[TimerTriggerAzureFunction.cs](https://gist.github.com/ankitvijay/684e078d745dfbdab56a3d5df7104090#file-timertriggerazurefunction-cs)
hosted with ❤ by [GitHub](https://github.com)

That’s it! With this small change, `CommandHandler` on my worker was able to process the message from Azure Service Bus.

Note that this fix is not limited to Azure Functions. It can be applied to all the scenarios where we need to publish the message from a native sender to a `NServiceBus` receiver.

Happy coding 🙂

Photo by [Yucel Moran](https://unsplash.com/@yucelmoran?utm_source=unsplash&utm_medium=referral&utm_content=creditCopyText) on [Unsplash](https://unsplash.com/s/photos/bus?utm_source=unsplash&utm_medium=referral&utm_content=creditCopyText)
