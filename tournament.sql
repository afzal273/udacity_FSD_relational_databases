-- Table definitions for the tournament project.
--
-- Put your SQL 'create table' statements in this file; also 'create view'
-- statements if you choose to use it.
--
-- You can write comments in this file by starting them with two dashes, like
-- these lines here.


-- CREATE database tournament;

CREATE TABLE players(
Player_id serial PRIMARY KEY,
Name text
);

CREATE TABLE matches(
Match_number serial,
Id1 INTEGER REFERENCES players(Player_id),
Id2 INTEGER REFERENCES players(Player_id),
winner INTEGER REFERENCES players(Player_id),
loser INTEGER REFERENCES players(Player_id)
);

CREATE TABLE standings (
Player_id INTEGER REFERENCES players(Player_id),
Matches INTEGER,
Wins INTEGER,
Losses INTEGER,
NetScore INTEGER
);

CREATE VIEW player_standings AS
(SELECT players.player_id, players.name, standings. wins, standings.matches
FROM players, standings
WHERE players.player_id = standings.player_id
ORDER BY standings.netscore DESC, standings.matches DESC);