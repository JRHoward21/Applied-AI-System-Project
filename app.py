import streamlit as st

from games import GAMES
from recommender import recommend_games
from ai_layer import generate_ai_recommendation_layer
from guardrails import validate_user_input, validate_recommendations, enforce_fallback
from history import append_user_history, get_user_history

st.set_page_config(page_title="AI Game Selector", layout="wide")

# --- THEME & STYLES ---
CSS_NEON = """
:root{--twitch:#9146FF;--spotify:#1DB954;--bg:#0b0b0d;--card:#0f1113}
html,body,#root{background:linear-gradient(120deg,var(--twitch),var(--spotify)) fixed!important}
section[data-testid="stSidebar"] {background: rgba(0,0,0,0.45);}
.app-card{background:linear-gradient(180deg, rgba(255,255,255,0.02), rgba(0,0,0,0.12));backdrop-filter: blur(6px);border-radius:12px;padding:12px;margin:8px 0;box-shadow:0 6px 18px rgba(0,0,0,0.35);color:#fff}
.genre-chip{display:inline-block;padding:4px 8px;border-radius:999px;background:rgba(255,255,255,0.04);color:#fff;margin-right:6px;font-size:12px}
.carousel{display:flex;gap:12px;overflow-x:auto;padding:8px 2px}
.carousel::-webkit-scrollbar{height:8px}
.carousel-item{flex:0 0 380px}
.reco-title{font-weight:700;color:#fff;font-size:18px}
.small-muted{color:rgba(255,255,255,0.78);font-size:13px}
.button-row button{margin-right:6px;padding:6px 10px;border-radius:8px;border:none;background:rgba(255,255,255,0.06);color:#fff}
"""

CSS_DARK = """
:root{--bg:#0b0b0d;--card:#0f1113}
html,body,#root{background:#0b0b0d!important;color:#e6e6e6}
section[data-testid="stSidebar"] {background: rgba(255,255,255,0.03);}
.app-card{background:linear-gradient(180deg, rgba(255,255,255,0.02), rgba(255,255,255,0.01));backdrop-filter: blur(2px);border-radius:8px;padding:12px;margin:8px 0;box-shadow:0 4px 14px rgba(0,0,0,0.5);color:#e6e6e6}
.genre-chip{display:inline-block;padding:4px 8px;border-radius:999px;background:rgba(255,255,255,0.03);color:#e6e6e6;margin-right:6px;font-size:12px}
.carousel{display:flex;gap:12px;overflow-x:auto;padding:8px 2px}
.carousel-item{flex:0 0 380px}
.reco-title{font-weight:700;color:#e6e6e6;font-size:18px}
.small-muted{color:rgba(230,230,230,0.78);font-size:13px}
.button-row button{margin-right:6px;padding:6px 10px;border-radius:8px;border:none;background:rgba(255,255,255,0.03);color:#e6e6e6}
"""

# --- SESSION STATE ---
if "queue" not in st.session_state:
    st.session_state.queue = []
if "feedback" not in st.session_state:
    st.session_state.feedback = {}

# --- SIDEBAR ---
with st.sidebar:
    st.header("Player")
    theme = st.selectbox("Theme", ["Neon (default)", "Dark"])
    st.button("Clear Queue", on_click=lambda: st.session_state.queue.clear())
    st.markdown("**Queue**")
    for i, q in enumerate(st.session_state.queue, 1):
        st.markdown(f"{i}. {q}")

# Apply selected theme CSS
try:
    selected_css = CSS_NEON if (theme or "").lower().startswith("neon") else CSS_DARK
except NameError:
    selected_css = CSS_NEON

st.markdown(f"<style>{selected_css}</style>", unsafe_allow_html=True)

# --- PAGE HEADER / INPUTS ---
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

# --- Helpers / Interactive card ---
def render_card(rec, idx):
    thumb = rec.get("thumb", "assets/default_thumb.png")
    title = rec.get("title", "Unknown")
    base_score = rec.get("score", 0)
    fb_adj = st.session_state.feedback.get(title, 0)
    display_score = base_score + (fb_adj * 0.1)

    with st.container():
        col_img, col_body = st.columns([1, 3])
        with col_img:
            st.image(thumb, width=140, use_column_width=False)
        with col_body:
            st.markdown(f"**{idx}. {title}**")
            st.markdown(f"**Score:** {display_score:.2f}  •  **AI source:** {rec.get('ai_source','unknown')}")
            if rec.get("ai_confidence") is not None:
                st.markdown(f"**AI confidence:** {rec.get('ai_confidence')}")
            st.markdown(f"**Genres:** {', '.join(rec.get('genres', []))}")
            st.markdown(f"**Platforms:** {', '.join(rec.get('platforms', []))}")
            st.write(f"**Base reason:** {rec.get('reason','')}")
            with st.expander("AI explanation"):
                st.write(rec.get("ai_reason", "No AI explanation available."))

            btns = st.columns([1,1,1,1])
            if btns[0].button("▶ Preview", key=f"preview_{idx}"):
                st.info("Preview not implemented in this demo.")
            if btns[1].button("💾 Save", key=f"save_{idx}"):
                st.success("Saved (demo).")
            if btns[2].button("Share", key=f"share_{idx}"):
                st.info("Share link copied (demo).")
            if btns[3].button("+ Queue", key=f"queue_{idx}"):
                st.session_state.queue.append(title)
                st.success(f"Added '{title}' to queue")

            fb_cols = st.columns([1,1])
            if fb_cols[0].button("👍", key=f"up_{idx}"):
                st.session_state.feedback[title] = st.session_state.feedback.get(title, 0) + 1
                st.success("Thanks — local score updated.")
            if fb_cols[1].button("👎", key=f"down_{idx}"):
                st.session_state.feedback[title] = st.session_state.feedback.get(title, 0) - 1
                st.success("Thanks — local score updated.")

# --- Generate & Render Recommendations ---
if st.button("Generate Recommendations"):
    user_prefs = {
        "system": selected_system,
        "genres": selected_genres,
        "favorite_game": favorite_game,
        "history": history,
    }
    # Record the raw user inputs into a persistent history store
    try:
        append_user_history(user_prefs)
    except Exception:
        st.warning("Could not write user history to disk.")

    valid_input, input_errors = validate_user_input(user_prefs)
    if not valid_input:
        for err in input_errors:
            st.error(err)
    else:
        base_recommendations = recommend_games(user_prefs, GAMES, top_k=12)
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
                    "ai_reason_preview": rec.get("ai_reason", "")[:120] + "..."
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
            # Featured carousel (top 3)
            st.markdown("### Featured Picks")
            featured = final_recommendations[:3]
            carousel_html = "<div class='carousel'>"
            for rec in featured:
                thumb = rec.get("thumb", "assets/default_thumb.png")
                genres_html = " ".join([f"<span class='genre-chip'>{g}</span>" for g in rec.get("genres", [])])
                carousel_html += f"""
                <div class="carousel-item app-card">
                  <img src="{thumb}" width=100 style="float:left;margin-right:10px;border-radius:6px"/>
                  <div style="padding-left:110px">
                    <div class="reco-title">{rec['title']}</div>
                    <div class="small-muted">Score: {rec['score']}</div>
                    <div style="margin-top:8px">{genres_html}</div>
                  </div>
                </div>
                """
            carousel_html += "</div>"
            st.markdown(carousel_html, unsafe_allow_html=True)

            # List / grid for all recommendations with interactive controls
            st.markdown("### More suggestions")
            for i, rec in enumerate(final_recommendations, start=1):
                render_card(rec, i)