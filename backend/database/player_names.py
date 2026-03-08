from dotenv import load_dotenv
import os
from supabase import create_client

load_dotenv()

SB_URL = os.environ["SUPABASE_URL"]
SB_KEY = os.environ["SUPABASE_KEY"]
supabase = create_client(SB_URL, SB_KEY)

def get_names():
    names = (supabase.table("players").select("player_name").execute())
    names = names.data
    names = [name for n in names for name in n.values()]
    del names[:3]
    return names