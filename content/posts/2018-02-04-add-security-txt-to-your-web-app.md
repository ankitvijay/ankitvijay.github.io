---
title: "Add security.txt to your website"
date: "2018-02-04T22:54:02+10:00"
lastmod: "2018-02-06T07:47:14+10:00"
url: "/2018/02/04/add-security-txt-to-your-web-app/"
slug: "add-security-txt-to-your-web-app"
wp_id: 3590
category: ["security-txt"]
tag: ["net", "security", "security-txt"]
summary: "[sg_popup id=”3″ event=”onload”][/sg_popup] Recently, I came across below tweet from security expert Troy Hunt Google now has a security.txt file – so should you! https://t.co/fXmeNG9Yem https://t.co/drbJQ1Ynw8 — Troy Hunt (@troyhunt) February 3, 2018 The tweet talked about a file named security.txt. I went on reading his post to understand what exactly is security.txt and what problem"
---

[sg_popup id=”3″ event=”onload”][/sg_popup]

Recently, I came across below tweet from security expert Troy Hunt

<blockquote class="twitter-tweet" data-dnt="true" data-width="500">
<p dir="ltr" lang="en">Google now has a security.txt file – so should you! <a href="https://t.co/fXmeNG9Yem">https://t.co/fXmeNG9Yem</a> <a href="https://t.co/drbJQ1Ynw8">https://t.co/drbJQ1Ynw8</a></p>
<p>— Troy Hunt (@troyhunt) <a href="https://twitter.com/troyhunt/status/959724034622595072?ref_src=twsrc%5Etfw">February 3, 2018</a></p></blockquote>

The tweet talked about a file named `security.txt`. I went on reading [his post](https://www.troyhunt.com/fixing-data-breaches-part-3-the-ease-of-disclosure/) to understand what exactly is `security.txt` and what problem does it solves.

## So, what is Security.txt

No organization wants to be caught on a wrong foot when it comes to security. A data or security breach could lead to financial and reputation loss of a company. When a security researcher finds a  potential breach or security vulnerability in an organization website/ application, he/she tries to contact the organization to “responsibly disclose” the issue. The disclosure is confidential in nature and allows the organization time to take appropriate action against the issue.

But, who does the security researcher reach out to? Usually, in scenarios like this, they would not prefer to reach out to the organization via a general “contact us” page on the website or emailing/ calling a customer care of the organization. They would rather like to reach out to someone in the organization who can take immediate action, someone with authority.

That’s where `security.txt` can come to rescue.  The concept of `security.txt` was proposed by security researcher **Ed Foudil.**According to his website, [securitytxt.org](https://securitytxt.org/):

> The main purpose of security.txt is to help make things easier for companies and security researchers when trying to secure platforms. Thanks to security.txt, security researchers can easily get in touch with companies about security issues.

The organizations can add `security.txt` to their website to provide information of how or who security researchers can reach out to when they come across a security vulnerability on their website.

The website also provides an easy way to [generate the security.txt](https://securitytxt.org/#generate) file. The file needs to be added to the path `/.well-known/security.txt`.

Many websites including [Google](https://www.google.com/.well-known/security.txt) have started adding `security.txt`, maybe its time you should add one too 🙂
