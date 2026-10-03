---
title: "Dispose HttpClient or have a static instance?"
date: "2016-09-25T15:21:01+00:00"
lastmod: "2018-05-18T06:49:22+10:00"
url: "/2016/09/25/dispose-httpclient-or-have-a-static-instance/"
slug: "dispose-httpclient-or-have-a-static-instance"
wp_id: 1139
category: ["c", "httpclient", "net", "visual-studio"]
tag: ["c", "httpclient", "net", "static", "visual-studio"]
summary: "Recently, I came across this blog post from ASP.NET Monsters which talks about correct using HttpClient. The post talks about issues of related to disposing HttpClient object for each request. As per the post calling HttpClient as below can lead to issues."
---

Recently, I came across [this](http://aspnetmonsters.com/2016/08/2016-08-27-httpclientwrong/) blog post from ASP.NET Monsters which talks about correct using HttpClient.

The post talks about issues of related to disposing HttpClient object for each request. As per the post calling HttpClient as below can lead to issues.

This file contains hidden or bidirectional Unicode text that may be interpreted or compiled differently than what appears below. To review, open the file in an editor that reveals hidden Unicode characters.
[Learn more about bidirectional Unicode characters](https://github.co/hiddenchars)

[Show hidden characters]({{ revealButtonHref }})

|  |  |
| --- | --- |
|  | using (var httpClient = new HttpClient()) |
|  | { |
|  | await httpClient.GetAsync(new Uri("<http://bing.com&quot>;)); |
|  | } |

[view raw](https://gist.github.com/ankitvijay/29a9929175bbf9b152653fea70900a78/raw/653f3c1c99251f7c35cec75d5cbc2b355e8dc89f/Program.cs)
 [Program.cs](https://gist.github.com/ankitvijay/29a9929175bbf9b152653fea70900a78#file-program-cs)
hosted with ❤ by [GitHub](https://github.com)

I have been using the HttpClient object like this for almost all of my projects. Hence, this post was an eye opener for me.

Also, as per the [patterns and practices](https://github.com/mspnp/performance-optimization/blob/master/ImproperInstantiation/docs/ImproperInstantiation.md) documentation:

> In a web application this technique is not scalable. Each user request results in the creation of a new HttpClient object. Under a heavy load, the web server can exhaust the number of sockets available resulting in SocketException errors.

From above two articles I could conclude, below are the major issues with disposing the HttpClient object for each request:

- The execution time of the HttpClient request is higher. This is obvious since we create and dispose the object every time for a new request.
- Disposing HttpClient object every time could potentially lead to SocketException. This is because disposing the HttpClient object does not really close TCP connection. Quoting from the ASP.NET monster post:

> ..the application has exited and yet there are still a bunch of these connections open to the Azure machine which hosts the ASP.NET Monsters website. They are in the `TIME_WAIT` state which means that the connection has been closed on one side (ours) but we’re still waiting to see if any additional packets come in on it because they might have been delayed on the network somewhere

I wanted to test the performance improvements when we create a static instance of HttpClient. The aim of my test was ONLY to see the difference of execution time between the two approaches when we open multiple connections. To test this, I wrote following code:

This file contains hidden or bidirectional Unicode text that may be interpreted or compiled differently than what appears below. To review, open the file in an editor that reveals hidden Unicode characters.
[Learn more about bidirectional Unicode characters](https://github.co/hiddenchars)

[Show hidden characters]({{ revealButtonHref }})

|  |  |
| --- | --- |
|  | namespace HttpClientTest |
|  | { |
|  | using System; |
|  | using System.Net.Http; |
|  |  |
|  | class Program |
|  | { |
|  | private static readonly int _connections = 1000; |
|  | private static readonly HttpClient _httpClient = new HttpClient(); |
|  |  |
|  | private static void Main() |
|  | { |
|  | TestHttpClientWithStaticInstance(); |
|  | TestHttpClientWithUsing(); |
|  | } |
|  |  |
|  | private static void TestHttpClientWithUsing() |
|  | { |
|  | try |
|  | { |
|  | for (var i = 0; i &lt; _connections; i++) |
|  | { |
|  | using (var httpClient = new HttpClient()) |
|  | { |
|  | var result = httpClient.GetAsync(new Uri("<http://bing.com&quot>;)).Result;} |
|  | } |
|  | } |
|  | } |
|  | catch (Exception exception) |
|  | { |
|  | Console.WriteLine(exception); |
|  | } |
|  | } |
|  |  |
|  | private static void TestHttpClientWithStaticInstance() |
|  | { |
|  | try |
|  | { |
|  | for (var i = 0; i &lt; _connections; i++) |
|  | { |
|  | var result = _httpClient.GetAsync(new Uri("<http://bing.com&quot>;)).Result; |
|  | } |
|  | } |
|  | catch (Exception exception) |
|  | { |
|  | Console.WriteLine(exception); |
|  | } |
|  | } |
|  | } |

[view raw](https://gist.github.com/ankitvijay/93c47740b5ed5242871fa654a9725cfc/raw/001b22746d14a47cba16515d2c5e13af1aa84287/Program.cs)
 [Program.cs](https://gist.github.com/ankitvijay/93c47740b5ed5242871fa654a9725cfc#file-program-cs)
hosted with ❤ by [GitHub](https://github.com)

For testing:

- I ran the code with 10, 100, 1000 and 1000 connections.
- Ran each test 3 times to find out the average
- Executed ONLY one method at a time

My machine configuration was:

![machineconfiguration](https://ankitvijaydotin.wordpress.com/wp-content/uploads/2016/09/machineconfiguration.png)

System Configuration

Below are the results from the **Visual Studio Instrumentation Profiling:**

|  |  |  |  |  |
| --- | --- | --- | --- | --- |
| Method | No Of Connections | Time in Seconds | Difference in Seconds | Performance Improvement in % |
| TestHttpClientWithUsing | 10 | 2.6 |  |  |
| TestHttpClientWithStaticInstance | 1.8 | 1 | 44 |
| TestHttpClientWithUsing | 100 | 408 |  |  |
| TestHttpClientWithStaticInstance | 240 | 168 | 70 |
| TestHttpClientWithUsing | 1000 | 241 |  |  |
| TestHttpClientWithStaticInstance | 160 | 81 | 51 |
| TestHttpClientWithUsing | 10000 | 2456 |  |  |
| TestHttpClientWithStaticInstance | 1630 | 826 | 51 |

As you can see the time of execution for the static instance is far lesser than disposable object.

Does it means we should use static client object all the time? It depends.

One of the issues people have found with static HttpClient Instance is that it does not support DNS changes. Refer [this article](http://byterot.blogspot.in/2016/07/singleton-httpclient-dns.html). For .NET application, there is a workaround available where you can you can set connnectonLeaseTimeOut by using ServicePoint object as mentioned in post.

However, for an ASP.NET Core, you may be out of luck as per [this issue](https://github.com/dotnet/corefx/issues/11224) in GitHub as similar property does not seem to exist.

Hope this post help you take informed decision in your projects. Please share your thoughts in comments section.
