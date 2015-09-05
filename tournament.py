#!/usr/bin/env python
# 
# tournament.py -- implementation of a Swiss-system tournament
#

from utils import *


def deleteMatches():
    """Remove all the match records from the database."""
    sql1 = "DELETE FROM matches"
    sql2 = "DELETE FROM standings"
    runQuery(sql1, commit=True)
    runQuery(sql2, commit=True)


def deletePlayers():
    """Remove all the player records from the database."""
    deleteMatches()
    sql = "DELETE FROM players"
    runQuery(sql, commit=True)


def countPlayers():
    """Returns the number of players currently registered."""
    sql = "SELECT count(*) as num from players"
    return runQuery(sql, rtype="count")


def registerPlayer(name):
    """Adds a player to the tournament database.
  
    The database assigns a unique serial id number for the player.  (This
    should be handled by your SQL database schema, not in your Python code.)
  
    Args:
      name: the player's full name (need not be unique).
    """
    sql = "INSERT INTO players (name) VALUES (%s);"
    data = (name,)
    runQuery(sql, commit=True, data=data)


def playerStandings():
    """Returns a list of the players and their win records, sorted by wins.

    The first entry in the list should be the player in first place, or a player
    tied for first place if there is currently a tie.

    Returns:
      A list of tuples, each of which contains (id, name, wins, matches):
        id: the player's unique id (assigned by the database)
        name: the player's full name (as registered)
        wins: the number of matches the player has won
        matches: the number of matches the player has played
    """
    sql = "select * from player_standings"
    return runQuery(sql, rtype="rows")


def getStats(player_id):
    """
    Retuns the current stats for the player from the standings table
    """
    get_stats_sql = "SELECT * FROM standings WHERE player_id = %s;"
    data = (player_id,)
    return runQuery(get_stats_sql, rtype='rows', data=data)

def updateMatchesTable(winner, loser):
    insert_matches_sql = "INSERT INTO matches (id1, id2, winner, loser) VALUES  (%s, %s, %s, %s);"
    data = (winner, loser, winner, loser)
    runQuery(insert_matches_sql, commit=True, data=data)

def reportMatch(winner, loser):
    """Records the outcome of a single match between two players.

    Args:
      winner:  the id number of the player who won
      loser:  the id number of the player who lost
    """
    # DB = connect()
    # cursor = DB.cursor()
    # cursor.execute\
    #     ("INSERT INTO matches (id1, id2, winner, loser) VALUES  (%s, %s, %s, %s)", )
    updateMatchesTable(winner, loser)
    # TODO - udpate standings table
    updateStandingsTable(winner, 'winner')
    updateStandingsTable(loser, 'loser')


def updateStandingsTable(player_id, result):
    data = (player_id,)
    fetch_stats_sql = "SELECT * FROM standings WHERE player_id = %s;"
    current_stats = runQuery(fetch_stats_sql, rtype='one_row', data=data)
    data = (player_id,)

    update_sql = None
    # Determining which sql to run
    if result == 'winner':
        if current_stats:
            update_sql = "UPDATE standings SET matches = matches +1, wins = wins + 1, netscore = netscore +1 WHERE player_id = %s;"
        else:
            update_sql = "INSERT INTO standings (player_id, matches, wins, losses, netscore) VALUES  (%s, 1, 1, 0, 1);"
    elif result == 'loser':
        if current_stats:
            update_sql = "UPDATE standings SET matches = matches +1, losses = losses + 1, netscore = netscore - 1 WHERE player_id = %s;"
        else:
            update_sql = "INSERT INTO standings (player_id, matches, wins, losses, netscore) VALUES  (%s, 1, 0, 1, -1);"

    runQuery(update_sql, commit=True, data=data)



 
 
def swissPairings():
    """Returns a list of pairs of players for the next round of a match.
  
    Assuming that there are an even number of players registered, each player
    appears exactly once in the pairings.  Each player is paired with another
    player with an equal or nearly-equal win record, that is, a player adjacent
    to him or her in the standings.
  
    Returns:
      A list of tuples, each of which contains (id1, name1, id2, name2)
        id1: the first player's unique id
        name1: the first player's name
        id2: the second player's unique id
        name2: the second player's name
    """




