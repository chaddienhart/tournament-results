#!/usr/bin/env python
# 
# tournament.py -- implementation of a Swiss-system tournament
#

import psycopg2
import string


def connect():
    """Connect to the PostgreSQL database.  Returns a database connection."""
    return psycopg2.connect("dbname = tournament")

def dbExecute(sql, isfetch=None):
    """Open the database, get a cursor, call the sql passed in
    if this is a fetch command: fetchall 
    if this is NOT a fetch commit the database change
    returns the result of fetchall if fetch was called"""
    db = connect()
    c = db.cursor()
    c.execute(sql)
    if isfetch is not None:
        result = c.fetchall()
    else:
        db.commit()
    c.close()
    db.close()
    if isfetch is not None:
        return result
    
def deleteMatches():
    """Remove all the match records from the database."""
    dbExecute('DELETE FROM matches;')

def deletePlayers():
    """Remove all the player records from the database."""
    dbExecute("DELETE FROM players;")

def countPlayers():
    """Returns the number of players currently registered.
    select the count of 'id' in the players table, if the table is empty
    the COUNT(id) will be null and a more suitable value of zero is returned """
    
    num = dbExecute("SELECT COALESCE(COUNT(id), 0) as count FROM players;", True)
    return num[0][0]

def registerPlayer(name):
    """Adds a player to the tournament database.
  
    The database assigns a unique serial id number for the player.  (This
    should be handled by your SQL database schema, not in your Python code.)
  
    Args:
      name: the player's full name (need not be unique).
      
    format any "'" in the name to be "''". for example "Boots O'Neal" becomes "Boots O''Neal"  """
    name = string.replace(name, "'", "''")
    dbExecute("INSERT INTO players (id, name) VALUES (DEFAULT, '%s')" %(name,) )

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
    standings = dbExecute("SELECT matchesplayed.id, matchesplayed.name, " + \
                          "COALESCE(wins.win_count, 0)AS wins, matchesplayed.count AS matches_played " + \
                          "FROM matchesplayed LEFT JOIN wins ON matchesplayed.id = wins.id " + \
                          "ORDER BY wins.win_count DESC NULLS LAST;", True)
    return standings

def reportMatch(winner, loser, tie = 'false'):
    """Records the outcome of a single match between two players.

    Args:
      winner:  the id number of the player who won
      loser:  the id number of the player who lost
      tie:     for future enhancement, always defaults to false for now
    """
    dbExecute("INSERT INTO matches VALUES (%d, %d, %s)" % (winner, loser, tie) )
 
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
    # join the matchesplayed view with the wins view on player id, then order by descending
    # number of wins, with nulls last (in case there are players who have not played yet)
    standings = dbExecute("SELECT matchesplayed.id, matchesplayed.name " + \
                          "FROM matchesplayed LEFT JOIN wins ON matchesplayed.id = wins.id " + \
                          "ORDER BY wins.win_count DESC NULLS LAST;", True)
                          
    pairings = [] # create a list that will get the tuples appended and returned
    
    """ **** Extra credit ****
    If there are an odd number of players run query to get the player with the most matches 
    and most wins. Add an entry into the pairings with this player receiving a bye.
    Then remove that player from the list of standings used to create the swiss pairings.
    """
    section check for an odd number of players    
    if len(standings) % 2 != 0: 
        # get the player with the most matches and wins to give the bye to
        excld = dbExecute("SELECT matchesplayed.id " + \
        "FROM matchesplayed LEFT JOIN wins ON matchesplayed.id = wins.id " + \
        "ORDER BY matchesplayed.count DESC NULLS LAST, wins.win_count DESC NULLS LAST LIMIT 1;", True)
        temp = [id for id in standings if id[0] == excld[0][0]][0]  + (0, "bye")
        pairings.append(temp)
        standings = [id for id in standings if id[0] != excld[0][0]]
    """ **** End Extra credit section **** """

        
    # loop over standings counting by 2s 
    for i in range(0, len(standings)-1, 2):
        temp = standings[i] + standings[i+1]
        pairings.append(temp)
    return pairings
    

