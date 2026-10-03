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

This is my fourth post in the [Series: Enumeration classes – DDD and beyond](/2020/06/12/series-enumeration-classes-ddd-and-beyond/). If you are new to the Enumeration class, I suggest going through my previous posts.

- Part 1: [Introduction to Enumeration Classes](/2020/05/21/introduction-enumeration-class/)
- Part 2: [Enumeration class and JSON Serialization](/2020/06/01/enumeration-class-serialization/)
- Part 3: [Enumeration class as query string parameter](/2020/06/14/enumeration-class-query-string/)
- Part 4: Generating client code with NSwag for Enumeration class (this post)
- Part 5: [Implementing Inheritance with Enumeration class](/2020/08/08/inheritance-enumeration-class/)

## NuGet and source code

The Enumeration class and other dependent classes are available as the [NuGet packages](https://www.nuget.org/packages?q=ankitvijay). You can find the source code for the series at [this GitHub link](https://github.com/ankitvijay/Enumeration).

## What is NSwag?

From the NSwag GitHub [documentation](https://github.com/RicoSuter/NSwag):

> NSwag is a Swagger/OpenAPI 2.0 and 3.0 toolchain for .NET, .NET Core, Web API, ASP.NET Core, TypeScript (jQuery, AngularJS, Angular 2+, Aurelia, KnockoutJS and more) and other platforms, written in C#. The OpenAPI/Swagger specification uses JSON and JSON Schema to describe a RESTful web API. The NSwag project provides tools to generate OpenAPI specifications from existing ASP.NET Web API controllers and client code from these OpenAPI specifications.

If you are new to NSwag, Microsoft documentation [here](https://docs.microsoft.com/en-us/aspnet/core/tutorials/getting-started-with-nswag?view=aspnetcore-3.1&tabs=visual-studio) will come handy. Also, please have a look at [youtube video](https://www.youtube.com/watch?v=3UlCaK9iJaI) created by my former colleague and friend,Rahul, where he has described how to use NSwag and NSwagStudio in detail.

### The sample API

Let us go back to our old **PaymentType**Enumeration class.

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

Consider a simple **HttpPost**endpoint, which accepts a **Transaction**object in the body.

```csharp
public class Transaction
{
    public PaymentType PaymentType { get; set; }

    public decimal Amount { get; set; }
}
```

```csharp
[ApiController]
[Route("[controller]")]
public class TransactionController : ControllerBase
{
    private static readonly List<Transaction> s_Transactions = new List<Transaction>();

    [HttpPost]
    [Route("create")]
    public IActionResult CreateTransaction(Transaction transaction)
    {
        s_Transactions.Add(transaction);
        return Ok();
    }
}
```

As you can see in the above code, **Transaction**DTO has a property **PaymentType**..

NSwag [does not support](https://github.com/RicoSuter/NSwag/issues/2243) **System.Text.Json**at the time of this writing. As a result, we need to fallback to our trustworthy old friend **NewtonsoftJson**. We will configure the API to use NewtonsoftJson and add **EnumerationJsonConverter,**as explained in [Part 2 of this series](/2020/06/01/enumeration-class-serialization/).

```csharp
// Import Microsoft.AspNetCore.Mvc.NewtonsoftJson

public void ConfigureServices(IServiceCollection services)
{
    services.AddControllers().AddNewtonsoftJson(options =>
    {
        options.SerializerSettings.Converters.Add(new EnumerationJsonConverter());
    });
}
```

### Testing Api on Postman

The Postman request accepts the PaymentType as both as name and value, just like a normal **EnumType.**

![Figure 1: Using PaymentType as name in request body](/wp-content/uploads/2022/12/d340d-paymenttypeasstring.png)

*Figure 1: Using PaymentType as name in request body*

![Figure 2: Using PaymentType as value in request body](/wp-content/uploads/2022/12/c7ce9-paymenttypeasvalue.png)

*Figure 2: Using PaymentType as value in request body*

### Adding Swagger to Api

To generate client code from NSwag, let us first add Swagger support to our API.

```csharp
// Import Swashbuckle.AspNetCore.SwaggerGen
// Import Swashbuckle.AspNetCore.SwaggerUI

public void ConfigureServices(IServiceCollection services)
{
    services.AddControllers().AddNewtonsoftJson(options =>
    {
        options.SerializerSettings.Converters.Add(new EnumerationJsonConverter());
    });

    services.AddSwaggerGen(options =>
    {
        options.SwaggerDoc("v1", new OpenApiInfo {Title = "Enumeration NSwagger Sample", Version = "v1"});
    });
}

public void Configure(IApplicationBuilder app, IWebHostEnvironment env)
{
    if (env.IsDevelopment())
    {
        app.UseDeveloperExceptionPage();

        app.UseSwagger();

        app.UseSwaggerUI(options =>
        {
            options.SwaggerEndpoint("v1/swagger.json", "Enumeration NSwagger Sample");
        });
    }

    app.UseHttpsRedirection();

    app.UseRouting();

    app.UseAuthorization();

    app.UseEndpoints(endpoints => { endpoints.MapControllers(); });
}
```

The swagger page of our application would look similar to below.

![Figure 3: PaymentType rendered as a complex object on Swagger](/wp-content/uploads/2022/12/3bebf-swagger-1.png)

*Figure 3: PaymentType rendered as a complex object on Swagger*

Notice that **the PaymentType**schema is as a complex object instead of an Enum type.

To fix this, we need to extend our OpenAPI specification by creating a new SchemaFilter that renders an Enumeration class as an Enum type in Swagger.

```csharp
// Import Swashbuckle.AspNetCore.SwaggerGen

public class EnumerationToEnumSchemaFilter : ISchemaFilter
{
    public void Apply(OpenApiSchema schema, SchemaFilterContext context)
    {
        if (!context.Type.IsSubclassOf(typeof(Enumeration)))
        {
            return;
        }

        var fields = context.Type.GetFields(BindingFlags.Static | BindingFlags.Public);

        schema.Enum = fields.Select(field => new OpenApiString(field.Name)).Cast<IOpenApiAny>().ToList();
        schema.Type = "string";
        schema.Properties = null;
        schema.AllOf = null;
    }
}
```

Next, we need to add **EnumerationToEnumSchemaFilter**to the **SwaggerGen**options in Startup.cs.

```csharp
services.AddSwaggerGen(options =>
{
    options.SwaggerDoc("v1", new OpenApiInfo {Title = "Enumeration NSwagger Sample", Version = "v1"});

    options.SchemaFilter<EnumerationToEnumSchemaFilter>();
});
```

If we run our application now, the PaymentType schema is an Enum type.

![Figure 4: PaymentType rendered as a Enum type on Swagger](/wp-content/uploads/2022/12/d4244-swagger-2.png)

*Figure 4: PaymentType rendered as a Enum type on Swagger*

### Generating client code from NSwagger Studio

Now, we let us generate the client using [NSwagger studio](https://github.com/RicoSuter/NSwag/wiki/NSwagStudio). We need to specify the path to swagger.json and click **Generate Outputs**. Note the schema for **PaymentType**in OpenAPI specification. It is of an Enum type just like on the Swagger page.

![Figure 5: Open Api/ Swagger specification on NSwagStudio](/wp-content/uploads/2022/12/991c9-nswagstudio-1.png)

*Figure 5: Open Api/ Swagger specification on NSwagStudio*

The generated C# client also creates an Enum type.

![Figure 6:  Generated C# client code through NSwagStudio](/wp-content/uploads/2022/12/930c6-nswagstudio-2.png)

*Figure 6: Generated C# client code through NSwagStudio*

## Wrapping up

This post explains how we can render an Enumeration class as an Enum type in our client code generated through NSwag. I hope this series has given a complete picture of how we can replace Enumeration class at various parts of our system, including but not limited to web Api, persistence, and Domain-Driven-Design.
