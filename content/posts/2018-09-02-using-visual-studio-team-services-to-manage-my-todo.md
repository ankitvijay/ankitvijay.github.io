---
title: "Using Visual Studio Team Services to manage my ToDo"
date: "2018-09-02T08:45:11+10:00"
lastmod: "2022-12-23T23:07:09+10:00"
url: "/2018/09/02/using-visual-studio-team-services-to-manage-my-todo/"
slug: "using-visual-studio-team-services-to-manage-my-todo"
wp_id: 3735
category: ["productivity", "todo", "visual-studio", "visual-studio-team-services", "vsts"]
tag: ["todo", "visual-studio", "vsts"]
summary: "I’m quite an unorganized person. I spend most of my time in front of a computer in my office or in meetings. At home, I’m usually busy with my 2-year old or household chores. As a result, my list of ToDo items keeps on growing. And when I do find some time to work on"
---

I’m quite an unorganized person. I spend most of my time in front of a computer in my office or in meetings. At home, I’m usually busy with my 2-year old or household chores. As a result, my list of ToDo items keeps on growing. And when I do find some time to work on the list, I fail to prioritize them in the right order or in the worst case forget about an important work altogether.

Now, this is a common problem and I’m sure most of you come across this.

In the past, I have tried to use a few ToDo apps, Windows sticky notes, OneNote, Reminders etc. to keep track of my items. However, each of these would work well for a few days, then I would be back to square one.

Few of my pain-points were:

- A task (or a ToDo item) could be quite **complex** in nature. it could involve multiple sub-tasks, at different point of time.  None of these apps really let me do that easily. While I could create those tasks using free text on OneNote or Sticky notes, I found it quite disorganized and inconsistent.
- The task could be of different **categories**. For example, a personal task like renew insurance, pay bills or an official task like following up with a colleague. Again, the ToDo apps fell short of expectation when it comes to categorizing the tasks.
- The task could be in different **stages** like not yet started, in-progress, waiting for a response/ blocked etc.  I could not do that in a ToDo app.
- Each task could have **priorities** based on their **categories**. For example, I can have multiple tasks which need attention but they fall into the different buckets. Putting them into a ToDo app or OneNote is a huge task in itself.

These issues made me think of my problem statement differently. I realized that a ToDo app or a reminder app not alone is[sg_popup id=”3716″ event=”inherit”][/sg_popup] not sufficient to solve my problem. That’s when I switched to Visual Studio Team Services (VSTS) to manage my ToDo task list.

## **Why VSTS?**

Before shortlisting VSTS I considered following workflow tools:

- Jira
- Trello
- VSTS

At the office, we use Jira for our software development projects. However, I have found Jira to be quite heavy and cumbersome to use. In general, my experience with any of the  [Atlassian](https://www.atlassian.com/) products like Jira, Bitbucket, Confluence etc has not been very great.

What I needed was something which is lightweight, easy to create/ modify tasks, easy to customize but minimal management overhead. Trello looked to ticked few of the boxes but I had not used it much personally. And Whats more? It is now acquired by Atlassian 🙂

[Visual Studio Team Services](https://visualstudio.microsoft.com/team-services/), on the other hand, was a familiar product and easy to use as compared to Jira. There was a risk of getting bogged down by the different features (like repository, build configuration etc) which I did not need, but it since it checked all my boxes, I decided to go ahead with VSTS.

## VSTS Configuration

I tried to keep things very simple since I needed VSTS to only manage work items.

Here is my configuration:

- A new VSTS **project** (aptly named, ToDo) with no repository or build configuration
- **Kanban** process with “New/ Preview” VSTS navigations.
- **Stories board** to manage my the ToDo items
- **Swimlanes**/ **Tags**to categorize different work types like Office, Personal etc.
- Each story has zero or more (sub) **tasks** depending on the complexity of the story.

![ToDoBoard](/wp-content/uploads/2022/12/d0cb8-untitled.png)

**My ToDo Board**

![SubTasks.png](/wp-content/uploads/2022/12/45d45-subtasks.png)

**(Sub) Tasks under a ToDo Item/ Story**

I have been using VSTS Kanban board to maintain my ToDo list little over 2 months now, and it has greatly helped me to always be on the top of things.

One issue I have using VSTS is that it does not have a  good mobile app to maintain the work items. Also, its mobile website does not allow to easily move work items. Fortunately, since most of my time is spent in front of the computer screen anyway, it is not a huge issue. If there is anything that needs attention at a particular time of the day, I still use reminders on phone. This **hybrid**model is working quite well for me at least for now.

Hope this tip helps some of you to manage your tasks better.
