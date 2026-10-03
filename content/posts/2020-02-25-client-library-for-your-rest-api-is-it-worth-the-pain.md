---
title: "Client library for your Rest API – Is it worth the pain?"
date: "2020-02-25T19:04:13+10:00"
lastmod: "2020-09-26T08:46:18+10:00"
url: "/2020/02/25/client-library-for-your-rest-api-is-it-worth-the-pain/"
slug: "client-library-for-your-rest-api-is-it-worth-the-pain"
wp_id: 4600
category: ["architecture", "asp-net-core", "microservices", "net-core"]
tag: ["asp-net-core", "c", "client-library", "httpclient", "net", "net-core", "nuget", "swagger"]
summary: "Creating a client library for your Rest service can help your clients consume your Rest API. But is it a silver bullet to every problem?"
---

As I have written in my previous posts, we are working on a greenfield solution and developing multiple microservices as part of it. Most of these microservices are Rest APIs built on ASP.NET Core. The consumers for most of these microservices are mostly other internal services, again built on ASP.NET Core.

### Where we started

Now, when we started our development there were not many consumers of our microservices. Things were still simple. We simply exposed the Swagger specification along with some guidelines on how to consume the API. This was enough for anyone who needs to consume our API. We did not feel the need to spend effort in creating a client library for our API. Each consumer had their own “version” of integration Rest client to talk to our API. The consumers would auto-generate methods and models through tools such as [NSwagger](https://github.com/rmaclean/nSwagger) or sometimes simply duplicate the models and create custom [Typed HttpClient](https://docs.microsoft.com/en-us/dotnet/architecture/microservices/implement-resilient-applications/use-httpclientfactory-to-implement-resilient-http-requests#how-to-use-typed-clients-with-httpclientfactory)to talk to our API. There was not one single consistent way of talking to our Rest service.

![](/wp-content/uploads/2022/12/a2065-image.png)

*Our initial design*

### Issues

The complexity of our system increased over a period of time. We had multiple consumers for our API. There were cross-cutting concerns such as authentication, authorization, custom headers, logging, etc. which every client needed to adhere to. The models/ requests became complex. It started to become difficult for each client to keep the pace of new features or the changes introduced to our API. We had some healthy discussions within our team and we felt the need of exposing a client library as a **NuGet package** along with our Rest API.

The concept of the client library is not new. It has been around forever in some form or the other. For example, at the time of web services, we had [WSDL](https://www.w3schools.com/XML/xml_wsdl.asp) document to describe the web service. We could auto-generate the client methods to make a call over the wire. There are also plenty of examples of the client libraries (or SDKs) from tech gaints such as Microsoft, Amazon, Google, etc.

![](/wp-content/uploads/2022/12/ac11a-image-2.png)

*The updated design*

### Why client library?

Here are the reasons why we felt the client library was a good choice for us:

#### A consistent way of calling the API

One of the first important wins we had with the client library was that it gave clients a single and consistent way of calling our API. It allowed us to get rid of different client shims and replace them with one single implementation.

#### Client-side validation

With the client library, we could to do a basic model validation even before the client request hit the server. This helped save a precious HTTP call and provide faster feedback to the client.

#### Versioning

The client library provided us with the ability to handle versioning better. Since, we controlled the client library we could **Obsolete**a method, provide a new implementation, have different overloads for the same REST endpoint. For the client, it was a simple method call but under the hood, we were able to format the request any way we liked. Since all the consumers we have are internal application it was easier for us to control when the client upgrades to the newer package.

#### Cross-cutting concerns

The client library provided us a consistent way of handling cross-cutting concerns such as authentication, authorization, and logging. The client simply had to inject our “Typed” client service and we were able to hook authentication token, correlation id, custom headers, etc. to the request through **HttpHandlers**.

#### **Caching**

The client library provided us with an opportunity to have a consistent and correct caching strategy for the Rest service. As the API owner, we had an understanding of the implementation details of the API. This gave us a way to answer questions such as what should be the cache duration, when the cache should be invalidated or most importantly does it need to be cached?

#### Resilience and Fault Tolerance

The client library provided us with the way of defining retry policies, timeout and implementing circuit-breaker pattern. This helps to improve the resiliency of our application. We could use a framework such as [Polly](https://www.hanselman.com/blog/AddingResilienceAndTransientFaultHandlingToYourNETCoreHttpClientWithPolly.aspx) under the hood without leaking the details to the client.

#### Change implementations under the hood

Having the client library before our API client provided us a wrapper to the REST Client. It gives ways to change our implementation without impacting our clients. Hypothetically, we could use SignalR, gRPC or mix of these but still provide a single interface for the client to call our services.

### Is it a silver bullet?

Despite all the above advantages, I would still not go to the extent to say that the client library is a fit for all purposes. The client library is an additional effort for library maintainers. An effort that could be easily absorbed by the consumer of your API. In our scenario, we only have .NET consumers so we had to only maintain one library. What if, the API needs to be consumed by heterogeneous clients on different platforms and technology such as JavaScript, Python, Ruby, etc.? Is it still worth the effort to create a client library for each of these consumers? I’m not sure! Before, creating a client library I would probably ask these questions: What is the size of the team, who is the target audience, the complexity of the REST API, does the team have experts in creating a client library in the required platform/ language?

### Conclusion

Providing a Nuget package to clients to consume our Rest APIs enabled them to call our services in a simple and consistent manner. However, I would still warn against creating the client libraries for every Rest API you have.
