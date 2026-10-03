---
title: "Set up web app on new Azure Virtual Machines"
date: "2016-05-06T03:27:54+00:00"
lastmod: "2021-06-21T11:42:34+10:00"
url: "/2016/05/06/set-up-web-app-on-new-azure-virtual-machines/"
slug: "set-up-web-app-on-new-azure-virtual-machines"
wp_id: 67
category: ["uncategorized"]
summary: "Setting up a website on classic Azure Virtual Machine is straight forward as in classic Azure VM we have the Endpoints for port 80 and 443 open by default. For each classic Azure VM we also had cloud service created. Hence, if we host a website directly on port 80 or 443 it would work"
---

Setting up a website on classic Azure Virtual Machine is straight forward as in classic Azure VM we have the Endpoints for port 80 and 443 open by default. For each classic Azure VM we also had cloud service created. Hence, if we host a website directly on port 80 or 443 it would work without much hassle.

Recently, I landed up in an issue where I created a new Windows Virtual Machine with deployment mode as “**Resource Manager**” and deployed my web app on Azure VM, but I did not find the corresponding cloud service for the virtual machine. Hence, I could not browse my application through internet since I didn’t have DNS. I then tried to access my application through public IP address of the Virtual Machine but again it didn’t work. After digging into various Virtual Machine options in new Azure Portal I found out the issue. The new Azure VMs do not have port 80 or 443 opened by default. Additionally, they do not have DNS configured by default. To resolve the issue you need to follow below two steps.

**Open http port 80/ 443**

The open port option in new Azure VM is a bit obscure. You need to go **Virtual Machine -> Settings -> Network Interfaces -> Select Network Interface -> Network Security Group -> Settings -> Inbound security rules** as explain in the below two figures.

![open-endpoint1](/wp-content/uploads/2016/05/open-endpoint1.png)

![open-endpoint2](/wp-content/uploads/2016/05/open-endpoint2.png)

Now, click on **Inbound security rules** and add a new inbound security rule to open port 80 as shown in figure below.![open-port-80.png](/wp-content/uploads/2016/05/open-port-80.png)

Similarly, open port 443 or any other port where your application is hosted. With this you can now access your application via public port number.

But you still cannot access your application through DNS. For that you need to first configure DNS name.

**Configure DNS Name**

To configure DNS name you need to go to first go Network Interface as explained in the previous step. Now, Select **Public IP address -> Settings -> Configuration** as shown in figure below:

![DNS-Configure1.PNG](/wp-content/uploads/2016/05/dns-configure1.png)

Now, just provide preferred DNS name and you are free to access, test, share your web app.

![DNS-Configure2.png](/wp-content/uploads/2016/05/dns-configure2.png)

Hope this post helps someone to save time.
