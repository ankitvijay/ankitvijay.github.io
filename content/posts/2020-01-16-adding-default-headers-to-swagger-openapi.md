---
title: "Adding Default Headers to Swagger (OpenAPI)"
date: "2020-01-16T07:58:18+10:00"
lastmod: "2020-09-26T08:48:47+10:00"
url: "/2020/01/16/adding-default-headers-to-swagger-openapi/"
slug: "adding-default-headers-to-swagger-openapi"
wp_id: 4518
category: ["asp-net-core", "asp-net-core-3-1", "net-core"]
tag: ["asp-net-core", "asp-net-core-3-1", "net", "net-core", "swagger", "tip"]
summary: "Adding Default Headers to Swagger / Open API definition in ASP.NET Core 3.1 application."
---

Recently, we had a requirement to pass a mandatory/ default **header**to all our HTTP POST requests. Our application is built on ASP.NET Core 3.1 and uses Swagger to describe and expose our Web APIs to the consumer.

To ensure that each POST request includes the required header, I intended to add the header information to the Swagger (now OpenAPI) Definition. Here’s how I was able to achieve this.

To use Swagger/ Open API in your .NET Core 3+ application, you need to use Swashbuckle.AspNetCore version 5.0 in your project. At the time of writing, this NuGet package is still in preview.

```bash
dotnet add package Swashbuckle.AspNetCore
```

A typical ASP.NET Core 3.1 Startup project with a Swagger definition looks as below:

```csharp
 public void ConfigureServices(IServiceCollection services)
 {
    services.AddControllers();
    services.AddSwaggerGen(options =>
     {
         options.SwaggerDoc("v1", new OpenApiInfo { Title = "My Awesome Application", Version = "v1" });
     });
}

public void Configure(IApplicationBuilder app, IWebHostEnvironment env)
{
    app.UseRouting();

    app.UseSwagger();
    app.UseSwaggerUI(options =>
    {
       options.SwaggerEndpoint("v1/swagger.json", "My Awesome Application");
    });

    app.UseEndpoints(endpoints => {
                endpoints.MapControllers();
    });
}
```

To add the default header to each POST request, implement **IOperationFilter** as below:

```csharp
using System;
using System.Net.Http;
using Microsoft.OpenApi.Any;
using Microsoft.OpenApi.Models;
using Swashbuckle.AspNetCore.SwaggerGen;

namespace MyAwesomeApplication
{
    public class DefaultHeaderFilter : IOperationFilter
    {
        public void Apply(OpenApiOperation operation, OperationFilterContext context)
        {
            if (string.Equals(context.ApiDescription.HttpMethod, HttpMethod.Post.Method, StringComparison.InvariantCultureIgnoreCase))
            {
                operation.Parameters.Add(new OpenApiParameter
                {
                    Name = "my-default-header",
                    In = ParameterLocation.Header,
                    Required = false,
                    Example = new OpenApiString("my-default-header-value")
                });
            }
        }
    }
}
```

Now, Update AddSwaggerGenCommand in Startup → ConfigureServices method to include the new **DefaultHeaderFilter**

```csharp
 public void ConfigureServices(IServiceCollection services)
 {
    services.AddControllers();
    services.AddSwaggerGen(options =>
     {
         options.SwaggerDoc("v1", new OpenApiInfo { Title = "My Awesome Application", Version = "v1" });
         c.OperationFilter<DefaultHeaderFilter>();
     });
}
```

That’s it! Your Swagger UI will now have the default header for each POST request with this change.

![](/wp-content/uploads/2020/01/Swagger.png)

*Swagger with Default Header*
