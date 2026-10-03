---
title: "Microsoft Bot Framework – Part 2: Publish Bot Service to Azure"
date: "2017-09-12T01:43:23+05:30"
lastmod: "2022-12-23T23:04:46+10:00"
url: "/2017/09/12/microsoft-bot-framework-part-2/"
slug: "microsoft-bot-framework-part-2"
wp_id: 2582
category: ["azure", "bot", "c", "net"]
tag: ["azure", "bot", "bot-framework", "c", "faq", "microsoft-bot-framework", "net", "qna-service"]
summary: "This blog post is Part 2 of how to create a chat bot with Microsoft Bot Framework which can answer FAQs on your website. This is in continuation to my previous post where I explained how to create a QnA service using Microsoft QnA service maker. You can read Part 1 of my post here."
---

This blog post is Part 2 of how to create a chat bot with Microsoft Bot Framework which can answer FAQs on your website. This is in continuation to my previous post where I explained how to create a QnA service using Microsoft QnA service maker. You can read Part 1 of my post [here](https://ankitvijaydotin.wordpress.com/2017/09/08/microsoft-bot-framework-part-1-qna-service/).

In this post, I will demonstrate how to deploy the service we previously created on Azure. The only pre-requisite is to have an Azure account. You can sign up for [free](https://azure.microsoft.com/en-gb/free/).

Log in to your Microsoft Azure account and search for “Microsoft Bot Framework”, you should get one result “Bot Service”. Select the Bot Service to proceed and click **Create**. At the time of writing **Bot Service** is still in preview.![Azure-BotService](https://ankitvijaydotin.wordpress.com/wp-content/uploads/2017/09/azure-botservice.png)

- Next, provide the name of your app, select hosting plan and click **Create.**The app service will be created within few minutes.
- Next, select the service created in the last step and you will get a screen similar to below.

![RegisterBot.PNG](https://ankitvijaydotin.wordpress.com/wp-content/uploads/2017/09/registerbot.png)

- Follow the steps to register your bot with**Microsoft App Id.**
- In the next step, choose the language you are comfortable in developing your bot framework. Currently, C# and NodeJS are supported.

> **Note:**  Your initial code will be **auto-generated** when you create a bot. So, you do not need to jump to the code right away.

- Next, you get an option to choose a template. Select template **Questions and Answer**and click **Create.**

![CreateBot](https://ankitvijaydotin.wordpress.com/wp-content/uploads/2017/09/createbot.png)

- In the next step, you can integrate the QnA service created in **Part 1****.**Sign in with your QnA maker account credentials, select your existing knowledge base from the drop-down and click OK.

![QnAMakerSelectKnowledgeBase](https://ankitvijaydotin.wordpress.com/wp-content/uploads/2017/09/qnamakerselectknowledgebase.png)

- This will provision your bot and deploy your Bot Service. It can take few minutes to complete this step.
- Next, you will be asked how to work with your code. You can choose to edit in online editor, download source code Zip or set up continuous deployment from your source control.
- That’s it, you can now test your Bot by clicking “**Test**”  button on the top right.

![TestingMicrosoftBot](https://ankitvijaydotin.wordpress.com/wp-content/uploads/2017/09/testingmicrosoftbot.png)

In the next post, I will explain how to connect to different channels like Skype, Web Chat, Facebook Messenger etc. from your Bot Framework.

Stay Tune! 🙂
