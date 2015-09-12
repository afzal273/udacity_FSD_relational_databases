#!/usr/bin/env python
#
# tournament.py -- implementation of a Swiss-system tournament
#

from utils import *


def deleteMatches(tournament_id=None):
    """Remove all the match records from the database."""

    data = None

    if tournament_id:
        # Make all match records 0 in standings table and delete all matches
        # only for the tournament_id specified
        update_matches_sql = "DELETE FROM matches WHERE tournament_id=(%s);"
        update_standings_sql = "UPDATE standings SET matches = 0, wins = 0, ties = 0, losses = 0, netscore = 0 WHERE tournament_id=(%s);"
        data = (tournament_id,)

    else:
        # Make all match records 0 in standings table and delete all matches
        update_matches_sql = "DELETE FROM matches;"
        update_standings_sql = "UPDATE standings SET matches = 0, wins = 0, ties = 0, losses = 0, netscore = 0;"

    runQuery(update_matches_sql, data=data, commit=True)
    runQuery(update_standings_sql, data=data, commit=True)


def deletePlayers(tournament_id=None):
    """Remove player records from the database for all players or for a tournament"""

    # Delete rows from players, matches and standings tables for tournament_id
    # specified
    if tournament_id:
        runQuery("DELETE FROM matches WHERE tournament_id = %s;",
                 data=(tournament_id,), commit=True)
        runQuery("DELETE FROM standings WHERE tournament_id = %s;",
                 data=(tournament_id,), commit=True)
        runQuery("DELETE FROM player_tournaments WHERE tournament_id = %s;", data=(
            tournament_id,), commit=True)
        runQuery("DELETE FROM tournaments WHERE tournament_id = %s;",
                 data=(tournament_id,), commit=True)
    else:
        # Delete all rows from players, matches and standings tables
        runQuery("DELETE FROM matches", commit=True)
        runQuery("DELETE FROM standings", commit=True)
        runQuery("DELETE FROM player_tournaments", commit=True)
        runQuery("DELETE FROM players", commit=True)
        runQuery("DELETE FROM tournaments", commit=True)
        # Reset player_id sequence to start from 1 when player table is cleared
        resetPlayerNumberSequence()

        # Reset match_number sequence to start from 1 when matches table is
        # cleared
        resetMatchNumberSequence()


def countPlayers(tournament_id=None):
    """Returns the number of players currently registered."""

    # If tournament id is specified return count only for the tournament
    if tournament_id:
        return runQuery("SELECT count(*) as num from player_tournaments WHERE tournament_id = %s;", data=(tournament_id,), rtype='count')
    else:
        return runQuery("SELECT count(*) as num from players;", rtype='count')


def registerPlayer(name, tournament_id=None):
    """Adds a player to the tournament database.

    The database assigns a unique serial id number for the player.  (This
    should be handled by your SQL database schema, not in your Python code.)

    Args:
      name: the player's full name (need not be unique).
    """
    # Insert player into the players table
    insert_player_sql = "INSERT INTO players (name) VALUES (%s) RETURNING player_id;"

    # Grab the player_id so tournament details can be added
    player_id = (runQuery(insert_player_sql, rtype='one_row',
                          commit=True, data=(name,)))[0]

    # If player is registering for a tournament call the function below
    if tournament_id:
        registerPlayerToTournament(player_id, tournament_id)


def registerPlayerToTournament(player_id, tournament_id):
    """
    Adds a player to a tournament tables and populates standing tables
    :param player_id: player_id
    :param tournament_id: tournament_id

    """

    # insert into tournaments if the tournament is not already in there
    insert_into_touranments_sql = "INSERT INTO tournaments (Tournament_id) SELECT (%s) WHERE NOT EXISTS (SELECT * FROM tournaments WHERE Tournament_id = %s);"
    data = (tournament_id, tournament_id)
    runQuery(insert_into_touranments_sql, data=data, commit=True)

    # insert into player_tournaments and populate standings table
    insert_into_player_tournaments_sql = "INSERT INTO player_tournaments (Player_id, Tournament_id) VALUES (%s, %s);"
    data = (player_id, tournament_id)
    runQuery(insert_into_player_tournaments_sql, data=data, commit=True)

    updateStandingsTable(player_id, 'new_player', tournament_id)


def playerStandings(tournament_id):
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

    player_standings_sql = "SELECT player_id, name, wins, ties, matches FROM player_standings WHERE tournament_id = %s;"
    return runQuery(player_standings_sql, data=(tournament_id,), rtype='rows')


def reportMatch(winner, loser, tournament_id, isTie=False):
    """Records the outcome of a single match between two players.

    :param isTie:
    Args:
      winner:  the id number of the player who won
      loser:  the id number of the player who lost
      isTie: is the match a tie?
    """

    # Update matches table and standings table
    updateMatchesTable(winner, loser, isTie, tournament_id)
    if isTie:
        updateStandingsTable(winner, 'tie', tournament_id)
        updateStandingsTable(loser, 'tie', tournament_id)
    else:
        updateStandingsTable(winner, 'winner', tournament_id)
        updateStandingsTable(loser, 'loser', tournament_id)


def swissPairings(tournament_id):
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
    curr_standings = playerStandings(tournament_id)
    # Take 2 tuples out of the current standings at a time and make a list of
    # player_id and name tuples from each tuple
    return [(p1[0], p1[1], p2[0], p2[1]) for (p1, p2) in zip(curr_standings[::2], curr_standings[1::2])]
