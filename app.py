import streamlit as st

from games import GAMES
from recommender import recommend_games
from ai_layer import generate_ai_recommendation_layer
from guardrails import validate_user_input, validate_recommendations, enforce_fallback


st.set_page_config(page_title="AI Game Selector", layout="wide")

st.title("🎮 AI Game Selector")
st.caption("A Twitch-inspired, Spotify-style game recommender with AI-enhanced explanations and guardrails.")

st.markdown("### Enter your gaming preferences")

systems = ["", "PC", "PlayStation 5", "Xbox Series X", "Nintendo Switch"]
genres = ["RPG", "Action", "Adventure", "Horror", "FPS", "Indie", "Sandbox", "Survival", "Simulation", "Strategy", "Puzzle", "Cozy"]

col1, col2 = st.columns(2)

with col1:
    selected_system = st.selectbox("System", systems)
    selected_genres = st.multiselect("Favorite Genres", genres)

with col2:
    favorite_game = st.text_input("Favorite Game", placeholder="Example: Minecraft")
    history = st.text_area(
        "Gameplay History / Style",
        placeholder="Example: I like building, crafting, survival, exploration, and cozy games."
    )

show_steps = st.checkbox("Show intermediate reasoning steps", value=True)

if st.button("Generate Recommendations"):
    user_prefs = {
        "system": selected_system,
        "genres": selected_genres,
        "favorite_game": favorite_game,
        "history": history,
    }

    valid_input, input_errors = validate_user_input(user_prefs)

    if not valid_input:
        for err in input_errors:
            st.error(err)
    else:
        base_recommendations = recommend_games(user_prefs, GAMES, top_k=6)

        ai_recommendations = generate_ai_recommendation_layer(user_prefs, base_recommendations)
        valid_output, output_errors = validate_recommendations(ai_recommendations, GAMES)

        final_recommendations = enforce_fallback(ai_recommendations, base_recommendations, min_items=3)

        if show_steps:
            st.markdown("## Intermediate Steps")
            st.write("**Step 1: User profile**")
            st.json(user_prefs)

            st.write("**Step 2: Base candidate retrieval and ranking**")
            st.dataframe([
                {
                    "title": rec["title"],
                    "score": rec["score"],
                    "matched_features": ", ".join(rec["matched_features"][:4]),
                }
                for rec in base_recommendations
            ])

            st.write("**Step 3: AI enhancement layer**")
            st.dataframe([
                {
                    "rank": rec.get("rank"),
                    "title": rec["title"],
                    "score": rec["score"],
                    "ai_reason_preview": rec["ai_reason"][:120] + "..."
                }
                for rec in final_recommendations
            ])

            st.write("**Step 4: Guardrail status**")
            if valid_output:
                st.success("Output validation passed.")
            else:
                for err in output_errors:
                    st.warning(err)

        st.markdown("## Final Recommendations")

        if not final_recommendations:
            st.info("No strong matches found. Try a broader description.")
        else:
            for rec in final_recommendations:
                with st.container(border=True):
                    st.subheader(f"{rec.get('rank', '-')}. {rec['title']}")
                    st.write(f"**Score:** {rec['score']}")
                    st.write(f"**AI source:** {rec.get('ai_source', 'unknown')}")
                    st.write(f"**Genres:** {', '.join(rec['genres'])}")
                    st.write(f"**Platforms:** {', '.join(rec['platforms'])}")
                    st.write(f"**Base reason:** {rec['reason']}")
                    st.write(f"**AI explanation:** {rec.get('ai_reason', 'No AI explanation available.')}")
                    if rec.get("matched_features"):
                        st.write(f"**Matched features:** {', '.join(rec['matched_features'][:5])}")