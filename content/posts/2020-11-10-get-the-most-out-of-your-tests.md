---
title: "Get the most out of your tests"
date: "2020-11-10T23:03:31+10:00"
lastmod: "2020-11-11T06:46:12+10:00"
url: "/2020/11/10/get-the-most-out-of-your-tests/"
slug: "get-the-most-out-of-your-tests"
wp_id: 42884
category: ["automation-testing", "functional-tests", "integration-testing", "manual-testing", "testing", "ui-testing", "unit-testing", "xunit"]
tag: ["automated-testing", "best-practices", "functional-testing", "integration-testing", "net", "nunit", "testing", "tip", "unit-testing", "xunit"]
summary: "This post provides tips that can help you write great tests and get the best results from your test suite."
---

Some personal news, I recently switched jobs and joined [Zip Co](https://zip.co/). Could not find much time to blog as I was trying to settle in the new position. It has been a great first month at Zip, and I’m fortunate to work with some incredible engineers.

In my new team, we had some discussion around how we can get more out of our tests where I got an opportunity to share experience from my previous workplaces. I realized that I could share this across the wider audience.

The list below describes some of the practices we used to follow in my last team when it comes to writing useful tests.

**Note**: I have used the term “Tests” here loosely. The tests include Unit Tests, Functional Tests and Integration tests unless otherwise stated.

### Have a meaningful name; test name should be able to explain Given-When-Then (GWT)

While there a few ways we can arrange our tests to describe GWT. Here is one example of how we can achieve this:

- The name of the test class can denote “Given”. For example, **CreateCustomerCommandHandlerTests**name describes the tests in the class are for CreateCustomerCommandHandler
- The name of the test can provide **When**and **Then**of the information. For example, **WhenEmailIdIsInvalid_CustomerShouldNotBeCreate**
- If **When**is obvious, we may choose to ignore it. For example, **FirstNameShouldNotBeEmpty**

The end goal is that just by looking at the name of the test, a developer should be able to understand the purpose of the test.

### Code coverage is a necessary but not a sufficient condition

It is common to have build checks to fail the build if we do not meet a certain code coverage threshold. However, just the code coverage alone mustn’t drive our tests. The purpose of the tests is much more than just testing all the paths in our code. The tests should cover our technical and functional requirements.

### Tests are not step-child. Given tests the first-class treatment

Do not treat your tests differently from your code. Give them the same love. A code path is usually validated by running against multiple tests. We generally end-up having more “test” code than “real” code in our solution. Hence, it is essential to maintain the same quality standard for tests if not more. **An average code with a great test suite is better than a great code with an average test suite.** That is because we can always refactor our code. And when we refactor tests validates that we have not broken anything.

### Keep unit tests clear and concise. Do not combine multiple tests into one.

Ideally, a unit test only a assert a “unit” or a single path. Combining multiple tests makes it less meaningful. For example, let us say we need to write tests for class **CreateCustomerValidator.**It is better to have multiple tests with clearly defined Assert like **FirstNameLengthShouldBeLessThanOrEqualTo50**rather than one single test **WhenCustomerDataIsInvalid_ShouldThrowValidationError**. The issue with the latter is that it does not give any information about how the data is invalid.

### Tests are documentation

A good code is self-explanatory, and great tests are the documentation for our code. Taking the above example, **FirstNameLengthShouldBeLessThanOrEqualTo50**tells us that we have a business rule to restrict the first name to less than or equal to 50. If in future, the business rule changes we know precisely which test should break and what we need to fix.

### If we change code logic and a test does not fail, we are not testing right

Changing business logic in our code should be reflected by a failed test. If all the tests still pass even after changing a considerable part of code, it shows we have a gap in our tests.

### A bug in production? Write a test

If we find a bug in production or during the manual test, start with a test to reproduce that bug in local. The test obviously would fail first, and after fixing bug would pass. In future, if we refractor that portion of the code, we have a test which helps to validate that we do not reintroduce the same bug again. It also ensures that the overall quality of the code increases as the code matures.

### Use builder pattern to setup “Arrange” of tests

Builder patterns is a great way to set up “Arrange” of our tests. Steve Smith has written an [excellent post](https://zipmoney.atlassian.net/wiki/spaces/PLAT/pages/1138327802/Account+Cache+Builder+Debezium+-+Load+Tests) on how builder pattern can help keep our tests neat.

### Try to use rich libraries such as Shouldly or Fluent Assertion

[Shouldly](https://github.com/shouldly/shouldly) and [Fluence Assertion](https://fluentassertions.com/) are assertion frameworks which focus on giving great error messages when the assertion fails while being simple to use. They provide an extensive set of extension methods that allow us to specify the expected outcome of the tests in TDD and BDD-style. These libraries are not also not specific to a test engine such as XUnit or NUnit, so if different projects use different test engines, we still have one consistent way of Assert.

### Try to use Libraries such as Autofixture, Bogus to generate test/ fake data

The libraries such as [Autofixture](https://github.com/AutoFixture/AutoFixture)and [Bogus](https://github.com/bchavez/Bogus) make it easier for developers to do Test-Driven Development by automating non-relevant Test Fixture Setup, allowing developers to focus on the essentials of each test case. The idea is also not to reinvent the wheel by creating our own “Random-Fixture” library.

### Assert Mocks

So many times, I have seen code which “mocks” dependencies outside the class not being asserted. Not asserting mocks takes the value out of the unit tests. A test may be green even when the code is broken. All the major mock libraries such as NSubstitute, Moq, Rhino.Mocks provide an excellent way of asserting the mock result such as is the method called with the right parameters, how many times the method is called, and so on.

### If you can’t mock, use real dependencies. But still have a test.

When we write unit tests many times, we restrict our tests within a boundary such as a single class. However, many times it is not trivial to limit the test within the class for all the right reasons. In such cases, it acceptable to have tests which go beyond the boundary. Be pragmatic rather than restricting yourself to the traditional definition of tests.

### For repositories, have functional tests if it makes sense.

Our repositories do much heavy lifting. They talk to an external data source and act as an interface between our business logic and database. Writing unit tests for repositories is hard. Repositories cannot be mocked easily, and the in-memory database does emulate the same behaviour as a real “database”. In such a scenario, it is better to have functional tests rather than fighting unit tests.

### Try to have an integration test for every Acceptance Criteria of your user story

As a developer, the onus is on us to validate if requirements in the user story are clearly defined and if we have met all the acceptance criteria specified in a user story. Integration tests are a way to prove that. In a CI/CD world, every commit is a release candidate and keeping code quality high is very important. If a QA can find a glaring bug in our story or then it reflects inadequate dev testing.

## Wrapping up

I do not claim the above list to be the best or recommended practice, instead consider them as a suggestion and do what works best for your team. I hope you the post helps you to think deeper about how can improve your test suite.
