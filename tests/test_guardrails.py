from guardrails import validate_user_input, validate_recommendations


def test_validate_user_input_empty():
    ok, errs = validate_user_input({})
    assert not ok
    assert errs


def test_validate_recommendations_basic():
    catalog = [{"title": "A", "genres": [], "platforms": [], "reason": "x"}]
    recs = [{"title": "A", "score": 5, "reason": "x"}]
    ok, errs = validate_recommendations(recs, catalog)
    assert ok

    # missing title
    bad = [{"title": "B", "score": 0, "reason": ""}]
    ok2, errs2 = validate_recommendations(bad, catalog)
    assert not ok2
