from games import GAMES
from recommender import recommend_games
from ai_layer import generate_ai_recommendation_layer
from guardrails import validate_user_input, validate_recommendations, enforce_fallback


TEST_PROFILES = [
    {
        "name": "Sandbox Builder",
        "prefs": {
            "system": "PC",
            "genres": ["Sandbox", "Survival"],
            "favorite_game": "Minecraft",
            "history": "building crafting exploration cozy",
        },
    },
    {
        "name": "Horror Story Fan",
        "prefs": {
            "system": "PlayStation 5",
            "genres": ["Horror", "Action"],
            "favorite_game": "Resident Evil",
            "history": "cinematic survival tense story",
        },
    },
    {
        "name": "Cozy Switch Player",
        "prefs": {
            "system": "Nintendo Switch",
            "genres": ["Cozy", "Simulation"],
            "favorite_game": "Animal Crossing",
            "history": "relaxing casual cozy customization",
        },
    },
]


def run_evaluation():
    passed = 0
    total = len(TEST_PROFILES)

    print("=== AI Game Selector Evaluation ===\n")

    for profile in TEST_PROFILES:
        name = profile["name"]
        prefs = profile["prefs"]

        print(f"--- Testing: {name} ---")

        valid_input, input_errors = validate_user_input(prefs)
        if not valid_input:
            print("FAIL: Invalid input")
            for err in input_errors:
                print(" -", err)
            print()
            continue

        base = recommend_games(prefs, GAMES, top_k=6)
        ai = generate_ai_recommendation_layer(prefs, base)
        final = enforce_fallback(ai, base, min_items=3)

        valid_output, output_errors = validate_recommendations(final, GAMES)
        if not valid_output:
            print("FAIL: Output validation failed")
            for err in output_errors:
                print(" -", err)
            print()
            continue

        if len(final) < 3:
            print("FAIL: Fewer than 3 recommendations produced.\n")
            continue

        print("PASS")
        for rec in final[:3]:
            print(f" - {rec['title']} (score={rec['score']})")
        print()
        passed += 1

    print("=== Summary ===")
    print(f"Passed: {passed}/{total}")
    print(f"Score: {passed / total:.0%}")


if __name__ == "__main__":
    run_evaluation()