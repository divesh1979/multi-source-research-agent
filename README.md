# Multi-Source AI Research Agent

A parallel AI research agent built using **LangGraph**, **LangChain**, **GPT-4o**, and **Pydantic**. It queries Google Search, Reddit discussions, and scrapes deep web pages concurrently via BrightData API, then synthesizes the data into structured reports with verified source citations.

---

## Key Features

- **LangGraph Parallel Workflow**: Uses a state graph to fan-out queries across multiple sources concurrently (`google_node`, `reddit_node`, `scraping_node`) before merging them in an aggregation node.
- **Pydantic Structured Output**: Enforces strict typing (`ResearchReport`, `SourceCitation`, `KeyFinding`, `SentimentOverview`) via GPT-4o `with_structured_output` to prevent malformed responses.
- **BrightData Scraping & Local Snapshots**: Real-time web scraping with HTML-to-Markdown conversion and local timestamped caching under `snapshots/`.
- **Dual Interfaces**: 
  - **CLI (`main.py`)**: Terminal UI with progress spinners, formatted markdown, and summary tables.
  - **Streamlit Web App (`app.py`)**: Interactive web dashboard to run queries, view live progress, inspect snapshots, and export JSON/Markdown.
- **Offline / Fallback Support**: Runs with fallback search and scraping engines if API keys are not provided.

---

## Architecture Overview

```
                          ┌──► Google Search Node ──────┐
                          │                             │
[User Query] ──► [Planner] ├──► Reddit Node ─────────────┼──► [Aggregator] ──► [GPT-4o Synthesis] ──► [Structured Report]
                          │                             │
                          └──► BrightData Scraper Node ─┘
```

---

## Setup & Installation

### 1. Clone the repository
```bash
git clone https://github.com/divesh1979/multi-source-research-agent.git
cd multi-source-research-agent
```

### 2. Create virtual environment & install requirements
```bash
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

### 3. Configure environment variables
Copy `.env.example` to `.env` and set your API keys:
```bash
cp .env.example .env
```
*(If left empty, the project automatically uses built-in mock/fallback engines for testing).*

---

## How to Run

### Command Line Interface (CLI)
```bash
python main.py --query "DeepSeek-R1 vs GPT-4o architecture comparison for agentic coding"
```

### Streamlit Web Dashboard
```bash
streamlit run app.py
```

---

## Testing
Run unit and integration tests with Pytest:
```bash
pytest tests/ -v
```

---

## Project Structure

```
multi-source-research-agent/
├── agent/
│   ├── graph.py             # LangGraph StateGraph pipeline configuration
│   └── nodes.py             # Parallel search and LLM synthesis nodes
├── schemas/
│   ├── research_state.py    # AgentState TypedDict for state propagation
│   └── output_models.py     # Pydantic v2 schemas for report output
├── tools/
│   ├── google_search.py     # Google Search tool (SerpAPI / Tavily / DDG)
│   ├── reddit_search.py     # Reddit discussion scraper (PRAW / JSON API)
│   └── brightdata_scraper.py # BrightData REST scraper + SnapshotManager
├── prompts/
│   └── templates.py         # LangChain ChatPromptTemplate definitions
├── config.py                # Environment settings & config
├── main.py                  # CLI application entrypoint
├── app.py                   # Streamlit dashboard entrypoint
├── tests/
│   └── test_agent.py        # Pytest test suite
├── requirements.txt         # Dependencies
└── README.md                # Project documentation
```
