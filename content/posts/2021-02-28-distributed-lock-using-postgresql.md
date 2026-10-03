---
title: "Distributed lock using PostgreSQL"
date: "2021-02-28T09:02:56+10:00"
lastmod: "2022-12-23T23:04:47+10:00"
url: "/2021/02/28/distributed-lock-using-postgresql/"
slug: "distributed-lock-using-postgresql"
wp_id: 150660
category: ["architecture", "distributed-lock", "event-driven-architecture", "microservices", "net-5", "net-core", "postgresql"]
tag: ["distributed-lock", "event-driven-architecture", "microservices", "net", "net-5", "net-core", "postgresql"]
summary: "This post talks about why you may need a distributed lock and how you can create a distributed lock using PostgreSQL."
featured_image: "/wp-content/uploads/2022/12/b71ab-distributedlock-featureimage.jpg"
---

In my [previous post](/2021/02/22/a-poor-mans-scheduler-using-net-background-serivce/), I talked about creating a simple scheduler service using the .NET Background service. The scheduler service would work well as long as we only have a single instance of worker deployed. However, if there are more than one worker nodes, it would cause the scheduler to run once for every worker instance, which is not desirable. We can fix this issue using a **distributed lock**.

All the major data store vendors, such as Oracle, SQL Server, Redis, etc., provide us with a way to create a distributed lock.

In this post, I will explain how you can create distributed lock in .NET using PostgreSQL.

## Why do we need a distributed lock?

The distributed lock ensures that only one node or instance of our service performs the task. That task might be storing data in a data store, calling an API, publishing an event, and so on. With distributed lock, the task is performed only once, improving [efficiency and ensuring correctness](https://martin.kleppmann.com/2016/02/08/how-to-do-distributed-locking.html).

## Distributed lock using PostgreSQL

We can create distributed lock using PostgreSQL through advisory locks. From the [documentation](https://www.postgresql.org/docs/8.2/explicit-locking.html):

> These are called *advisory locks*, because the system does not enforce their use — it is up to the application to use them correctly. Advisory locks can be useful for locking strategies that are an awkward fit for the MVCC model. Once acquired, an advisory lock is held until explicitly released or the session ends.

## Source Code

You can follow [this GitHub repository](https://github.com/ankitvijay/PostgreSqlDistributedLock) for the source code of the implementation.

Let us first start with creating a sample PostgreSQL DB using the **docker run** command.

```bash
docker run --name distributed-lock-test -e POSTGRES_USER=dbUser -e POSTGRES_DB=distributed-lock-db -e POSTGRES_PASSWORD=password -p 5432:5432 -d postgres
```

Next, let us create an empty class library project. We connect to PostgreSQL using a popular Nuget package, **Npgsql**and log through default **Microsoft.Extension.Logging**

Next, we create a class DistributedLock, as shown below:

```csharp
using System;
using System.Threading.Tasks;
using Microsoft.Extensions.Logging;
using Npgsql;

namespace PostgreSQLDistributedLock
{
    public sealed class DistributedLock : IDisposable
    {
        private readonly ILogger<DistributedLock> _logger;
        private bool _disposed;
        private NpgsqlConnection _connection;

        public DistributedLock(string connectionString, ILogger<DistributedLock> logger)
        {
            _logger = logger;
            var builder = new NpgsqlConnectionStringBuilder(connectionString);
            _connection = new NpgsqlConnection(builder.ToString());
            _connection.Open();
        }

        public async Task<bool> TryExecuteInDistributedLock(long lockId, Func<Task> exclusiveLockTask)
        {
            var hasLockedAcquired = await TryAcquireLockAsync(lockId);

            if (!hasLockedAcquired)
            {
                return false;
            }

            try
            {
                await exclusiveLockTask();
            }
            finally
            {
                await ReleaseLock(lockId);
            }

            return true;
        }

        private async Task<bool> TryAcquireLockAsync(long lockId)
        {
            var sessionLockCommand = $"SELECT pg_try_advisory_lock({lockId})";
            _logger.LogInformation("Trying to acquire session lock for Lock Id {@LockId}", lockId);
            var commandQuery = new NpgsqlCommand(sessionLockCommand, _connection);
            var result = await commandQuery.ExecuteScalarAsync();
            if (result != null && bool.TryParse(result.ToString(), out var lockAcquired) && lockAcquired)
            {
                _logger.LogInformation("Lock {@LockId} acquired", lockId);
                return true;
            }

            _logger.LogInformation("Lock {@LockId} rejected", lockId);
            return false;
        }

        private async Task ReleaseLock(long lockId)
        {
            var transactionLockCommand = $"SELECT pg_advisory_unlock({lockId})";
            _logger.LogInformation("Releasing session lock for {@LockId}", lockId);
            var commandQuery = new NpgsqlCommand(transactionLockCommand, _connection);
            await commandQuery.ExecuteScalarAsync();
        }

        public void Dispose()
        {
            Dispose(true);
        }

        private void Dispose(bool disposing)
        {
            if (_disposed)
            {
                return;
            }

            if (disposing)
            {
                _connection?.Close();
                _connection?.Dispose();
                _connection = null;
            }

            _disposed = true;
        }
    }
}
```

Let us deep dive, into the code. We have a single public method, **TryExecuteInDistributedLock,**that takes **lockId**and **exclusiveLockTask**

 as parameters. Within the method where we do the following:

- First, we try to acquire a session lock for the passed lock id. To acquire the lock, we call PostgreSQL in-built function **pg_try_advisory_lock**
- If the lock is not acquired successfully, we return false, indicating that we could not acquire the session lock and the task was not executed.
- If the lock is acquired successfully, we run the **exclusiveLockTask.**
- Once **exclusiveLockTask**is executed successfully, we release the lock by calling function **pg_advisory_unlock** so that it can be acquired later.

To validate our implementation, here is the test:

```csharp
using System.Linq;
using System.Threading.Tasks;
using Microsoft.Extensions.Logging;
using Microsoft.Extensions.Logging.Abstractions;
using Xunit;
using Xunit.Abstractions;

namespace PostgreSQLDistributedLock.Tests
{
    public class DistributedLockTests
    {
        private readonly ITestOutputHelper _testOutputHelper;
        private readonly string _connectionString;

        public DistributedLockTests(ITestOutputHelper testOutputHelper)
        {
            _testOutputHelper = testOutputHelper;
            _connectionString = "Host=localhost;Username=dbUser;Password='password';Database=distributed-lock-db;";
        }

        [Fact]
        public void DistributedLockIsAcquiredSuccessfully()
        {

            async Task ExclusiveLockTask(int node)
            {
                _testOutputHelper.WriteLine($"Executing a long running task on Node {node}");
                // Add 5 second delay
                await Task.Delay(5000);
            }

            const long lockId = 50000;

            // Simulate with 5 nodes
            var nodes = Enumerable.Range(1, 5).ToList();
            Parallel.ForEach(nodes, async node =>
            {
                // Act and Arrange
                _testOutputHelper.WriteLine($"Trying to acquire session lock and run task for Node {node}");
                using var distributedLock = new DistributedLock(_connectionString, NullLogger<DistributedLock>.Instance);
                if (!await distributedLock.TryExecuteInDistributedLock(lockId, () => ExclusiveLockTask(node)))
                {
                    _testOutputHelper.WriteLine($"Node {node} could not acquire lock");
                }
            });
        }
    }
}
```

As you can see in the above code, we have tried to simulate a distributed scenario by creating five nodes that try to acquire a distributed lock simultaneously. However, only one node is successful in acquiring the lock and executing the task. The output of the above test run is:

![](/wp-content/uploads/2022/12/6f512-testoutput-1.png)

*Long running task executed on a single node*

## Wrapping Up!

This post explains how you can create a distributed lock using PostgreSQL and ensure that a task is executed only once.

> Feature Photo by [Georg Bommeli](https://unsplash.com/@calina?utm_source=unsplash&utm_medium=referral&utm_content=creditCopyText) on [Unsplash](https://unsplash.com/s/photos/lock?utm_source=unsplash&utm_medium=referral&utm_content=creditCopyText)
