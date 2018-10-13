DROP TABLE IF EXISTS players;
DROP TABLE IF EXISTS fines;
DROP TABLE IF EXISTS players_fines;
DROP TABLE IF EXISTS teams;

CREATE TABLE players (
  uuid TEXT UNIQUE PRIMARY KEY, 
  first_name TEXT NOT NULL,
  last_name TEXT NOT NULL,
  banker INTEGER NOT NULL,
  email TEXT UNIQUE NOT NULL,
  team_uuid TEXT,
  password TEXT NOT NULL
);

CREATE TABLE fines (
  uuid TEXT PRIMARY KEY, 
  label TEXT UNIQUE NOT NULL,
  cost INTEGER NOT NULL
);

CREATE TABLE players_fines (
  uuid TEXT UNIQUE PRIMARY KEY, 
  player_uuid TEXT,
  fine_uuid TEXT
);

CREATE TABLE teams (
  uuid TEXT UNIQUE PRIMARY KEY,
  label TEXT NOT NULL
);
