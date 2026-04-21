# AI Game Selector Project

AI Game Selector is a compact, extendable project that combines a deterministic, rule-based recommender with an AI explanation and refinement layer to produce personalized, grounded game recommendations.

Key capabilities
- Rule-based candidate retrieval from a local game catalog
- AI explanation layer that produces human-friendly reasoning (local fallback or OpenAI)
- Input/output guardrails and fallback behavior for reliability
- Streamlit demo UI and an evaluation harness for batch testing

What's included in this README
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

Architecture (high level)
- `games.py`: local game catalog and helper utilities
- `recommender.py`: deterministic candidate selection and scoring
- `ai_layer.py`: prompt construction, provider client abstraction, and local fallback explainer
- `guardrails.py`: input validation, whitelist checks, and output verification
- `app.py`: Streamlit demo and user-facing integration
- `eval.py`: batch evaluation harness that runs the pipeline for example profiles

Project structure
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
├── assets/
│   └── visual_system_diagram.mmd
│
└── examples/
    ├── example_profiles.py
    └── sample_outputs.md
```

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

