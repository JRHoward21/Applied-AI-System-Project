from typing import Dict, List, Tuple


ALLOWED_SYSTEMS = {
    "PC",
    "PlayStation 5",
    "Xbox Series X",
    "Nintendo Switch",
}

ALLOWED_GENRES = {
    "RPG",
    "Action",
    "Adventure",
    "Horror",
    "FPS",
    "Indie",
    "Sandbox",
    "Survival",
    "Simulation",
    "Strategy",
    "Puzzle",
    "Cozy",
}


def validate_user_input(user_prefs: Dict) -> Tuple[bool, List[str]]:
    errors = []

    system = user_prefs.get("system", "")
    genres = user_prefs.get("genres", [])
    favorite_game = user_prefs.get("favorite_game", "").strip()
    history = user_prefs.get("history", "").strip()

    if system and system not in ALLOWED_SYSTEMS:
        errors.append(f"Unsupported system: {system}")

    invalid_genres = [g for g in genres if g not in ALLOWED_GENRES]
    if invalid_genres:
        errors.append(f"Unsupported genres: {', '.join(invalid_genres)}")

    if not system and not genres and not favorite_game and not history:
        errors.append("Please provide at least one preference before generating recommendations.")

    return len(errors) == 0, errors


def validate_recommendations(recommendations: List[Dict], catalog: List[Dict]) -> Tuple[bool, List[str]]:
    errors = []
    catalog_titles = {game["title"] for game in catalog}

    if not recommendations:
        errors.append("No recommendations were produced.")
        return False, errors

    for rec in recommendations:
        if rec["title"] not in catalog_titles:
            errors.append(f"Recommendation '{rec['title']}' is not in the game catalog.")
        if rec.get("score", 0) <= 0:
            errors.append(f"Recommendation '{rec['title']}' has a non-positive score.")
        if not rec.get("reason"):
            errors.append(f"Recommendation '{rec['title']}' is missing an explanation.")

    return len(errors) == 0, errors


def enforce_fallback(recommendations: List[Dict], fallback: List[Dict], min_items: int = 3) -> List[Dict]:
    if len(recommendations) >= min_items:
        return recommendations
    return fallback[:max(min_items, len(fallback))]