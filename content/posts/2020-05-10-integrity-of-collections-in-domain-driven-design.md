---
title: "Integrity of Collections in Domain-Driven Design"
date: "2020-05-10T14:59:27+10:00"
lastmod: "2020-09-26T08:39:40+10:00"
url: "/2020/05/10/integrity-of-collections-in-domain-driven-design/"
slug: "integrity-of-collections-in-domain-driven-design"
wp_id: 4856
category: ["architecture", "architecture-and-design", "ddd", "domain-driven-design", "net-core"]
tag: ["c", "collection", "ddd", "domain-driven-design", "ienumerable", "immutablearray", "immutablelist", "ireadonlycollection", "net", "net-core"]
summary: "The post describes the issues with Collection integrity in DDD and how we can use ImmutableList to avoid manipulating collections outside the Domain."
---

Domain-Driven-Design (or DDD) helps us to move away from the anemic model towards a richer behavior. One of the core principles of DDD is to ensure that we lock down the entry-points in our domain model. We do not allow an entity outside our domain to manipulate our data or property directly. That’s why in C# we avoid having public setters on our properties.

However, does the private setters work for collections? Let me try to explain this with a simple example.

For the sake of brevity and focus on the problem statement, I will not talk about the concepts of ValueObject, Entity, or Aggregate in my example and assume that you are already aware of it.

### Version 1

Let us say we have an **OrderItem** class.

This file contains hidden or bidirectional Unicode text that may be interpreted or compiled differently than what appears below. To review, open the file in an editor that reveals hidden Unicode characters.
[Learn more about bidirectional Unicode characters](https://github.co/hiddenchars)

[Show hidden characters]({{ revealButtonHref }})

|  |  |
| --- | --- |
|  | public class OrderItem |
|  | { |
|  | public OrderItem(int orderId, string orderName) |
|  | { |
|  | OrderId = orderId; |
|  | OrderName = orderName; |
|  | } |
|  |  |
|  | public int OrderId { get; private set; } |
|  |  |
|  |  |
|  | public string OrderName { get; private set; } |
|  | } |

[view raw](https://gist.github.com/ankitvijay/fb9101904d4c027973fb84d0da44854a/raw/3803fd1d0789aa9f3006a232e41429f881495870/OrderItem.cs)
[OrderItem.cs](https://gist.github.com/ankitvijay/fb9101904d4c027973fb84d0da44854a#file-orderitem-cs)
hosted with ❤ by [GitHub](https://github.com)

Now, consider we have an **`Order`** class that contains a ReadOnly collection of `OrderItems`.

This file contains hidden or bidirectional Unicode text that may be interpreted or compiled differently than what appears below. To review, open the file in an editor that reveals hidden Unicode characters.
[Learn more about bidirectional Unicode characters](https://github.co/hiddenchars)

[Show hidden characters]({{ revealButtonHref }})

|  |  |
| --- | --- |
|  | public class Order |
|  | { |
|  | private ICollection<OrderItem> _orderItems; |
|  | public Order() |
|  | { |
|  | _orderItems = new List<OrderItem>(); |
|  | } |
|  |  |
|  | public IReadOnlyCollection<OrderItem> OrderItems |
|  | { |
|  | get => (IReadOnlyCollection<OrderItem>)_orderItems; |
|  | private set => _orderItems = (ICollection<OrderItem>)value; |
|  | } |
|  |  |
|  | public void AddOrderItem(OrderItem orderItem) |
|  | { |
|  | _orderItems.Add(orderItem); |
|  | } |
|  |  |
|  | public void RemoveOrderItem(OrderItem orderItem) |
|  | { |
|  | _orderItems.Add(orderItem); |
|  | } |
|  | } |

[view raw](https://gist.github.com/ankitvijay/a6196f80c85cc9ac3d219c9f2b91c913/raw/2c95dae1c45f51bb442f04f0acfddb01974bf798/Order.cs)
[Order.cs](https://gist.github.com/ankitvijay/a6196f80c85cc9ac3d219c9f2b91c913#file-order-cs)
hosted with ❤ by [GitHub](https://github.com)

As you can see, following the principles of DDD we do not have a public setter on **OrderItems**. The **OrderItems** can be only manipulated by calling methods **AddOrderItem** and **RemoveOrderItem**.

However, is **OrderItems** safe? Is there any way we can still manipulate the collection outside of the **Order** domain? Unfortunately, there is. Consider, below xUnit test.

This file contains hidden or bidirectional Unicode text that may be interpreted or compiled differently than what appears below. To review, open the file in an editor that reveals hidden Unicode characters.
[Learn more about bidirectional Unicode characters](https://github.co/hiddenchars)

[Show hidden characters]({{ revealButtonHref }})

|  |  |
| --- | --- |
|  | public class OrderTests |
|  | { |
|  | [Fact] |
|  | public void OrderItemsShouldNotBeManipulatedOutsideOrder() |
|  | { |
|  | var order = new Order(); |
|  | order.AddOrderItem(new OrderItem(1, "Laptop")); |
|  | order.AddOrderItem(new OrderItem(2, "Keyboard")); |
|  |  |
|  | Assert.True(order.OrderItems.Count == 2); |
|  |  |
|  | var orderItem = new OrderItem(3, "Mouse"); |
|  |  |
|  | var orderItems = (ICollection<OrderItem>)order.OrderItems; |
|  | orderItems.Add(orderItem); |
|  |  |
|  | Assert.True(order.OrderItems.Count == 2); |
|  | } |
|  | } |

[view raw](https://gist.github.com/ankitvijay/8b9722a42890b934d1f8695a73db5c89/raw/7458c64da03ff797d8048db943f7844c4dd89168/OrderTests.cs)
[OrderTests.cs](https://gist.github.com/ankitvijay/8b9722a42890b934d1f8695a73db5c89#file-ordertests-cs)
hosted with ❤ by [GitHub](https://github.com)

This test would fail at line number 17. The **OrderItems** count is 3 instead of 2. That is, we could manipulate the **OrderItem** collection outside the **Order** class. This is not ideal and violates one of the Core DDD principles to maintain [model integrity](https://en.wikipedia.org/wiki/Domain-driven_design#Strategic_domain-driven_design).

### Version 2

How can we solve this problem? The answer to that perhaps lies in **ImmutableList** (or **ImmutableArray**). From the [Microsoft documentation](https://docs.microsoft.com/en-us/dotnet/api/system.collections.immutable.immutablelist-1?view=netcore-3.1):

> ImmutableList represents an immutable list, which is a strongly typed list of objects that can be accessed by index.

The updated **Order** class after the changes would look something similar to below:

This file contains hidden or bidirectional Unicode text that may be interpreted or compiled differently than what appears below. To review, open the file in an editor that reveals hidden Unicode characters.
[Learn more about bidirectional Unicode characters](https://github.co/hiddenchars)

[Show hidden characters]({{ revealButtonHref }})

|  |  |
| --- | --- |
|  | public class Order |
|  | { |
|  | private readonly List<OrderItem> _orderItems; |
|  |  |
|  | public Order() |
|  | { |
|  | _orderItems = new List<OrderItem>(); |
|  | } |
|  |  |
|  | public IImmutableList<OrderItem> OrderItems => _orderItems.ToImmutableList(); |
|  |  |
|  | public void AddOrderItem(OrderItem orderItem) |
|  | { |
|  | _orderItems.Add(orderItem); |
|  | } |
|  |  |
|  | public void RemoveOrderItem(OrderItem orderItem) |
|  | { |
|  | _orderItems.Add(orderItem); |
|  | } |
|  | } |

[view raw](https://gist.github.com/ankitvijay/ca4a695f1bb3cc038ca2fddea507d6e2/raw/9d6b80a58c5961b80d0f2f862e9b58d0f24ab24a/Order.cs)
[Order.cs](https://gist.github.com/ankitvijay/ca4a695f1bb3cc038ca2fddea507d6e2#file-order-cs)
hosted with ❤ by [GitHub](https://github.com)

The same xUnit test after this change would throw below runtime exception on line number 15.

**System.NotSupportedException** : Specified method is not supported.
at System.Collections.Immutable.ImmutableList`1.System.Collections.Generic.ICollection.Add(T item)

### **Version 3**

Having the **ImmutableList** for collection helps us to resolve the integrity issue with our domain model. However, the above code still has a couple of issues. Unlike, IReadOnlyCollection **ImmutableList**hasan**Add** method. That means a user can call **order.OrderItems.Add(orderItem)**outside the domain. Calling the **Add**method on ImmutableList will not add an item to the collection, it just returns a copy of the list with specified object added to the list. But, this can still confuse the consumer.

In addition to this, **OrderItems** is not **Serializable** without a private setter. If we try to save our domain model in NoSql DBs like RavenDb or CosmosDb the **OrderItems** collection would not be saved.

Also, if we try to map the domain model to a DTO using mapper libraries like Automapper, the mapping between the two objects would fail.

The fix for these issues is simple. We just need to introduce a **private setter** and expose the Collection as **IReadOnlyCollection**.

This file contains hidden or bidirectional Unicode text that may be interpreted or compiled differently than what appears below. To review, open the file in an editor that reveals hidden Unicode characters.
[Learn more about bidirectional Unicode characters](https://github.co/hiddenchars)

[Show hidden characters]({{ revealButtonHref }})

|  |  |
| --- | --- |
|  | public class Order |
|  | { |
|  | private List<OrderItem> _orderItems; |
|  |  |
|  | public Order() |
|  | { |
|  | _orderItems = new List<OrderItem>(); |
|  | } |
|  |  |
|  | public IReadOnlyCollection<OrderItem> OrderItems |
|  | { |
|  | get => _orderItems.ToImmutableList(); |
|  | private set => _orderItems = value.ToList(); |
|  | } |
|  |  |
|  | public void AddOrderItem(OrderItem orderItem) |
|  | { |
|  | _orderItems.Add(orderItem); |
|  | } |
|  |  |
|  | public void RemoveOrderItem(OrderItem orderItem) |
|  | { |
|  | _orderItems.Add(orderItem); |
|  | } |
|  | } |

[view raw](https://gist.github.com/ankitvijay/8356ea097eaa132349860d46d829215e/raw/a78d0a029f52cf9af3950d844bad391d66700584/Order.cs)
[Order.cs](https://gist.github.com/ankitvijay/8356ea097eaa132349860d46d829215e#file-order-cs)
hosted with ❤ by [GitHub](https://github.com)

That’s it! With this one small change, we can now protect our collection in the domain and also ensure that it is saved to our domain in our data-store.

### **ImmutableList** vs ImmutableArray

The above example can also be replaced by **ImmutableArray** instead of **ImmutableList**. The Microsoft link [here](https://docs.microsoft.com/en-us/dotnet/api/system.collections.immutable.immutablearray-1?view=netcore-3.1#remarks) describes different scenarios best suited for either.

**TL;DR**: If updating the data is rare or number expected elements are less than 16 items, then **ImmutableArray** is more preferable than an **ImmutableList**

### **Conclusion**

**ReadOnlyCollection or IEnumerable** do not guarantee the integrity of a collection in a Domain-Driven Design. To ensure the collection cannot be modified outside of the domain, we can use **an ImmutableList** or **ImmutableArray** as explained above.

> Featured Photo by [Kaleidico](https://unsplash.com/@kaleidico?utm_source=unsplash&utm_medium=referral&utm_content=creditCopyText) on [Unsplash](https://unsplash.com/s/photos/business-model?utm_source=unsplash&utm_medium=referral&utm_content=creditCopyText)
