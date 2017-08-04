#!/usr/bin/env python
# 
# tournament.py -- implementation of a Swiss-system tournament
#

import psycopg2


def connect(database_name="tournament"):
    """Connect to the PostgreSQL database.  Returns a database connection."""
    try:
        db = psycopg2.connect("dbname={}".format(database_name))
        cursor = db.cursor()
        return db, cursor
    except:
        print "Error connecting to database!"


def deleteMatches():
    """Remove all the match records from the database."""
    db_con, cursor = connect()
    # db_con = connect()
    # cursor = db_con.cursor()
    matches = "DELETE FROM matches"
    cursor.execute(matches)
    db_con.commit()
    db_con.close()

def deletePlayers():
    """Remove all the player records from the database."""
    db_con, cursor = connect()

    # db_con = connect()
    # cursor = db_con.cursor()
    cursor.execute("DELETE FROM players")
    db_con.commit()
    db_con.close()


def countPlayers():
    """Returns the number of players currently registered."""
    # db_con = connect()
    # cursor = db_con.cursor()
    db_con, cursor = connect()
    sql = """SELECT count(*) FROM players"""
    cursor.execute(sql)
    players = cursor.fetchone()[0]
    db_con.close()
    # print players
    return players


def registerPlayer(name):
    """Adds a player to the tournament database.

    The database assigns a unique serial id number for the player.  (This
    should be handled by your SQL database schema, not in your Python code.)

    Args:
      name: the player's full name (need not be unique).
    """
    # db_con = connect()
    # cursor = db_con.cursor()
    db_con, cursor = connect()
    player = """INSERT INTO players (name) VALUES (%s) """
    cursor.execute(player, (name,))
    db_con.commit()
    db_con.close()


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

    # db_conn = connect()
    # cursor = db_conn.cursor()
    db_con, cursor = connect()
    standings_query = "SELECT * FROM player_standings"
    cursor.execute(standings_query)
    player_standings = cursor.fetchall()

    i = 0
    for player in player_standings:

        player_standings[i] = (player[0], player[1], player[2], player[3])
        db_con.commit()
        db_con.close()
        return player_standings


def reportMatch(winner, loser):
    """Records the outcome of a single match between two players.

    Args:
      winner:  the id number of the player who won
      loser:  the id number of the player who lost
    """

    # db_conn = connect()
    # cursor = db_conn.cursor()
    db_con, cursor = connect()
    match = "INSERT INTO matches (winner_id, loser_id, draw) VALUES (%s,%s,%s)"
    cursor.execute(match, (winner, loser, False))
    db_con.commit()
    db_con.close()


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

    # db_conn = connect()
    # cursor = db_conn.cursor()
    db_con, cursor = connect()
    query = "SELECT COUNT(*) FROM player_standings"
    standings = playerStandings()
    cursor.execute(query)
    result = cursor.fetchall()
    player = [item[0:2] for item in standings]
    index = 0
    pairings = []

    for row in result:
        while index < row[0]:
            pair = player[index]+player[index+1]
            pairings.append(pair)
            index = index + 2
    db_con.close()
    return pairings
