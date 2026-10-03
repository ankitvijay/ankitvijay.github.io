---
title: "async await best practices"
date: "2016-11-12T07:53:08+05:30"
lastmod: "2017-09-29T06:08:04+10:00"
url: "/2016/11/12/asyncawait-best-practices/"
slug: "asyncawait-best-practices"
wp_id: 1394
category: ["async-await", "c", "net", "task-parallel-library"]
tag: ["async-await", "c", "cpu-bound", "io-bound", "net", "task-parallel-library", "task-run", "tpl"]
summary: "aysnc await is probably one of the most important features of C#. It has made the life of developers easy. It helps developers to write clean code without any callbacks which are messy and difficult to understand."
---

`aysnc` `await` is probably one of the most important features of C#. It has made the life of developers easy. It helps developers to write clean code without any callbacks which are messy and difficult to understand.However, if used incorrectly `async` `await` it can cause havoc. It can lead to performance issues, deadlocks which are hard to debug. I have burnt hands due to incorrect use of  `async await` in the past and based on my little experience I can tell these issues will make your life hell, you will start questioning your very existence on this earth or why you chose to be a developer 🙂

I have tried to add common pitfalls while using async `await`  below. These are some of my learnings while working on problems that arise due to incorrect use of async `await` Much of these is inspired from [Stephen Cleary blogs](http://blog.stephencleary.com/) and [Lucian Wischik six essential tips for Async](https://channel9.msdn.com/Series/Three-Essential-Tips-for-Async) channel 9 videos.

Here are tips:

- **AVOID** using `Task.Result` or `Task.Wait()`. They make the calls synchronous and block async code.
- Make your calls `async` all the way.
- **USE** `Task.Delay` instead of `Thread.Sleep`
- **[Understand](https://channel9.msdn.com/Series/Three-Essential-Tips-for-Async/Tip-2-Distinguish-CPU-Bound-work-from-IO-bound-work)** the difference between CPU bound and IO bound operation before using Task Parallel Library or TPL
- **[USE](http://blog.stephencleary.com/2013/11/taskrun-etiquette-examples-using.html)**`Task.Run` or `Parallel.ForEach` for CPU bound operation.
- **USE** `await` for IO bound operation.
- **[USE](https://channel9.msdn.com/Series/Three-Essential-Tips-for-Async/Async-library-methods-should-consider-using-Task-ConfigureAwait-false-)** `ConfigureAwait(false)`on the web APIs or library code. On the WPF application do not use `ConfigureAwait(false)` at the top level methods.
- **[AVOID](http://blog.stephencleary.com/2013/08/startnew-is-dangerous.html)** using `Task.Factory.StartNew`. Use `Task.Run`
- **[DO NOT](https://channel9.msdn.com/Series/Three-Essential-Tips-for-Async/Async-Library-Methods-Shouldn-t-Lie)** expose a synchronous method as asynchronous or visa vesra. In other words your library method should expose the true nature of method.
- [**DO NOT**](https://channel9.msdn.com/Series/Three-Essential-Tips-for-Async/Tip-1-Async-void-is-for-top-level-event-handlers-only) use `async void` other than top level Events. ALWAYS return `async Task`

I hope these tips help few of you and help avoid common mistakes. Please suggest any other tips in the comments section.
