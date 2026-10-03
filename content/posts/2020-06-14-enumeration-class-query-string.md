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

This is my third post in the [S](https://ankitvijaydotin.wordpress.com/2020/06/12/series-enumeration-classes-ddd-and-beyond/)[eries: Enumeration classes – DDD and beyond](https://ankitvijaydotin.wordpress.com/2020/06/12/series-enumeration-classes-ddd-and-beyond/). If you are new to the Enumeration class, I suggest going through my previous posts.

- Part 1: [Introduction to Enumeration Classes](https://ankitvijaydotin.wordpress.com/2020/05/21/introduction-enumeration-class/)
- Part 2: [Enumeration class and JSON Serialization](https://ankitvijaydotin.wordpress.com/2020/06/01/enumeration-class-serialization/)
- Part 3: Enumeration class as query string parameter (this post)
- Part 4: [Generating client code with NSwag for Enumeration class](https://ankitvijaydotin.wordpress.com/2020/07/12/enumeration-class-nswag/)
- Part 5: [Implementing Inheritance with Enumeration class](https://ankitvijaydotin.wordpress.com/2020/08/08/inheritance-enumeration-class/)

## NuGet and source code

The Enumeration class and other dependent classes are available as the [NuGet packages](https://www.nuget.org/packages?q=ankitvijay). You can find the source code for the series at [this GitHub link](https://github.com/ankitvijay/Enumeration).

### Using Enum as a query string parameter

In an HTTP Get request, we can pass additional parameters in the query string. These parameters are typically a string or an integer data type.

Since an **Enum** is a Value-Type, we can parse Enum into a string or an integer. That helps us to use the Enum in a query string parameter without any drama.

For example, consider below Enum, PaymentType:

This file contains hidden or bidirectional Unicode text that may be interpreted or compiled differently than what appears below. To review, open the file in an editor that reveals hidden Unicode characters.
[Learn more about bidirectional Unicode characters](https://github.co/hiddenchars)

[Show hidden characters]({{ revealButtonHref }})

|  |  |
| --- | --- |
|  | public enum PaymentType |
|  | { |
|  | DebitCard = 0, |
|  | CreditCard = 1 |
|  | } |

[view raw](https://gist.github.com/ankitvijay/777888c7815faa02d6b83c3e8773c60d/raw/8aede7ee51fca54b503ff9adbff9f5dc9fd873d1/PaymentType.cs)
[PaymentType.cs](https://gist.github.com/ankitvijay/777888c7815faa02d6b83c3e8773c60d#file-paymenttype-cs)
hosted with ❤ by [GitHub](https://github.com)

Using an Enum as a query string parameter is easy; it does not require any special setup.

The below API endpoint demonstrates how we can use **PaymentType**Enum as a query string parameter to return the PaymentType code.

This file contains hidden or bidirectional Unicode text that may be interpreted or compiled differently than what appears below. To review, open the file in an editor that reveals hidden Unicode characters.
[Learn more about bidirectional Unicode characters](https://github.co/hiddenchars)

[Show hidden characters]({{ revealButtonHref }})

|  |  |
| --- | --- |
|  | [ApiController] |
|  | [Route("[controller]")] |
|  | public class EnumTransactionController |
|  | { |
|  | [HttpGet] |
|  | [Route("code")] |
|  | public string Get(PaymentType paymentType) |
|  | { |
|  | return paymentType == PaymentType.CreditCard ? "CC" : "DC"; |
|  | } |
|  | } |

[view raw](https://gist.github.com/ankitvijay/e36f0618c20d69b4a0bb81282fba6dda/raw/1956ea897846c62b51aa4b5784bffecf2b61adf6/EnumTransactionController.cs)
[EnumTransactionController.cs](https://gist.github.com/ankitvijay/e36f0618c20d69b4a0bb81282fba6dda#file-enumtransactioncontroller-cs)
hosted with ❤ by [GitHub](https://github.com)

The client can call the API endpoint with either an integer or string enum value.

![](https://ankitvijaydotin.wordpress.com/wp-content/uploads/2022/12/53866-enumoutput-1.png)

*Figure 1: Query string can parse Enum value as both integer and string*

![](/wp-content/uploads/2020/06/EnumBadRequest2.png)

*Figure 2: Bad request when Enum value is not valid*

### Enumeration class as a query string parameter

Unlike an Enum type, the Enumeration class is not a value-type. We would need custom logic to bind it as a query string parameter.

The good news is that we can achieve this without massive effort through custom [**Model Binders**](https://docs.microsoft.com/en-us/aspnet/core/mvc/advanced/custom-model-binding?view=aspnetcore-3.1)**.**

From Microsoft documentation:

> Model binding uses specific definitions for the types it operates on. A simple type is converted from a single string in the input. A complex type is converted from multiple input values. The framework determines the difference based on the existence of a TypeConverter. We recommended you create a type converter if you have a simple string -> SomeType mapping that doesn’t require external resources.

We can create a custom Model Binder for the Enumeration class as below:

This file contains hidden or bidirectional Unicode text that may be interpreted or compiled differently than what appears below. To review, open the file in an editor that reveals hidden Unicode characters.
[Learn more about bidirectional Unicode characters](https://github.co/hiddenchars)

[Show hidden characters]({{ revealButtonHref }})

|  |  |
| --- | --- |
|  | public class EnumerationQueryStringModelBinder<T> : IModelBinder |
|  | where T : Enumeration |
|  | { |
|  | public Task BindModelAsync(ModelBindingContext bindingContext) |
|  | { |
|  | if (bindingContext == null) |
|  | { |
|  | throw new ArgumentNullException(nameof(bindingContext)); |
|  | } |
|  |  |
|  | var enumerationName = bindingContext.ValueProvider.GetValue(bindingContext.FieldName); |
|  | if (string.IsNullOrEmpty(enumerationName.FirstValue)) |
|  | { |
|  | bindingContext.Result = ModelBindingResult.Success(default(T)); |
|  | } |
|  | else if (Enumeration.TryGetFromValueOrName<T>(enumerationName.FirstValue, out var result)) |
|  | { |
|  | bindingContext.Result = ModelBindingResult.Success(result); |
|  | } |
|  | else |
|  | { |
|  | bindingContext.Result = ModelBindingResult.Failed(); |
|  |  |
|  | bindingContext.ModelState.AddModelError(nameof(bindingContext.FieldName), |
|  | $"{enumerationName.FirstValue} is not supported."); |
|  | } |
|  |  |
|  | return Task.CompletedTask; |
|  | } |
|  | } |

[view raw](https://gist.github.com/ankitvijay/11cc2b1c9e80d526fc7168dd79a75852/raw/1e9f1759085fad94f233839b7ce2a397c52600f5/EnumerationQueryStringModelBinderOfT.cs)
[EnumerationQueryStringModelBinderOfT.cs](https://gist.github.com/ankitvijay/11cc2b1c9e80d526fc7168dd79a75852#file-enumerationquerystringmodelbinderoft-cs)
hosted with ❤ by [GitHub](https://github.com)

As you can see in the above code, we get the value of the incoming field and then validate it against passed Enumeration class type. If the incoming value matches against **Enumeration Value** or **Name**, then bind the result and return **Success**. Else, add a Model error and return **Failed**.

To use this ModelBinder, we need to implement an [IModelBinderProvider](https://docs.microsoft.com/en-us/aspnet/core/mvc/advanced/custom-model-binding?view=aspnetcore-3.1#implementing-a-modelbinderprovider). In **IModelBinderProvider**implementation, we would need to create an instance of generic **EnumerationQueryStringModelBinder**with the type of Enumeration inferred at the runtime. To create an instance of a generic

First, we create a static class, **EnumerationQueryStringModelBinder,**with a static method to create an instance of **EnumerationQueryStringModelBinder<T>**.

This file contains hidden or bidirectional Unicode text that may be interpreted or compiled differently than what appears below. To review, open the file in an editor that reveals hidden Unicode characters.
[Learn more about bidirectional Unicode characters](https://github.co/hiddenchars)

[Show hidden characters]({{ revealButtonHref }})

|  |  |
| --- | --- |
|  | public static class EnumerationQueryStringModelBinder |
|  | { |
|  | public static EnumerationQueryStringModelBinder<T> CreateInstance<T>() |
|  | where T : Enumeration |
|  | { |
|  | return new EnumerationQueryStringModelBinder<T>(); |
|  | } |
|  | } |

[view raw](https://gist.github.com/ankitvijay/f509904b618b7c1f9fb08cf8a067cbf2/raw/790c4413619f0b5f2fd493fe15ca3bf15ec771ed/EnumerationQueryParameterModelBinder.cs)
[EnumerationQueryParameterModelBinder.cs](https://gist.github.com/ankitvijay/f509904b618b7c1f9fb08cf8a067cbf2#file-enumerationqueryparametermodelbinder-cs)
hosted with ❤ by [GitHub](https://github.com)

Next, we create an **EnumerationQueryStringModelBinderProvider,**which implements the **GetBinder**method of interface IModelBinder**.**

This file contains hidden or bidirectional Unicode text that may be interpreted or compiled differently than what appears below. To review, open the file in an editor that reveals hidden Unicode characters.
[Learn more about bidirectional Unicode characters](https://github.co/hiddenchars)

[Show hidden characters]({{ revealButtonHref }})

|  |  |
| --- | --- |
|  | public class EnumerationQueryStringModelBinderProvider : IModelBinderProvider |
|  | { |
|  | public IModelBinder GetBinder(ModelBinderProviderContext context) |
|  | { |
|  | if (context == null) |
|  | { |
|  | throw new ArgumentNullException(nameof(context)); |
|  | } |
|  |  |
|  | var fullyQualifiedAssemblyName = context.Metadata.ModelType.FullName; |
|  |  |
|  | if (fullyQualifiedAssemblyName == null) |
|  | { |
|  | return null; |
|  | } |
|  |  |
|  | var enumType = context.Metadata.ModelType.Assembly.GetType |
|  | (fullyQualifiedAssemblyName, false); |
|  |  |
|  | if (enumType == null || !enumType.IsSubclassOf(typeof(Enumeration))) |
|  | { |
|  | return null; |
|  | } |
|  |  |
|  | var methodInfo = typeof(EnumerationQueryStringModelBinder) |
|  | .GetMethod("CreateInstance" |
|  | , BindingFlags.Static | BindingFlags.Public); |
|  |  |
|  | if (methodInfo == null) |
|  | { |
|  | throw new InvalidOperationException("Invalid operation"); |
|  | } |
|  |  |
|  | var genericMethod = methodInfo.MakeGenericMethod(enumType); |
|  | var invoke = genericMethod.Invoke(null, null); |
|  |  |
|  | return invoke as IModelBinder; |
|  | } |
|  | } |

[view raw](https://gist.github.com/ankitvijay/18fbbe16bf1cd5c26244c409f50471a1/raw/48e2509abbe156986d60ff4c94785a48f060d57a/EnumerationQueryParameterModelBinderProvider.cs)
[EnumerationQueryParameterModelBinderProvider.cs](https://gist.github.com/ankitvijay/18fbbe16bf1cd5c26244c409f50471a1#file-enumerationqueryparametermodelbinderprovider-cs)
hosted with ❤ by [GitHub](https://github.com)

Last but not least, we register our IModelBinderProvider in **Startup.cs.**

This file contains hidden or bidirectional Unicode text that may be interpreted or compiled differently than what appears below. To review, open the file in an editor that reveals hidden Unicode characters.
[Learn more about bidirectional Unicode characters](https://github.co/hiddenchars)

[Show hidden characters]({{ revealButtonHref }})

|  |  |
| --- | --- |
|  | public void ConfigureServices(IServiceCollection services) |
|  | { |
|  | services.AddControllers(options => |
|  | { |
|  | options.ModelBinderProviders.Insert(0, new EnumerationQueryStringModelBinderProvider()); |
|  | }); |
|  | } |

[view raw](https://gist.github.com/ankitvijay/2692060b84d6c4436ace64905516cdb8/raw/1de3d0dda1b729d2be77a69704ddaf1db0c965d6/Startup.cs)
[Startup.cs](https://gist.github.com/ankitvijay/2692060b84d6c4436ace64905516cdb8#file-startup-cs)
hosted with ❤ by [GitHub](https://github.com)

### Usage

Let us go back to our **Payment Type** Enumeration class from previous posts.

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

We can convert the original API endpoint to use the **PaymentType**Enumeration class as a query string request parameter.

This file contains hidden or bidirectional Unicode text that may be interpreted or compiled differently than what appears below. To review, open the file in an editor that reveals hidden Unicode characters.
[Learn more about bidirectional Unicode characters](https://github.co/hiddenchars)

[Show hidden characters]({{ revealButtonHref }})

|  |  |
| --- | --- |
|  | [ApiController] |
|  | [Route("[controller]")] |
|  | public class TransactionController : ControllerBase |
|  | { |
|  | [HttpGet] |
|  | [Route("code")] |
|  | public string Get(PaymentType paymentType) |
|  | { |
|  | return paymentType.Code; |
|  | } |
|  | } |

[view raw](https://gist.github.com/ankitvijay/93d566082542684e77d333eedd7a6fd1/raw/2b4157f6a3611a605f232d60dab4dadbfffcdba2/TransactionController.cs)
[TransactionController.cs](https://gist.github.com/ankitvijay/93d566082542684e77d333eedd7a6fd1#file-transactioncontroller-cs)
hosted with ❤ by [GitHub](https://github.com)

Our API endpoint works the same way as before.

![](https://ankitvijaydotin.wordpress.com/wp-content/uploads/2022/12/8f907-enumerationclassoutput.png)

*Figure 3: Enumeration class binded as Query string*

It also returns a Bad Request (404) when the client passes an invalid Enumeration name or value.

![](/wp-content/uploads/2020/06/EnumerationBadRequest2.png)

*Figure 4: Bad request when Model binder cannot parse the Enumeration class*

## Wrapping up

In this post, I explained how you could use an Enumeration class as a query string parameter. With JSON Serialization and Model Binding, I have tried to cover the most common uses-cases of using Enumeration class as an alternate to Enum. I hope you find these posts helpful.
