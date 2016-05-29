#!/usr/bin/env python
# 
# tournament.py -- implementation of a Swiss-system tournament
#

import psycopg2
import sys

#Code to connect to the tournament database.
def connect(database_name="tournament"):
    """Connect to the PostgreSQL database.  Returns a database connection."""
    try:
        db = psycopg2.connect("dbname={}".format(database_name))
        cursor = db.cursor()
        return db, cursor
    except:
        print ("There was an error connecting to the database %s", database_name)


#Code to delete matches from the database
def deleteMatches():
    """Remove all the match records from the database."""
    conn, c = connect()
    query = "DELETE FROM matches"
    c.execute(query)
    conn.commit()
    conn.close()

#Code to ddelete players from the database
def deletePlayers():
    """Remove all the player records from the database."""
    conn, c = connect()
    query = "DELETE FROM players"
    c.execute(query)
    conn.commit()
    conn.close()

#Code to count all players in the database
def countPlayers():
    """Returns the number of players currently registered."""
    conn, c = connect()
    query = "SELECT count(*) as num FROM players"
    c.execute(query)
    count = c.fetchone()
    conn.close()
    return count[0]

#Code to regoster a player in the database.
def registerPlayer(name):
    """Adds a player to the tournament database.
  
    The database assigns a unique serial id number for the player.  (This
    should be handled by your SQL database schema, not in your Python code.)
  
    Args:
      name: the player's full name (need not be unique).
    """
    conn, c = connect()
    parameters = (name,)
    query = "INSERT INTO players (name) VALUES (%s)"
    c.execute(query, parameters)
    conn.commit()
    conn.close()

#Code to check a players' standing in the database
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
    conn, c = connect()
    query = """SELECT p.id, p.name, count(m.winner) as wins, g.num 
                FROM gameNmb AS g,players AS p
                LEFT JOIN matches AS m
                ON p.id = m.winner
                WHERE p.id = g.id
                GROUP BY p.id, p.name, g.num
                ORDER BY wins, p.name"""
    c.execute(query)
    rankings = c.fetchall()
    conn.close()
    return rankings

#Code to eecord outcome of the match
def reportMatch(winner, loser):
    """Records the outcome of a single match between two players.

    Args:
      winner:  the id number of the player who won
      loser:  the id number of the player who lost
    """
    conn, c = connect()
    query = """INSERT INTO matches (winner, loser) 
        VALUES (%s,%s)"""
    parameters = (winner,loser)
    c.execute(query, parameters)
    conn.commit()
    conn.close()
 
 #Code to pair up players based upon win records
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
    #Get players in ranked order from playerStandings function
    rankings = playerStandings()
    pairings = []
    count = 0

    # Loop through query two at a time assigning 2 players to a tuple for a match
    while(count < len(rankings)):
        pairholder = (rankings[count][0],rankings[count][1],
            rankings[count + 1][0], rankings[count + 1][1])
        pairings.append(pairholder)
        count = count + 2

    return pairings



