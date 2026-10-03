---
title: "SAST Tooling – Part 2: The selection criteria"
date: "2019-06-26T07:46:55+10:00"
lastmod: "2022-12-23T23:04:47+10:00"
url: "/2019/06/26/security-tooling-part-2/"
slug: "security-tooling-part-2"
wp_id: 4018
category: ["code-analysis", "sast"]
tag: ["checkmarx", "code-analysis", "coverity", "fortify-on-demand", "jira", "kiuwan", "net", "sast", "security", "sonarqube", "teamcity", "veracode", "visual-studio"]
summary: "Disclaimer: This post is not an endorsement or opposition of any product or tool. Opinions present here is based on our experiences. Please exercise your own independent skill and judgement before you rely on the information in this post. 🙂 This is Part-2 of my blog series on Static Analysis Software Testing (SAST) tooling. In"
---

> ***Disclaimer****: This post is not an endorsement or opposition of any product or tool. Opinions present here is based on our experiences. Please exercise your own independent skill and judgement before you rely on the information in this post. 🙂*

This is Part-2 of my blog series on Static Analysis Software Testing (SAST) tooling.

In the [Part 1](/2019/06/22/security-tooling-part-1/), I described our pain-points using Veracode and what motivated us to look elsewhere. In this part , I will describe how we went about looking for a tool better suited for our needs.

#### A “**perfect” SAST tool**

Buying a third-party tool is not only expensive but also a huge investment for an organization. It can take considerable amount on effort to customize the tool according to organization needs and visa-versa. It is equally hard to build a ecosystem around it. Since, we had already burnt our hands with Veracode, it was extremely important that we were second time right with our selection. There was no room for mistake. We were aware that if we do not do a due diligence, then it could be fatal and entire IT would need to carry the burden of our mistake for the years to come.

With that in mind, my colleague, Chris from SecOps (Security Operations) and I came up with a selection criteria to shortlist the SAST tools. Based on the selection criteria, we did an independent research on various SAST tools available in the market. The selection criteria helped us remove our unconscious bias while trying to short-list the SAST tools.

#### Our selection criteria

We divided our criteria into Must-Have, Good-To-have and Should-have. We also categorized the our requirements based on the stakeholders like Dev, Security, IT management. Below are few points we considered during our selection process at a very high level:

- Support for security risk and software error such as SANS 25, CERT, OWASP Top 10
- Provide a detailed, executive report summary customized as per stakeholder such as Dev, Security, IT management.
- More control to user – Allow user to configure scan policy as per project.
- Allow user to export reports outside portal via well-known formats like email, pdf and not just propriety formats.
- High accuracy rate and low false positive rates.
- Good explanation of vulnerabilities within the context of the code.
- Provide sample code and guidelines to fix the issue.
- Good integration with tools such JIRA, Visual Studio, Visual Studio code.
- Integrate well with our build pipeline and CI/CD process.
- Easy to understand, navigate and a modern User Interface
- Scan turnaround time
- Ability to scan on locally
- Support for JavaScript frameworks like Angular, VueJS etc and the latest .Net Core framework.
- Report vulnerabilities for 3rd party dependencies added through NuGet and NPM.
- Provide a rich set of APIs to perform the operations like viewing scan, downloading reports etc
- Excellent documentation
- Good Support
- Cost effective
- Capabilities beyond security such as code efficiency, duplicate code, etc

#### What we did not consider

- Reviews from sites such as [ITcentralstation](https://www.itcentralstation.com/). We found the reviews about the product could be misleading and they were more focused on IT operations.
- The size of the organization. Our experience from Veracode made us realize that bigger is not always better. Hence, we kept it out of our selection criteria.
- We tried to keep a distance from the product marketing teams as from our experience it does not help much in getting answers to our query.

The above criteria helped us narrow down our search to following products:

- Checkmarx
- Fortify on Demand
- Kiuwan
- SonarQube
- Coverity + Black Duck

In the next and final post, I will talk about the tool how we further reduce our long list of SAST tools and what we ended up procuring.

> Photo by [Vladislav Babienko](https://unsplash.com/@garri?utm_source=unsplash&utm_medium=referral&utm_content=creditCopyText) on [Unsplash](https://unsplash.com/search/photos/selection-criteria?utm_source=unsplash&utm_medium=referral&utm_content=creditCopyText)
