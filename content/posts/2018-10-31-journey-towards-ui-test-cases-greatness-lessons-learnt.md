---
title: "Journey towards UI tests greatness – Lessons Learnt"
date: "2018-10-31T08:08:48+10:00"
lastmod: "2022-12-23T23:04:46+10:00"
url: "/2018/10/31/journey-towards-ui-test-cases-greatness-lessons-learnt/"
slug: "journey-towards-ui-test-cases-greatness-lessons-learnt"
wp_id: 3763
category: ["automation-testing", "continuous-delivery", "continuous-integration", "devops", "selenium", "specflow", "testing", "ui-testing"]
tag: ["automated-testing", "c", "ci-cd", "net", "selenium", "testing", "ui-test"]
summary: "A bit of a background I work on a long-running running project in our organization. We have a CI/CD pipeline for our project following the GitHub flow and backed by thousands of unit tests, hundreds of integration tests. However, until recently we were missing a key piece to the puzzle. UI Tests!"
---

## **A bit of a background**

I work on a long-running running project in our organization. We have a CI/CD pipeline for our project following the GitHub flow and backed by thousands of unit tests, hundreds of integration tests. However, until recently we were missing a key piece to the puzzle. UI Tests!

It’s not that we did not have UI tests, we had plenty (rather just too many) but we were not able to run them on our build server with **confidence** for the reasons I will go into later. And since UI tests were not running on every build, we still needed to verify each build for regression. In short, we were not really doing a **Continuous Delivery**. Our QA as smart he is, then built his own set of UI test suite which he would run on every build to validate the quality of the build.

## Why we were not able to run UI tests with Confidence

- Our UI tests were **flaky**. The tests would fail often to due ***external factors*** especially on the build server***.*** On top of it, the very nature of UI tests is that they are very slow as compared to unit tests or integration tests. To run the entire test suite every time a test failed due to some *external factors* wasted a lot of time.
- Our UI tests were **brittle.** They were trying to do more than a UI test. They were heavily reliant on the HTML page structure. As a result, they would fail even with minimal changes.
- The flaky and brittle nature of UI tests meant that the developers lost trust in the UI test framework. As a result, they were **not well maintained**.
- The UI tests were flooded with a lot of a **Thread.Sleep**. And Thread.Sleep led to two bigger issues:
  - There was no way we could know what was the right delay. Each second delay added had a ripple effect on the already slow tests
  - In spite of adding the delays, there was no guarantee that the tests would pass.
- The UI tests did **not** really represent the **business scenarios**. They were written more with an idea of testing the UI elements. Hence, at times we end up testing not the actual business use case.
- The tests **did not** follow **SOLID** and **DRY** principles. They never got the same love and treatment as application code. This made them difficult and harder to maintain.

## **Fixing the broken tests**

We are a very small team of dev and single QA. However, we deliver the new business features and bug-fixes at a very high velocity. As the complexity of the solution started growing it became more evident and obvious to that we cannot deliver the solution with a high confidence without the UI tests. Our QA was forced to focus more on mundane testing rather than planning ahead for the next User Stories.

That’s when we took a step back and decided to do something about it. We listed down our pain-points with existing UI framework and worked upon each point to develop **UI framework 2.0**. The ultimate aim of this exercise was to resolve the above issues and start running the tests as part of our CI/CD pipeline.

## The Solution

- **Put business first** – To ensure that we do not repeat our mistakes we started our UI tests with the question how would our consumers use our application. We worked with our QA to get the list of important business scenarios. We planned our test cases BDD style and chose [SpecFlow](https://wordpress.com/post/ankitvijay.net/3763) to write our tests. SpecFlow allowed us to write tests in such that both our BA and QA could easily understand the test cases and even contribute to the tests. While planning for the test cases we kept reminding ourselves of [Test Pyramid](https://martinfowler.com/bliki/TestPyramid.html).
- **Follow good development practices –** The UI test framework was no longer a rejected child. We developed the framework same way as we would write an application code. The tests followed SOLID and DRY principles. All the components such as SpecFlow, Business Logic, Selenium were loosely coupled. The framework allowed Dev to not worry about the low-level UI elements but only what steps needed to be executed in a scenario.
- **No Thread.Sleep –** Thread.Sleep in UI tests is evil. At the start, it looks to be the solution to every problem. But soon it starts creating problems. The framework 2.0 did not use Thread.Sleep anywhere (or may just one place :)). The **Thread.Sleep** was replaced by Selenium [implicit and explicit](https://www.seleniumhq.org/docs/04_webdriver_advanced.jsp) waits. This helped us keep the tests fast and reliable.
- **Compatible with Feature Flags –** I mentioned in one of my [older posts](/2017/10/08/launch-darkly/) that we use Launch Darkly for feature flag management. The new UI framework allowed us to test scenarios with different feature flag variations (example: feature turned OFF/ ON). Feature flags were an essential part of our tests as they could vary depending on the environment, flow etc. Hence, it was important for us to be able to test all the variations easily.
- **Retry Policy** – In spite of all the goodness mentioned in the above points, the UI test suite could still fail due to factors beyond our control. That’s where we decided to add retry policy. The retry policy was defined at two levels:
  - Retry the ***action,*** if the action failed in the first attempt.
  - Retry the ***test case***, if the test failed in the first attempt.

Developing UI framework 2.0 was a journey and it took quite some time and effort for us to reach to the point where we could start running our UI tests as part of our CI/CD pipeline again. As we worked on the framework to get the constant feedback, we ran the UI tests on the build server separate to our CI/CD pipeline. Running the UI tests in a separate build allowed us to make improvements to the framework without impacting the business-as-usual. And once we had enough confidence in our UI tests we got rid of the separate build and made the UI tests part of the mainline build.

## **What’s Next**

There is no such thing as a perfect solution or framework. We intend to improve the framework further. Few things which we are looking to improve in future are:

- Run tests in parallel to reduce the build time on the server
- Add more complex business scenarios to bring the test effort to minimal
- Integrate tests with [BrowserStack](https://www.browserstack.com/) to across the platform and devices. Check out my [post](/2018/06/15/cross-browser-testing-through-browserstack/) to know more about BrowserStack.
