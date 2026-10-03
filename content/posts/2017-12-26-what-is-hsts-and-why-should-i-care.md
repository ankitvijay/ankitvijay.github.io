---
title: "What is HSTS and why should I care?"
date: "2017-12-26T08:43:20+10:00"
lastmod: "2017-12-30T17:18:24+10:00"
url: "/2017/12/26/what-is-hsts-and-why-should-i-care/"
slug: "what-is-hsts-and-why-should-i-care"
wp_id: 3410
category: ["hsts", "https"]
tag: ["hsts", "https", "security"]
summary: "Recently, there was an interesting conversation that happened between security expert Troy Hunt and a leading UK bank, NatWest. It all started when someone on twitter reported about the unsecured landing page of NatWest bank."
---

Recently, there was an interesting conversation that happened between security expert Troy Hunt and a leading UK bank, NatWest. It all started when someone on twitter reported about the unsecured landing page of NatWest bank.

<blockquote class="twitter-tweet" data-dnt="true" data-width="500">
<p dir="ltr" lang="en">Hi there Troy, the website contains general information, rest assured when you are logging in that the website is secure. Please feel free to DM me if you have anymore queries around this. Thank you, DC</p>
<p>— NatWest (@NatWest_Help) <a href="https://twitter.com/NatWest_Help/status/940665749668016129?ref_src=twsrc%5Etfw">December 12, 2017</a></p></blockquote>

According to the bank, their landing page does not have any sensitive information so it was OK for them to load their page on HTTP or insecure connection. This became a huge issue and even caught the attention of media.

<blockquote class="twitter-tweet" data-dnt="true" data-width="500">
<p dir="ltr" lang="en"><a href="https://twitter.com/troyhunt?ref_src=twsrc%5Etfw">@troyhunt</a> so you've made it onto the BBC main technology page <a href="https://t.co/Dwp0taYopF">https://t.co/Dwp0taYopF</a> <a href="https://t.co/4UTzBbMKBa">pic.twitter.com/4UTzBbMKBa</a></p>
<p>— Dan Clarke (@OverByDan) <a href="https://twitter.com/OverByDan/status/941339518564741121?ref_src=twsrc%5Etfw">December 14, 2017</a></p></blockquote>

Later, Troy Hunt wrote a blog post on the issue explaining why it important to have even your landing page secured or on `HTTPS`. [Here](https://www.troyhunt.com/im-sorry-you-feel-this-way-natwest-but-https-on-your-landing-page-is-important/) is the blog post. To their credit, NatWest pulled up their socks quickly and went https on their landing page.

If you haven’t read Troy Hunt’s post, I would recommend you to go through his post where he has very well explained why even a non-sensitive webpage/ website can lead to [man in the middle](https://en.wikipedia.org/wiki/Man-in-the-middle_attack) and [phishing](https://en.wikipedia.org/wiki/Phishing) attacks.

Now, that we have established that irrespective of the content the website should ALWAYS be on https. But, immediately the next question that arises: *Is Https enough?*The answer to this, you guessed it right, is *No**.***That’s where **HTTP Strict Transport Security (HSTS)**comes into the picture. Let us dig deeper.

## Is HTTPS enough to secure your website?

Let us say your website, foo.com is on HTTPS. When a user goes to the address bar of the browser and types <http://foo.com> or simply foo.com, the request event is as follows:

- **Step 1**: The client makes an insecure (HTTP) request to the server
- **Step 2:**The server responds with [HTTP 301 or permanent redirect](https://httpstatuses.com/301). This tells to make an HTTPS request. It does so by sending the secure website URI (<https://foo.com>) in the response header.
- **Step 3:**The client makes the HTTPS request to load the page

![HSTS.png](/wp-content/uploads/2022/12/402b4-hsts.png)

HTTPS request without HSTS

As you can see, the first request here is insecure (HTTP) and this puts the request sent by the client at risk. This can potentially lead to a man-in-the-middle attack where the where the attacker could intercept the traffic and hijack the session or redirect the user to a spoof page (phishing attack). In a nutshell, this could put the client at a big risk even though the website was HTTPS

## HSTS comes to your rescue

The solution to the above issue is HTTP Strict Transport Security or HSTS. According to [wiki](https://en.wikipedia.org/wiki/HTTP_Strict_Transport_Security):

> **HTTP Strict Transport Security** (**HSTS**) is a web security policy mechanism which helps to protect websites against protocol downgrade attacks and cookie hijacking. It allows web servers to declare that web browsers (or other complying user agents) should only interact with it using secure HTTPS connections, and never via the insecure HTTP protocol.

To enable HSTS, the server adds following header in the HTTPS reply:

> Strict-Transport-Security: max-age=1234578;

Where max-age defines the number of seconds the current domain should only be contacted over HTTPS. So, even if the user types <http://foo.com> or foo.com on the browser, HTTPS is the default for the period of time max-age is defined. There is no 301 permanent redirection, but a [307 temporary redirection](https://httpstatuses.com/307). This way, HSTS can help prevent man-in-the-middle attack and spoofing.

To read more about how to implement HSTS on your server, please follow [this](https://www.globalsign.com/en/blog/what-is-hsts-and-how-do-i-use-it/) link.

However, implementing HSTS alone does not solve the problem completely. There is one issue still remaining: [Trust On First Use (TOFU)](https://en.wikipedia.org/wiki/Trust_on_first_use).

Even when you have implemented HSTS policy **very first request** from the browser is still insecure. Any subsequent request will have the HSTS header, but not the first request.

## HSTS Preload

The solution to this issue is HSTS preload. As the name suggests, with HSTS preload the browser is already aware that domain is HTTPS/ secure and it pushes HSTS even for the **first request.**To enable HSTS preload you need to register your domain on <https://hstspreload.org>. This site is part of [Chromium project](https://www.chromium.org/) and compiles the list of domains which are HTTPS only. Most of the modern browsers like Chrome, Firefox, Opera, Safari, IE11 and Edge respect the HSTS preload list.

This prevents the browser to make the first request on HTTP to the server. This way the attacker cannot intercept the request.

## Conclusion

Security our website is as important as building website. It is our responsibility to ensure that user data is not compromised in any way. We need to ensure that we do whatever it takes to keep our users safe.

**References**

- <https://www.chromium.org/>
- <https://en.wikipedia.org/wiki/HTTP_Strict_Transport_Security>
- <https://www.globalsign.com/en/blog/what-is-hsts-and-how-do-i-use-it/>
- <https://app.pluralsight.com/library/courses/https-every-developer-must-know>
