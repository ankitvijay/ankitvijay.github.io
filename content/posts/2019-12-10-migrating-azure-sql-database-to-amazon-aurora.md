---
title: "Migrating Azure SQL Database to Amazon Aurora"
date: "2019-12-10T08:09:51+10:00"
lastmod: "2020-09-15T07:39:51+10:00"
url: "/2019/12/10/migrating-azure-sql-database-to-amazon-aurora/"
slug: "migrating-azure-sql-database-to-amazon-aurora"
wp_id: 4331
category: ["amazon-aurora", "aws", "azure-sql-database"]
tag: ["amazon-aurora", "aws", "azure", "azure-sql-database", "mysql", "net", "sql-server"]
summary: "I recently got an opportunity to work on migrating Azure SQL Database to Amazon Aurora. Well, it was not technically a migration since our platform needed to support both Azure SQL and Amazon Aurora. The motivation behind this is perhaps a separate post in itself. For those who have not worked on either of these"
---

I recently got an opportunity to work on migrating Azure SQL Database to Amazon Aurora. Well, it was not technically a migration since our platform needed to support both Azure SQL and Amazon Aurora. The motivation behind this is perhaps a separate post in itself.

For those who have not worked on either of these database engines, here is a little introduction to both.

**[Azure SQL Database](https://azure.microsoft.com/en-us/services/sql-database/)** is SQL Server compatible Database as Service on Microsoft’s cloud, Azure.

[Amazon Aurora](https://aws.amazon.com/rds/aurora/) is a MySQL and PostgreSQL-compatible relational database built on Amazon cloud, AWS. We chose to use MySQL flavor for Amazon Aurora.

There was an option to use [Amazon RDS for SQL Server](https://aws.amazon.com/rds/sqlserver/). However, there was a significant price difference between SQL Server and Aurora. We realized that the cost and effort for the rewrite would be far less than hosting on Amazon RDS for SQL Server in the longer run.

The migration was a great learning experience for someone like me who has not kept his foot outside Microsoft Technologies or Azure for most of part of his career.

Here are some of the changes we had to do to add support for Amazon Aurora.

### The changes required

#### Docker Image

With Azure SQL, we used [docker image](https://hub.docker.com/_/microsoft-mssql-server) `mcr.microsoft.com/mssql/server` for development since Azure SQL is compatible with SQL Server.

Amazon Aurora, on the other hand, [is compatible](https://aws.amazon.com/rds/aurora/faqs/?nc=sn&loc=6) with MySQL 5.6 and 5.7 using the InnoDB storage engine. The [docker image](https://hub.docker.com/_/mysql) we used for our development was `mysql:5.7`

#### SQL IDE/ Editor

The SQL Server comes with [SQL Server Management Studio](https://docs.microsoft.com/en-us/sql/ssms/download-sql-server-management-studio-ssms?view=sql-server-ver15) (SSMS) from Microsoft. SSMS provided an easy way to view and manipulate tables/ queries.

For MySQL, we ended up using [MySQL Workbench](https://www.mysql.com/products/workbench/). One interesting issue we had while trying to write SQL queries on MySQL Workbench was that the queries MySQL Workbench by default supported version 8, and the query syntax was not compatible with `MySQL 5.7`.

This was a little bit surprising for me since with SQL Server query syntax has mostly been backward compatible. To support the previous version of MySQL I had to update the MySQL default target version by going to `Edit -> Preferences -> Modeling -> MySQL` and setting the version to `5.7.28`.

![](/wp-content/uploads/2022/12/8b705-capture-1.png)

*Default Target MySQL Version setting*

#### Database Setup – SSDT vs UpDatabase

Our existing DB scripts were written using SSDT for SQL Server. With MySQL, we ended up using the `dbup-mysql` [Nuget package](https://www.nuget.org/packages/dbup-mysql) to deploy and upgrade the SQL Server database.

Note that `dbup` also supports [SQL Server](https://www.nuget.org/packages/dbup-sqlserver). However, there was no motivation for us to move our existing SQL Server implementation to `dbup` since SSDT works very well for us.

#### SQL Script differences

Both SQL Server and MySQL are SQL. In reality, their syntax is more different than they are similar. Here are a few differences we came across while converting our queries to MySQL.

- We need to use backtick or `` ` `` in MySQL to escape keywords instead of `[]` in SQL Server.
- `AUTO_INCREMENT` keyword to define `IDENTITY`.
- MySQL does not support `DateTimeOffset`. As a result, we need to save the date in `UTC` format.
- MySQL and SQL Server differ in the way we define indexes. For example, MySQL does not support the [filtered index](https://docs.microsoft.com/en-us/sql/relational-databases/indexes/create-filtered-indexes?view=sql-server-ver15).
- MySQL does not allow us to `DECLARE` variables outside of Stored Procedures
- MySQL does not have support for syntax like `MERGE INTO`, `WHEN MATCH` etc.
- One interesting and less obvious difference between the two is that the data type of `COUNT` in `MySQL` is `Int64` while in SQL sever it is `INT32`. SQL Server `COUNT_BIG` is the closest to MySQL `COUNT` .

> **Note:** This list is not exhaustive and it only describes a few of differences I came across during the conversion

#### Dapper Support

We used [Dapper](https://github.com/StackExchange/Dapper) ORM to talk SQL Server from code. This turned out a great choice for us as Dapper also has support for MySQL. This made the porting the queries quite easy. We were able to have a common interface that defined operations and then specific implementation for SQL Server and MySQL.

### Conclusion

It was a bit of work but a fun learning exercise for us to add support for Amazon Aurora along with the existing Azure SQL Database.
