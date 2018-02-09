#!/usr/bin/env python
#
# logs.py -- project for the FSND Udacity program
#

import psycopg2


def connect():
    """Connect to the PostgreSQL database.  Returns a database connection."""
    return psycopg2.connect("dbname=news")


def top_error():
    """Prints the day with the most errors."""
    DB = connect()
    c = DB.cursor()
    c.execute("""
        SELECT
            CAST(CAST(time AS DATE) as varchar),
            CAST(
                COUNT(CASE WHEN status = '404 NOT FOUND' THEN status END)
                AS float)
            / CAST(
                COUNT(CASE WHEN status = '200 OK' THEN status END)
                AS float)
            * 100 AS percentage_error
        FROM log
        GROUP BY CAST(time AS DATE)
        ORDER BY percentage_error DESC;
    """)
    errors = c.fetchall()
    DB.commit()
    DB.close()
    print "\n\nLet's see how our pages are doing:\n"

    for entry in errors:
        if entry[1] > 1:
            print "On this date", entry[0], ", the error rate was: "
            "%.2f" % entry[1]
        else:
            break
    print "\nThis is it for bad days."


def top_writer():
    """Prints authors with the sum of views of their articles"""
    DB = connect()
    c = DB.cursor()
    c.execute("""
        SELECT SUM(path_slug_count.count), authors.name
        FROM path_slug_count
            INNER JOIN articles
                ON path_slug_count.path_slug = articles.slug
            INNER JOIN authors
                ON authors.id = articles.author
        GROUP BY authors.name
        ORDER BY COUNT(authors.name) DESC;
    """)
    writers = c.fetchall()
    DB.commit()
    DB.close()

    print "\n\nLet's see what our writers are doing:\n"
    for writer in writers:
        print writer[1], "wrote articles that got", writer[0], "views!"
    print "\nProlific writers!"


def top_article():
    """Prints the article that got the most views"""
    DB = connect()
    c = DB.cursor()
    c.execute("""
        SELECT path_slug_count.count, articles.title
        FROM path_slug_count JOIN articles
        ON path_slug_count.path_slug = articles.slug;
    """)
    top_article = c.fetchone()
    DB.commit()
    DB.close()

    print "\n\nLet's see which article is the hottest:\n"
    print "This article: '" + top_article[1] + "' got", top_article[0], "views"
    print "\nWhohohoa!"


def check_view():
    DB = connect()
    c = DB.cursor()
    try:
        c.execute("""
            SELECT * FROM path_slug_count
            LIMIT 1;
        """)
        view_response = True
    except:
        print "No views, please CREATE VIEWS - check README.md"
        view_response = False
    DB.commit()
    DB.close()
    return view_response

# if view is present run analysis code
if check_view():
    print "\n                   Starting analysis..."
    top_article()
    top_writer()
    top_error()
    print "\n\n------------------------------------"
    print "\n                   Analysis completed\n\n"
