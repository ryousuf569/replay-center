from nba_api.stats.endpoints import playergamelogs
import pandas as pd

SEASON = "2025-26"

# fetch league-wide player game logs
df = playergamelogs.PlayerGameLogs(
    season_nullable=SEASON
).get_data_frames()[0]

# find rows where player name is null
bad_rows = df[df["PLAYER_NAME"].isna()]

# get unique player IDs that have null names
bad_ids = bad_rows["PLAYER_ID"].drop_duplicates().to_list()

print(bad_ids)