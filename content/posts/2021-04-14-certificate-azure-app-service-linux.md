---
title: "Loading certificate in Azure App Service for Linux"
date: "2021-04-14T08:27:30+10:00"
lastmod: "2021-04-15T06:06:57+10:00"
url: "/2021/04/14/certificate-azure-app-service-linux/"
slug: "certificate-azure-app-service-linux"
wp_id: 197227
category: ["azure-app-service", "certificate", "cloud", "net-core", "tips-tricks"]
tag: ["azure", "azure-app-service", "c", "certificate", "cloud", "net", "net-core", "tips-tricks"]
summary: "In this post, I have explained how you can load a certificate through code in Azure App Service for Linu"
featured_image: "https://ankitvijaydotin.wordpress.com/wp-content/uploads/2022/12/d9e8c-featured-image-e1618352370954.jpg"
---

In this post, I will explain how you can load a certificate through code in Azure App Service for a Linux container. The steps to use a certificate in Azure App Service are already described in [Microsoft documentation](https://docs.microsoft.com/en-us/azure/app-service/configure-ssl-certificate-in-code). However, I found a couple of gaps in the documentation specifically for Linux. Hence, I decided to write this post.

To follow along you would need an App Service for Linux hosted on Azure.

## Why need a certificate

There are various reasons you may need to access a certificate in your code, like encryption/ decryption, authentication, authorization and so on. For example, Raven DB requires a private client certificate to allow access to the data store.

#### Step 1: Upload your certificate

You can upload the certificate in different ways, such as directly through the portal, Azure CLI or CI/CD pipeline.

![](https://ankitvijaydotin.wordpress.com/wp-content/uploads/2022/12/0fe0c-upload-private-certificate.png?w=1024&h=414)

*A private certificate uploaded to Azure portal.*

**Tip**: Certificate, its thumbprint and passphrase key for a private certificate are sensitive information. DO NOT store them in your source control.

#### Step 2: Make your certificate accessible

To access your certificate, through code, you need to make it accessible by creating an app setting `WEBSITE_LOAD_CERTIFICATES` . `WEBSITE_LOAD_CERTIFICATES` should be set to comma-separated values of certificate thumbprints.

![](https://ankitvijaydotin.wordpress.com/wp-content/uploads/2022/12/444f3-app-settings-website-load-certificate-1.png?w=1024&h=366)

*WEB_LOAD_CERTIFICATES app setting*

`WEBSITE_LOAD_CERTIFICATES` is a magic app setting that makes your certificates accessible to your application. For Linux container, it keeps the private certificates at the location `/var/ssl/private` and public certificates at `/var/ssl/certs`.

You can view the certificates by logging into`ssh` at `https://YOUR_APP_SERVICE_NAME.scm.azurewebsites.net/webssh/host`

![](https://ankitvijaydotin.wordpress.com/wp-content/uploads/2022/12/c2fa8-view-certificate-in-ssl.png)

**Note**: Azure App service accepts a certificate of **.pfx** and **.cer** formats only. It then exposes them as **.p12** and **.der** formats respectively.

For a windows container, Azure App Service automatically exposes the certificate paths through environment variables such as `WEBSITE_PRIVATE_CERTS_PATH`, `WEBSITE_PUBLIC_CERTS_PATH`. Unfortunately, you either need to set the environment variables manually or hard code the certificate path in your code for a Linux container.

#### STEP 3: Accessing certificate in C# code

Finally, you can access certificate in your C# code as shown below:

This file contains hidden or bidirectional Unicode text that may be interpreted or compiled differently than what appears below. To review, open the file in an editor that reveals hidden Unicode characters.
[Learn more about bidirectional Unicode characters](https://github.co/hiddenchars)

[Show hidden characters]({{ revealButtonHref }})

|  |  |
| --- | --- |
|  | using System; |
|  | using System.IO; |
|  | using System.Security.Cryptography.X509Certificates; |
|  |  |
|  | public static class CertificateExtensions |
|  | { |
|  | // Private certificatePath: $"/var/ssl/private/{thumbprint}.p12" |
|  | // Public certificatePath: $"/var/ssl/certs/{thumbprint}.der" |
|  |  |
|  |  |
|  | public static X509Certificate2 LoadCertificate(string thumbprint, string certificatePath) |
|  | { |
|  | if (string.IsNullOrWhiteSpace(thumbprint)) |
|  | { |
|  | throw new ArgumentNullException(nameof(thumbprint)); |
|  | } |
|  |  |
|  | if (string.IsNullOrWhiteSpace(certificatePath)) |
|  | { |
|  | throw new ArgumentNullException(nameof(certificatePath)); |
|  | } |
|  |  |
|  | var bytes = File.ReadAllBytes(certificatePath); |
|  | var certificate = new X509Certificate2(bytes); |
|  | return certificate; |
|  | } |
|  | } |

[view raw](https://gist.github.com/ankitvijay/2cce84b77c6692e4ee8b9b943aeda9e8/raw/eddb791c4d1cb8b69d8a49449fcdcf32c13316ea/LoadCertificate)
[LoadCertificate](https://gist.github.com/ankitvijay/2cce84b77c6692e4ee8b9b943aeda9e8#file-loadcertificate)
hosted with ❤ by [GitHub](https://github.com)

**Note**: To load a private certificate (p12), you do not need to supply a passphrase/ password. I found it the hard way since the code snippet to load a private certificate was missing in the [Microsoft documentation](https://docs.microsoft.com/en-us/azure/app-service/configure-ssl-certificate-in-code#feedback). I have [raised a PR](https://github.com/MicrosoftDocs/azure-docs/pull/73572) to fix this. At the time of writing the PR is still in review.
