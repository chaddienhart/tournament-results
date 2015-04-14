-- Table definitions for the tournament project.
--
CREATE DATABASE tournament;

-- Put your SQL 'create table' statements in this file; also 'create view'
-- statements if you choose to use it.
--
-- I needed to add this to get the tables created in the correct database
\connect tournament;
-- create two tables: 

-- players contains a unique id, and a name 
CREATE TABLE players (id serial primary key, name text);

-- matches records matches played (winner and loser) by player id
-- tie is not used but is here for future enhancement
CREATE TABLE matches (winner integer REFERENCES players, loser integer REFERENCES players, tie boolean);

-- create view to count all the matches played by each player
-- return the id, name, and total matches played as count
CREATE VIEW matchesplayed AS
SELECT name, id, count(winner) as count 
FROM players left join matches
ON id = winner OR id = loser
GROUP BY id
;

-- create a view to count all the wins for each player
-- return the id, name, and total wins as win_count
CREATE VIEW wins AS
SELECT a.id, a.name, count(*) as win_count
FROM players as a, matches as b
WHERE a.id = b.winner
GROUP BY a.id
ORDER BY win_count DESC
;


-- for testing in sqlfiddle.com
-- insert into players (id, name) VALUES (DEFAULT, 'test1');
-- insert into players (id, name) VALUES (DEFAULT, 'test2');
-- insert into players (id, name) VALUES (DEFAULT, 'test3');
-- insert into players (id, name) VALUES (DEFAULT, 'test4');

-- insert into matches VALUES (1, 2, false);
-- insert into matches VALUES (4, 3, false);
-- insert into matches VALUES (1, 3, false);
-- insert into matches VALUES (2, 3, false);
-- insert into matches VALUES (1, 4, false);
-- insert into matches VALUES (2, 4, false);
