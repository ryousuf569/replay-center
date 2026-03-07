from nba_api.stats.endpoints import playergamelogs
import pandas as pd
from dotenv import load_dotenv
import os
from supabase import create_client

load_dotenv()

SB_URL = os.environ["SUPABASE_URL"]
SB_KEY = os.environ["SUPABASE_KEY"]
supabase = create_client(SB_URL, SB_KEY)

SEASON = "2025-26"

def get_latest_date():
    date = (supabase.table("player_game_logs").select("game_date").order("game_date", 
            desc=True).limit(1).execute())
    
    if not date.data:
        return None
    latest = date.data[0]["game_date"]
    return pd.to_datetime(latest).strftime("%m/%d/%Y")

def fetch_game_logs(start_date):

    parameters = {'season_nullable' : SEASON}
    if start_date is not None:
        parameters['date_from_nullable'] = start_date
    else:
        parameters['date_from_nullable'] = ''

    df = playergamelogs.PlayerGameLogs(**parameters).get_data_frames()[0]
    return df

def format_logs(df):
    
    if df.empty:
        return df
    
    # needa format for the supabase schema I created
    df = df.rename(columns={
        "PLAYER_ID": "player_id",
        "GAME_ID": "game_id",
        "GAME_DATE": "game_date",
        "MATCHUP": "matchup",
        "WL": "wl",
        "MIN": "min",
        "FGM": "fgm",
        "FGA": "fga",
        "FG_PCT": "fg_pct",
        "FG3M": "fg3m",
        "FG3A": "fg3a",
        "FG3_PCT": "fg3_pct",
        "FTM": "ftm",
        "FTA": "fta",
        "FT_PCT": "ft_pct",
        "OREB": "oreb",
        "DREB": "dreb",
        "REB": "reb",
        "AST": "ast",
        "STL": "stl",
        "BLK": "blk",
        "TOV": "tov",
        "PF": "pf",
        "PTS": "pts",
        "PLUS_MINUS": "plus_minus",
    })

    keep_cols = [
        "player_id", "game_id", "game_date", "matchup", "wl", "min",
        "fgm", "fga", "fg_pct", "fg3m", "fg3a", "fg3_pct",
        "ftm", "fta", "ft_pct", "oreb", "dreb", "reb", "ast",
        "stl", "blk", "tov", "pf", "pts", "plus_minus"
    ]

    df = df[keep_cols].copy()
    df["season"] = SEASON
    df["updated_at"] = pd.Timestamp.utcnow().isoformat()
    df["game_date"] = pd.to_datetime(df["game_date"], errors="coerce").dt.strftime("%Y-%m-%d")
    df = df.where(pd.notnull(df), None)

    return df

# splitting the df to send to supabase to avoid timeouts (learned the hard way)
def split(sequence, size):
    for i in range(0, len(sequence), size):
        yield sequence[i:i + size]

def upsert_logs(df):
    if df.empty:
        print("No new logs found.")
        return

    records = df.to_dict(orient="records")

    for batch in split(records, 500):
        (
            supabase
            .table("player_game_logs")
            .upsert(batch, on_conflict="player_id,game_id")
            .execute()
        )

    print(f"Upserted {len(records)} rows.")


def main():
    start_date = get_latest_date()
    print("Latest Supabase date:", start_date)

    raw_df = fetch_game_logs(start_date)
    print("Fetched rows:", len(raw_df))

    clean_df = format_logs(raw_df)
    bad_ids = [196295533, 196295531, 196295539, 196295532, 196295528, 196295530, 196295529, 196295526, 
               196295527, 196295491, 196295497, 196295501, 196295493, 196295492, 196295482, 196295502, 
               196295483, 196295496, 196295499, 196295484, 196295487, 196295500, 196295485, 196295498, 
               196295488, 196295489, 196295495, 196295504, 196295494, 196295307, 196295486, 196295490, 
               196295481]
    clean_df["player_id"] = pd.to_numeric(clean_df["player_id"], errors="coerce")
    clean_df = clean_df[~clean_df["player_id"].isin(bad_ids)]
    upsert_logs(clean_df)


if __name__ == "__main__":
    main()


