# Logs Analysis Project

## Table of Contents

* [Project description](#project-description)
* [Source](#source)
* [Requirements](#requirements)
* [How to run](#how-to-run)
* [Code design](#code-design)
* [Views created](#views-created)


## Project description

This is a project from the Udacity Full Stack Nanodegree program, its point is to create a Python script that uses psycopg2 to query a mock PostgreSQL database. This database contains fictional log data from a news webiste. The queries generate a report that answer the following 3 questions

1. What are the most popular three articles of all time?
2. Who are the most popular article authors of all time?
3. On which days did more than 1% of requests lead to errors?


The logs.py file contains 3 functions to perform this analysis (`top_article()`, `top_writer()` and `top_error()`) and one helper function to inform the user to create view, if view not present (`check_view()`).


## Source

This is a project from the Udacity Full Stack Nanodegree program: https://www.udacity.com/course/full-stack-web-developer-nanodegree--nd004. Download data [here](https://d17h27t6h515a5.cloudfront.net/topher/2016/August/57b5f748_newsdata/newsdata.zip). Unzip `newsdata.zip` to extract `newsdata.sql`.


## Requirements

Install the following to run the project

[Vagrant](https://www.vagrantup.com/downloads.html)
[VirtualBox](https://www.virtualbox.org/wiki/Download_Old_Builds_5_1)


I also used these:
- Python 2.7
- PostgreSQL
- psycopg2 - module to connect to the database.


## How to run

- cd to folder with project
- vagrant init
- vagrant up
- vagrant ssh
- cd /vagrant
- if no data:
	- add data to database (with `psql -d news -f newsdata.sql`)
	- add view from [Views created](#views-created)

- then
	- run the python file (with `python logs.py`)
	OR
	- start database (`psql -d news`)


## Views created

Here is the view I created to run my queries:

```sql
CREATE VIEW path_slug_count AS
SELECT COUNT(path), log.path AS path
FROM log GROUP BY path
ORDER BY COUNT(path) DESC;
```

## FUN
