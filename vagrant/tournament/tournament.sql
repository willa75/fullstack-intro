-- Table definitions for the tournament project.
--
-- Put your SQL 'create table' statements in this file; also 'create view'
-- statements if you choose to use it.
--
-- You can write comments in this file by starting them with two dashes, like
-- these lines here.

CREATE TABLE players (name TEXT,
					id SERIAL);

CREATE TABLE matches(id SERIAL,
					winner INTEGER,
					player1 INTEGER,
					player2 INTEGER);

CREATE VIEW gameNmb AS 
SELECT players.id, count(matches.*) AS num
FROM players
LEFT JOIN matches
ON matches.player1 = players.id OR matches.player2 = players.id
group by players.id;
