# AI Game Selector Project

## Original Base Project
The original project was a recommendation system concept inspired by Twitch and Spotify. Its goal was to help users discover games based on their system, preferred genres, favorite titles, and gameplay history. The original version used rule-based scoring logic to rank games from a structured local catalog.

## Goal of the Extended Project
This extended version transforms the original recommender into an AI-enhanced game recommendation system. It adds:
- a Streamlit interface
- an AI explanation layer using structured prompting behavior
- guardrails for input/output reliability
- a test harness for repeated evaluation across multiple user profiles

## Current System Capabilities
The system:
- accepts platform, genre, favorite game, and playstyle/history inputs
- retrieves and ranks candidate games from a structured dataset
- generates AI-enhanced recommendation explanations
- validates both inputs and outputs with guardrails
- runs an evaluation script on predefined user profiles

## Substantial AI Feature
The substantial AI feature is an **AI explanation and refinement layer** integrated into the recommendation workflow. After the rule-based recommender selects candidate games, the AI layer interprets the user's profile and generates more personalized explanations grounded in matched features from the catalog.

This changes system behavior meaningfully because the output is no longer just a sorted list of games; it becomes a personalized recommendation response with profile-aware reasoning.

## Reliability / Guardrails
The system includes:
- input validation
- allowed platform/genre checking
- output validation against the local game catalog
- fallback behavior if too few valid recommendations are produced

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
│   └── visual_system_diagram.mmd
│
└── examples/
    └── example_profiles.py

Additional project details
--------------------------

A compact, extendable game recommendation system that combines a deterministic, rule-based recommender with an AI explanation layer to produce personalized, grounded recommendations.

Highlights
---------
- Rule-based candidate retrieval from a local game catalog
- AI explanation and refinement layer that produces human-friendly reasoning
- Input/output guardrails and fallback behavior for reliability
- Streamlit-based demo interface and an evaluation harness for batch testing

Getting started
---------------

1. Create a virtual environment and install dependencies:

```bash
python -m venv .venv
.\.venv\Scripts\activate
pip install -r requirements.txt
```

2. Run the Streamlit demo (recommended):

```bash
streamlit run app.py
```

3. Run the evaluation harness to test multiple example profiles:

```bash
python eval.py
```

Core components
---------------
- `app.py`: Streamlit demo / UI entrypoint
- `games.py`: Local game catalog and helpers
- `recommender.py`: Rule-based candidate selection and scoring
- `ai_layer.py`: AI prompt + explanation logic
- `guardrails.py`: Input/output validation and fallback rules
- `eval.py`: Batch evaluation using `examples/example_profiles.py`

Extending the project
---------------------
- Add new games by editing `games.py` (platforms, genres, tags, descriptions).
- Swap AI provider by updating the LLM client in `ai_layer.py`.
- Improve ranking by refining `recommender.py` scoring rules.

Examples and evaluation
-----------------------
- Run `python eval.py` to process `examples/example_profiles.py` and inspect `examples/sample_outputs.md` for example outputs.

License & Contribution
----------------------
No license is included by default. Add a `LICENSE` file (for example MIT) if you plan to share the project. Consider adding `CONTRIBUTING.md` and tests in a `tests/` folder for collaborators.

Contact
-------
Open an issue or reach out to the maintainer for questions, improvements, or contributions.
