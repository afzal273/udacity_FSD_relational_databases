import psycopg2

__author__ = 'Afzal Syed'

def connect():
    """Connect to the PostgreSQL database.  Returns a database connection."""
    return psycopg2.connect("dbname=tournament")


def runQuery(sql, commit=None, rtype=None, data=None):
    """
    Execute a sql query
    :param sql: The sql to be executed
    :param commit: should the DB be commited to?
    :param data: data to be passed to the sql
    :param rtype: return type, determines how the query results should be parsed and returned
                  allowed return types - count for number of rows
                                       - rows for multiple rows from db if present
                                       - one_row - return the first row
    :return: the query result if select or None if insert or select query
    """
    result = None

    DB = connect()
    cursor = DB.cursor()
    cursor.execute(sql, data)

    # Fetch result according to return type
    if rtype == 'count':
        # if fetching count, fetch and return first row
        result = cursor.fetchone()[0]
    elif rtype == 'one_row':
        # if fetching all rows, return all rows
        result = cursor.fetchone()
    elif rtype == 'rows':
        # if fetching all rows, return all rows
        result = cursor.fetchall()

    # If commit is true then commit to the DB
    if commit:
        DB.commit()
    DB.close()

    return result
