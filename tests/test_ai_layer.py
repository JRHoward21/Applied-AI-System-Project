from ai_layer import local_ai_explanations, build_profile_summary


def test_build_profile_summary_defaults():
    s = build_profile_summary({})
    assert "System:" in s


def test_local_ai_explanations_shape():
    user = {"system": "PC", "genres": ["Sandbox"], "favorite_game": "Minecraft", "history": "building"}
    recs = [{"title": "Minecraft", "score": 10, "genres": [], "platforms": [], "reason": "x", "matched_features": ["a"]}]
    out = local_ai_explanations(user, recs)
    assert isinstance(out, list)
    assert out[0].get("ai_reason")
