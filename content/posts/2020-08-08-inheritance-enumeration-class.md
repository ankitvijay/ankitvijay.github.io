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

This is my fifth post in the [Series: Enumeration classes – DDD and beyond](https://ankitvijaydotin.wordpress.com/2020/06/12/series-enumeration-classes-ddd-and-beyond/). If you have jumped right in, I suggest going through my previous posts on the Enumeration class, especially the first post.

- Part 1: [Introduction to Enumeration Classes](https://ankitvijaydotin.wordpress.com/2020/05/21/introduction-enumeration-class/)
- Part 2: [Enumeration class and JSON Serialization](https://ankitvijaydotin.wordpress.com/2020/06/01/enumeration-class-serialization/)
- Part 3: [Enumeration class as query string parameter](https://ankitvijaydotin.wordpress.com/2020/06/14/enumeration-class-query-string/)
- Part 4: [Generating client code with NSwag for Enumeration class](https://ankitvijaydotin.wordpress.com/2020/07/12/enumeration-class-nswag/)
- Part 5: Inheritance with Enumeration class (this post)

Inheritance is a critical concept of object-oriented programming. It helps us to reuse, extend, or change the behavior of a class. Unfortunately, the traditional Enums being a value type do not support inheritance. 

Enumeration class being a “class type” can help us get rid of this limitation. However, since the properties of the Enumeration class are static, the solution may not be pretty. In this post, I have tried to provide a couple of ways you can approach this problem.

## NuGet and source code

The Enumeration class and other dependent classes are available as the [NuGet packages](https://www.nuget.org/packages?q=ankitvijay). You can find the source code for the series at [this GitHub link](https://github.com/ankitvijay/Enumeration).

### Problem Statement

Let us go back to our ever-green example of the **PaymentType** Enumeration class.

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

Let us say that the organization goes global, and now the solution needs to work in many regions across the world. Specifically, the US region supports a new PaymentType **BitCoin,**while the rest of the world is still catching up. How do we introduce the BitCoin payment type for the US region alone?

Here are my couple of attempts to solve this problem.

### Solution 1

In our first solution, we extend PaymentType by creating a derived class.

We adjust the PaymentType class by making the constructor protected.

This file contains hidden or bidirectional Unicode text that may be interpreted or compiled differently than what appears below. To review, open the file in an editor that reveals hidden Unicode characters.
[Learn more about bidirectional Unicode characters](https://github.co/hiddenchars)

[Show hidden characters]({{ revealButtonHref }})

|  |  |
| --- | --- |
|  | protected PaymentType(int value, string name = null) : base(value, name) |
|  | { |
|  | } |

[view raw](https://gist.github.com/ankitvijay/e0bc59c7b6dfd0b115f29c4167789b59/raw/e873b768872d358940977f99674468dcd85ecf1b/PaymentType.cs)
[PaymentType.cs](https://gist.github.com/ankitvijay/e0bc59c7b6dfd0b115f29c4167789b59#file-paymenttype-cs)
hosted with ❤ by [GitHub](https://github.com)

We then introduce **StatesPaymentType**for the US region derived from PaymentType.

This file contains hidden or bidirectional Unicode text that may be interpreted or compiled differently than what appears below. To review, open the file in an editor that reveals hidden Unicode characters.
[Learn more about bidirectional Unicode characters](https://github.co/hiddenchars)

[Show hidden characters]({{ revealButtonHref }})

|  |  |
| --- | --- |
|  | public abstract class StatesPaymentType : PaymentType |
|  | { |
|  | public static readonly PaymentType Bitcoin = new BitCoinType(); |
|  |  |
|  | private class BitCoinType : PaymentType |
|  | { |
|  | public BitCoinType() : base(3, "Bitcoin") |
|  | { |
|  | } |
|  |  |
|  | public override string Code => "BT"; |
|  | } |
|  |  |
|  | protected StatesPaymentType(int value, string name = null) : base(value, name) |
|  | { |
|  | } |
|  | } |

[view raw](https://gist.github.com/ankitvijay/92a351ac0c4056858ef844feec7ae6f9/raw/f172b3b1c408e17149372473e062a0a75ad27e56/StatesPaymentType.cs)
[StatesPaymentType.cs](https://gist.github.com/ankitvijay/92a351ac0c4056858ef844feec7ae6f9#file-statespaymenttype-cs)
hosted with ❤ by [GitHub](https://github.com)

As you can see, this is a simple solution to extend the PaymentType with an additional option for the US.

Here are tests for our newly created StatesPaymentType Enumeration class.

This file contains hidden or bidirectional Unicode text that may be interpreted or compiled differently than what appears below. To review, open the file in an editor that reveals hidden Unicode characters.
[Learn more about bidirectional Unicode characters](https://github.co/hiddenchars)

[Show hidden characters]({{ revealButtonHref }})

|  |  |
| --- | --- |
|  | public class InheritanceExample1Tests |
|  | { |
|  | [Fact] |
|  | public void CanReadAllPaymentTypesForUnitedStates() |
|  | { |
|  | Assert.Equal("CC", StatesPaymentType.CreditCard.Code); |
|  | Assert.Equal("DC", StatesPaymentType.DebitCard.Code); |
|  | Assert.Equal("BT", StatesPaymentType.Bitcoin.Code); |
|  | } |
|  |  |
|  | [Fact] |
|  | public void CommonPaymentTypesAreEqual() |
|  | { |
|  | Assert.Equal(PaymentType.CreditCard, StatesPaymentType.CreditCard); |
|  | Assert.Equal(PaymentType.DebitCard, StatesPaymentType.DebitCard); |
|  | } |
|  |  |
|  | [Fact] |
|  | public void CanReadAllPaymentTypesForRestOfTheWorld() |
|  | { |
|  | Assert.Equal("CC", PaymentType.CreditCard.Code); |
|  | Assert.Equal("DC", PaymentType.DebitCard.Code); |
|  | } |
|  | } |

[view raw](https://gist.github.com/ankitvijay/9e0b8542a7ca973a3a70df791b923708/raw/ddc6d343f2a591b3b64234bc21fb49204e78d625/InheritanceExample1Tests.cs)
[InheritanceExample1Tests.cs](https://gist.github.com/ankitvijay/9e0b8542a7ca973a3a70df791b923708#file-inheritanceexample1tests-cs)
hosted with ❤ by [GitHub](https://github.com)

The solution is all good except, when you try to access the parent PaymentType values from StatesPaymentType, you will get a warning to use a base class qualifier.

![](https://ankitvijaydotin.wordpress.com/wp-content/uploads/2022/12/6674c-solution1-warning-1.png)

*Figure 1: Warning – Use base class qualifier*

### Solution 2

In our second attempt, we try to solve this problem by *hiding*parent property using a **new**modifier.

First, we update PaymentType further by making more members protected. 

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
|  | protected PaymentType(int value, string name = null) : base(value, name) |
|  | { |
|  | } |
|  |  |
|  | protected class DebitCardType : PaymentType |
|  | { |
|  | public DebitCardType() : base(0, "DebitCard") |
|  | { |
|  | } |
|  |  |
|  | public override string Code => "DC"; |
|  | } |
|  |  |
|  | protected class CreditCardType : PaymentType |
|  | { |
|  | public CreditCardType() : base(1, "CreditCard") |
|  | { |
|  | } |
|  |  |
|  | public override string Code => "CC"; |
|  | } |
|  | } |

[view raw](https://gist.github.com/ankitvijay/a3e87ba586a7a6d588f38e11f4b6ff2d/raw/593954d0c1059dc9a79dd702a87c9ac7664f4f47/PaymentType.cs)
[PaymentType.cs](https://gist.github.com/ankitvijay/a3e87ba586a7a6d588f38e11f4b6ff2d#file-paymenttype-cs)
hosted with ❤ by [GitHub](https://github.com)

Next, we update the StatesPaymentType Enumeration class is as below.

This file contains hidden or bidirectional Unicode text that may be interpreted or compiled differently than what appears below. To review, open the file in an editor that reveals hidden Unicode characters.
[Learn more about bidirectional Unicode characters](https://github.co/hiddenchars)

[Show hidden characters]({{ revealButtonHref }})

|  |  |
| --- | --- |
|  | public abstract class StatesPaymentType : PaymentType |
|  | { |
|  | public new static readonly PaymentType DebitCard = new DebitCardType(); |
|  |  |
|  | public new static readonly PaymentType CreditCard = new CreditCardType(); |
|  |  |
|  | public static readonly PaymentType Bitcoin = new BitCoinType(); |
|  |  |
|  | private class BitCoinType : PaymentType |
|  | { |
|  | public BitCoinType() : base(3, "Bitcoin") |
|  | { |
|  | } |
|  |  |
|  | public override string Code => "BT"; |
|  | } |
|  |  |
|  | protected StatesPaymentType(int value, string name = null) : base(value, name) |
|  | { |
|  | } |
|  | } |

[view raw](https://gist.github.com/ankitvijay/f2cb6ea8414dac1b1056e92690da7fa1/raw/47cb08accd7c81adb0ddb45bac93f9a0fc8914a8/StatesPaymentType.cs)
[StatesPaymentType.cs](https://gist.github.com/ankitvijay/f2cb6ea8414dac1b1056e92690da7fa1#file-statespaymenttype-cs)
hosted with ❤ by [GitHub](https://github.com)

Note that anewmodifieris **forbidden** in general, as it can lead to some [unexpected behavior and side-effects](https://www.codeproject.com/Articles/1215488/Be-careful-using-new-modifier-in-your-Csharp-code). However, in a scenario where we understand the risk, and there is no possible side effect, a new modifier can help solve some unique use-cases.

With this little tweak, we no longer get the warning as in the first solution. 

## Conclusion

This post demonstrates how the Enumeration class can help you solve Enum type limitation with inheritance.

This post is also a wrap of my series on the Enumeration class. I hope you found this series useful. Please feel free to reach out to me on [twitter](https://twitter.com/vijayankit) or the comments section if you have any feedback. 🙂
