---
title: "Publish Web App to Azure Virtual Machine – Part 2"
date: "2016-05-18T03:50:39+00:00"
lastmod: "2022-12-23T23:04:46+10:00"
url: "/2016/05/18/publish-web-app-to-azure-virtual-machine-part-2/"
slug: "publish-web-app-to-azure-virtual-machine-part-2"
wp_id: 334
category: ["azure-vm", "visual-studio-team-services", "web-app-set-up"]
tag: ["azure", "azure-resource-manager", "virtual-machine", "visual-studio", "web-deploy"]
summary: "This post is Part 2 of the series – Publish web app to Azure VM. In this post I will take the application, we created in Part 1 and publish it on Azure Virtual Machine through Visual Studio Team Services."
---

This post is Part 2 of the series – Publish web app to Azure VM. In this post I will take the application, we created in Part 1 and publish it on Azure Virtual Machine through Visual Studio Team Services.

Before you go any further I you recommend to go through [Part 1](/2016/05/18/publish-web-app-to-azure-virtual-machine-part-1/) of the series, if you have not already.

As a pre-requisite I have assumed that your solution along with the publish profile you created in part 1 is checked in Visual Studio Team Services. For this demo I have used the **Team Foundation** as my version control. But steps are same if you have used **Git** as your version control.

## Publish Web App from Visual Studio Team Services

First, go to your Visual Studio Team Services dashboard of your project. Your visual studio team services dashboard should look similar to the figure below:

![visual-studio-dashboard.PNG](/wp-content/uploads/2016/05/visual-studio-dashboard.png)

Visual Studio Team Services Dashboard

Now, click on Continuous Integrate to create your build definition. This will take you to a new page where you will see a “+” icon on left navigation pane. Click on icon to create a new build definition and then select **Visual Studio** template.

![CI - step1.png](/wp-content/uploads/2016/05/ci-step11.png)

Create new build Definition

Click next, select your repository in the second step and then click create.

Your build definition will have some default build steps added. Keep only **Nuget restore** and remove rest of the build steps as this demo is focussed only on publishing the build to Azure VM.

![ci-step3.PNG](/wp-content/uploads/2016/05/ci-step32.png)

Visual Studio Definition – Nuget restore build step

Next, click on Add Build step and add MsBuild task from **Add build step window.** We will use MsBuild to publish the publish profile we created in first part of this series.

Now, select MS Build step and specify your MsBuild arguments as

```
/p:DeployOnBuild=true /p:PublishProfile="$(publishProfileName)" /p:Password="$(userServerPassword)" /p:Configuration="$(BuildConfiguration)"
```

Let us go through each argument one by one:

- **DeployOnBuild**: Setting DeployOnBuild to true means, we will deploy the solution after building
- **PublishProfile**: Defines the name of the publish profile we use for the deploying. We have provided the value of publish profile as user defined variable, $(publishProfileName). We will define this variable later.
- **Password**: Defines the user password of the Azure virtual machine. Again, we have provided the value of password as variable $(userServerPassword) which we will define later.
- **Configuration:** Defines the build configuration of the solution. This build configuration value can be either be release or debug based on kind of deployment you are doing.

With this our build steps are completed.

![ci-step4](/wp-content/uploads/2016/05/ci-step4.png)

Visual Studio Definition – MS Build Step

Next, we need to define the variables we used in MSBuild step. Select Variables tab in the build definition. Click, Add variable and give the variable name as **publishProfileName.** Provide the value of the variable same as the name of your publish profile. Click, on Add variable again and give the name of variable as **userServerPassword.** Provide password of Azure VM user in the value field of variable. Since, password is sensitive information, make sure to click on the lock icon present on the right side of the variable field.

For both the variables also check **Allow at Queue Time**. This will prompt the user to change the values of variables before queueing the build.

Also, notice that variable $(BuildConfiguration) is created by default so we do not need to add it again.

![ci-step5.PNG](/wp-content/uploads/2016/05/ci-step5.png)

Visual Studio Definition – Variables

Next, you can **optionally** define the when this build definition would be executed from Triggers tab. You can chose to either build each check-in (Continuous Integration) or schedule it at a specific time.

Now, click save and provide the name of the build to complete our visual studio definition.

![ci-step6.PNG](/wp-content/uploads/2016/05/ci-step61.png)

Visual Studio Definition – Save

With this all our build definition is complete. Now, just queue you build and verify that publish to Azure is successful.

![ci-step7](/wp-content/uploads/2016/05/ci-step7.png)

Queue Build

### Important Note

Your build definition may fail with error **#ERROR_CERTIFICATE_VALIDATION_FAILED.** This error comes up because the remote server has a self-signed certificate for the Remote Agent Service or the Web Management Service. In this case, you need to bypass the certificate validation. Go to your publish profile in your solution under Properties -> PublishProfiles. Add below line to the property group

```xml
<AllowUntrustedCertificate>True</AllowUntrustedCertificate>
```

This option should **NOT be used for Production**. In production make sure to have a valid certificate on remote server.
