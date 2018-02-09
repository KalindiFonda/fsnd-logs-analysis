# Logs Analysis Project

## Table of Contents

* [Source](#source)
* [Aims](#aims)
* [Views created](#views-created)
* [Code design](#code-design)
* [How to run](#how-to-run)

## Source


This is a project from the Udacity Full Stack Nanodegree program: https://eu.udacity.com/course/full-stack-web-developer-nanodegree--nd004. Download data [here](https://d17h27t6h515a5.cloudfront.net/topher/2016/August/57b5f748_newsdata/newsdata.zip)


## How to run

- cd to folder with vagrant
- vagrant up
- vagrant ssh
- cd /vagrant
- if no data:
	- add data to database (with `psql -d news -f newsdata.sql`)

- then
	- run the python file (with `python logs.py`)
	OR
	- start database (`psql -d news`)


## Code design

The logs.py file contains 3 function to perform analysis, and one helper function to inform the user to create view. `top_article()`, `top_writer()` and `top_error()` answer the following questions:

1. What are the most popular three articles of all time?
2. Who are the most popular article authors of all time?
3. On which days did more than 1% of requests lead to errors?


## Views created

Here is the view I created to run my queries:

```
CREATE VIEW path_slug_count AS
SELECT COUNT(path), SUBSTRING(log.path, 10, LENGTH(log.path)) AS path_slug
FROM log GROUP BY path_slug
ORDER BY COUNT(path) DESC;
```

## FUN
