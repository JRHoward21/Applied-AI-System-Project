# AI Game Selector Project

## Orginal Base Project
The original project was a game recommendation system inspired by Twitch and Spotify. Its goal was to help users discover games based on their platform, preferred genres, favorite titles, and gameplay history. The first version relied on rule-based scoring over a structured local game catalog.

## AI Game Selector
Is a compact, extendable project that combines a deterministic, rule-based recommender with an AI explanation and refinement layer to produce personalized, grounded game recommendations.

## Goal of the Extended Project
This extended version turns the original recommender into an AI-enhanced game recommendation system. It adds:
- a Streamlit interface for interactive use
- an AI explanation layer with optional OpenAI API support
- guardrails for input and output reliability
- an evaluation harness for repeated testing across multiple user profiles

## How Real Recommendation Systems Work
Real-world recommendation systems such as Spotify, YouTube, and similar platforms use data about items and users to rank results. In this project, the input data includes game features such as genres, platforms, tags, and gameplay styles. User preferences include the selected platform, genres, favorite game, and a natural-language description of playstyle/history. The recommender compares those inputs against the catalog, scores candidate games, and ranks the strongest matches. The AI layer then improves the explanations so the results are easier to understand and feel more personalized.

## Current System capabilities
The system:
- accepts platform, genre, favorite game, and playstyle/history inputs
- retrieves and ranks candidate games from a structured dataset
- generates AI-enhanced recommendation explanations
- validates both inputs and outputs with guardrails
- falls back to a local explanation layer if an API key is unavailable or the API call fails
- runs an evaluation script on predefined user profiles

## Substantial AI Feature
The substantial AI feature is an **AI explanation and refinement layer** integrated directly into the recommendation workflow. After the rule-based recommender selects candidate games, the AI layer interprets the user’s profile and produces personalized explanations grounded in matched features from the catalog.

This changes system behavior meaningfully because the output is no longer just a sorted list of games. Instead, the system produces a profile-aware recommendation response with more detailed, personalized reasoning.

## Reliability / Guardrails
The system includes:
- input validation
- allowed platform and genre checking
- output validation against the local game catalog
- fallback behavior if too few valid recommendations are produced
- fallback AI explanation generation if the OpenAI API is unavailable

These guardrails improve reliability by preventing unsupported inputs, reducing invalid outputs, and ensuring the system still works even if the API path fails.


## What's included in this README
- Quickstart: install, configuration, and run examples
- System overview and architecture
- File map and extension points
- Development, testing, and contribution notes

Features
- Accepts platform, genres, favorite games, and brief playstyle/history inputs
- Retrieves and ranks candidate games from a structured dataset
- Generates AI-enhanced recommendation explanations grounded in catalog features
- Validates inputs and outputs; falls back when external APIs are unavailable

Getting started (Quickstart)

1. Create and activate a virtual environment, then install dependencies:

```bash
python -m venv .venv
.\.venv\Scripts\activate
pip install -r requirements.txt
```

2. Run the Streamlit demo (interactive):

```bash
streamlit run app.py
```

3. Run the evaluation harness to process example profiles:

```bash
python eval.py
```

Configuration
- OpenAI API (optional): if you want to use the OpenAI path for richer explanations, set the environment variable `OPENAI_API_KEY`.
- The system is designed to detect a missing API key and automatically use the local explanation fallback so the app still works offline.

Usage examples
- Streamlit UI: follow the web UI to input platform, genre, favorite titles, and playstyle; the app shows ranked recommendations and AI explanations.
- Programmatic: import `recommender` and `ai_layer` in a script to produce recommendations and explanations from a profile object.

## System Architecture
The architecture includes:
- **Streamlit UI (`app.py`)** for collecting user preferences and showing results
- **Game Catalog (`games.py`)** containing structured metadata about games
- **Rule-Based Recommender (`recommender.py`)** for retrieval, scoring, and ranking
- **AI Layer (`ai_layer.py`)** for explanation generation and optional OpenAI enhancement
- **Guardrails (`guardrails.py`)** for validating input and output
- **Evaluation Harness (`eval.py`)** for testing the system on multiple example profiles

The architecture diagram is included in:
- `Assets/visual_system_diagram.mmd`
- `Assets/visual_system_diagram.png`

## Project Structure
```text
Applied-AI-System-Project/
│── app.py
│── games.py
│── recommender.py
│── ai_layer.py
│── guardrails.py
│── eval.py
│── requirements.txt
│── README.md
│
├── Assets/
│   ├── visual_system_diagram.mmd
│   └── visual_system_diagram.png
│
├── examples/
│   ├── example_profiles.py
│   └── sample_outputs.md
│
└── tests/
    ├── test_ai_layer.py
    ├── test_guardrails.py
    ├── test_history.py
    └── test_recommender.py

Core components (brief)
- `app.py`: Streamlit demo / UI entrypoint
- `games.py`: Local game catalog and helpers
- `recommender.py`: Rule-based candidate selection and scoring
- `ai_layer.py`: AI prompt + explanation logic (switchable provider)
- `guardrails.py`: Validation & fallback rules
- `eval.py`: Batch evaluation using `examples/example_profiles.py`

Extending the project
- Add new games by editing `games.py` (platforms, genres, tags, descriptions).
- Swap AI provider by updating the LLM client abstraction in `ai_layer.py`.
- Improve ranking by refining scoring rules in `recommender.py`.

Development & testing
- There are no automated tests by default. To validate changes manually:

```bash
python eval.py
streamlit run app.py
```

- Consider adding `pytest` and a `tests/` folder for CI integration.

Notes on reliability and guardrails
- Input validation ensures only supported platforms/genres are accepted.
- Output validation cross-checks recommended games against the local catalog.
- If the OpenAI API is unreachable or the key is missing, the system uses a local explanation generator to preserve functionality.

Contributing
- Fork the repo, create a feature branch, and open a pull request with a short description of changes.
- Consider adding tests for new behavior and update `examples/sample_outputs.md` when outputs change significantly.

License
- No license file is included by default. Add a `LICENSE` (for example MIT) if you plan to publish the project publicly.

Contact
- Open an issue or reach out to the maintainer for questions, improvements, or contributions.

Acknowledgements
- Inspired by recommendation patterns in streaming and music platforms; the project is meant for education and experimentation.

