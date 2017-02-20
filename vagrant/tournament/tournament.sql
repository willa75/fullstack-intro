-- Table definitions for the tournament project.
--
-- Created two tables to hold the players and games.
DROP DATABASE IF EXISTS tournament;
CREATE DATABASE tournament;
\c tournament;

CREATE TABLE players (name TEXT NOT NULL,
					id SERIAL PRIMARY KEY);

CREATE TABLE games(id SERIAL PRIMARY KEY,
					winner INT REFERENCES players(id),
					loser INT REFERENCES players(id));

--Create a view to get the total number of games a player has been in.
CREATE VIEW gameNmb AS 
SELECT players.id, count(games.*) AS num
FROM players
LEFT JOIN games
ON games.winner = players.id OR games.loser = players.id
group by players.id;
