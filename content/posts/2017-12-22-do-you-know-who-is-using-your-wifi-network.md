---
title: "Do you know who is using your Wifi?"
date: "2017-12-22T18:20:26+10:00"
lastmod: "2017-12-24T09:27:55+10:00"
url: "/2017/12/22/do-you-know-who-is-using-your-wifi-network/"
slug: "do-you-know-who-is-using-your-wifi-network"
wp_id: 3376
category: ["router", "security", "wifi"]
tag: ["isp", "router", "security", "wifi"]
summary: "A few days back, internet at my home was very slow. It took ages to open any webpage. I had found the internet to be slow on earlier occasions as well. But, this time it was just unusable. Out of curiosity, I went to the default gateway of my wireless router. I logged in with"
---

A few days back, internet at my home was very slow. It took ages to open any webpage. I had found the internet to be slow on earlier occasions as well. But, this time it was just unusable. Out of curiosity, I went to the default gateway of my wireless router. I logged in with the ***default***username and password which my Internet Service Provider (ISP) had provided. What I found after logging in blew up my mind.

There were as many as 6 active devices using my wireless connection. I had only 2 active devices (my laptop and mobile), I was shocked to see the other 4 active devices. So, it became obvious to me that some unauthorized person was using my wifi connection and this probably could be the reason for my slow internet connection. Now, I never shared my wifi network password with anyone so how was it possible for someone to leach into my wifi connection? It did not take me long to find out ***how.***

The default username and password provided by my ISP was ***admin*** and ***admin@<router>***. When you open the default gateway page the ISP name and router name are clearly visible on the page. Anyone with basic google skills or anyone who might have used services of my ISP before would not take long to determine the default username and password. And once you have that, it is like a piece of cake to get the network key. I immediately changed my default password, network key and kicked out other devices out of network. Once, I did that my internet was back to sanity.

This, however, raises some very serious questions. How many people really change their ***default*** credentials on the gateway? It is so easy for someone to sneak into your network and use your network without your permission or knowledge. The person may use your wifi for surfing the net, downloading movies from Torrent or even worst for some anti-national/ terrorist activity. He could change your network key and kick you out of your own network. And he could all these on a “secure” wifi connection. This problem is not limited to one **specific ISP.** The default credentials provided by most of the ISPs are just too easy to discover. This put us at such a huge risk.

So, what can you do? Well, for starters, go and change the default router credentials on your gateway. To know your default gateway, you can go to command prompt and type command ipconfig on your windows machine.

Please go and check if someone unknown is using your wireless connection without your permission. Be safe 🙂

Happy holidays!!!
