#!/usr/bin/env python
#
# tournament.py -- implementation of a Swiss-system tournament
#

from utils import *


def deleteMatches():
    """Remove all the match records from the database."""

    # Delete all rows from matches table
    runQuery("DELETE FROM matches", commit=True)

    # Reset match_number sequence to start from 1 when matches table is cleared
    resetMatchNumberSequence()

    # Make all match records 0 in standings table
    update_standings_sql = "UPDATE standings SET matches = 0, wins = 0, ties = 0, losses = 0, netscore = 0;"
    runQuery(update_standings_sql, commit=True)


def deletePlayers():
    """Remove all the player records from the database."""

    # Delete all rows from players, matches and standings tables
    runQuery("DELETE FROM matches", commit=True)
    runQuery("DELETE FROM standings", commit=True)
    runQuery("DELETE FROM players", commit=True)

    # Reset player_id sequence to start from 1 when player table is cleared
    resetPlayerNumberSequence()

    # Reset match_number sequence to start from 1 when matches table is cleared
    resetMatchNumberSequence()


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
    # Insert player into the players table
    insert_player_sql = "INSERT INTO players (name) VALUES (%s) RETURNING player_id;"
    data = (name,)

    # Grab the player_id
    player_id = (runQuery(insert_player_sql, rtype='one_row', commit=True, data=data,))[0]

    # Insert a row in the standings table with 0s so it can return swiss
    # pairings for the first time
    updateStandingsTable(player_id, 'new_player')


def playerStandings():
    """Returns a list of the players and their win records, sorted by wins.

    The first entry in the list should be the player in first place, or a player
    tied for first place if there is currently a tie.

    Returns:
      A list of tuples, each of which contains (id, name, wins, ties, matches):
        id: the player's unique id (assigned by the database)
        name: the player's full name (as registered)
        wins: the number of matches the player has won
        matches: the number of matches the player has played
    """
    return runQuery("select * from player_standings", rtype="rows")


def reportMatch(winner, loser, isTie=False):
    """Records the outcome of a single match between two players.

    :param isTie:
    Args:
      winner:  the id number of the player who won
      loser:  the id number of the player who lost
      isTie: is the match a tie?
    """

    # Update matches table and standings table
    updateMatchesTable(winner, loser, isTie)
    if isTie:
        updateStandingsTable(winner, 'tie')
        updateStandingsTable(loser, 'tie')
    else:
        updateStandingsTable(winner, 'winner')
        updateStandingsTable(loser, 'loser')


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
    curr_standings = playerStandings()
    # Take 2 tuples out of the current standings at a time and make a list of player_id and name tuples from each tuple
    return [(p1[0], p1[1], p2[0], p2[1]) for (p1, p2) in zip(curr_standings[::2], curr_standings[1::2])]
