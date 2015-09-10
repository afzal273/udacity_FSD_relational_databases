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
    :return: the query result if select or None if no results asked for
    """
    result = None

    DB = connect()
    cursor = DB.cursor()
    cursor.execute(sql, data)

    # Fetch result according to return type
    if rtype == 'count':
        # if fetching count, fetch and return first row
        result = int(cursor.fetchone()[0])
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


def resetMatchNumberSequence():
    """
    Reset the match number sequence to start from 1
    """
    runQuery("ALTER SEQUENCE matches_match_number_seq RESTART WITH 1;")


def resetPlayerNumberSequence():
    """
    Reset the player_id sequence to start from 1
    """
    runQuery("ALTER SEQUENCE players_player_id_seq RESTART WITH 1;")


def getStats(player_id):
    """
    Retuns the current stats for the player from the standings table
    :param player_id: player_id to get stats for
    :return stats for the player_id
    """
    get_stats_sql = "SELECT * FROM standings WHERE player_id = %s;"
    data = (player_id,)
    return runQuery(get_stats_sql, rtype='rows', data=data)


def updateMatchesTable(winner, loser, isTie):
    """
    Updates the matches table with winner and loser
    :param winner: winner of the current match
    :param loser: loser of the current match
    :param isTie: Is the reported match a tie?

    """
    insert_matches_sql = "INSERT INTO matches (id1, id2, winner, isTie) VALUES  (%s, %s, %s, %s);"
    data = (winner, loser, winner, isTie)
    runQuery(insert_matches_sql, commit=True, data=data)


def updateStandingsTable(player_id, result=None):
    """
    Update standings table with outcome of a match or when new player is registered
    Give 1 point for a win, -1 for a loss and 0.5 for a tie to the netscore

    :param player_id:
    :param result: winner, loser, tie or new_player
    """
    data = (player_id,)
    update_sql = None
    if result == 'winner':
        update_sql = "UPDATE standings SET matches = matches +1, wins = wins + 1, netscore = netscore +1 WHERE player_id = %s;"
    elif result == 'loser':
        update_sql = "UPDATE standings SET matches = matches +1, losses = losses + 1, netscore = netscore - 1 WHERE player_id = %s;"
    elif result == 'tie':
        update_sql = "UPDATE standings SET matches = matches +1, ties = ties + 1, netscore = netscore + 0.5  WHERE player_id = %s;"
    elif result == 'new_player':
        update_sql = "INSERT INTO standings (player_id, matches, wins, ties, losses, netscore) VALUES  (%s, 0, 0, 0, 0, 0);"
    else:
        return "Result should be winner, loser, tie or new_player"

    runQuery(update_sql, commit=True, data=data)
