---
title: "Implementing inheritance with Enumeration class"
date: "2020-08-08T09:18:46+10:00"
lastmod: "2022-12-23T23:04:47+10:00"
url: "/2020/08/08/inheritance-enumeration-class/"
slug: "inheritance-enumeration-class"
wp_id: 5130
category: ["enum", "enumeration-class", "inheritance", "net-core"]
tag: ["c", "enum", "enumeration", "inhertiance", "net", "net-core"]
summary: "The traditional Enum types do not support inheritance. The Enumeration class helps us to get away from the limitation."
---

This is my fifth post in the [Series: Enumeration classes – DDD and beyond](/2020/06/12/series-enumeration-classes-ddd-and-beyond/). If you have jumped right in, I suggest going through my previous posts on the Enumeration class, especially the first post.

- Part 1: [Introduction to Enumeration Classes](/2020/05/21/introduction-enumeration-class/)
- Part 2: [Enumeration class and JSON Serialization](/2020/06/01/enumeration-class-serialization/)
- Part 3: [Enumeration class as query string parameter](/2020/06/14/enumeration-class-query-string/)
- Part 4: [Generating client code with NSwag for Enumeration class](/2020/07/12/enumeration-class-nswag/)
- Part 5: Inheritance with Enumeration class (this post)

Inheritance is a critical concept of object-oriented programming. It helps us to reuse, extend, or change the behavior of a class. Unfortunately, the traditional Enums being a value type do not support inheritance.

Enumeration class being a “class type” can help us get rid of this limitation. However, since the properties of the Enumeration class are static, the solution may not be pretty. In this post, I have tried to provide a couple of ways you can approach this problem.

## NuGet and source code

The Enumeration class and other dependent classes are available as the [NuGet packages](https://www.nuget.org/packages?q=ankitvijay). You can find the source code for the series at [this GitHub link](https://github.com/ankitvijay/Enumeration).

### Problem Statement

Let us go back to our ever-green example of the **PaymentType** Enumeration class.

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

Let us say that the organization goes global, and now the solution needs to work in many regions across the world. Specifically, the US region supports a new PaymentType **BitCoin,**while the rest of the world is still catching up. How do we introduce the BitCoin payment type for the US region alone?

Here are my couple of attempts to solve this problem.

### Solution 1

In our first solution, we extend PaymentType by creating a derived class.

We adjust the PaymentType class by making the constructor protected.

```csharp
protected PaymentType(int value, string name = null) : base(value, name)
{
}
```

We then introduce **StatesPaymentType**for the US region derived from PaymentType.

```csharp
public abstract class StatesPaymentType : PaymentType
{
    public static readonly PaymentType Bitcoin = new BitCoinType();

    private class BitCoinType : PaymentType
    {
        public BitCoinType() : base(3, "Bitcoin")
        {
        }

        public override string Code => "BT";
    }

    protected StatesPaymentType(int value, string name = null) : base(value, name)
    {
    }
}
```

As you can see, this is a simple solution to extend the PaymentType with an additional option for the US.

Here are tests for our newly created StatesPaymentType Enumeration class.

```csharp
public class InheritanceExample1Tests
{
    [Fact]
    public void CanReadAllPaymentTypesForUnitedStates()
    {
        Assert.Equal("CC", StatesPaymentType.CreditCard.Code);
        Assert.Equal("DC", StatesPaymentType.DebitCard.Code);
        Assert.Equal("BT", StatesPaymentType.Bitcoin.Code);
    }

    [Fact]
    public void CommonPaymentTypesAreEqual()
    {
        Assert.Equal(PaymentType.CreditCard, StatesPaymentType.CreditCard);
        Assert.Equal(PaymentType.DebitCard, StatesPaymentType.DebitCard);
    }

    [Fact]
    public void CanReadAllPaymentTypesForRestOfTheWorld()
    {
        Assert.Equal("CC", PaymentType.CreditCard.Code);
        Assert.Equal("DC", PaymentType.DebitCard.Code);
    }
}
```

The solution is all good except, when you try to access the parent PaymentType values from StatesPaymentType, you will get a warning to use a base class qualifier.

![](/wp-content/uploads/2022/12/6674c-solution1-warning-1.png)

*Figure 1: Warning – Use base class qualifier*

### Solution 2

In our second attempt, we try to solve this problem by *hiding*parent property using a **new**modifier.

First, we update PaymentType further by making more members protected.

```csharp
public abstract class PaymentType : Enumeration
{
    public static readonly PaymentType DebitCard = new DebitCardType();

    public static readonly PaymentType CreditCard = new CreditCardType();

    public abstract string Code { get; }

    protected PaymentType(int value, string name = null) : base(value, name)
    {
    }

    protected class DebitCardType : PaymentType
    {
        public DebitCardType() : base(0, "DebitCard")
        {
        }

        public override string Code => "DC";
    }

    protected class CreditCardType : PaymentType
    {
        public CreditCardType() : base(1, "CreditCard")
        {
        }

        public override string Code => "CC";
    }
}
```

Next, we update the StatesPaymentType Enumeration class is as below.

```csharp
public abstract class StatesPaymentType : PaymentType
{
    public new static readonly PaymentType DebitCard = new DebitCardType();

    public new static readonly PaymentType CreditCard = new CreditCardType();

    public static readonly PaymentType Bitcoin = new BitCoinType();

    private class BitCoinType : PaymentType
    {
        public BitCoinType() : base(3, "Bitcoin")
        {
        }

        public override string Code => "BT";
    }

    protected StatesPaymentType(int value, string name = null) : base(value, name)
    {
    }
}
```

Note that anewmodifieris **forbidden** in general, as it can lead to some [unexpected behavior and side-effects](https://www.codeproject.com/Articles/1215488/Be-careful-using-new-modifier-in-your-Csharp-code). However, in a scenario where we understand the risk, and there is no possible side effect, a new modifier can help solve some unique use-cases.

With this little tweak, we no longer get the warning as in the first solution.

## Conclusion

This post demonstrates how the Enumeration class can help you solve Enum type limitation with inheritance.

This post is also a wrap of my series on the Enumeration class. I hope you found this series useful. Please feel free to reach out to me on [twitter](https://twitter.com/vijayankit) or the comments section if you have any feedback. 🙂
