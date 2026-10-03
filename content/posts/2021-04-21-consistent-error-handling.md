---
title: "An opinionated way to consistent Error Handling in ASP.NET Core"
date: "2021-04-21T08:23:23+10:00"
lastmod: "2021-04-21T09:10:08+10:00"
url: "/2021/04/21/consistent-error-handling/"
slug: "consistent-error-handling"
wp_id: 202251
category: ["architecture-and-design", "asp-net-core", "ddd", "domain-driven-design", "error-handling", "net-5", "net-core"]
tag: ["architecture-and-design", "asp-net-core", "ddd", "error-handling", "net", "net-5"]
summary: "In this post, I have explained an opinionated way to achieve consistent error handling for your ASP.NET Core through Error response object."
featured_image: "https://ankitvijaydotin.wordpress.com/wp-content/uploads/2022/12/10680-feature-image.jpg"
---

### Background

Last year my organization decided to have a standard specification across all our internal REST APIs. As a part of that exercise, we decided to adopt [JSON:API spec](https://jsonapi.org/) for our APIs.

I had also written a post on [JSON:API for .NET Developers](https://atomic-temporary-110830594.wpcomstaging.com/2021/01/09/json-api-dotnet-part-1/). I intended to write a series on JSON:API. However, my company’s plan to adopt JSON:API spec dropped, and those posts remain in my drafts.

But the entire exercise was not a complete waste of time. JSON:API taught me a few lessons. And one of them was handling the different HTTP error status codes in a [single consistent way](https://jsonapi.org/format/#errors).

### Challenges with Error Handling in REST APIs

REST APIs have a very loose interpretation. There is no single “standard”. And this also shows in the error handling code for ASP.NET Core. There are primarily two issues I see with the error handling implementation in ASP.NET Core:

- It is common to see that popular HTTP error status codes such as `400 Bad Request`, `401 Unauthorized`, `404 Not found`, `500 Internal Server Error`, and so on return different HTTP Response format. In fact, even for a single status code, the response could be plain text or JSON. This makes the error parsing at the client-side very difficult since the response could vary based on status code and sometimes even for the same status code.
- In addition to this, the error handling logic is scattered across all the Controllers. That makes it tricky to change a response object since we would need to update every controller.

Below pseudo-code is an example controller with the inconsistent response for different error codes.

This file contains hidden or bidirectional Unicode text that may be interpreted or compiled differently than what appears below. To review, open the file in an editor that reveals hidden Unicode characters.
[Learn more about bidirectional Unicode characters](https://github.co/hiddenchars)

[Show hidden characters]({{ revealButtonHref }})

|  |  |
| --- | --- |
|  | [HttpPatch] |
|  | public async Task<IActionResult> Update([FromBody] OrderDto order) |
|  | { |
|  | try |
|  | { |
|  | if (!ModelState.IsValid) |
|  | { |
|  | // Returns response of type `ModelState` on "Bad Request" |
|  | return BadRequest(ModelState); |
|  | } |
|  |  |
|  | if (DoSomeCustomValidation(order)) |
|  | { |
|  | // Returns pain-text on "Bad Request" |
|  | return BadRequest("Order is invalid"); |
|  | } |
|  |  |
|  | if (!await _repository.OrderExists(order.Id)) |
|  | { |
|  | // Returns pain-text on "Not Found" |
|  | return NotFound("Order is not found"); |
|  | } |
|  |  |
|  | await _repository.UpdateOrder(order); |
|  | return NoContent(); |
|  | } |
|  | catch (Exception e) |
|  | { |
|  | // Only returns status code 500 on unhandled error with empty response |
|  | return new StatusCodeResult(StatusCodes.Status500InternalServerError); |
|  | } |
|  | } |

[view raw](https://gist.github.com/ankitvijay/adf19124d24d7378ba2d28331ee567dc/raw/34ec0ec199d66914a95b55421f2e50852a2c122b/OrderController.cs)
[OrderController.cs](https://gist.github.com/ankitvijay/adf19124d24d7378ba2d28331ee567dc#file-ordercontroller-cs)
hosted with ❤ by [GitHub](https://github.com)

Warning: The code-snippet is for demonstration purposes only.

### Consistent Error Handling

Taking a leaf out of [JSON:API specification](https://jsonapi.org/) and [JsonApiDotNetCore](https://github.com/json-api-dotnet/JsonApiDotNetCore), I tried to implement a consistent way of handling errors in ASP.NET Core.

But before I go further, a quick disclaimer.

**Disclaimer**: It is a highly opinionated approach that has worked well for my team. But please exercise caution and see if it fits your purpose before adopting.

#### Return Error Response object

We first start by creating an `Error` response object that we will return for any error status code from our application.

This file contains hidden or bidirectional Unicode text that may be interpreted or compiled differently than what appears below. To review, open the file in an editor that reveals hidden Unicode characters.
[Learn more about bidirectional Unicode characters](https://github.co/hiddenchars)

[Show hidden characters]({{ revealButtonHref }})

|  |  |
| --- | --- |
|  | public class ErrorResponse |
|  | { |
|  | public HttpStatusCode StatusCode { get; set; } |
|  |  |
|  | public string Title { get; set; } |
|  |  |
|  | public string Exception { get; set; } |
|  |  |
|  | public List<ErrorEntry> Entries { get; set; } |
|  | } |

[view raw](https://gist.github.com/ankitvijay/dc32271b90baa1c541ef2d2b34ec2b32/raw/ab91fd895d7ff710b057b56483a2f03f455b7198/1_ErrorResponse.cs)
[1_ErrorResponse.cs](https://gist.github.com/ankitvijay/dc32271b90baa1c541ef2d2b34ec2b32#file-1_errorresponse-cs)
hosted with ❤ by [GitHub](https://github.com)

This file contains hidden or bidirectional Unicode text that may be interpreted or compiled differently than what appears below. To review, open the file in an editor that reveals hidden Unicode characters.
[Learn more about bidirectional Unicode characters](https://github.co/hiddenchars)

[Show hidden characters]({{ revealButtonHref }})

|  |  |
| --- | --- |
|  | public class ErrorEntry |
|  | { |
|  | public string Code { get; set; } |
|  | public string Title { get; set; } |
|  | public string Source { get; set; } |
|  | } |

[view raw](https://gist.github.com/ankitvijay/dc32271b90baa1c541ef2d2b34ec2b32/raw/ab91fd895d7ff710b057b56483a2f03f455b7198/2_ErrorEntry.cs)
[2_ErrorEntry.cs](https://gist.github.com/ankitvijay/dc32271b90baa1c541ef2d2b34ec2b32#file-2_errorentry-cs)
hosted with ❤ by [GitHub](https://github.com)

The first part of our problem can be easily solved using an `ErrorResponse` object for every HTTP error response. However, we still need to handle errors everywhere in the code.

#### Create Exception Class

To solve the next part of our problem, we start by creating an `Exception` class for every error status code.

This file contains hidden or bidirectional Unicode text that may be interpreted or compiled differently than what appears below. To review, open the file in an editor that reveals hidden Unicode characters.
[Learn more about bidirectional Unicode characters](https://github.co/hiddenchars)

[Show hidden characters]({{ revealButtonHref }})

|  |  |
| --- | --- |
|  | using System; |
|  | using System.Runtime.Serialization; |
|  |  |
|  | [Serializable] |
|  | // Used for HttpStatusCode 404 (NotFound) |
|  | public class ResourceNotFoundException : Exception |
|  | { |
|  | public ResourceNotFoundException(string message) : base(message) |
|  | { |
|  | } |
|  |  |
|  | public ResourceNotFoundException(string message, Exception innerException) : base(message, innerException) |
|  | { |
|  | } |
|  |  |
|  | protected ResourceNotFoundException(SerializationInfo info, StreamingContext context) : base(info, context) |
|  | { |
|  | } |
|  | } |

[view raw](https://gist.github.com/ankitvijay/e0c03d9983e5d30087fa6e9261ec796c/raw/a6c5decc9f1098ed82bec114df43aac22cbe874d/1_ResourceNotFoundException.cs)
[1_ResourceNotFoundException.cs](https://gist.github.com/ankitvijay/e0c03d9983e5d30087fa6e9261ec796c#file-1_resourcenotfoundexception-cs)
hosted with ❤ by [GitHub](https://github.com)

This file contains hidden or bidirectional Unicode text that may be interpreted or compiled differently than what appears below. To review, open the file in an editor that reveals hidden Unicode characters.
[Learn more about bidirectional Unicode characters](https://github.co/hiddenchars)

[Show hidden characters]({{ revealButtonHref }})

|  |  |
| --- | --- |
|  | using System; |
|  | using System.Runtime.Serialization; |
|  |  |
|  | [Serializable] |
|  | // Used for HttpStatusCode 400 (BadRequest) or 422 (UnprocessableEntity) |
|  | public class DomainException : Exception |
|  | { |
|  | public DomainException(string message) : base(message) |
|  | { |
|  | } |
|  |  |
|  | public DomainException(string message, Exception innerException) : base(message, innerException) |
|  | { |
|  | } |
|  |  |
|  | protected DomainException(SerializationInfo info, StreamingContext context) : base(info, context) |
|  | { |
|  | } |
|  | } |

[view raw](https://gist.github.com/ankitvijay/e0c03d9983e5d30087fa6e9261ec796c/raw/a6c5decc9f1098ed82bec114df43aac22cbe874d/2_DomainException.cs)
[2_DomainException.cs](https://gist.github.com/ankitvijay/e0c03d9983e5d30087fa6e9261ec796c#file-2_domainexception-cs)
hosted with ❤ by [GitHub](https://github.com)

This file contains hidden or bidirectional Unicode text that may be interpreted or compiled differently than what appears below. To review, open the file in an editor that reveals hidden Unicode characters.
[Learn more about bidirectional Unicode characters](https://github.co/hiddenchars)

[Show hidden characters]({{ revealButtonHref }})

|  |  |
| --- | --- |
|  | using System; |
|  | using System.Runtime.Serialization; |
|  |  |
|  | [Serializable] |
|  | // Used for HttpStatusCode 403 (Forbidden) |
|  | public class UnauthorizedException : Exception |
|  | { |
|  | public UnauthorizedException(string message) : base(message) |
|  | { |
|  | } |
|  |  |
|  | public UnauthorizedException(string message, Exception innerException) : base(message, innerException) |
|  | { |
|  | } |
|  |  |
|  | protected UnauthorizedException(SerializationInfo info, StreamingContext context) : base(info, context) |
|  | { |
|  | } |
|  | } |

[view raw](https://gist.github.com/ankitvijay/e0c03d9983e5d30087fa6e9261ec796c/raw/a6c5decc9f1098ed82bec114df43aac22cbe874d/3_UnauthorizedException.cs)
[3_UnauthorizedException.cs](https://gist.github.com/ankitvijay/e0c03d9983e5d30087fa6e9261ec796c#file-3_unauthorizedexception-cs)
hosted with ❤ by [GitHub](https://github.com)

As you can see in the above code, we have a separate exception class for every error status code that we expect our application to return.

We can also reuse existing Exception classes if it fits our purpose. For example, if we are using [FluentValidation](https://github.com/FluentValidation/FluentValidation) for model validation, then we can leverage [ValidationException](https://docs.fluentvalidation.net/en/latest/start.html#throwing-exceptions) class for `BadRequest` or `UnprocessableEntity`.

#### Throwing relevant exception from code

Next, instead of returning HTTP error status code from the `Controller`, we throw a relevant exception.

If you are following Clean Architecture or Domain-Driven Design (DDD) in your project, then the Controllers are usually thin. With DDD, the business logic stays within the Domain. `QueryHandler` and `CommandHandler` act as an interface between the `Controller`and `Domain`/ `Repository`. In addition to this, the cross-cutting concerns such a validation, authorization etc., are handled through `Middeware` or `ActionFilter`, keeping the Controllers lean.

This allows us to throw a relevant exception from different parts of our code. The below pseudo-code demonstrates how we can keep the error handling outside the Controllers by throwing the Exceptions.

This file contains hidden or bidirectional Unicode text that may be interpreted or compiled differently than what appears below. To review, open the file in an editor that reveals hidden Unicode characters.
[Learn more about bidirectional Unicode characters](https://github.co/hiddenchars)

[Show hidden characters]({{ revealButtonHref }})

|  |  |
| --- | --- |
|  |  |
|  | public class GetOrderQueryHandler |
|  | { |
|  | . |
|  | . |
|  | . |
|  |  |
|  | public async Task<OrderDto> Handle(GetOrderQuery request, CancellationToken cancellationToken) |
|  | { |
|  | var order = await _repository.Get(request.OrderId); |
|  | if (order == null) |
|  | { |
|  | throw new ResourceNotFoundException($"Order with {request.OrderId} is not found"); |
|  | } |
|  | . |
|  | . |
|  | . |
|  | } |
|  | } |

[view raw](https://gist.github.com/ankitvijay/e4870f208e622a86f223b43728cc80d0/raw/ebe850ff273186d2ed5ab9066ff583bfb78d17da/1_GetOrderQueryHandler.cs)
[1_GetOrderQueryHandler.cs](https://gist.github.com/ankitvijay/e4870f208e622a86f223b43728cc80d0#file-1_getorderqueryhandler-cs)
hosted with ❤ by [GitHub](https://github.com)

This file contains hidden or bidirectional Unicode text that may be interpreted or compiled differently than what appears below. To review, open the file in an editor that reveals hidden Unicode characters.
[Learn more about bidirectional Unicode characters](https://github.co/hiddenchars)

[Show hidden characters]({{ revealButtonHref }})

|  |  |
| --- | --- |
|  | public class Order : IAggregateRoot |
|  | { |
|  | public int OrderId { get; private set; } |
|  |  |
|  | public List<OrderItem> OrderItems { get; private set;} = new List<OrderItem>(); |
|  | . |
|  | . |
|  | . |
|  |  |
|  | public void ProcessOrder() |
|  | { |
|  | if (!OrderItems.Any()) |
|  | { |
|  | throw new DomainException("Cannot process order when no items are added"); |
|  | } |
|  | . |
|  | . |
|  | . |
|  | } |
|  | } |

[view raw](https://gist.github.com/ankitvijay/e4870f208e622a86f223b43728cc80d0/raw/ebe850ff273186d2ed5ab9066ff583bfb78d17da/2_Order.cs)
[2_Order.cs](https://gist.github.com/ankitvijay/e4870f208e622a86f223b43728cc80d0#file-2_order-cs)
hosted with ❤ by [GitHub](https://github.com)

This file contains hidden or bidirectional Unicode text that may be interpreted or compiled differently than what appears below. To review, open the file in an editor that reveals hidden Unicode characters.
[Learn more about bidirectional Unicode characters](https://github.co/hiddenchars)

[Show hidden characters]({{ revealButtonHref }})

|  |  |
| --- | --- |
|  | public class CustomAuthorizationHandler : AuthorizationHandler<CustomRequirement> |
|  | { |
|  | . |
|  | . |
|  | . |
|  |  |
|  | protected override async Task HandleRequirementAsync(AuthorizationHandlerContext context, |
|  | CustomRequirement requirement) |
|  | { |
|  |  |
|  | if (!context.User.HasClaim(e => e.Type == "SuperImportantClaim") |
|  | { |
|  | throw new UnauthorizedException("User is not authorized"); |
|  | } |
|  | . |
|  | . |
|  | . |
|  | } |
|  |  |
|  | } |

[view raw](https://gist.github.com/ankitvijay/e4870f208e622a86f223b43728cc80d0/raw/ebe850ff273186d2ed5ab9066ff583bfb78d17da/3_CustomAuthorizationHandler.cs)
[3_CustomAuthorizationHandler.cs](https://gist.github.com/ankitvijay/e4870f208e622a86f223b43728cc80d0#file-3_customauthorizationhandler-cs)
hosted with ❤ by [GitHub](https://github.com)

#### Create Application Exception Middleware and ExceptionHandler

Next, we create `ApplicationExceptionMiddleware`and `ExceptionHandler`classes to handle all the exceptions that are thrown from the different parts of the code. The `ExceptionHandler` is one single place where we handle all our HTTP error status, and we return the error response to the client through `ApplicationExceptionMiddleware`.

This file contains hidden or bidirectional Unicode text that may be interpreted or compiled differently than what appears below. To review, open the file in an editor that reveals hidden Unicode characters.
[Learn more about bidirectional Unicode characters](https://github.co/hiddenchars)

[Show hidden characters]({{ revealButtonHref }})

|  |  |
| --- | --- |
|  | using System; |
|  |  |
|  | public interface IExceptionHandler |
|  | { |
|  | public Error HandleException(Exception exception); |
|  | } |

[view raw](https://gist.github.com/ankitvijay/168c41f3abb3e817375be05e7b2e7083/raw/6b9023e191503268d6c9a72ac18d92e893a0bb5a/1_IExceptionHandler.cs)
[1_IExceptionHandler.cs](https://gist.github.com/ankitvijay/168c41f3abb3e817375be05e7b2e7083#file-1_iexceptionhandler-cs)
hosted with ❤ by [GitHub](https://github.com)

This file contains hidden or bidirectional Unicode text that may be interpreted or compiled differently than what appears below. To review, open the file in an editor that reveals hidden Unicode characters.
[Learn more about bidirectional Unicode characters](https://github.co/hiddenchars)

[Show hidden characters]({{ revealButtonHref }})

|  |  |
| --- | --- |
|  | using System; |
|  | using System.Collections.Generic; |
|  | using System.Diagnostics; |
|  | using System.Linq; |
|  | using System.Net; |
|  | using FluentValidation; |
|  | using Microsoft.Extensions.Hosting; |
|  | using Microsoft.Extensions.Logging; |
|  |  |
|  | public class ExceptionHandler : IExceptionHandler |
|  | { |
|  | private readonly ILogger<ExceptionHandler> _logger; |
|  | private readonly IHostEnvironment _environment; |
|  |  |
|  | public ExceptionHandler(ILogger<ExceptionHandler> logger, |
|  | IHostEnvironment environment) |
|  | { |
|  | _logger = logger; |
|  | _environment = environment; |
|  | } |
|  |  |
|  | public Error HandleException(Exception exception) |
|  | { |
|  | var error = exception switch |
|  | { |
|  | ValidationException validationException => HandleValidationException(validationException), |
|  | DomainException domainException => HandleDomainException(domainException), |
|  | ResourceNotFoundException resourceNotFoundException => HandleResourceNotFoundException(resourceNotFoundException), |
|  | UnauthorizedException unauthorizedException => HandleUnauthorizedException(unauthorizedException), |
|  | _ => HandleUnhandledExceptions(exception) |
|  | }; |
|  |  |
|  | if (_environment.IsDevelopment()) |
|  | { |
|  | error.Exception = exception.ToString(); |
|  | } |
|  |  |
|  | return error; |
|  | } |
|  |  |
|  | private Error HandleResourceNotFoundException(ResourceNotFoundException resourceNotFoundException) |
|  | { |
|  | _logger.LogInformation(resourceNotFoundException, resourceNotFoundException.Message); |
|  |  |
|  | return new Error |
|  | { |
|  | Title = resourceNotFoundException.Message, |
|  | StatusCode = HttpStatusCode.NotFound, |
|  | }; |
|  | } |
|  |  |
|  | // ValidationException from FluentValidation |
|  | private Error HandleValidationException(ValidationException validationException) |
|  | { |
|  | _logger.LogInformation(validationException, validationException.Message); |
|  |  |
|  | var error = new Error |
|  | { |
|  | Title = validationException.Message, |
|  | StatusCode = HttpStatusCode.BadRequest |
|  | }; |
|  |  |
|  | if (validationException.Errors != null && validationException.Errors.Any()) |
|  | { |
|  | error.Entries = new List<ErrorEntry>(); |
|  |  |
|  | error.Entries.AddRange(validationException.Errors.Select(validationError => |
|  | new ErrorEntry |
|  | { |
|  | Code = validationError.ErrorCode, |
|  | Title = validationError.ErrorMessage, |
|  | Source = validationError.PropertyName |
|  | })); |
|  | } |
|  |  |
|  | return error; |
|  | } |
|  |  |
|  | private Error HandleDomainException(DomainException domainException) |
|  | { |
|  | _logger.LogInformation(domainException, domainException.Message); |
|  |  |
|  | return new Error |
|  | { |
|  | Title = domainException.Message, |
|  | StatusCode = HttpStatusCode.BadRequest |
|  | } |
|  | } |
|  |  |
|  | private Error HandleUnauthorizedException(UnauthorizedException unauthorizedException) |
|  | { |
|  | _logger.LogInformation(unauthorizedException, unauthorizedException.Message); |
|  |  |
|  | return new Error |
|  | { |
|  | Title = unauthorizedException.Message, |
|  | StatusCode = HttpStatusCode.Unauthorized |
|  | }; |
|  | } |
|  |  |
|  | private Error HandleUnhandledExceptions(Exception exception) |
|  | { |
|  | _logger.LogError(exception, exception.Message); |
|  |  |
|  | return new Error |
|  | { |
|  | Title = "An unhandled error occurred while processing this request", |
|  | StatusCode = HttpStatusCode.InternalServerError |
|  | }; |
|  | } |
|  | } |

[view raw](https://gist.github.com/ankitvijay/168c41f3abb3e817375be05e7b2e7083/raw/6b9023e191503268d6c9a72ac18d92e893a0bb5a/2_ExceptionHandler.cs)
[2_ExceptionHandler.cs](https://gist.github.com/ankitvijay/168c41f3abb3e817375be05e7b2e7083#file-2_exceptionhandler-cs)
hosted with ❤ by [GitHub](https://github.com)

This file contains hidden or bidirectional Unicode text that may be interpreted or compiled differently than what appears below. To review, open the file in an editor that reveals hidden Unicode characters.
[Learn more about bidirectional Unicode characters](https://github.co/hiddenchars)

[Show hidden characters]({{ revealButtonHref }})

|  |  |
| --- | --- |
|  | using System; |
|  | using System.Net.Mime; |
|  | using System.Text.Json; |
|  | using System.Threading.Tasks; |
|  | using Microsoft.AspNetCore.Http; |
|  | using Microsoft.Extensions.Logging; |
|  |  |
|  | public class ApplicationExceptionMiddleware |
|  | { |
|  | private readonly RequestDelegate _next; |
|  | private readonly IExceptionHandler _exceptionHandler; |
|  | private readonly ILogger<ApplicationExceptionMiddleware> _logger; |
|  |  |
|  | public ApplicationExceptionMiddleware( |
|  | RequestDelegate next, |
|  | IExceptionHandler exceptionHandler, |
|  | ILogger<ApplicationExceptionMiddleware> logger) |
|  | { |
|  | _next = next; |
|  | _exceptionHandler = exceptionHandler; |
|  | _logger = logger; |
|  | } |
|  |  |
|  | public async Task InvokeAsync(HttpContext httpContext) |
|  | { |
|  | try |
|  | { |
|  | await _next(httpContext); |
|  | } |
|  | catch (Exception ex) |
|  | { |
|  | var error = _exceptionHandler.HandleException(ex); |
|  | if (!httpContext.Response.HasStarted) |
|  | { |
|  | httpContext.Response.Clear(); |
|  | httpContext.Response.ContentType = MediaTypeNames.Application.Json; |
|  | httpContext.Response.StatusCode = (int) errorDocument.StatusCode; |
|  | await httpContext.Response.WriteAsync(JsonSerializer.Serialize( |
|  | errorDocument)); |
|  | } |
|  | } |
|  | } |
|  | } |

[view raw](https://gist.github.com/ankitvijay/168c41f3abb3e817375be05e7b2e7083/raw/6b9023e191503268d6c9a72ac18d92e893a0bb5a/3_ApplicationExceptionMiddleware.cs)
[3_ApplicationExceptionMiddleware.cs](https://gist.github.com/ankitvijay/168c41f3abb3e817375be05e7b2e7083#file-3_applicationexceptionmiddleware-cs)
hosted with ❤ by [GitHub](https://github.com)

Last but not the least, we need to register `ExceptionHandler`and `ApplicationExceptionMiddleware`in `Startup`

This file contains hidden or bidirectional Unicode text that may be interpreted or compiled differently than what appears below. To review, open the file in an editor that reveals hidden Unicode characters.
[Learn more about bidirectional Unicode characters](https://github.co/hiddenchars)

[Show hidden characters]({{ revealButtonHref }})

|  |  |
| --- | --- |
|  | public class Startup |
|  | { |
|  | public void ConfigureServices(IServiceCollection services) |
|  | { |
|  | . |
|  | . |
|  | services.AddSingleton<IExceptionHandler, ExceptionHandler>(); |
|  | . |
|  | . |
|  |  |
|  | } |
|  |  |
|  | public void Configure(IApplicationBuilder app) |
|  | { |
|  | app.UseMiddleware<ApplicationExceptionMiddleware>(); |
|  | . |
|  | . |
|  | } |
|  | } |
|  |  |

[view raw](https://gist.github.com/ankitvijay/d76a0b04b4b76a71be8bed9f4575df6a/raw/9aac424a81c3906644f5e2c1ade288cbf98dbc78/Startup.cs)
[Startup.cs](https://gist.github.com/ankitvijay/d76a0b04b4b76a71be8bed9f4575df6a#file-startup-cs)
hosted with ❤ by [GitHub](https://github.com)

### Wrapping Up

In this post, I have presented an opinionated way to achieve consistent error handling for your ASP.NET Core Rest APIs. I hope you enjoy reading this post and it was helpful in some way.

Please share your feedback in the comment section below. 🙂
