---
title: "Introduction to Enumeration Classes"
date: "2020-05-21T07:21:30+10:00"
lastmod: "2020-09-26T08:38:56+10:00"
url: "/2020/05/21/introduction-enumeration-class/"
slug: "introduction-enumeration-class"
wp_id: 4919
category: ["architecture-and-design", "domain-driven-design", "net-core"]
tag: ["c", "ddd", "domain-driven-design", "enum", "enumeration", "net", "net-core"]
summary: "This is the first post in the series: Enumeration classes – DDD and beyond. This post gives an introduction to an Enumeration class."
---

This is the first post in the [Series: Enumeration classes – DDD and beyond](/2020/06/12/series-enumeration-classes-ddd-and-beyond/). In this post I will provide an introduction to an Enumeration class.

- Part 1: Introduction to Enumeration Classes (this post)
- Part 2: [Enumeration class and JSON Serialization](/2020/06/01/enumeration-class-serialization/)
- Part 3: [Enumeration class as query string parameter](/2020/06/14/enumeration-class-query-string/)
- Part 4: [Generating client code with NSwag for Enumeration class](/2020/07/12/enumeration-class-nswag/)
- Part 5: [Implementing Inheritance with Enumeration class](/2020/08/08/inheritance-enumeration-class/)

Enumeration or Enum types are an integral part of C# language. They have been around since the inception of language. Unfortunately, the Enum types also have some limitations. Enum types are not object-oriented. When we have to use Enums for control flow statements, behavior around Enums gets scattered across the application. We cannot inherit or extend the Enum types. These issues can especially be a deal-breaker in Domain-Driven Design (DDD).

### **Enumeration classes**

Enumeration classes help get around the limitations of Enum types. The concept of Enumeration classes is [not new](https://stackoverflow.com/questions/469287/c-sharp-vs-java-enum-for-those-new-to-c). There are some excellent [materials available](https://docs.microsoft.com/en-us/dotnet/architecture/microservices/microservice-ddd-cqrs-patterns/enumeration-classes-over-enum-types) around how we can use Enumeration classes in Domain-Driven Design (DDD). This post will be a multi-part series where I would not only demo some advantages of Enumeration classes over traditional Enum types but also discuss how we can use these classes beyond DDD.

### **Code**

Here is an example of the Enumeration class. The [eShopOnContainers example](https://github.com/dotnet-architecture/eShopOnContainers/blob/dev/src/Services/Ordering/Ordering.Domain/SeedWork/Enumeration.cs) on GitHub inspires this code. I have made some adjustments to the class and also added a couple of methods. These changes would make more sense in the upcoming posts.

```csharp
public abstract class Enumeration : IComparable
{
    public string Name { get; }

    public int Value { get; }

    protected Enumeration(int value, string name)
    {
        Value = value;
        Name = name;
    }

    public override string ToString() => Name;

    public static IEnumerable<T> GetAll<T>() where T : Enumeration
    {
        var fields = typeof(T).GetFields(
            BindingFlags.Public |
            BindingFlags.Static |
            BindingFlags.DeclaredOnly);

        return fields.Select(f => f.GetValue(null)).Cast<T>();
    }

    public override bool Equals(object obj)
    {
        if (!(obj is Enumeration otherValue))
            return false;

        var typeMatches = GetType() == obj.GetType();
        var valueMatches = Value.Equals(otherValue.Value);

        return typeMatches && valueMatches;
    }

    public override int GetHashCode() => Value.GetHashCode();

    public static int AbsoluteDifference(Enumeration firstValue, Enumeration secondValue)
    {
        var absoluteDifference = Math.Abs(firstValue.Value – secondValue.Value);
        return absoluteDifference;
    }

    public static bool TryGetFromValueOrName<T>(
        string valueOrName,
        out T enumeration)
        where T : Enumeration
    {
        return TryParse(item => item.Name == valueOrName, out enumeration) ||
               int.TryParse(valueOrName, out var value) &&
               TryParse(item => item.Value == value, out enumeration);
    }

    public static T FromValue<T>(int value) where T : Enumeration
    {
        var matchingItem = Parse<T, int>(value, "nameOrValue", item => item.Value == value);
        return matchingItem;
    }

    public static T FromName<T>(string name) where T : Enumeration
    {
        var matchingItem = Parse<T, string>(name, "name", item => item.Name == name);
        return matchingItem;
    }

    private static bool TryParse<TEnumeration>(
        Func<TEnumeration, bool> predicate,
        out TEnumeration enumeration)
        where TEnumeration : Enumeration
    {
        enumeration = GetAll<TEnumeration>().FirstOrDefault(predicate);
        return enumeration != null;
    }

    private static TEnumeration Parse<TEnumeration, TIntOrString>(
        TIntOrString nameOrValue,
        string description,
        Func<TEnumeration, bool> predicate)
        where TEnumeration : Enumeration
    {
        var matchingItem = GetAll<TEnumeration>().FirstOrDefault(predicate);

        if (matchingItem == null)
        {
            throw new InvalidOperationException(
                $"'{nameOrValue}' is not a valid {description} in {typeof(TEnumeration)}");
        }

        return matchingItem;
    }

    public int CompareTo(object other) => Value.CompareTo(((Enumeration)other).Value);
}
```

**The Usage**

Let us consider we have a traditional Enum **PaymentType**as below.

```csharp
public enum PaymentType
{
    DebitCard = 0,
    CreditCard = 1
}
```

Now, consider PaymentType also has some behavior around the enum values. With the Enum types, this behavior can be added only outside of PaymentType with ugly control statements such as this.

```csharp
public static class PaymentTypeExtensions
{
    public static string GetPaymentTypeCode(this PaymentType paymentType)
    {
        switch (paymentType)
        {
            case PaymentType.CreditCard:
                return "CC";
            case PaymentType.DebitCard:
                return "DC";
            default:
                throw new ArgumentOutOfRangeException(
                    nameof(paymentType), paymentType, "Invalid payment type");
        }
    }
}
```

We can convert PaymentType Enum to an Enumeration class as below:

```csharp
public class PaymentType : Enumeration
{
    public static readonly PaymentType DebitCard = new PaymentType(0);

    public static readonly PaymentType CreditCard = new PaymentType(1);

    private PaymentType(int value, [CallerMemberName] string name = null) : base(value, name)
    {
    }
}
```

The PaymentType now is just a regular class. That allows us to further enhance the Enumeration class by adding new behavior within the PaymentType class.

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

As you can see in the above code, with Enumeration classes, we can get rid of switch statements and move the implementation details within PaymentType. In the DDD world, it means that the behavior does not leak outside our domain model anymore. The usage of PaymentType is the same as before, making it easier to refactor code and replace the existing Enum type to Enumeration.

## **Source Code**

You can find the source code of this series at [this GitHub](https://github.com/ankitvijay/Enumeration) repository.

### **Conclusion**

Enumeration classes provide a great alternative to Enum types. They can be especially useful in DDD by preventing the behavior leaking outside of the domain model. In my subsequent posts, I would discuss how we can take this concept further.
