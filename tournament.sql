-- Table definitions for the tournament project.
--
-- Put your SQL 'create table' statements in this file; also 'create view'
-- statements if you choose to use it.
--
-- You can write comments in this file by starting them with two dashes, like
-- these lines here.


DROP DATABASE IF EXISTS tournament;
CREATE DATABASE tournament;

\c tournament

CREATE TABLE players(
Player_id serial PRIMARY KEY,
Name TEXT NOT NULL
);

CREATE TABLE tournaments(
Tournament_id TEXT NOT NULL UNIQUE
);

CREATE TABLE player_tournaments(
Player_id INTEGER REFERENCES players(Player_id),
Tournament_id TEXT REFERENCES tournaments(Tournament_id),
UNIQUE (Player_id, Tournament_id)
);

CREATE TABLE matches(
Match_number serial,
Id1 INTEGER REFERENCES players(Player_id),
Id2 INTEGER REFERENCES players(Player_id),
winner INTEGER REFERENCES players(Player_id),
isTie BOOLEAN,
Tournament_id TEXT REFERENCES tournaments(Tournament_id)
);

CREATE TABLE standings (
Player_id INTEGER REFERENCES players(Player_id),
Matches INTEGER,
Wins INTEGER,
Ties INTEGER,
Losses INTEGER,
NetScore DECIMAL,
Tournament_id TEXT REFERENCES tournaments(Tournament_id),
UNIQUE (Player_id, Tournament_id)
);

CREATE VIEW player_standings AS
(SELECT players.player_id, players.name, standings. wins, standings.ties, standings.matches, standings.tournament_id
FROM players, standings
WHERE players.player_id = standings.player_id
ORDER BY standings.tournament_id, standings.netscore DESC, standings.matches ASC
);