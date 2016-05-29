-- Table definitions for the tournament project.
--
-- Created two tables to hold the players and matches.
DROP DATABASE IF EXISTS tournament;
CREATE DATABASE tournament;
\c tournament;

CREATE TABLE players (name TEXT NOT NULL,
					id SERIAL PRIMARY KEY);

CREATE TABLE matches(id SERIAL PRIMARY KEY,
					winner INT REFERENCES players(id),
					loser INT REFERENCES players(id));

--Create a view to get the number of matches a player has been in.
CREATE VIEW gameNmb AS 
SELECT players.id, count(matches.*) AS num
FROM players
LEFT JOIN matches
ON matches.winner = players.id OR matches.loser = players.id
group by players.id;
