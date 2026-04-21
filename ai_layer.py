import os
from typing import Dict, List


def build_profile_summary(user_prefs: Dict) -> str:
    system = user_prefs.get("system", "Unknown")
    genres = ", ".join(user_prefs.get("genres", [])) or "None provided"
    favorite_game = user_prefs.get("favorite_game", "") or "None provided"
    history = user_prefs.get("history", "") or "None provided"

    return (
        f"System: {system}\n"
        f"Genres: {genres}\n"
        f"Favorite Game: {favorite_game}\n"
        f"Playstyle History: {history}"
    )


def local_ai_explanations(user_prefs: Dict, recommendations: List[Dict]) -> List[Dict]:
    profile_summary = build_profile_summary(user_prefs)
    enhanced = []

    for idx, rec in enumerate(recommendations, start=1):
        matched = ", ".join(rec.get("matched_features", [])[:4]) or "general preference alignment"
        enhanced_reason = (
            f"AI summary: Based on your profile ({profile_summary}), "
            f"'{rec['title']}' stands out because it {matched}. "
            f"It also fits the broader style suggested by your preferences."
        )

        updated = dict(rec)
        updated["ai_reason"] = enhanced_reason
        updated["rank"] = idx
        enhanced.append(updated)

    return enhanced


def generate_ai_recommendation_layer(user_prefs: Dict, recommendations: List[Dict]) -> List[Dict]:
    """
    This project uses a local structured-prompt style AI layer.
    If you later add an API key, you can extend this function.
    """
    _api_key = os.getenv("OPENAI_API_KEY")
    return local_ai_explanations(user_prefs, recommendations)