from typing import List, Dict


def tokenize(text: str) -> List[str]:
    if not text:
        return []
    return [word.strip().lower() for word in text.replace(",", " ").replace(".", " ").split() if word.strip()]


def score_game(user_prefs: Dict, game: Dict) -> Dict:
    score = 0
    matched_features = []

    system = user_prefs.get("system", "").strip()
    genres = [g.lower() for g in user_prefs.get("genres", [])]
    favorite_game = user_prefs.get("favorite_game", "").lower().strip()
    history_words = tokenize(user_prefs.get("history", ""))

    if system and system in game["platforms"]:
        score += 3
        matched_features.append(f"supports {system}")

    game_genres_lower = [g.lower() for g in game["genres"]]
    for genre in genres:
        if genre in game_genres_lower:
            score += 3
            matched_features.append(f"matches genre '{genre}'")

    if favorite_game:
        if favorite_game in game["title"].lower():
            score += 8
            matched_features.append("matches favorite game directly")

        for related in game["similar_to"]:
            related_lower = related.lower()
            if favorite_game in related_lower or related_lower in favorite_game:
                score += 5
                matched_features.append(f"similar to {related}")

        for tag in game["tags"]:
            if tag.lower() in favorite_game:
                score += 2
                matched_features.append(f"favorite game implies tag '{tag}'")

        for style in game["gameplay_type"]:
            if style.lower() in favorite_game:
                score += 2
                matched_features.append(f"favorite game implies playstyle '{style}'")

    for word in history_words:
        if any(word in tag.lower() for tag in game["tags"]):
            score += 1
            matched_features.append(f"history mentions '{word}'")

        if any(word in style.lower() for style in game["gameplay_type"]):
            score += 1
            matched_features.append(f"playstyle matches '{word}'")

        if any(word in genre.lower() for genre in game["genres"]):
            score += 1
            matched_features.append(f"genre aligns with '{word}'")

    explanation = game["reason"]
    return {
        "title": game["title"],
        "genres": game["genres"],
        "platforms": game["platforms"],
        "tags": game["tags"],
        "reason": explanation,
        "score": score,
        "matched_features": list(dict.fromkeys(matched_features))
    }


def recommend_games(user_prefs: Dict, games: List[Dict], top_k: int = 5) -> List[Dict]:
    scored = [score_game(user_prefs, game) for game in games]
    filtered = [game for game in scored if game["score"] > 0]
    filtered.sort(key=lambda x: x["score"], reverse=True)
    return filtered[:top_k]