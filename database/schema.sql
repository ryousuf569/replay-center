CREATE TABLE IF NOT EXISTS players (
  player_id BIGINT primary key,
  player_name TEXT NOT null
);

CREATE TABLE IF NOT EXISTS player_game_logs (
  player_id bigint not null references players(player_id) on delete cascade,
  game_id text not null,
  game_date date,
  matchup text,
  wl text,
  min text,
  fgm integer,
  fga integer,
  fg_pct numeric,
  fg3m integer,
  fg3a integer,
  fg3_pct numeric,
  ftm integer,
  fta integer,
  ft_pct numeric,
  oreb integer,
  dreb integer,
  reb integer,
  ast integer,
  stl integer,
  blk integer,
  tov integer,
  pf integer,
  pts integer,
  plus_minus integer,
  season text not null,
  updated_at timestamptz default now(),
  PRIMARY key (player_id, game_id)
);