---
title: "SAST Tooling – Part 3: The Winner"
date: "2019-06-30T07:06:10+10:00"
lastmod: "2022-12-23T23:04:47+10:00"
url: "/2019/06/30/security-tooling-part-3/"
slug: "security-tooling-part-3"
wp_id: 4049
category: ["code-analysis", "sast"]
tag: ["checkmarx", "coverity", "fortify-on-demand", "kiuwan", "net", "sast", "security", "sonarqube", "teamcity", "veracode", "visual-studio"]
summary: "Disclaimer: This post is not an endorsement or opposition of any product or tool. Opinions present here is based on our experiences. Please exercise your own independent skill and judgement before you rely on the information in this post. 🙂 This is Part-3 and final part of my blog series on Static Analysis Software Testing"
---

***Disclaimer****: This post is not an endorsement or opposition of any product or tool. Opinions present here is based on our experiences. Please exercise your own independent skill and judgement before you rely on the information in this post. 🙂*

This is Part-3 and final part of my blog series on Static Analysis Software Testing (SAST) tooling.

In the [Part-2](https://ankitvijaydotin.wordpress.com/2019/06/26/security-tooling-part-2/), I described our selection criteria to select an alternate to Veracode and how we narrow down our search to just few tools. In this post I will describe how we came about selecting the winner.

#### The Dilemma

Its good to have choices but it also makes it difficult to choose just one. While, our selection criteria was good enough to shortlist 5 SAST tools, we realized that we needed to do a lot more to select the one which would work best for us.

Documentation and public information did not help us get an answer to all our questions. Hence, we scheduled a demo with each organization to understand more about their product. We prepared a common questionnaire for each vendor. Additionally, we invited folks from different teams such Development, Security, Operations and management so each team had their say. All the demos were organized in a single week so that experience from previous demo was still fresh in our minds.

#### The weighted Matrix

Product demo was a great way for us understand the capability of each tools and further shorten the list. However, we still did not have a clear winner. We needed to be more objective with our approach. That’s when we came up with an idea of weighted matrix. We wrote down our selection criteria in an Excel sheet and gave a weight to each criteria on a scale of 1 to 10, where 10 would mean an absolute must have and 1 would mean that no one would die if the product does not have that capability. For example: Thoroughness of Security Checks was weighted as 10, Product Support was weighted as 8, while ability to check licensing in 3rd party open source dependencies was weighted just 2.

After that, we rated tools on a scale of 1-5 on each selection criteria and then came with with a weighted score as below:

```
Tool Criteria score = Criteria Weighting * Tool rating (1-5)
```

I would not go into the details of total criteria score of each tool as it was our *internal research* and *specific* to our organization needs.

#### The Winner

The weighted matrix helped us to come up with total weighted score for each tool and the results were a bit surprising. The SAST tool we ended up selecting was lesser known tool **Kiuwan**. **Checkmarx** and **Coverity** should also get a special mention as they fared quite well in our analysis.

Once, the tool was selected we worked closely with Kiuwan development team to do a POC with few of our applications.

#### Why Kiuwan

Here are few reasons why we chose to go for Kiuwan:

- While Kiuwan did not have a 24 * 7 support, we found that they were quite prompt in their response. During the POC, one of our developers questioned few of their security findings. Kiuwan development team accepted the one of the findings and agreed to fix it. For the others, they provided an explanation why they think it was valid.
- During the demo we found team from Kiuwan to be quite transparent. They answered our questions with honesty without making tall promises. There were few (cough.. Fortify) who tried to convince us that we were not asking the *right* question.
- Kiuwan turned out to be the least expensive among all the products we evaluated.
- Due to the value for money it offered, we were able to a get great bundling deal on Code Security (SAST), Insights, and Code Analysis features from Kiuwan.
- We found its UI modern and intuitive. It came up with some good features such as security rating, estimated number of hours to improve the security rating, action plan, grouping of vulnerabilities etc.
- Kiuwan allowed us to scan the source code locally and upload only the findings along with impacted line instead of uploading the entire source code. This was an important requirement for us, more so because we are using their cloud offering.
- Kiuwan was the most up-to-date when it came to supporting the latest .NET Core frameworks or the modern JavaScript frameworks.
- We found its reporting to be the best among all the products.
- Kiuwan documentation was up-to-date and easy to follow.
- We found Kiuwan updates and its release cycle to be the fastest among all the tools.

Whether or not Kiuwan would turned out to be a true to its hype, only time will tell. But as they say, well begun is half done. So we are keeping our fingers crossed. 🙂

> Photo by [Fauzan Saari](https://unsplash.com/@fznsr_?utm_source=unsplash&utm_medium=referral&utm_content=creditCopyText) on [Unsplash](https://unsplash.com/search/photos/winner?utm_source=unsplash&utm_medium=referral&utm_content=creditCopyText)
