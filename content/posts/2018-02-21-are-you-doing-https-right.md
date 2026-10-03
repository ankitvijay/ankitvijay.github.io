---
title: "Are you doing HTTPS right?"
date: "2018-02-21T06:34:47+10:00"
lastmod: "2022-12-23T23:04:46+10:00"
url: "/2018/02/21/are-you-doing-https-right/"
slug: "are-you-doing-https-right"
wp_id: 3621
category: ["csp", "https", "mixed-content", "upgrade-insecure-requests"]
tag: ["csp", "https", "mixed-content", "net", "security", "upgrade-insecure-requests"]
summary: "Last year, internet reached an important milestone when it comes to web security. More than half of the websites all over the world are now on HTTPS. As the awareness about HTTPS is rising, more and more organizations and individuals are moving their websites to HTTPS. Certificate authorities like Lets Encrypt which offer free certificates have made"
---

Last year, internet reached an important milestone when it comes to web security. More than half of the websites all over the world are [now on HTTPS](https://techcrunch.com/2017/02/22/eff-half-the-web-is-now-encrypted/). As the awareness about HTTPS is rising, more and more organizations and individuals are moving their websites to HTTPS.  Certificate authorities like [Lets Encrypt](https://letsencrypt.org/) which offer free certificates have made it easier than ever to migrate to HTTPS. In addition to this,  big organizations like Google, Mozilla are pushing hard for HTTPS. Starting July, Chrome will mark all [HTTP sites as non-secure](https://www.theverge.com/2018/2/8/16991254/chrome-not-secure-marked-http-encryption-ssl).

While moving to HTTPS is an important leap towards securing your website, it is still just one of many important steps. One such step is HSTS. For more info on HSTS, please refer to my [previous post on HSTS](/2017/12/26/what-is-hsts-and-why-should-i-care/).

One other common issue many people face while moving to HTTPS is mixed content. According to [Google developer documentation](https://developers.google.com/web/fundamentals/security/prevent-mixed-content/what-is-mixed-content)

> **Mixed content** occurs when initial HTML is loaded over a secure HTTPS connection, but other resources (such as images, videos, stylesheets, scripts) are loaded over an insecure HTTP connection. This is called mixed content because both HTTP and HTTPS content are being loaded to display the same page, and the initial request was secure over HTTPS. Modern browsers display warnings about this type of content to indicate to the user that this page contains insecure resources.

## Mixed content on website

There are many websites out there today which face the issue of mixed content. I recently came across one such website, [Jetstart.com](http://www.jetstar.com/au/en/home).

As of this writing, the landing page of Jetstar is not on HTTPS and [this is an issue in itself.](https://www.troyhunt.com/im-sorry-you-feel-this-way-natwest-but-https-on-your-landing-page-is-important/) Even though, when you go to a page like “**Manage Booking**” which requires your personal information like email address and booking reference to view your booking is encrypted, there is one caveat. The page loads some of the resources on HTTP (or an insecure connection).

When you load a website on HTTPS, all leading browsers today show “Secure” symbol on the address bar. For example,  when you open my post on the Chrome browser, the address bar shows “Secure” as shown below.

![Secure-website.png](/wp-content/uploads/2022/12/cd8c2-secure-website.png)

Secure symbol (Chrome Browser)

The secure symbol also signifies that all the resources that are requested while loading on the website, be it an image or a third-party script are all HTTPS. However, if your website loads mixed content, then users of your website will not see trusted “Secure” symbol on the address bar even when the site itself is on HTTPS. Here is the example of how “Manage Booking” page of Jetstar looks like on Edge Browser:

![](/wp-content/uploads/2022/12/fcaad-insurewebsitewarning-1.png)

Website content not encrypted warning (Edge Browser)

Whats worse is that Jetstar also takes credit card information of the user. So, when a user sees one such warning from the browser, he can lose trust in the brand and may think twice before making a purchase.

## How can you avoid this?

Well, one of the most obvious ways to avoid this issue is to deliver all your content over HTTPS.  Unfortunately, It is not as easy as it sounds. Especially, if you are loading hundreds of resources from different sources on your website. It is not trivial to migrate all the resources to HTTPS and then update the links on the page. In addition to this, we still do not have control over the contents of any third-party library we may be using on our website.

That’s where Content Security Policy (CSP) **upgrade-insecure-requests**can come to rescue. As per [MDN docs](https://developer.mozilla.org/en-US/docs/Web/HTTP/Headers/Content-Security-Policy/upgrade-insecure-requests):

> The HTTP [`Content-Security-Policy`](https://developer.mozilla.org/en-US/docs/Web/HTTP/Headers/Content-Security-Policy "The HTTP Content-Security-Policy response header allows web site administrators to control resources the user agent is allowed to load for a given page. With a few exceptions, policies mostly involve specifying server origins and script endpoints. This helps guard against cross-site scripting attacks (XSS).") (CSP) `upgrade-insecure-requests` directive instructs user agents to treat all of a site’s insecure URLs (those served over HTTP) as though they have been replaced with secure URLs (those served over HTTPS). This directive is intended for web sites with large numbers of insecure legacy URLs that need to be rewritten.
> The `upgrade-insecure-requests` directive is evaluated before [`block-all-mixed-content`](https://developer.mozilla.org/en-US/docs/Web/HTTP/Headers/Content-Security-Policy/block-all-mixed-content "The HTTP Content-Security-Policy (CSP) block-all-mixed-content directive prevents loading any assets using HTTP when the page is loaded using HTTPS.") and if it is set, the latter is effectively a no-op. It is recommended to set one directive or the other, but not both.

To add it to your website, simply add below meta tag to your HTML

`<meta http-equiv="Content-Security-Policy" content="upgrade-insecure-requests">`

> **A NOTE OF CAUTION** The CSP: upgrade-insecure-requests can only migrate a requested resource on HTTPS when the resource is available over HTTPS . If  however, the requested resource is not actually available on HTTPS, the request **WILL FAIL** without any fallback to HTTP.

Unfortunately, **Edge**and **Safari** browsers still do not support this CSP directive at this point in time. Chrome, Firefox, and Opera have the support of this directive.

Hope you find this post useful. Happy coding!!! 🙂

[sg_popup id=”3″ event=”onload”][/sg_popup]
