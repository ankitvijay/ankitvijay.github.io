---
title: "Generating client code with NSwag for Enumeration class"
date: "2020-07-12T08:24:22+10:00"
lastmod: "2022-12-23T23:04:47+10:00"
url: "/2020/07/12/enumeration-class-nswag/"
slug: "enumeration-class-nswag"
wp_id: 5082
category: ["architecture-and-design", "asp-net-core", "asp-net-core-3-1", "domain-driven-design", "enum", "enumeration-class", "microservices", "net-core", "nswag", "nswagstudio", "swagger"]
tag: ["architecture-and-design", "asp-net-core", "c", "domain-driven-design", "enumeration", "net", "net-core", "nswag", "nswagstudio", "schemafilter", "swagger"]
summary: "This post describes how we can render an Enumeration class as an Enum type in client code with NSwag by implementing Swagger ISchemaFilter."
---

This is my fourth post in the [Series: Enumeration classes – DDD and beyond](https://ankitvijaydotin.wordpress.com/2020/06/12/series-enumeration-classes-ddd-and-beyond/). If you are new to the Enumeration class, I suggest going through my previous posts.

- Part 1: [Introduction to Enumeration Classes](https://ankitvijaydotin.wordpress.com/2020/05/21/introduction-enumeration-class/)
- Part 2: [Enumeration class and JSON Serialization](https://ankitvijaydotin.wordpress.com/2020/06/01/enumeration-class-serialization/)
- Part 3: [Enumeration class as query string parameter](https://ankitvijaydotin.wordpress.com/2020/06/14/enumeration-class-query-string/)
- Part 4: Generating client code with NSwag for Enumeration class (this post)
- Part 5: [Implementing Inheritance with Enumeration class](https://ankitvijaydotin.wordpress.com/2020/08/08/inheritance-enumeration-class/)

## NuGet and source code

The Enumeration class and other dependent classes are available as the [NuGet packages](https://www.nuget.org/packages?q=ankitvijay). You can find the source code for the series at [this GitHub link](https://github.com/ankitvijay/Enumeration).

## What is NSwag?

From the NSwag GitHub [documentation](https://github.com/RicoSuter/NSwag):

> NSwag is a Swagger/OpenAPI 2.0 and 3.0 toolchain for .NET, .NET Core, Web API, ASP.NET Core, TypeScript (jQuery, AngularJS, Angular 2+, Aurelia, KnockoutJS and more) and other platforms, written in C#. The OpenAPI/Swagger specification uses JSON and JSON Schema to describe a RESTful web API. The NSwag project provides tools to generate OpenAPI specifications from existing ASP.NET Web API controllers and client code from these OpenAPI specifications.

If you are new to NSwag, Microsoft documentation [here](https://docs.microsoft.com/en-us/aspnet/core/tutorials/getting-started-with-nswag?view=aspnetcore-3.1&tabs=visual-studio) will come handy. Also, please have a look at [youtube video](https://www.youtube.com/watch?v=3UlCaK9iJaI) created by my former colleague and friend,Rahul, where he has described how to use NSwag and NSwagStudio in detail.

### The sample API

Let us go back to our old **PaymentType**Enumeration class.

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

Consider a simple **HttpPost**endpoint, which accepts a **Transaction**object in the body.

This file contains hidden or bidirectional Unicode text that may be interpreted or compiled differently than what appears below. To review, open the file in an editor that reveals hidden Unicode characters.
[Learn more about bidirectional Unicode characters](https://github.co/hiddenchars)

[Show hidden characters]({{ revealButtonHref }})

|  |  |
| --- | --- |
|  | public class Transaction |
|  | { |
|  | public PaymentType PaymentType { get; set; } |
|  |  |
|  | public decimal Amount { get; set; } |
|  | } |

[view raw](https://gist.github.com/ankitvijay/2d58f5cefba20f4fa202bbd96c9133cd/raw/2d79a57d2cafae93fabe95adba0022efb10d3236/01_Transaction.cs)
[01_Transaction.cs](https://gist.github.com/ankitvijay/2d58f5cefba20f4fa202bbd96c9133cd#file-01_transaction-cs)
hosted with ❤ by [GitHub](https://github.com)

This file contains hidden or bidirectional Unicode text that may be interpreted or compiled differently than what appears below. To review, open the file in an editor that reveals hidden Unicode characters.
[Learn more about bidirectional Unicode characters](https://github.co/hiddenchars)

[Show hidden characters]({{ revealButtonHref }})

|  |  |
| --- | --- |
|  | [ApiController] |
|  | [Route("[controller]")] |
|  | public class TransactionController : ControllerBase |
|  | { |
|  | private static readonly List<Transaction> s_Transactions = new List<Transaction>(); |
|  |  |
|  | [HttpPost] |
|  | [Route("create")] |
|  | public IActionResult CreateTransaction(Transaction transaction) |
|  | { |
|  | s_Transactions.Add(transaction); |
|  | return Ok(); |
|  | } |
|  | } |
|  |  |

[view raw](https://gist.github.com/ankitvijay/2d58f5cefba20f4fa202bbd96c9133cd/raw/2d79a57d2cafae93fabe95adba0022efb10d3236/02_TransactionController.cs)
[02_TransactionController.cs](https://gist.github.com/ankitvijay/2d58f5cefba20f4fa202bbd96c9133cd#file-02_transactioncontroller-cs)
hosted with ❤ by [GitHub](https://github.com)

As you can see in the above code, **Transaction**DTO has a property **PaymentType**..

NSwag [does not support](https://github.com/RicoSuter/NSwag/issues/2243) **System.Text.Json**at the time of this writing. As a result, we need to fallback to our trustworthy old friend **NewtonsoftJson**. We will configure the API to use NewtonsoftJson and add **EnumerationJsonConverter,**as explained in [Part 2 of this series](https://ankitvijaydotin.wordpress.com/2020/06/01/enumeration-class-serialization/).

This file contains hidden or bidirectional Unicode text that may be interpreted or compiled differently than what appears below. To review, open the file in an editor that reveals hidden Unicode characters.
[Learn more about bidirectional Unicode characters](https://github.co/hiddenchars)

[Show hidden characters]({{ revealButtonHref }})

|  |  |
| --- | --- |
|  | // Import Microsoft.AspNetCore.Mvc.NewtonsoftJson |
|  |  |
|  | public void ConfigureServices(IServiceCollection services) |
|  | { |
|  | services.AddControllers().AddNewtonsoftJson(options => |
|  | { |
|  | options.SerializerSettings.Converters.Add(new EnumerationJsonConverter()); |
|  | }); |
|  | } |

[view raw](https://gist.github.com/ankitvijay/4b6c8bb9db8937a58622b2da20b44841/raw/002f1901f078f79d8c15c9079cee8ec97722fcdf/Startup.cs)
[Startup.cs](https://gist.github.com/ankitvijay/4b6c8bb9db8937a58622b2da20b44841#file-startup-cs)
hosted with ❤ by [GitHub](https://github.com)

### Testing Api on Postman

The Postman request accepts the PaymentType as both as name and value, just like a normal **EnumType.**

![Figure 1: Using PaymentType as name in request body](https://ankitvijaydotin.wordpress.com/wp-content/uploads/2022/12/d340d-paymenttypeasstring.png)

*Figure 1: Using PaymentType as name in request body*

![Figure 2: Using PaymentType as value in request body](https://ankitvijaydotin.wordpress.com/wp-content/uploads/2022/12/c7ce9-paymenttypeasvalue.png?w=1024&h=294)

*Figure 2: Using PaymentType as value in request body*

### Adding Swagger to Api

To generate client code from NSwag, let us first add Swagger support to our API.

This file contains hidden or bidirectional Unicode text that may be interpreted or compiled differently than what appears below. To review, open the file in an editor that reveals hidden Unicode characters.
[Learn more about bidirectional Unicode characters](https://github.co/hiddenchars)

[Show hidden characters]({{ revealButtonHref }})

|  |  |
| --- | --- |
|  | // Import Swashbuckle.AspNetCore.SwaggerGen |
|  | // Import Swashbuckle.AspNetCore.SwaggerUI |
|  |  |
|  | public void ConfigureServices(IServiceCollection services) |
|  | { |
|  | services.AddControllers().AddNewtonsoftJson(options => |
|  | { |
|  | options.SerializerSettings.Converters.Add(new EnumerationJsonConverter()); |
|  | }); |
|  |  |
|  | services.AddSwaggerGen(options => |
|  | { |
|  | options.SwaggerDoc("v1", new OpenApiInfo {Title = "Enumeration NSwagger Sample", Version = "v1"}); |
|  | }); |
|  | } |
|  |  |
|  | public void Configure(IApplicationBuilder app, IWebHostEnvironment env) |
|  | { |
|  | if (env.IsDevelopment()) |
|  | { |
|  | app.UseDeveloperExceptionPage(); |
|  |  |
|  | app.UseSwagger(); |
|  |  |
|  | app.UseSwaggerUI(options => |
|  | { |
|  | options.SwaggerEndpoint("v1/swagger.json", "Enumeration NSwagger Sample"); |
|  | }); |
|  | } |
|  |  |
|  | app.UseHttpsRedirection(); |
|  |  |
|  | app.UseRouting(); |
|  |  |
|  | app.UseAuthorization(); |
|  |  |
|  | app.UseEndpoints(endpoints => { endpoints.MapControllers(); }); |
|  | } |

[view raw](https://gist.github.com/ankitvijay/afd1a7d90ab9dd07c17de06ec5c1b3e7/raw/df879b95383b5da8cae3972193e6e871f41b9288/Startup.cs)
[Startup.cs](https://gist.github.com/ankitvijay/afd1a7d90ab9dd07c17de06ec5c1b3e7#file-startup-cs)
hosted with ❤ by [GitHub](https://github.com)

The swagger page of our application would look similar to below.

![Figure 3: PaymentType rendered as a complex object on Swagger](https://ankitvijaydotin.wordpress.com/wp-content/uploads/2022/12/3bebf-swagger-1.png)

*Figure 3: PaymentType rendered as a complex object on Swagger*

Notice that **the PaymentType**schema is as a complex object instead of an Enum type.

To fix this, we need to extend our OpenAPI specification by creating a new SchemaFilter that renders an Enumeration class as an Enum type in Swagger.

This file contains hidden or bidirectional Unicode text that may be interpreted or compiled differently than what appears below. To review, open the file in an editor that reveals hidden Unicode characters.
[Learn more about bidirectional Unicode characters](https://github.co/hiddenchars)

[Show hidden characters]({{ revealButtonHref }})

|  |  |
| --- | --- |
|  | // Import Swashbuckle.AspNetCore.SwaggerGen |
|  |  |
|  | public class EnumerationToEnumSchemaFilter : ISchemaFilter |
|  | { |
|  | public void Apply(OpenApiSchema schema, SchemaFilterContext context) |
|  | { |
|  | if (!context.Type.IsSubclassOf(typeof(Enumeration))) |
|  | { |
|  | return; |
|  | } |
|  |  |
|  | var fields = context.Type.GetFields(BindingFlags.Static | BindingFlags.Public); |
|  |  |
|  | schema.Enum = fields.Select(field => new OpenApiString(field.Name)).Cast<IOpenApiAny>().ToList(); |
|  | schema.Type = "string"; |
|  | schema.Properties = null; |
|  | schema.AllOf = null; |
|  | } |
|  | } |

[view raw](https://gist.github.com/ankitvijay/038d7c59bc978550dffa9dcc8931e2fd/raw/17701220ac32d438b6038d288a68e5a4f7725873/EnumerationToEnumSchemaFilter.cs)
[EnumerationToEnumSchemaFilter.cs](https://gist.github.com/ankitvijay/038d7c59bc978550dffa9dcc8931e2fd#file-enumerationtoenumschemafilter-cs)
hosted with ❤ by [GitHub](https://github.com)

Next, we need to add **EnumerationToEnumSchemaFilter**to the **SwaggerGen**options in Startup.cs. 

This file contains hidden or bidirectional Unicode text that may be interpreted or compiled differently than what appears below. To review, open the file in an editor that reveals hidden Unicode characters.
[Learn more about bidirectional Unicode characters](https://github.co/hiddenchars)

[Show hidden characters]({{ revealButtonHref }})

|  |  |
| --- | --- |
|  | services.AddSwaggerGen(options => |
|  | { |
|  | options.SwaggerDoc("v1", new OpenApiInfo {Title = "Enumeration NSwagger Sample", Version = "v1"}); |
|  |  |
|  | options.SchemaFilter<EnumerationToEnumSchemaFilter>(); |
|  | }); |

[view raw](https://gist.github.com/ankitvijay/c571b4f1b42306891e169c3c643afdcb/raw/9e97b0e7bedd9fdd38f8f09cca1600867755f337/Startup.cs)
[Startup.cs](https://gist.github.com/ankitvijay/c571b4f1b42306891e169c3c643afdcb#file-startup-cs)
hosted with ❤ by [GitHub](https://github.com)

If we run our application now, the PaymentType schema is an Enum type.

![Figure 4: PaymentType rendered as a Enum type on Swagger](https://ankitvijaydotin.wordpress.com/wp-content/uploads/2022/12/d4244-swagger-2.png)

*Figure 4: PaymentType rendered as a Enum type on Swagger*

### Generating client code from NSwagger Studio

Now, we let us generate the client using [NSwagger studio](https://github.com/RicoSuter/NSwag/wiki/NSwagStudio). We need to specify the path to swagger.json and click **Generate Outputs**. Note the schema for **PaymentType**in OpenAPI specification. It is of an Enum type just like on the Swagger page.

![Figure 5: Open Api/ Swagger specification on NSwagStudio](https://ankitvijaydotin.wordpress.com/wp-content/uploads/2022/12/991c9-nswagstudio-1.png?w=1024&h=596)

*Figure 5: Open Api/ Swagger specification on NSwagStudio*

The generated C# client also creates an Enum type.

![Figure 6:  Generated C# client code through NSwagStudio](https://ankitvijaydotin.wordpress.com/wp-content/uploads/2022/12/930c6-nswagstudio-2.png)

*Figure 6: Generated C# client code through NSwagStudio*

## Wrapping up

This post explains how we can render an Enumeration class as an Enum type in our client code generated through NSwag. I hope this series has given a complete picture of how we can replace Enumeration class at various parts of our system, including but not limited to web Api, persistence, and Domain-Driven-Design.
