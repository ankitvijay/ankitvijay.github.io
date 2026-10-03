---
title: "Testing in Modern App Development"
date: "2017-06-18T18:43:45+05:30"
lastmod: "2018-10-30T07:48:30+10:00"
url: "/2017/06/18/testing-in-modern-app-development/"
slug: "testing-in-modern-app-development"
wp_id: 2011
category: ["testing"]
tag: ["net"]
summary: "I’m back to writing blogs after a small break. Things have changed for me personally since, I have made a career move recently. I hope to be more regular going forward. In my new team, we follow Kanban flow. Our application is customer facing and due to nature of our project we need to do a"
---

I’m back to writing blogs after a small break. Things have changed for me personally since, I have made a career move recently. I hope to be more regular going forward.

In my new team, we follow [Kanban flow](https://kanbanflow.com/). Our application is customer facing and due to nature of our project we need to do a frequent releases. This means we need to deliver the features faster and an external application the code quality and UI needs to be of the highest quality.

While quality of the product has been centre piece of all my projects,  I have been in discussion with my manager lately on our approach towards testing. The project complexity is growing each day and we are adding new features to application at very a fast pace, but team size remains constant. Hence, there has been increased need of changing the way we look at our development and especially QA process.

In modern app development it has become increasingly important to write ready to ship code. While no one can claim to [write a bug free code](https://en.wikibooks.org/wiki/Bug_Free_Programming), ensuring the quality of the product is no longer just the responsibility of QA. The responsibility of writing a reliable code lies equally on the developer team. In the past dev and QA used to be different departments in an organization. But, this trend is changing. The Dev and QA are now part of **one project**/ **one team**. The line between a developer and QA is diminishing. As a  developer you should be prepared to test your own and your peer’s code.

In this blog, I’m not trying to explain meaning of each level of testing, I believe every developer knows it already. I’m trying to explain their significance in the app development and how they can help you develop feature faster, prevent bugs and improve quality. I also try to give examples from my own experiences.

## **Unit Testing**

Unit testing is the first and probably the most important pillar of a resilient code. Many times it may seem the unit testing is rather **imposed** by the organization than developer understanding the true value for it. The result is bad unit tests. I feel a **bad unit test case is even worse than no unit test case.**If as a developer you are writing just to get the unit test case coverage or because someone else has asked you to do so, you need to think again. Writing a unit test case to just achieve the code coverage gives the team false assurance that the each line of code has been unit tested. **Code coverage is a necessary but not a sufficient condition**. Quality of unit test case is more important than code coverage. Additionally, the naming convention of a unit test case should reflect the intension of the test case. Example of a bad unit test case name is `PopTest`, and a good unit test case name could be `PopStackWithNoItemShouldFail`

While, I do not have any strong preference for Test Driven Development (TDD), I do feel it is one of the better ways to unit test your application. Even if you do not follow TDD your UTs should be written after you have developed a part of your logic/ feature rather than after writing the entire functionality/ feature.

Consider this scenario: You are working on a web application with a significantly complex flow. Now, you need to make a small change but one which has a huge impact in your entire application.  If you test these changes  directly from web app, you would end up spending significant amount of time to validate all the basic test cases like null check, input validation etc. And even then, you cannot be sure to cover all the test cases.  That’s where, unit test cases come handy. You just test your **Unit of work.** You can test all the flows/ conditions in your code way faster. Once, you are satisfied with the changes you may proceed to test your app at higher level. Remember even if  it is time consuming to write unit test cases, it is way cheaper to make changes to the code at this stage.

## Integration Testing

Integration testing is the second level of defence for your code. Consider the same example as before, your small change has an indirect impact on some other module of your web application and you may not be even aware of it. Since, you have tested your part you happily deliver this code to your test. But what do you get? **Regression bugs**. The cost of a regression bug is very high in software development lifecycle. Integration testing helps you prevent those regression bugs. Many times, developers do not understand the importance of integration tests. It might look like it is waste of time to write and maintain them. But, it is **not a waste of time.**The integration tests you gives the team confidence that code changes they have made do not break other functionality.

You can also bind the business requirements to your code (BDD) through integration tests. [Specflow](http://specflow.org/)  is one of widely use framework in .NET to define business behaviour in your code. It bridges the gap between business and technology. The granularity of test cases can vary from project to project. In one of my previous projects, we used to have a test case for all the acceptance criteria (ACs) for a User Story. This helped us validate and confirm the requirements well before it reaches to testing. If your integration test cases are good enough and complete, then you can reduce the chances of functional bugs at the time of QA significantly.

## UI Automation Testing

Automation Testing, I believe has never not got enough love from developers. It is not consider part of development and many times it is left to QA. The QAs too keep it restricted to [Build Verification Tests/ Smoke Tests](https://en.m.wikipedia.org/wiki/Smoke_testing_(software)). The dynamics of team has changed rapidly as the organizations move towards Agile. The number of testers per developers are lesser than traditional development lifecycle. Yet, the complexity of code has increased significantly and you are suppose to deliver high quality ready-to-ship code. UI Automation plays a very important role in this. I believe the responsibility of writing the UI Automation tests for their features should lie on developers. This may seem overkill initially and it may look like that it reduces team velocity. But again, once your initial set up is done it will be much faster to write the automation tests. [Selenium](http://www.seleniumhq.org/) and [Coded UI](https://msdn.microsoft.com/en-us/library/dd286726.aspx) are two UI automation frameworks in .NET. In our team, while we have very good UI Automation already, we are undergoing a shift towards our approach to Automation testing. We intend to automate complex workflows and scenarios, making it ***data-driven*** using external data source like excel. Additionally, we plan to run the UI test cases as part of Pull Request build (we use Git as source control). This essentially means the code cannot be merge to the master if the UI Test cases are failing. This also means our master branch is  ***always*** ready to ship. Well… Almost!! 🙂

## Manual Testing

The last pillar of testing before the code is ready to ship or move to UAT is Manual testing. If you have followed all the previous steps thoroughly, then manual testing becomes more of a validation. If a tester is able to find the most basic or obvious bugs in the application, then there is something wrong with process you are following as a team.

Personally, I prefer the QA to be part of development team only and not a separate department. When QA comes from a different department within an organization, then their end goals can be different. Instead of developers and QAs having discussion on the priority or severity of bug or whether it is a regression or existing bug, the conversation needs to move to what it takes to provide a stable quality build.

Please share your experiences of testing in your projects. 🙂
