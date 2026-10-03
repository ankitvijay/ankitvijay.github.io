---
title: "JSON:API for .NET developers – Part 1"
date: "2021-01-09T11:08:07+10:00"
lastmod: "2021-01-09T11:17:01+10:00"
url: "/2021/01/09/json-api-dotnet-part-1/"
slug: "json-api-dotnet-part-1"
wp_id: 98264
category: ["asp-net-core", "jsonapi", "net-core"]
tag: ["asp-net-core", "json", "jsonapi", "jsonapidotnetcore", "net", "net-core", "rest"]
summary: "This post is the first of my new series on JSON:API for .NET developers. JSON:API has been around for a while but has not been widely known in the .NET world."
featured_image: "/wp-content/uploads/2022/12/21c92-jsonapi-part-1-feature-image-1.png"
---

This post is the first of my new series on JSON:API for .NET developers. JSON:API has been around for a while but very familiar in the .NET world. At least I had not heard of it until recently. I hope you find this series interesting and useful.

**REST APIs**

REST APIs have been part of ASP.NET for around a decade. First, as part of .NET Framework in the form of ASP.NET Web API and now as part of ASP.NET Core.

REST is an architecture style and initially came as a response to the issues with SOAP. REST is built on HTTP and allows client-server interaction through HTTP verbs such as GET, POST, DELETE etc.

The REST architecture has many advantages. It is built on standard HTTP protocols which make widely acceptable across the client-server application. It is simple, clean, and supports various formats such as JSON, XML, etc.

The flexibility of REST also comes at a cost. Its interpretation is quite loose. As a result, the implementations can vary across industry, organization and even within teams. REST implementation can lead to either multiple round trips or over-fetching of data.

## So what is JSON:API?

[JSON:API](https://jsonapi.org/) extends REST with a standardized structure and shared convention. It gives an ability to the client to fine-grain the request and only fetch the resources it needs.

> *JSON:API is designed to minimize both the number of requests and the amount of data transmitted between clients and servers. This efficiency is achieved without compromising readability, flexibility, or discoverability.*
>
> Source: [JSON:API — Latest Specification (v1.0)](https://jsonapi.org/format/)

JSON:API is highly opinionated, and unlike traditional REST architecture, it provides clear guidance on how client request and server response should be defined. It bridges the gap in the way the client and server interpret the data. It mandates media type **application/vnd.api+json**forexchanging data between client and server. It also provides recommendation on URL structure, fetching resources, relationship, sorting, filtering, etc.

Here is one example of a GET request from the client:

```yaml
GET /posts HTTP/1.1
Accept: application/vnd.api+json
```

Response from the server:

```json
{
  "links": {
    "self": "http://atomic-temporary-110830594.wpcomstaging.com/posts"
  },
  "data": [{
    "type": "posts",
    "id": "1",
    "attributes": {
      "title": "Introduction to Enumeration Classes"
    }
  }, {
    "type": "posts",
    "id": "2",
    "attributes": {
      "title": "JSON:API for .NET developers - Part 1"
    }
  }]
}
```

## Why use JSON:API?

Now that we understand what JSON:API is, let us talk about some advantages of using JSON:API over traditional REST architecture:

- **Compound Documents:** JSON:API can reduce the number of HTTP requests by allowing servers to include related resources with the primary resource. It is known as [Compound Documents](https://jsonapi.org/format/#document-compound-documents).

- **Related resources:**The JSON:API endpoint offers the client flexibility to ask for related resources in request parameters.

- **Sorting, Pagination, Filtering:**JSON:API specification provides guidelines for sorting, pagination and filtering if the server supports it.

- **Sparse FieldSet**: JSON:API gives the client an ability to **only**request the data from specific fields. It can further help to reduce the response payload size from the server.

- **Error Objects:**JSON:API specification has specific guidelines on shape error response from the server. It makes it easy for the client to parse a client error (such as Bad Request) or server error (such as Internal Server Error) consistently and uniformly.

## JSON:API for .NET Developers

ASP.NET does not have first-party support for JSON:API. Perhaps, this explains why it is not so popular in the .NET world. That said, there are some excellent [3rd party OSS solutions](https://jsonapi.org/implementations/#server-libraries-net) that implements JSON:API.

Before starting on the JSON:API journey, I explored a few Nuget packages for .NET and found [JsonApiDotNetCore](https://github.com/json-api-dotnet/JsonApiDotNetCore)to be the most active and loved library on GitHub.

## Wrapping Up!

This post was an introduction to JSON:API. In subsequent posts, I will explain JSON:API implementation in detail using JsonApiDotNetCore library. I will also touch-base upon the pros, cons, extension points and limitations of both the library and JSON:API. Stay tuned 🙂
