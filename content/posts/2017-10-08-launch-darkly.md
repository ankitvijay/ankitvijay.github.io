---
title: "Feature Management with Launch Darkly"
date: "2017-10-08T17:15:18+10:00"
lastmod: "2019-02-15T09:40:09+10:00"
url: "/2017/10/08/launch-darkly/"
slug: "launch-darkly"
wp_id: 3167
category: ["continuous-delivery", "continuous-integration", "devops", "git", "testing"]
tag: ["cd", "ci", "launch-darkly", "net"]
summary: "In my workplace, our project is set up for Continuous Delivery. We do a production deployment almost daily and sometimes even more than once in a day. Ours is a fairly big solution built primarily on Microsoft technologies and Git as a Source Control. Setting up CI/ CD for your solution is easier said than"
---

In my workplace, our project is set up for Continuous Delivery. We do a production deployment almost daily and sometimes even more than once in a day. Ours is a fairly big solution built primarily on Microsoft technologies and Git as a Source Control.

Setting up CI/ CD for your solution is easier said than done. You may be working on one big feature which comprises of several User Stories. How do you make sure to do a Continous Delivery then? How do you make sure that your Master branch is always production ready? How do you make sure that you do not leak an untested or incomplete feature to production?

Well, this is definitely not a trivial problem to solve. One of the ways developers have solved this issue in the past is using **Feature Toggles**. That is, whatever new functionality you are working on you hide under a boolean flag sitting somewhere in your database. This gives you the flexibility to develop your feature under a feature flag and still continuously deliver other features to production.

While saving the feature toggles in DB is quite common in Modern App development, it has its own disadvantages. Maintaining the feature toggles can become a huge project in itself. For example, you may want to expose a particular set of functionality for a subset of your users, or you may want to have a different set of styles based on user regions. It is of course not impossible to develop this logic with creepy `if` and `else` conditions in your project. However, it is can soon turn out to be a maintenance headache. It takes you away from your core development and you get trapped in a lot of unnecessary lines of code in your project. To add to your problems, once your feature is complete, you now need to clean up your code and remove all those conditions from your code. Again, this can lead to potential bugs. All these issues can take your lot of time and effort.

This is where [Launch Darkly](https://launchdarkly.com/) can come to your rescue. Launch Darkly provides you one single stop for feature management. We switched to Launch Darkly recently in our project and do not regret the decision.

Below are the few advantages of using Launch Darkly over maintaining feature toggles within your project:

- Launch darkly provides you a User-Friendly dashboard to manage your feature flags (or toggles).
- You can use Launch Darkly to do a percentage rollout. This can help you to reduce the risk of introducing new features in your application. Based on the feedback of subset of users, you can take an informed decision before rolling out to a larger set of users.
- You can add custom logic to your feature flag based on attributes such as age, region email etc. This means you can customize your app based on specific customer needs.
- The dashboard gives you real-time visibility of how a particular feature is being used. It maintains a great audit trail. You have access to data like when the flag was added or changed, when was the last time a feature flag was accessed etc.
- With Launch Darkly, the feature flags are no longer just boolean, it can be multi-variant like string literal, float etc. This can be especially useful when you want to drive more than simple boolean conditions from your feature flags. For example, you may want to change your application style based on region and time.
- Launch Darkly comes up with an extensive set of APIs and SDKs for all the popular platforms such as Java, JavaScript, .NET, PHP, iOS, Andriod etc. I do find lot of scope of improvement with API and SDK but I’m sure its a work in progress.

If you are facing similar challenges in your project, I would suggest giving Launch Darkly a try. If you do, please share your experience. 🙂

> **Disclaimer:** The views in this post are of my own and I do not endorse any product. Please do full research before choosing what is it right for you.
