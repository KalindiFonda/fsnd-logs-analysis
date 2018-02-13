#!/usr/bin/env python
#
# logs.py -- project for the FSND Udacity program
#

import psycopg2


def connect():
    """Connect to the PostgreSQL database.  Returns a database connection."""
    return psycopg2.connect("dbname=news")


def top_error():
    """Prints the day where error rate is higher than 1%."""
    DB = connect()
    c = DB.cursor()
    c.execute("""
        SELECT * FROM (
            SELECT
                CAST(time AS DATE),
                CAST(
                    COUNT(CASE WHEN status = '404 NOT FOUND'
                        THEN status END) AS float)
                / COUNT(*)
                * 100 AS percentage_error
            FROM log
            GROUP BY CAST(time AS DATE)
            ORDER BY percentage_error DESC
        ) AS errors_on_date
        WHERE percentage_error > 1;
    """)

    errors = c.fetchall()
    DB.close()

    print "\n\nLet's see how our pages are doing:\n"
    for day_date, error in errors:
        print "On this date: {} " \
        "the error rate was: {:.2f} %!".format(day_date, error)
    print "\nThis is it for bad days."


def top_writer():
    """Prints authors with the sum of views of their articles"""
    DB = connect()
    c = DB.cursor()
    c.execute("""
        SELECT SUM(path_slug_count.count), authors.name
        FROM path_slug_count
            INNER JOIN articles
                ON '/article/' || articles.slug = path_slug_count.path
            INNER JOIN authors
                ON authors.id = articles.author
        GROUP BY authors.name
        ORDER BY COUNT(authors.name) DESC;
    """)
    writers = c.fetchall()
    DB.close()

    print "\n\nLet's see what our writers are doing:\n"
    for views, writer in writers:
        print "{} wrote articles that got {:,} views!".format(writer, views)
    print "\nProlific writers!"


def top_article():
    """Prints the article that got the most views"""
    DB = connect()
    c = DB.cursor()
    c.execute("""
        SELECT path_slug_count.count, articles.title
        FROM path_slug_count JOIN articles
         ON '/article/' || articles.slug = path_slug_count.path
        LIMIT 3;
    """)
    top_articles = c.fetchall()
    DB.close()

    print "\n\nLet's see which articles are the hottest:\n"
    for views, article in top_articles:
        print "This article: '{}' got {:,} views!".format(article, views)
    print "\nWhohohoa!"


def check_view():
    # checks if the views necessary to run the analysis are present.
    # If not present informs the user with a print statement.
    DB = connect()
    c = DB.cursor()
    try:
        c.execute("""
            SELECT 1 FROM path_slug_count;
        """)
        view_response = True
    except:
        print "No views, please CREATE VIEWS - check README.md"
        view_response = False
    DB.close()
    return view_response

# if view is present run analysis code
if __name__ == '__main__':
    if check_view():
        print "\n                   Starting analysis..."
        top_article()
        top_writer()
        top_error()
        print "\n\n------------------------------------"
        print "\n                   Analysis completed\n\n"
