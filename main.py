#!usr/bin/env python3

import psycopg2

# What are the most popular three articles of all time?
report_title_1 = ("The most popular 3 articles of all time:")
report_result_1 = (
    "select articles.title, count(*) as views "
    "from articles inner join log on log.path "
    "like concat('%', articles.slug, '%') "
    "where log.status like '%200%' group by "
    "articles.title, log.path order by views desc limit 3")

# Who are the most popular article authors of all time?
report_title_2 = ("The most popular article authors of all time:")
report_result_2 = (
    "select authors.name, count(*) as views from articles inner "
    "join authors on articles.author = authors.id inner join log "
    "on log.path like concat('%', articles.slug, '%') where "
    "log.status like '%200%' group "
    "by authors.name order by views desc")

# On which days did more than 1% of requests lead to errors
report_title_3 = ("The days did have more than 1% of requests lead to errors:")
report_result_3 = (
    "select day, perc from ("
    "select day, round((sum(requests)/(select count(*) from log where "
    "substring(cast(log.time as text), 0, 11) = day) * 100), 2) as "
    "perc from (select substring(cast(log.time as text), 0, 11) as day, "
    "count(*) as requests from log where status like '%404%' group by day)"
    "as log_percentage group by day order by perc desc) as final_query "
    "where perc >= 1")


def connect(database_name="news"):
    '''Connect to the PostgreSQL database & return the database connection '''
    try:
        db = psycopg2.connect("dbname={}".format(database_name))
        cursor = db.cursor()
        return db, cursor
    except BaseException:
        print("Cannot connect to the database")
	sys.exit(1)


def get_results(query):
    '''Return the answer for each questions'''
    db, cursor = connect()
    cursor.execute(query)
    return cursor.fetchall()
    db.close()


def print_results(query_results):
    print(query_results[1])
    for index, results in enumerate(query_results[0]):
        print("\t",
               index + 1,
               "-",
               results[0],
               "\t - ",
               str(results[1]),
               "views")


def print_error_results(query_results):
    print(query_results[1])
    for results in query_results[0]:
        print("\t", results[0], "-", str(results[1]) + "% errors")


if __name__ == '__main__':
    # Save the results
    popular_articles_results = get_results(report_result_1), report_title_1
    popular_authors_results = get_results(report_result_2), report_title_2
    load_error_days = get_results(report_result_3), report_title_3

    # Print the results
    print_results(popular_articles_results)
	#print the top popular articles.
    print_results(popular_authors_results)
	#print the top popular authors.
    print_error_results(load_error_days)
	#print the days which have more than 1% error.
