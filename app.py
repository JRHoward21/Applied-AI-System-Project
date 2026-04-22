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
    def reset_inputs():
        st.session_state.selected_system = ""
        st.session_state.selected_genres = []
        st.session_state.favorite_game = ""
        st.session_state.history = ""
    st.button("Reset Inputs", on_click=reset_inputs)
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
    st.selectbox("System", systems, key="selected_system")
    st.multiselect("Favorite Genres", genres, key="selected_genres")
with col2:
    st.text_input("Favorite Game", placeholder="Example: Minecraft", key="favorite_game")
    st.text_area(
        "Gameplay History / Style",
        placeholder="Example: I like building, crafting, survival, exploration, and cozy games.",
        key="history",
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
            st.image(thumb, width=140, use_container_width=False)
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

            # Actions use callbacks to update session_state before rerun so the
            # sidebar reflects changes immediately.
            def _add_to_queue(t):
                if t not in st.session_state.queue:
                    st.session_state.queue.append(t)

            def _save(t):
                st.session_state.last_saved = t

            def _share(t):
                st.session_state.last_shared = t

            btns = st.columns([1,1,1,1])
            btns[0].button("▶ Preview", key=f"preview_{idx}", on_click=lambda t=title: st.session_state.update({"last_preview": t}))
            btns[1].button("💾 Save", key=f"save_{idx}", on_click=_save, args=(title,))
            btns[2].button("Share", key=f"share_{idx}", on_click=_share, args=(title,))
            btns[3].button("+ Queue", key=f"queue_{idx}", on_click=_add_to_queue, args=(title,))

            fb_cols = st.columns([1,1])
            def _up(t):
                st.session_state.feedback[t] = st.session_state.feedback.get(t, 0) + 1

            def _down(t):
                st.session_state.feedback[t] = st.session_state.feedback.get(t, 0) - 1

            fb_cols[0].button("👍", key=f"up_{idx}", on_click=_up, args=(title,))
            fb_cols[1].button("👎", key=f"down_{idx}", on_click=_down, args=(title,))

# --- Generate & Render Recommendations ---
if st.button("Generate Recommendations"):
    user_prefs = {
        "system": st.session_state.get("selected_system", ""),
        "genres": st.session_state.get("selected_genres", []),
        "favorite_game": st.session_state.get("favorite_game", ""),
        "history": st.session_state.get("history", ""),
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
        # Persist the final recommendations in session state so interactive buttons
        # (preview/save/share/queue/feedback) work across reruns without needing
        # to press Generate again.
        st.session_state.recommendations = final_recommendations

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

# Render persisted recommendations (so card buttons work across reruns)
final_recommendations = st.session_state.get("recommendations", [])
if final_recommendations:
    st.markdown("## Final Recommendations")
    # Featured picks
    st.markdown("### Featured Picks")
    featured = final_recommendations[:3]
    cols = st.columns(len(featured))
    for c, rec in zip(cols, featured):
        with c:
            thumb = rec.get("thumb", "assets/default_thumb.png")
            st.image(thumb, width=160, use_container_width=False)
            st.markdown(f"**{rec.get('title','Unknown')}**")
            st.markdown(f"*Score: {rec.get('score')}*")
            st.markdown(" ".join([f"<span class='genre-chip'>{g}</span>" for g in rec.get('genres', [])]), unsafe_allow_html=True)

    st.markdown("### More suggestions")
    for i, rec in enumerate(final_recommendations, start=1):
        render_card(rec, i)