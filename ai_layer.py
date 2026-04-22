import os
import json
from typing import Dict, List

from openai import OpenAI


def build_profile_summary(user_prefs: Dict) -> str:
    system = user_prefs.get("system", "Unknown") or "Unknown"
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
        updated["ai_source"] = "local_fallback"
        enhanced.append(updated)

    return enhanced


def build_catalog_payload(recommendations: List[Dict]) -> List[Dict]:
    payload = []
    for rec in recommendations:
        payload.append(
            {
                "title": rec["title"],
                "score": rec["score"],
                "genres": rec["genres"],
                "platforms": rec["platforms"],
                "reason": rec["reason"],
                "matched_features": rec.get("matched_features", []),
            }
        )
    return payload


def openai_ai_explanations(user_prefs: Dict, recommendations: List[Dict]) -> List[Dict]:
    api_key = os.getenv("OPENAI_API_KEY")
    client = OpenAI(api_key=api_key) if api_key else OpenAI()

    profile_summary = build_profile_summary(user_prefs)
    catalog_payload = build_catalog_payload(recommendations)

    prompt = f"""
You are helping a game recommendation app explain its ranked results.

User profile:
{profile_summary}

Candidate recommendations (JSON):
{json.dumps(catalog_payload, indent=2)}

Return ONLY valid JSON in this exact format:
[
  {{
    "title": "string",
    "ai_reason": "2-3 sentence personalized explanation grounded in the candidate data only"
  }}
]

Rules:
- Use only the provided candidate titles.
- Do not invent games.
- Do not change the ranking.
- Keep explanations specific to the user's stated preferences.
- Ground explanations in genres, platforms, matched_features, and the base reason.
"""

    response = client.responses.create(
        model="gpt-5.4",
        input=prompt,
    )

    # Extract text robustly from different SDK response shapes
    text = ""
    try:
        if hasattr(response, "output_text") and response.output_text:
            text = response.output_text
        else:
            output = getattr(response, "output", None)
            if output:
                parts = []
                for item in output:
                    content = item.get("content", []) if isinstance(item, dict) else []
                    for c in content:
                        if isinstance(c, dict) and "text" in c:
                            parts.append(c["text"])
                        elif isinstance(c, str):
                            parts.append(c)
                text = "\n".join(parts)
    except Exception:
        text = ""

    text = (text or "").strip()

    # Try parsing JSON; if it fails, fall back to local explanations
    try:
        parsed = json.loads(text)
        if not isinstance(parsed, list):
            raise ValueError("parsed response is not a list")
    except Exception:
        return local_ai_explanations(user_prefs, recommendations)

    reason_map = {
        item["title"]: item["ai_reason"]
        for item in parsed
        if isinstance(item, dict) and "title" in item and "ai_reason" in item
    }

    enhanced = []
    for idx, rec in enumerate(recommendations, start=1):
        updated = dict(rec)
        updated["rank"] = idx
        updated["ai_reason"] = reason_map.get(
            rec.get("title"),
            f"{rec.get('title', 'This title')} is a strong fit based on your selected preferences and matched features."
        )
        updated["ai_source"] = "openai_api"
        enhanced.append(updated)

    return enhanced


def generate_ai_recommendation_layer(user_prefs: Dict, recommendations: List[Dict]) -> List[Dict]:
    """
    Hybrid mode:
    - If OPENAI_API_KEY is available, try the OpenAI API.
    - If anything fails, fall back to the local structured explanation layer.
    """
    api_key = os.getenv("OPENAI_API_KEY")

    if not api_key:
        return local_ai_explanations(user_prefs, recommendations)

    try:
        return openai_ai_explanations(user_prefs, recommendations)
    except Exception:
        return local_ai_explanations(user_prefs, recommendations)