---
title: "Microsoft Bot Framework – Part 1: QnA Service"
date: "2017-09-08T02:28:13+05:30"
lastmod: "2017-09-29T06:04:45+10:00"
url: "/2017/09/08/microsoft-bot-framework-part-1-qna-service/"
slug: "microsoft-bot-framework-part-1-qna-service"
wp_id: 2430
category: ["azure", "bot", "faq", "microsoft-bot-framework", "qna-service"]
tag: ["azure", "bot", "bot-framework", "faq", "microsoft-bot-framework", "qna", "qna-service"]
summary: "Recently, we had a hack day in our organization. As part of Hack day, we were given one day to work on our hobby project and demonstrate it to everyone. I took that opportunity to learn more about Microsoft Bot Framework and demonstrate its capability. 6 hours later, I was ready with a prototype of a"
---

Recently, we had a hack day in our organization. As part of Hack day, we were given one day to work on our hobby project and demonstrate it to everyone.

I took that opportunity to learn more about **Microsoft Bot Framework**and demonstrate its capability. 6 hours later, I was ready with a prototype of a chat Bot which answered FAQs on the company website (in the development environment of course :)). Additionally, the chat bot was also integrated with a Facebook page and Skype Messenger. The bot was hosted on Microsoft Azure and interestingly I did not write a single line of code to get it working.

The capability of Microsoft Bot Framework really amazed me and I was inspired to create a bot called **AskAnkit** which would answer some basic question on my behalf to my audience.

In a series of blog posts,  I will illustrate step by step process you can follow to create similar service for your organization or own personal blog. In its first part, I will explain how to create a FAQ knowledge base using Microsft QnA Maker.

# Create service using Microsoft QnA Maker

As a first step, go to [Microsoft QnA Maker](https://qnamaker.ai/) and log in with your **Office 365** or **Microsoft id**. The QnA Maker helps you create a bot from FAQ in within minutes. At the time of writing the QnA Maker is still in preview.

- Once you successfully log in to QnA maker, **Create new Service**
- In the next page, provide the name of your service.
- Next, you can provide the QnA to the service in following ways:
  - **Provide link to one or more FAQ Uris of your website** (if you have one): This helps to the service to gather relevant data and extracts the list of questions and answers
  - **Upload FAQ files**: Upload the FAQ file. Supported format are .tsv, .doc, .docx, and .xslx. For example, you may create a list of common questions and answers in excel and upload it to the service.
  - **Manually add questions and answers:**You can add the questions once the service is created
- Next, just click create and you will have a QnA service up and running within seconds.

![QnA](https://ankitvijaydotin.wordpress.com/wp-content/uploads/2017/09/qna.png)

QnA Service Knowledge Base

- You can add and update your Knowledge Base and once you are satisfied, Publish the service.
- Once, you publish the service, you can call this service as an API endpoint from anywhere. The settings tab has a Sample HTTP request.
- You can use [POSTMAN](https://www.getpostman.com/), [Fiddler](http://www.telerik.com/fiddler) or any other similar tool to test your service.

![TestingQnAService](https://ankitvijaydotin.wordpress.com/wp-content/uploads/2017/09/testingqnaservice.png)

Testing QnA Service on Postman

> Note: QnA maker is nothing but a plain vanilla API service. That means you may choose to just consume this QnA service without Microsoft or any other Bot Framework on the top.
