---
title: "Running an ASP.NET Core application against multiple DB providers – Part 2"
date: "2020-01-04T08:02:04+10:00"
lastmod: "2022-12-23T23:04:47+10:00"
url: "/2020/01/04/running-an-asp-net-core-application-against-multiple-db-providers-part-2/"
slug: "running-an-asp-net-core-application-against-multiple-db-providers-part-2"
wp_id: 4429
category: ["amazon-aurora", "architecture-and-design", "asp-net-core", "aws", "integration-testing", "net-core", "net-core-2-2", "testing", "visual-studio"]
tag: ["amazon-aurora", "architecture-and-design", "azure", "azure-sql-database", "integration-testing", "mysql", "net", "sql-server", "testing", "visual-studio"]
summary: "Different approaches we considered to set up integration tests when running against multiple DB providers in ASP.NET Core"
---

This is the second and last post in the series: Running an ASP.NET Core application against Azure SQL and Amazon Aurora database provider. In [part 1 of this series](https://ankitvijaydotin.wordpress.com/2019/12/23/running-an-asp-net-core-application-against-multiple-db-providers-part-1/), I talked about how we configured our ASP.NET application to run against both the DB providers. In this part, I will talk about how we set up our integration tests.

As mentioned in the previous post, a little disclaimer first:

**Disclaimer:**This entire exercise was a POC. The actual implementation turned out to be a lot different due to the organization’s Governance model, regional limitations, and cross-cutting concerns such as authentication, logging, build and deployment pipeline, etc.

### Goal

We had set up the following goals for our integration tests:

- Minimum change to existing code base since we already had integration tests running against SQL Server before introducing the MySQL (Amazon Aurora) flavor.
- Maximum test code reuse to avoid waste and ensure we have the same tests running against both the DB providers to avoid any side effect.
- The integration tests should run against both the DB providers to ensure that any new change introduced by the developer in one provider does not break the other.
- There should still be some separation between two test suits so that they can be run independently. For example, we needed to have a separate build pipeline for each DB provider. Each build pipeline would run the integration tests for the respective DB provider.

I had raised this question on [StackOverflow](https://stackoverflow.com/questions/59208096/run-single-test-against-multiple-configurations-in-visual-studio/59348184#59348184) to get the answers from the community. And I did receive one good answer which ticked most of the requirement boxes. However, the solution fell a little short of solving our problem completely. Below, I have explained all the different approaches we considered.

### Test Set up

Our integration tests are set up using **Xunit**. We use **Microsoft.AspNetCore.TestHost** to create the **TestServer** and **TestClient**. Here is the code snippet of our setup before the introduction of new DB provider (MySQL):

This file contains hidden or bidirectional Unicode text that may be interpreted or compiled differently than what appears below. To review, open the file in an editor that reveals hidden Unicode characters.
[Learn more about bidirectional Unicode characters](https://github.co/hiddenchars)

[Show hidden characters]({{ revealButtonHref }})

|  |  |
| --- | --- |
|  | public class TestStartup : IStartup |
|  | { |
|  | public IServiceProvider ConfigureServices(IServiceCollection services) |
|  | { |
|  | var configuration = new ConfigurationBuilder() |
|  | .SetBasePath(Directory.GetCurrentDirectory()) |
|  | .AddJsonFile("appsettings.json", false) |
|  | .AddEnvironmentVariables() |
|  | .Build(); |
|  |  |
|  | services.AddMvc() |
|  | .SetCompatibilityVersion(version: CompatibilityVersion.Version_2_2); |
|  |  |
|  | // Code to add required services based on configuration |
|  |  |
|  |  |
|  | return services.BuildServiceProvider(); |
|  | } |
|  |  |
|  | public void Configure(IApplicationBuilder app) |
|  | { |
|  | app.UseMvc(); |
|  |  |
|  | // Code to configure test Startup |
|  | } |
|  | } |

[view raw](https://gist.github.com/ankitvijay/14a500e46cd5d32cdf254f5581a074e4/raw/7b98a5f91d079100b7004fbbaf92947b3b1c59a5/1_TestStartup.cs)
[1_TestStartup.cs](https://gist.github.com/ankitvijay/14a500e46cd5d32cdf254f5581a074e4#file-1_teststartup-cs)
hosted with ❤ by [GitHub](https://github.com)

This file contains hidden or bidirectional Unicode text that may be interpreted or compiled differently than what appears below. To review, open the file in an editor that reveals hidden Unicode characters.
[Learn more about bidirectional Unicode characters](https://github.co/hiddenchars)

[Show hidden characters]({{ revealButtonHref }})

|  |  |
| --- | --- |
|  | public class TestServerFixture |
|  | { |
|  |  |
|  | public TestServerFixture() |
|  | { |
|  | var builder = new WebHostBuilder().ConfigureServices(services => |
|  | { |
|  | services.AddSingleton<IStartup>(new TestStartup()); |
|  | }); |
|  |  |
|  | var server = new TestServer(builder); |
|  | Client = server.CreateClient(); |
|  | } |
|  |  |
|  | public HttpClient Client { get; private set; } |
|  | } |

[view raw](https://gist.github.com/ankitvijay/14a500e46cd5d32cdf254f5581a074e4/raw/7b98a5f91d079100b7004fbbaf92947b3b1c59a5/2_TestServerFixture.cs)
[2_TestServerFixture.cs](https://gist.github.com/ankitvijay/14a500e46cd5d32cdf254f5581a074e4#file-2_testserverfixture-cs)
hosted with ❤ by [GitHub](https://github.com)

This file contains hidden or bidirectional Unicode text that may be interpreted or compiled differently than what appears below. To review, open the file in an editor that reveals hidden Unicode characters.
[Learn more about bidirectional Unicode characters](https://github.co/hiddenchars)

[Show hidden characters]({{ revealButtonHref }})

|  |  |
| --- | --- |
|  | public class MyTest : IClassFixture<TestServerFixture> |
|  | { |
|  | private readonly TestServerFixture _fixture; |
|  |  |
|  | public MyTest(TestServerFixture fixture) |
|  | { |
|  | _fixture = fixture; |
|  | } |
|  |  |
|  | [Fact] |
|  | public async Task ShouldValidateTheGetApiResponse() |
|  | { |
|  | var result = await _fixture.Client.GetAsync("SOME_API_URL"); |
|  |  |
|  | // Code to Assert Result |
|  | } |
|  | } |

[view raw](https://gist.github.com/ankitvijay/14a500e46cd5d32cdf254f5581a074e4/raw/7b98a5f91d079100b7004fbbaf92947b3b1c59a5/3_MyTest.cs)
[3_MyTest.cs](https://gist.github.com/ankitvijay/14a500e46cd5d32cdf254f5581a074e4#file-3_mytest-cs)
hosted with ❤ by [GitHub](https://github.com)

#### **Approach 1**

The first approach that we considered came from [**@Nkosi**](https://stackoverflow.com/users/5233410/nkosi) from StackOverflow. The idea was to use **Xunit Theory** attribute to pass on DB provider-specific settings to the test method. Then, use the setting to create a separate **TestClient** and **TestServer** for each setting.

This file contains hidden or bidirectional Unicode text that may be interpreted or compiled differently than what appears below. To review, open the file in an editor that reveals hidden Unicode characters.
[Learn more about bidirectional Unicode characters](https://github.co/hiddenchars)

[Show hidden characters]({{ revealButtonHref }})

|  |  |
| --- | --- |
|  | public class TestStartup : IStartup { |
|  | private readonly string settings; |
|  |  |
|  | public TestStartup(string settings) { |
|  | this.settings = settings; |
|  | } |
|  |  |
|  | public void ConfigureServices(IServiceCollection services) { |
|  | var configuration = new ConfigurationBuilder() |
|  | .SetBasePath(Directory.GetCurrentDirectory()) |
|  | .AddJsonFile(settings, false) // Load appsettings.azure.json or appsettings.aws.json |
|  | .AddEnvironmentVariables() |
|  | .Build(); |
|  |  |
|  | services.AddMvc() |
|  | .SetCompatibilityVersion(version: CompatibilityVersion.Version_2_2); |
|  |  |
|  | //…Code to add required services based on configuration |
|  |  |
|  | } |
|  |  |
|  | public void Configure(IApplicationBuilder app) { |
|  | app.UseMvc(); |
|  |  |
|  | //…Code to configure test Startup |
|  | } |
|  | } |

[view raw](https://gist.github.com/ankitvijay/644a68a03b24520ab5d758dc2048ba78/raw/0d70e818835560bb1a889052bd454fb7efbc2bbc/1_TestStartup.cs)
[1_TestStartup.cs](https://gist.github.com/ankitvijay/644a68a03b24520ab5d758dc2048ba78#file-1_teststartup-cs)
hosted with ❤ by [GitHub](https://github.com)

This file contains hidden or bidirectional Unicode text that may be interpreted or compiled differently than what appears below. To review, open the file in an editor that reveals hidden Unicode characters.
[Learn more about bidirectional Unicode characters](https://github.co/hiddenchars)

[Show hidden characters]({{ revealButtonHref }})

|  |  |
| --- | --- |
|  | public class TestServerFixture { |
|  | static readonly Dictionary<string, TestServer> cache = |
|  | new Dictionary<string, TestServer>(); |
|  |  |
|  | public TestServerFixture() { |
|  | //… |
|  | } |
|  |  |
|  | public HttpClient GetClient(string settings) { |
|  | TestServer server = null; |
|  | if(!cache.TryGetValue(settings, out server)) { |
|  | var startup = new TestStartup(settings); |
|  | var builder = new WebHostBuilder() |
|  | .ConfigureServices(services => { |
|  | services.AddSingleton<IStartup>(startup); |
|  | }); |
|  | server = new TestServer(builder); |
|  | cache.Add(settings, server); |
|  | } |
|  | return server.CreateClient(); |
|  | } |
|  | } |

[view raw](https://gist.github.com/ankitvijay/644a68a03b24520ab5d758dc2048ba78/raw/0d70e818835560bb1a889052bd454fb7efbc2bbc/2_TestServerFixture.cs)
[2_TestServerFixture.cs](https://gist.github.com/ankitvijay/644a68a03b24520ab5d758dc2048ba78#file-2_testserverfixture-cs)
hosted with ❤ by [GitHub](https://github.com)

This file contains hidden or bidirectional Unicode text that may be interpreted or compiled differently than what appears below. To review, open the file in an editor that reveals hidden Unicode characters.
[Learn more about bidirectional Unicode characters](https://github.co/hiddenchars)

[Show hidden characters]({{ revealButtonHref }})

|  |  |
| --- | --- |
|  | public class MyTest : IClassFixture<TestServerFixture> { |
|  | private readonly TestServerFixture fixture; |
|  |  |
|  | public MyTest(TestServerFixture fixture) { |
|  | this.fixture = fixture; |
|  | } |
|  |  |
|  | [Theory] |
|  | [InlineData("appsettings.aws.json")] |
|  | [InlineData("appsettings.azure.json")] |
|  | public async Task ShouldValidateTheGetApiResponse(string settings) { |
|  | var client = fixture.CreateClient(settings); |
|  |  |
|  | var result = await client.GetAsync("SOME_API_URL"); |
|  |  |
|  | // Code to Assert Result |
|  |  |
|  | } |
|  | } |

[view raw](https://gist.github.com/ankitvijay/644a68a03b24520ab5d758dc2048ba78/raw/0d70e818835560bb1a889052bd454fb7efbc2bbc/3_MyTest.cs)
[3_MyTest.cs](https://gist.github.com/ankitvijay/644a68a03b24520ab5d758dc2048ba78#file-3_mytest-cs)
hosted with ❤ by [GitHub](https://github.com)

[Here](https://stackoverflow.com/questions/59208096/run-single-test-against-multiple-configurations-in-visual-studio/59348184) is the link to the original answer.

While this approach was a smart and simple way to solve our problem, it did not solve our problem completely. We had the following issues with the approach:

- We couldn’t run tests for **aws** or **azure** setting individually. The reason it was important for us as in the future, there *could* two different teams maintaining their specific implementation and deployment. With Theory, it becomes slightly difficult to run tests against a single DB provider.
- Our build and deployment for pipelines for each setting or DB provider were required to be different. That would mean the tests for Azure SQL and Amazon Aurora would run on a separate build pipeline. This approach made it difficult to achieve.
- While the API endpoints, **Request**, and **Response** are absolutely the same today, we do not know if it will continue to be the case as our development proceed.

#### **Approach 2**

In our second approach, we considered having a common **class** library with common Fixture and Tests as an **abstract** class.

![Approach 2 - Common integration test project](https://ankitvijaydotin.wordpress.com/wp-content/uploads/2022/12/b6158-picture1.png?w=1024&h=336)

*Approach 2 – Common integration test project*

- Here is what **Common.IntegrationTests** project looked like after the changes.

This file contains hidden or bidirectional Unicode text that may be interpreted or compiled differently than what appears below. To review, open the file in an editor that reveals hidden Unicode characters.
[Learn more about bidirectional Unicode characters](https://github.co/hiddenchars)

[Show hidden characters]({{ revealButtonHref }})

|  |  |
| --- | --- |
|  | public abstract class TestStartup : IStartup |
|  | { |
|  | public abstract IServiceProvider ConfigureServices(IServiceCollection services); |
|  |  |
|  | public void Configure(IApplicationBuilder app) |
|  | { |
|  | app.UseMvc(); |
|  |  |
|  | // Code to configure test startup |
|  | } |
|  | } |

[view raw](https://gist.github.com/ankitvijay/8c08c2e01c96cde18628e2c063cba124/raw/96d1d1d605783674ae14a7d30ae76e9977b7f5d7/1_TestStartup.cs)
[1_TestStartup.cs](https://gist.github.com/ankitvijay/8c08c2e01c96cde18628e2c063cba124#file-1_teststartup-cs)
hosted with ❤ by [GitHub](https://github.com)

This file contains hidden or bidirectional Unicode text that may be interpreted or compiled differently than what appears below. To review, open the file in an editor that reveals hidden Unicode characters.
[Learn more about bidirectional Unicode characters](https://github.co/hiddenchars)

[Show hidden characters]({{ revealButtonHref }})

|  |  |
| --- | --- |
|  | public abstract class TestServerFixture |
|  | { |
|  |  |
|  | protected TestServerFixture(IStartup startup) |
|  | { |
|  | var builder = new WebHostBuilder().ConfigureServices(services => |
|  | { |
|  | services.AddSingleton<IStartup>(startup); |
|  | }); |
|  |  |
|  | var server = new TestServer(builder); |
|  | Client = server.CreateClient(); |
|  | } |
|  |  |
|  | public HttpClient Client { get; private set; } |
|  | } |

[view raw](https://gist.github.com/ankitvijay/8c08c2e01c96cde18628e2c063cba124/raw/96d1d1d605783674ae14a7d30ae76e9977b7f5d7/2_TestServerFixture.cs)
[2_TestServerFixture.cs](https://gist.github.com/ankitvijay/8c08c2e01c96cde18628e2c063cba124#file-2_testserverfixture-cs)
hosted with ❤ by [GitHub](https://github.com)

This file contains hidden or bidirectional Unicode text that may be interpreted or compiled differently than what appears below. To review, open the file in an editor that reveals hidden Unicode characters.
[Learn more about bidirectional Unicode characters](https://github.co/hiddenchars)

[Show hidden characters]({{ revealButtonHref }})

|  |  |
| --- | --- |
|  | public abstract class MyTest |
|  | { |
|  | private readonly HttpClient _client; |
|  |  |
|  | protected MyTest(TestServerFixture fixture) |
|  | { |
|  | _client = fixture.CreateClient(); |
|  | } |
|  |  |
|  | [Fact] |
|  | public async Task ShouldValidateTheGetApiResponse() |
|  | { |
|  | var result = await _client.GetAsync("SOME_API_URL"); |
|  |  |
|  | // Code to Assert Result |
|  | } |
|  | } |

[view raw](https://gist.github.com/ankitvijay/8c08c2e01c96cde18628e2c063cba124/raw/96d1d1d605783674ae14a7d30ae76e9977b7f5d7/3_MyTest.cs)
[3_MyTest.cs](https://gist.github.com/ankitvijay/8c08c2e01c96cde18628e2c063cba124#file-3_mytest-cs)
hosted with ❤ by [GitHub](https://github.com)

- Project **AWS.IntegrationTests**

This file contains hidden or bidirectional Unicode text that may be interpreted or compiled differently than what appears below. To review, open the file in an editor that reveals hidden Unicode characters.
[Learn more about bidirectional Unicode characters](https://github.co/hiddenchars)

[Show hidden characters]({{ revealButtonHref }})

|  |  |
| --- | --- |
|  | public class TestStartup : Common.IntegrationTests.TestStartup |
|  | { |
|  | public override IServiceProvider ConfigureServices(IServiceCollection services) |
|  | { |
|  | var configuration = new ConfigurationBuilder() |
|  | .SetBasePath(Directory.GetCurrentDirectory()) |
|  | .AddJsonFile("appsettings.aws.json", false) |
|  | .AddEnvironmentVariables() |
|  | .Build(); |
|  |  |
|  | services.AddMvc() |
|  | .SetCompatibilityVersion(version: CompatibilityVersion.Version_2_2); |
|  |  |
|  | // Code to add required services based on configuration |
|  |  |
|  |  |
|  | return services.BuildServiceProvider(); |
|  | } |
|  | } |

[view raw](https://gist.github.com/ankitvijay/bad3612b9c157e2e398efc2965d6a999/raw/ecc4b421a6adcfa8f9095da967e06aa8bfafb56a/1_TestStartup.cs)
[1_TestStartup.cs](https://gist.github.com/ankitvijay/bad3612b9c157e2e398efc2965d6a999#file-1_teststartup-cs)
hosted with ❤ by [GitHub](https://github.com)

This file contains hidden or bidirectional Unicode text that may be interpreted or compiled differently than what appears below. To review, open the file in an editor that reveals hidden Unicode characters.
[Learn more about bidirectional Unicode characters](https://github.co/hiddenchars)

[Show hidden characters]({{ revealButtonHref }})

|  |  |
| --- | --- |
|  | public class TestServerFixture : Fixtures.TestServerFixture |
|  | { |
|  | public TestServerFixture() : base(new TestStartup()) |
|  | { |
|  | } |
|  | } |

[view raw](https://gist.github.com/ankitvijay/bad3612b9c157e2e398efc2965d6a999/raw/ecc4b421a6adcfa8f9095da967e06aa8bfafb56a/2_TestServerFixture.cs)
[2_TestServerFixture.cs](https://gist.github.com/ankitvijay/bad3612b9c157e2e398efc2965d6a999#file-2_testserverfixture-cs)
hosted with ❤ by [GitHub](https://github.com)

This file contains hidden or bidirectional Unicode text that may be interpreted or compiled differently than what appears below. To review, open the file in an editor that reveals hidden Unicode characters.
[Learn more about bidirectional Unicode characters](https://github.co/hiddenchars)

[Show hidden characters]({{ revealButtonHref }})

|  |  |
| --- | --- |
|  | public class MyTest : Common.IntegrationTests.MyTests, IClassFixture<TestServerFixture> |
|  | { |
|  | public MyTest(TestServerFixture fixture) : base(fixture) |
|  | { |
|  | } |
|  | } |

[view raw](https://gist.github.com/ankitvijay/bad3612b9c157e2e398efc2965d6a999/raw/ecc4b421a6adcfa8f9095da967e06aa8bfafb56a/3_MyTest.cs)
[3_MyTest.cs](https://gist.github.com/ankitvijay/bad3612b9c157e2e398efc2965d6a999#file-3_mytest-cs)
hosted with ❤ by [GitHub](https://github.com)

- Project **Azure.IntegrationTests**

A similar structure as AWS.IntegrationTests

This approach ticked all the boxes of our requirements. However, we were still not 100% convinced with the approach. There was still some waste with a lot of abstract classes and inheritance. That’s where approach 3 came into the picture.

**Approach 3**

Approach 3 more of a variant of approach 2 with a difference that instead of creating a common integration test project with **abstract** classes, we chose to create a **Shared Project**.

What is a Shared Project? From the [Microsoft documentation](https://docs.microsoft.com/en-us/xamarin/cross-platform/app-fundamentals/shared-projects?tabs=windows):

> Shared Projects let you write common code that is referenced by a number of different application projects. The code is compiled as part of each referencing project and can include compiler directives to help incorporate platform-specific functionality into the shared code base.
> Unlike most other project types a shared project does not have any output (in DLL form), instead the code is compiled into each project that references it.

Shared Project was introduced to solve a specific problem in Xamarin. However, I feel it is probably one of the most underrated and lesser-known features of .NET. Its usage goes beyond Xamarin.

With Shared Project we were able to simplify our integration tests set up quite a bit. We no longer needed unnecessary class inheritance or abstraction. Also, there was no ugliness of [link files](https://grantwinney.com/visual-studio-add-file-as-link/) since the Shared Project is part of the Visual Studio solution just like a class library.

![Approach 3 -Shared Project](/wp-content/uploads/2020/01/Picture2-3.png)

*Approach 3 – Shared Project*

To conclude, we evaluated 3 different approaches to set up our integration tests and found the last approach to be the most suitable for our needs.

I hope this series helps you solve similar problems in your workplace.
