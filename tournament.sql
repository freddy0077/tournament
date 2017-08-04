-- Table definitions for the tournament project.
--
-- Put your SQL 'create table' statements in this file; also 'create view'
-- statements if you choose to use it.
--
-- You can write comments in this file by starting them with two dashes, like
-- these lines here.

-- noinspection SqlDialectInspection
DROP DATABASE IF EXISTS tournament;

CREATE DATABASE tournament;

\c tournament

CREATE TABLE players (
                       id SERIAL PRIMARY KEY,
                       name TEXT
                       );

CREATE TABLE matches (
                       id SERIAL PRIMARY KEY,
                       winner_id INTEGER REFERENCES players (id),
                       loser_id INTEGER REFERENCES players (id),
                       draw BOOLEAN
                       );

CREATE TABLE scores (
                          id SERIAL,
                          player_id INTEGER,
                          score INTEGER,
                          matches INTEGER
                          );

CREATE VIEW player_standings as
  SELECT players.id, players.name,
    COUNT(CASE WHEN players.id = matches.winner_id THEN 1 END) AS Wins,
    COUNT(matches.winner_id + matches.loser_id) AS matches
  FROM players LEFT JOIN matches
    ON players.id = matches.winner_id or players.id = matches.loser_id
  GROUP BY players.id ORDER BY Wins DESC;