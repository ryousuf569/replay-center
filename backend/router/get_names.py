from fastapi import APIRouter
from database import player_names

router = APIRouter(prefix='/player_names', tags=["Player Names"])
@router.get("/all")
def list_all_players():
    return {"players": player_names.get_names()}
