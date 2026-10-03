---
title: "Enumeration class as query string parameter"
date: "2020-06-14T08:19:45+10:00"
lastmod: "2022-12-23T23:04:47+10:00"
url: "/2020/06/14/enumeration-class-query-string/"
slug: "enumeration-class-query-string"
wp_id: 4999
category: ["architecture-and-design", "asp-net-core", "asp-net-core-3-1", "ddd", "enumeration-class", "model-binder", "net-core", "query-string", "query-string", "request-parameter"]
tag: ["asp-net-core", "asp-net-core-3-1", "c", "enumeration", "httpget", "model-binder", "net", "net-core", "query-string", "request-parameter"]
summary: "In this post, I have explained how you can use an Enumeration class as a query string parameter by creating a custom Model Binder."
---

This is my third post in the [S](/2020/06/12/series-enumeration-classes-ddd-and-beyond/)[eries: Enumeration classes – DDD and beyond](/2020/06/12/series-enumeration-classes-ddd-and-beyond/). If you are new to the Enumeration class, I suggest going through my previous posts.

- Part 1: [Introduction to Enumeration Classes](/2020/05/21/introduction-enumeration-class/)
- Part 2: [Enumeration class and JSON Serialization](/2020/06/01/enumeration-class-serialization/)
- Part 3: Enumeration class as query string parameter (this post)
- Part 4: [Generating client code with NSwag for Enumeration class](/2020/07/12/enumeration-class-nswag/)
- Part 5: [Implementing Inheritance with Enumeration class](/2020/08/08/inheritance-enumeration-class/)

## NuGet and source code

The Enumeration class and other dependent classes are available as the [NuGet packages](https://www.nuget.org/packages?q=ankitvijay). You can find the source code for the series at [this GitHub link](https://github.com/ankitvijay/Enumeration).

### Using Enum as a query string parameter

In an HTTP Get request, we can pass additional parameters in the query string. These parameters are typically a string or an integer data type.

Since an **Enum** is a Value-Type, we can parse Enum into a string or an integer. That helps us to use the Enum in a query string parameter without any drama.

For example, consider below Enum, PaymentType:

```csharp
public enum PaymentType
{
    DebitCard = 0,
    CreditCard = 1
}
```

Using an Enum as a query string parameter is easy; it does not require any special setup.

The below API endpoint demonstrates how we can use **PaymentType**Enum as a query string parameter to return the PaymentType code.

```csharp
[ApiController]
[Route("[controller]")]
public class EnumTransactionController
{
    [HttpGet]
    [Route("code")]
    public string Get(PaymentType paymentType)
    {
        return paymentType == PaymentType.CreditCard ? "CC" : "DC";
    }
}
```

The client can call the API endpoint with either an integer or string enum value.

![](/wp-content/uploads/2022/12/53866-enumoutput-1.png)

*Figure 1: Query string can parse Enum value as both integer and string*

![](/wp-content/uploads/2020/06/EnumBadRequest2.png)

*Figure 2: Bad request when Enum value is not valid*

### Enumeration class as a query string parameter

Unlike an Enum type, the Enumeration class is not a value-type. We would need custom logic to bind it as a query string parameter.

The good news is that we can achieve this without massive effort through custom [**Model Binders**](https://docs.microsoft.com/en-us/aspnet/core/mvc/advanced/custom-model-binding?view=aspnetcore-3.1)**.**

From Microsoft documentation:

> Model binding uses specific definitions for the types it operates on. A simple type is converted from a single string in the input. A complex type is converted from multiple input values. The framework determines the difference based on the existence of a TypeConverter. We recommended you create a type converter if you have a simple string -> SomeType mapping that doesn’t require external resources.

We can create a custom Model Binder for the Enumeration class as below:

```csharp
public class EnumerationQueryStringModelBinder<T> : IModelBinder
        where T : Enumeration
    {
        public Task BindModelAsync(ModelBindingContext bindingContext)
        {
            if (bindingContext == null)
            {
                throw new ArgumentNullException(nameof(bindingContext));
            }

            var enumerationName = bindingContext.ValueProvider.GetValue(bindingContext.FieldName);
            if (string.IsNullOrEmpty(enumerationName.FirstValue))
            {
                bindingContext.Result = ModelBindingResult.Success(default(T));
            }
            else if (Enumeration.TryGetFromValueOrName<T>(enumerationName.FirstValue, out var result))
            {
                bindingContext.Result = ModelBindingResult.Success(result);
            }
            else
            {
                bindingContext.Result = ModelBindingResult.Failed();

                bindingContext.ModelState.AddModelError(nameof(bindingContext.FieldName),
                    $"{enumerationName.FirstValue} is not supported.");
            }

            return Task.CompletedTask;
        }
    }
```

As you can see in the above code, we get the value of the incoming field and then validate it against passed Enumeration class type. If the incoming value matches against **Enumeration Value** or **Name**, then bind the result and return **Success**. Else, add a Model error and return **Failed**.

To use this ModelBinder, we need to implement an [IModelBinderProvider](https://docs.microsoft.com/en-us/aspnet/core/mvc/advanced/custom-model-binding?view=aspnetcore-3.1#implementing-a-modelbinderprovider). In **IModelBinderProvider**implementation, we would need to create an instance of generic **EnumerationQueryStringModelBinder**with the type of Enumeration inferred at the runtime. To create an instance of a generic

First, we create a static class, **EnumerationQueryStringModelBinder,**with a static method to create an instance of **EnumerationQueryStringModelBinder&lt;T>**.

```csharp
public static class EnumerationQueryStringModelBinder
    {
        public static EnumerationQueryStringModelBinder<T> CreateInstance<T>()
            where T : Enumeration
        {
            return new EnumerationQueryStringModelBinder<T>();
        }
    }
```

Next, we create an **EnumerationQueryStringModelBinderProvider,**which implements the **GetBinder**method of interface IModelBinder**.**

```csharp
public class EnumerationQueryStringModelBinderProvider : IModelBinderProvider
    {
        public IModelBinder GetBinder(ModelBinderProviderContext context)
        {
            if (context == null)
            {
                throw new ArgumentNullException(nameof(context));
            }

            var fullyQualifiedAssemblyName = context.Metadata.ModelType.FullName;

            if (fullyQualifiedAssemblyName == null)
            {
                return null;
            }

            var enumType = context.Metadata.ModelType.Assembly.GetType
                (fullyQualifiedAssemblyName, false);

            if (enumType == null || !enumType.IsSubclassOf(typeof(Enumeration)))
            {
                return null;
            }

            var methodInfo = typeof(EnumerationQueryStringModelBinder)
                .GetMethod("CreateInstance"
                    , BindingFlags.Static | BindingFlags.Public);

            if (methodInfo == null)
            {
                throw new InvalidOperationException("Invalid operation");
            }

            var genericMethod = methodInfo.MakeGenericMethod(enumType);
            var invoke = genericMethod.Invoke(null, null);

            return invoke as IModelBinder;
        }
    }
```

Last but not least, we register our IModelBinderProvider in **Startup.cs.**

```csharp
public void ConfigureServices(IServiceCollection services)
{
    services.AddControllers(options =>
    {
        options.ModelBinderProviders.Insert(0, new EnumerationQueryStringModelBinderProvider());
    });
}
```

### Usage

Let us go back to our **Payment Type** Enumeration class from previous posts.

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

We can convert the original API endpoint to use the **PaymentType**Enumeration class as a query string request parameter.

```csharp
[ApiController]
[Route("[controller]")]
public class TransactionController : ControllerBase
{
    [HttpGet]
    [Route("code")]
    public string Get(PaymentType paymentType)
    {
        return paymentType.Code;
    }
}
```

Our API endpoint works the same way as before.

![](/wp-content/uploads/2022/12/8f907-enumerationclassoutput.png)

*Figure 3: Enumeration class binded as Query string*

It also returns a Bad Request (404) when the client passes an invalid Enumeration name or value.

![](/wp-content/uploads/2020/06/EnumerationBadRequest2.png)

*Figure 4: Bad request when Model binder cannot parse the Enumeration class*

## Wrapping up

In this post, I explained how you could use an Enumeration class as a query string parameter. With JSON Serialization and Model Binding, I have tried to cover the most common uses-cases of using Enumeration class as an alternate to Enum. I hope you find these posts helpful.
