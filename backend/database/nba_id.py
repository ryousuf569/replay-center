from nba_api.stats.endpoints import playergamelogs
import pandas as pd
from dotenv import load_dotenv
import os
from supabase import create_client,Client

load_dotenv()

SB_URL = os.environ["SUPABASE_URL"]
SB_KEY = os.environ["SUPABASE_KEY"]
supabase = create_client(SB_URL, SB_KEY)

TABLE = "players"
SEASON = "2025-26"

players = playergamelogs.PlayerGameLogs(season_nullable=SEASON).get_data_frames()[0]
player_df = players[['PLAYER_ID', 'PLAYER_NAME']].drop_duplicates().rename(
    columns={
    "PLAYER_ID": "player_id",
    "PLAYER_NAME": "player_name"}).sort_values("player_name").reset_index(drop=True)

player_df = player_df[player_df["player_name"].notna() & 
                      (player_df["player_name"].astype(str).str.strip() != "")]

players_records = player_df.to_dict(orient="records")

supabase.table(TABLE).upsert(players_records, on_conflict="player_id").execute()
