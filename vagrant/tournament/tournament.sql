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