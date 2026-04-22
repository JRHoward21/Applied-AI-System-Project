import os
from recommender import tokenize, score_game, recommend_games


def test_tokenize_empty():
    assert tokenize("") == []


def test_tokenize_basic():
    assert "minecraft" in tokenize("I like Minecraft, crafting.")


def test_score_game_and_recommend():
    user = {"system": "PC", "genres": ["Sandbox"], "favorite_game": "Minecraft", "history": "building crafting"}
    from games import GAMES

    scored = [score_game(user, g) for g in GAMES]
    assert any(s["score"] >= 0 for s in scored)

    recs = recommend_games(user, GAMES, top_k=3)
    assert isinstance(recs, list)
    assert len(recs) <= 3
