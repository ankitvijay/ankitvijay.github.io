---
title: "Test your app across the browsers through BrowserStack"
date: "2018-06-15T09:08:28+10:00"
lastmod: "2018-10-30T07:47:21+10:00"
url: "/2018/06/15/cross-browser-testing-through-browserstack/"
slug: "cross-browser-testing-through-browserstack"
wp_id: 3683
category: ["automation-testing", "browserstack", "manual-testing", "selenium", "testing", "visual-studio"]
tag: ["automated-testing", "browserstack", "c", "manual-testing", "net", "selenium", "ui-test"]
summary: "Testing your applications cross-platform and cross-browser is not an easy problem to solve. Supporting different versions, operating systems and devices can be an extremely frustrating and time-consuming process. It can be especially painful if you need to support legacy browsers like IE 9 or IE 8."
---

Testing your applications cross-platform and cross-browser is not an easy problem to solve. Supporting different versions, operating systems and devices can be an extremely frustrating and time-consuming process. It can be especially painful if you need to support legacy browsers like IE 9 or IE 8.

We can use browser tools and emulators to test but they can only help to an extent. It requires an expensive setup of virtual machines, devices, and emulators to cover application testing across all the platforms and browsers. Yet, we cannot be 100% sure if we have covered all the scenarios. It makes us lose focus on our core objective to deliver value to our customer.

Recently, I got an opportunity to evaluate **BrowserStack** at my workplace which claims to solve the exact same problem.

As per [wiki](https://en.wikipedia.org/wiki/BrowserStack):

> **Brows****erStack** is a [cloud-based](https://en.wikipedia.org/wiki/Cloud_computing) [cross-browser](https://en.wikipedia.org/wiki/Cross-browser) testing tool that enables [developers](https://en.wikipedia.org/wiki/Web_developer) to test their websites across various [browsers](https://en.wikipedia.org/wiki/Web_browsers) on different [operating systems](https://en.wikipedia.org/wiki/Operating_system) and mobile devices, without requiring users to install [virtual machines](https://en.wikipedia.org/wiki/Virtual_machines), devices or [emulators](https://en.wikipedia.org/wiki/Emulators).

Here are few features of **BrowserStack**:

- It helps you to test your application on real browsers and devices (not emulators)
- It enables you to run automated Selenium tests on their cloud infrastructure across different browsers and devices.
- [Support](https://www.browserstack.com/docs?product=automate) for major languages such as C#, Java, NodeJS, PHP, Python, Ruby etc and test frameworks such as NUnit, SpecFlow, JUnit, etc.
- It enables you to test your local application behind the corporate firewall.
- It integrates well with the build pipeline.

![](/wp-content/uploads/2022/12/d8fd3-browesstackbrowseroptions.png)

**Browser selection in Browserstack (Image source: BrowserStack)**

![](/wp-content/uploads/2022/12/8bb0c-android-browserstack-local.png)

**Local testing on real devices on BrowserStack**

Overall, my experience using the BrowserStack was positive. Here are my key takeaways on BrowerStack:

### **The good**

- Does what it says quite well.
- Even if your organization is not deep into automation, you can take advantage of their manual testing feature which lets you test your application across
- BrowserStack has great documentation and code samples.
- Easy to run automated test cases (after initial hiccups).
- You can convert your existing Selenium UI test cases to run on BrowserStack easily by just adding [BrowserStack capabilities](https://www.browserstack.com/automate/capabilities).
- Good Support (not great)– Support is through email, a response is generally within a day.
- Great API support to extract network and console logs.
- BrowserStack creates a video of the entire automated session. Hence, you can playback the session if you need to debug an issue.

### **The bad**

- While trying to run local automated tests, resolving firewall and BrowserStack local issues took a bit of effort.
- Running tests on more browsers/ devices, means we need to take care of issues that come along. For example, a test case may run successfully for a particular browser version but the same test may fail on some other browser/device due to the way the page is being rendered or network latency.
- Support is through email, not instant via chat. Hence, it may sometimes take few days to resolve an issue.
- While the automated tests may be written in Selenium, BrowserStack may run the tests differently. For example, tests on an Apple iPhone device may run on [Appium.](http://appium.io/) As a result, you are also singing up for any limitation in the framework which BrowserStack uses internally.
- When a test fails, sometimes the exception thrown from BrowserStack is not very helping. For example one of the exceptions I received from BrowserStack was:

```
System.InvalidOperationException : Element is obscured (WARNING: The server did not provide any stacktrace information)
```

- BrowserStack does not show the status of the test correctly. Even if the test case fails, it shows the status as completed on the portal. This is not a huge an issue though, as the test cases status is still shown correctly on the test runner.

**Learnings**

- One of the side-effects of running automated tests across the variety of browsers and devices is that it can be quite time-consuming to run test cases, so it is good to run these test cases on a separate VM or nightly builds.
- Complex UI test cases are in general can be flaky. And BrowserStack may add an additional layer of complexity. As a result, sometimes a test case may fail for no particular reason. Hence, it is important to have a good retry strategy.
- It is good to have an understanding of BrowserStack-specific [capabilities](https://www.browserstack.com/automate/capabilities#) to help you configure the Selenium tests correctly. For example, your grouping of test cases, names of the test run/ build are all set through Capabilities. Hence. it is important to set them correctly to get desired results.
- Running local tests on BrowserStack adds to execution time to each test case due to additional set up and tear down process. Hence, test case execution is understandably slow as compared to local. I would recommend designing your test cases such that, they can run both locally and on BrowserStack.

If your organization has similar issues as mine, I would suggest giving BrowserStack as try. Please share your experience in the comments section. 🙂
