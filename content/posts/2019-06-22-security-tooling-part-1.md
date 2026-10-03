---
title: "SAST Tooling – Part 1: Why we ditched Veracode"
date: "2019-06-22T09:37:32+10:00"
lastmod: "2019-06-30T21:52:35+10:00"
url: "/2019/06/22/security-tooling-part-1/"
slug: "security-tooling-part-1"
wp_id: 4003
category: ["code-analysis", "sast"]
tag: ["code-analysis", "net", "sast", "security", "teamcity", "visual-studio"]
summary: "This post is Part-1 of multi-part series describing our journey to ditch popular Static Application Security Testing (SAST) tool Veracode and our quest for a better security tool. Background Until recently, our organization used Veracode for security analysis for few our applications. Veracode came with a lot of reputation. It is considered a leader in"
---

This post is Part-1 of multi-part series describing our journey to ditch popular Static Application Security Testing (SAST) tool [Veracode](https://www.veracode.com/) and our quest for a *better* security tool.

### Background

Until recently, our organization used Veracode for security analysis for few our applications. Veracode came with a lot of reputation. It is considered a [**leader**](https://info.veracode.com/analyst-report-gartner-mq-appsec-testing-2019.html)in Application Security by Gartner and is used by hundreds of organizations across the globe. Unfortunately, our experience with Veracode was quite opposite.

> ***Disclaimer****: This post talks about our experience with Veracode and other SAST tools based on our needs last year. It should not be seen as endorsement or opposition of any SAST tool.* *Please exercise your own independent skill and judgement before you rely on the information in this post.*

### **Veracode Pain-Points**

- Veracode Documentation did not keep up the pace with their updates (which anyway happened once in a blue moon). At few places even we found it misleading.
- We found the Veracode APIs very hard to use and integrate with our build pipeline.
- Veracode UI portal left lot to be desired. Its UI looked dated and far from intuitive. It did not support some basic integrations. For example, reports, scan results etc. could not be emailed.
- Veracode Support took weeks to respond and when they did respond, the responses were short with no help.
  - Support from tickets raised almost always included nothing more than a link to outdated documentation. This was even the case when the ticket raised was in regards to the same outdated documentation. 🙂
  - Often it took follow up emails to even get a response from them.
- Integration with JIRA was not usable and did not solve our purpose. We eventually fall-back to creating tickets manually in JIRA due to following reasons:
  - Veracode would raise dozens or even hundreds of tickets for the same finding if it was found in more than area such as a text box. For example, a client side validation issue that could be addressed by a single change to the validation library in place was flagged as a new ticket for every text box was created. This resulted in hundreds of new tickets being raised in JIRA creating a clutter.
  - Its JIRA plugin itself was not regularly updated. And one of our JIRA updates broke the Plug-in.
- The scans incorrectly identified one of the 3rd party libraries as our internal organization code. As a result, scans showed the incorrect results. This resulted in our code failing the scan. Developers cannot rewrite the code for 3rd party developers. It took months for Veracode to confirm that it was a bug and then another few to fix it.
- A number of dependencies in our applications like Castle Windsor and Autofaq were not supported. Veracode mentioned they no plans to support it.
- Veracode API Keys had a finite period of validity. We found that Veracode appeared to only send 1 notification regarding the pending expiration, just 1 day prior to the API key expiring. There were no additional follow up emails or notifications in the portal etc, that warn of the expired API key. As a result, our Veracode scans had been failing due the expired API keys. Overlooking a single email resulted in all associated scans from being unable to complete.
- If there was any issue while uploading the DLLs (eg. due to API key expiration), then the error we get on the portal are very cryptic and it was difficult to understand the root cause and possible solution.
- Veracode neither integrated with our source control nor offered local analysis. The only way to scan the code was to upload the DLLs to the Veracode portal.
- Scan Times were quite lengthy. Approximately 30 mins for a small size application. If a minor change is made to code and then all the DLLs were required to be uploaded and the full scan needed to run once more. We could not find a way to integrate it fully with our build pipeline.
- The features added to Veracode appear to be focused on creating new income streams via new paid products without addressing any of the known issues with the platform.
- Veracode came up with two Visual Studio plugins: Veracode and Veracode Greenlight. Veracode Greenlight was licensed separately. But more importantly, both these plugins were equally useless.
  - Veracode Plugin: Did not provide static scan with-in the editor. We still had to upload the DLLs and then download the report. While the developer uploaded files from their IDE, the machine was unusable and unresponsive. As each file was uploaded, focus returned to the upload window making performing any additional task at the same time impossible. Again, the upload could take a several minutes to complete.
  - Veracode Greenlight: While this plugin *supposedly*scanned the source code inline. It could only do it at the file level and not the DLLs. From our experience it could not even identify the vulnerabilities with in the file.
- Funnily, being a “Security ” product one would expect Veracode to be on the top of the security they built into their own product. But, unfortunately, this wasn’t the case. Their own survey for feedback were on insecure channel (that is `Http`), their password policy did not evolve with [time](https://www.troyhunt.com/passwords-evolved-authentication-guidance-for-the-modern-era/). For example: Veracode still mandated a regular password change which is not considered a great advice anymore.

These pain-points were felt by us every day and forced us to look for an alternate. In the next post, I will talk about our approach to evaluate different SAST tools out there in the market.

> Photo by [Taskin Ashiq](https://unsplash.com/@taskinhoo?utm_source=unsplash&utm_medium=referral&utm_content=creditCopyText) on [Unsplash](https://unsplash.com/search/photos/security-tool?utm_source=unsplash&utm_medium=referral&utm_content=creditCopyText)
