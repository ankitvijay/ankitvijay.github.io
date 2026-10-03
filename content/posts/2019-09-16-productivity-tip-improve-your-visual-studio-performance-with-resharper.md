---
title: "Productivity Tip – Improve your Visual Studio performance with ReSharper"
date: "2019-09-16T07:33:52+10:00"
lastmod: "2020-09-15T07:40:46+10:00"
url: "/2019/09/16/productivity-tip-improve-your-visual-studio-performance-with-resharper/"
slug: "productivity-tip-improve-your-visual-studio-performance-with-resharper"
wp_id: 4186
category: ["resharper", "visual-studio"]
tag: ["net", "productivity", "resharper", "tip", "visual-studio", "visual-studio-2019"]
summary: "Visual Studio is my bread and butter. It has played an important role in shaping my career. In the same breath, ReSharper has helped a lot to improve my productivity and make me a better programmer. And I’m sure there are many others like me who use Visual Studio and ReSharper on a daily basis."
---

Visual Studio is my bread and butter. It has played an important role in shaping my career. In the same breath, ReSharper has helped a lot to improve my productivity and make me a better programmer. And I’m sure there are many others like me who use Visual Studio and ReSharper on a daily basis.

#### ReSharper – A necessary evil

Unfortunately, the Visual Studio and ReSharper combo are not very good when it comes to performance. The situation has really gone worse with Visual Studio 2019.

For me, Visual Studio 2019 along with ReSharper and corporate anti-virus had made writing code a nightmare. The performance [tips](https://stackoverflow.com/questions/23737/do-you-have-any-tips-to-improve-resharper-and-or-visual-studio-performance) available online only helped to an extent. So much so that, I had to either disable the ReSharper or my [source control](https://stackoverflow.com/questions/21150060/how-can-you-disable-git-integration-in-visual-studio-2013-permanently#answer-25976947) plugin. Disabling the source control plugin on Visual Studio is trickier than it should be as the Visual Studio re-enables plugin each time after the Visual Studio restart. For a large solution, this is not ideal. I could go for a coffee, take a shower, a power nap, or watch a movie before the my Visual Studio came back to a state where I could start writing code 🙂

I even ranted my frustration over twitter.

<blockquote class="twitter-tweet" data-dnt="true" data-width="500"><p dir="ltr" lang="en">I love <a href="https://twitter.com/VisualStudio?ref_src=twsrc%5Etfw">@VisualStudio</a>, I love <a href="https://twitter.com/resharper?ref_src=twsrc%5Etfw">@resharper</a>. Just don't together… Visual Studio 2019 with ReSharper has become unusable…  Can you guys please fix this?<br/><br/>– A frustrated dev</p>— Ankit Vijay (@vijayankit) <a href="https://twitter.com/vijayankit/status/1159591167769530370?ref_src=twsrc%5Etfw">August 8, 2019</a></blockquote>

Here’s the response I received from one of the developer advocates at ReSharper.

<blockquote class="twitter-tweet" data-dnt="true" data-width="500"><p dir="ltr" lang="en">If you're interested in some background: <a href="https://t.co/FjkH4TgL8f">https://t.co/FjkH4TgL8f</a></p>— Maarten Balliauw @maartenballiauw@mastodon.online (@maartenballiauw) <a href="https://twitter.com/maartenballiauw/status/1159696796853166081?ref_src=twsrc%5Etfw">August 9, 2019</a></blockquote>

This post goes at length to explain the reasons why ReSharper performance is so poor on Visual Studio and what JetBrains is doing it to fix it. Unfortunately, it did not help fix my problem at hand.

#### What helped me

One of the tips from my colleague, ***@Marius*** that really helped me improve performance of my Visual Studio with ReSharper was to “Adjust Windows Performance options”. Here is how to do it.

- Go to “Performance Options” on your Windows machine. You can open this option by searching “Adjust the appearance and performance of Windows”

![](https://ankitvijaydotin.wordpress.com/wp-content/uploads/2022/12/af904-image.png)

*Search: Adjust the appearance and performance of Windows*

- Next, select the option “Adjust for best performance”. This will unselect all the Visual Effects options as shown in the screenshot below.

![](https://ankitvijaydotin.wordpress.com/wp-content/uploads/2022/12/2e875-image-2.png)

*Performance Options – Adjust for best performance*

- Unfortunately, this may result in a side effect where fonts on your machine could go haywire and they may appear like this:

![](https://ankitvijaydotin.wordpress.com/wp-content/uploads/2022/12/3ff5d-image-3.png)

*Fonts go haywire*

- To fix this, go to “Custom” option and select “Smooth edges of screen fonts”

![](https://ankitvijaydotin.wordpress.com/wp-content/uploads/2022/12/f8474-image-4.png)

*Smooth edges of screen fonts*

- This option gives you the best of both world, an improve performance with a better CPU and memory utilization and fonts which are not an eye-sore.

#### Conclusion

After trying different options, the above tip from my colleague helped me with the improved Visual Studio and ReSharper considerably. If you face similar performance issues with Visual Studio and ReSharper, please give this a try and see if it helps.

Photo by [Barn Images](https://unsplash.com/@barnimages?utm_source=unsplash&utm_medium=referral&utm_content=creditCopyText) on [Unsplash](https://unsplash.com/search/photos/tool?utm_source=unsplash&utm_medium=referral&utm_content=creditCopyText)
