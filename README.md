Tournament Planner
  
  Udacity Full Stack Web Developer - Project 2 - by Chad Dienhart

Uses Python and PostgreSQL to register, create Swiss pairings, track matches, and report standings for a tournament.

Designed for use with:
    
    PostgreSQL (http://www.postgresql.org/) -- version 9.3.6
    
    Python (https://www.python.org/downloads/) -- version 2.7.6
    
Files:
    tournament.sql - used to setup the PostgreSQL database, tables, views
    
    tournament_test.py - test code to check the functionality provided by tournament.py, 9 tests in total
    
    tournament.py - python functions to perform the following
        registerPlayer(name) - Adds a player to the tournament database and assigns an ID number to the player.
        countPlayers() - Returns the number of currently registered players.
        deletePlayers() - Removes all players from the database.
        reportMatch(winner, loser) - report match results using player ID number
        deleteMatches() - Removes all matches from the database.
        playerStandings() - Returns a list of (id, name, wins, matches) for each player, sorted by wins. 
                            Includes players with no wins.
        swissPairings() - generates and returns a list of pairings according to the Swiss system. 
                          Each pairing is a tuple (id1, name1, id2, name2), giving the ID and name of the 
                          paired players. If there is an odd number of players a bye is assigned to the 
                          player with the most matches and wins.
                          
Usage:

    1. Set up your database, tables, and views.
      run psql
      from the prompt import the tournament.sql file 
        => \i tournament.sql
        => \q 
      to exit
    
    2. to run the test suite
      from a shell prompt 
        :$ python tournament_test.py
    
  Should produce output like this:
  
        1. Old matches can be deleted.
        2. Player records can be deleted.
        3. After deleting, countPlayers() returns zero.
        4. After registering a player, countPlayers() returns 1.
        5. Players can be registered and deleted.
        6. Newly registered players appear in the standings with no matches.
        7. After a match, players have updated standings.
        8. After one match, players with one win are paired.
        9. After a complete round of matches each player received only one bye.
        Success!  All tests pass!
