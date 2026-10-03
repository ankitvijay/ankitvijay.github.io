---
title: "MICROSOFT BOT FRAMEWORK – PART 3: Add channels to bots"
date: "2017-09-17T08:18:58+10:00"
lastmod: "2017-09-29T06:02:23+10:00"
url: "/2017/09/17/microsoft-bot-framework-part-3-add-channels-to-bots/"
slug: "microsoft-bot-framework-part-3-add-channels-to-bots"
wp_id: 2691
category: ["bot", "faq", "net", "qna-service"]
tag: ["bot", "bot-framework", "microsoft-bot-framework"]
summary: "This is part 3 (and possibly the final) of Microsoft Bot Framework Series. If you have jumped right here, you may want to look into my part 1 and part 2 of my blog. In this post, I will explain how to add different channels to the Microsoft Bot Microsoft Bot Framework provides the option"
---

This is part 3 (and possibly the final) of Microsoft Bot Framework Series. If you have jumped right here, you may want to look into my [part 1](/2017/09/08/microsoft-bot-framework-part-1-qna-service/) and [part 2](/2017/09/12/microsoft-bot-framework-part-2/) of my blog. In this post, I will explain how to add different channels to the Microsoft Bot

Microsoft Bot Framework provides the option to add a variety of channels like Web, Bing, Team, Facebook Messanger, Slack, Telegram, Twilio etc. I will focus on the web, Skype and Facebook Messanger channels here.

You can add these channels directly from Azure Portal or through [Bot Framework Portal](https://dev.botframework.com/). I personally found the experience of managing Bots from the Bot Framework Portal more convenient.

- Go to [Bot Framework Portal](https://dev.botframework.com/) -> My Bot and select the Bot you created in the last step
- Under the “Channels” link you will find **Skype** and **Web Chat** channel are added to Bot by default.

![DefaultChannels.PNG](https://ankitvijaydotin.wordpress.com/wp-content/uploads/2017/09/defaultchannels.png)

Default Channels

## Connect to Skype Channel

- To test the Skype Bot, select Skype link and you will be redirected to **Add Skype Bot to Contact** screen. Click on the button to add the Bot to your Skype Account.

![AddSkypeBotToContacts.PNG](https://ankitvijaydotin.wordpress.com/wp-content/uploads/2017/09/addskypebottocontacts.png)

Add to Contacts

- Once, you have added the Bot, you can chat with the Bot same way shown in the last post.
- To configure the Skype Channel, click on edit button. This provides you an option to embed Skype directly to your website. Additionally, you can also update other settings like messaging, calling, and groups.
- Once, you have configured your Bot. You can go ahead and **publish the Skype Bot** to distribute it to an unlimited number of users. Your request will be first reviewed, and if you adhere to [review guidelines](https://docs.botframework.com/directory/review-guidelines/) your Bot will be published.
- After your Bot has been published, any Skype User can add it to their contacts to connect to you or your organization.

![AddSkypeBot](https://ankitvijaydotin.wordpress.com/wp-content/uploads/2017/09/addskypebot.png)

Add Bot to Skype Contact

## Connect to Web Chat

- Like Skype, Web Chat is another channel that is added by default when you create your Bot
- Configuring Web Chat is very easy. Click on Edit button and you will be presented with the HTML code that needs to be embedded to your Website. Adding the web chat is as easy as adding `<iframe>` to your website.

![AddingWebChat](https://ankitvijaydotin.wordpress.com/wp-content/uploads/2017/09/addingwebchat.png)

Embed bot as webchat to your website

> WARNING: Embedding the web chat control in your website using the secret is **NOT SECURE** as your secret key gets exposed with the `HTML`. Please exercise caution before using this option. Read more about connecting to Web Chat channel [here](https://docs.microsoft.com/en-us/bot-framework/channel-connect-webchat).

## Connect to Facebook Messager

- As a **pre-requisite** to Add Facebook Messanger channel to your Bot you would need a Facebook Page and Facebook App.
- Select **Facebook Messager** option to Facebook Messanger channel to your Bot.

![AddFMChannel](https://ankitvijaydotin.wordpress.com/wp-content/uploads/2017/09/addfmchannel.png)

Add Facebook Messanger Channel

- Next, you will need to provide Facebook Page Id, Facebook App Id, Facebook App Secret and Page Access Token. Please follow [this link](https://docs.microsoft.com/en-gb/bot-framework/channel-connect-facebook) to understand how to do so in depth.

![FMCred](https://ankitvijaydotin.wordpress.com/wp-content/uploads/2017/09/fmcred.png)

Your Facebook Messanger Credentials

- You would now, need to provide the Callback URL and Verify Token to Facebook. The above link also explains it in details. Hence, I will skip this step.
- Once, you have filled in all the required information you would need to Publish your app for review. Please go through the [submission guidelines](https://developers.facebook.com/docs/apps/review/) and submit your app for review.

That’s it. You now have FAQs of your organization available as chat on your website, Skype and Facebook messenger in few simple steps.

What’s next? The possibilities with Microsoft Bot Framework are enormous. What I have shown in these 3 posts is just a small preview of what you can achieve in a matter of hours. For more details on Bot Framework, please go through their [docs](https://docs.microsoft.com/en-us/bot-framework/).

Hope you liked the post. Please keep the feedback coming 🙂
