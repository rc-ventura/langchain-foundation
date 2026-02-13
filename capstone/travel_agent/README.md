# Travel Coordinator (LangGraph + MCP)

Multi-agent travel planning system using LangGraph, MCP (Kiwi), Tavily, and SQLite. This README reflects the **current** repository state.

## 📦 Structure

```
capstone/travel_agent/
├── langgraph.json
├── travel_agents.py
└── resources/
    ├── destinations.db
    └── create_destinations_db.sql
```

## ✅ Prerequisites

- Python 3.12
- Dependencies installed (`uv sync` or repo-appropriate install step)
- `.env` at the repo root (e.g., `../../.env`)

### Expected environment variables

```
OPENAI_API_KEY=...
TAVILY_API_KEY=...
LANGCHAIN_API_KEY=...
LANGCHAIN_TRACING_V2=true
LANGCHAIN_PROJECT=travel-coordinator
```

## ▶️ Running the script (CLI)

The default execution uses `main()` inside `travel_agents.py`:

```bash
uv run capstone/travel_agent/travel_agents.py
```

Or via Python (inside the venv):

```bash
python capstone/travel_agent/travel_agents.py
```

## 🧠 LangGraph Dev (UI)

Run **inside** `capstone/travel_agent`:

```bash
langgraph dev
```

> `langgraph.json` points to `./travel_agents.py:get_coordinator`.

## 🔧 How it works

### MCP Tools (Kiwi)
- The travel agent loads MCP tools with:
  - `await client.get_tools()`
- This requires async agent creation (`build_travel_agent()`)

### Wrapped sub-agents
- `accommodation_agent` and `activity_agent` are agents used inside tools.
- To avoid loops, each call uses `recursion_limit`:

```python
response = accommodation_agent.invoke(..., config={"recursion_limit": 20})
```

### Database (destinations & attractions)
- Local DB at: `capstone/travel_agent/resources/destinations.db`
- Contains 15 popular destinations and 36 tourist attractions
- Loaded via:

```python
db_path = Path(__file__).parent / "resources" / "destinations.db"
```

## 🧩 Key functions

- `build_travel_agent()` → creates the travel agent with MCP tools
- `search_flights` → tool that calls the travel agent
- `search_accommodations` → tool that calls the accommodation agent
- `suggest_activities` → tool that calls the activity agent
- `build_coordinator()` → creates the coordinator (main graph)
- `get_coordinator()` → LangGraph Dev entrypoint

## ⚠️ Common errors

### 1. GraphRecursionError
Cause: sub-agent invoked inside a tool without a stop condition. Current mitigation:
- `recursion_limit` on invocations
- prompts like “Return the best option after you have found it.”

### 2. SQLite `unable to open database file`
Cause: relative path. Current fix:
- absolute path via `Path(__file__).parent / "resources" / "destinations.db"`

## 📝 Example input

```
I'm from São Paulo and I'd like to visit Tokyo for 2 travelers, interested in cultural activities
```

## 🔄 Recent updates

- **Refactored from Wedding Coordinator to Travel Coordinator**
- Replaced `Chinook.db` (music) with `destinations.db` (tourism)
- Renamed: `WeddingState` → `TravelState`
- Renamed agents: `venue_agent` → `accommodation_agent`, `playlist_agent` → `activity_agent`
- Updated all system prompts for general tourism context
- Activity agent now queries destinations database + web search
- MCP tools loaded via `build_travel_agent()` (async)
- `recursion_limit` applied to tools that call sub-agents

## 🗺️ Database Schema

### destinations table
- `city`, `country`, `region`, `timezone`
- `best_season`, `description`, `popular_activities`

### attractions table
- `name`, `city`, `country`, `category`
- `description`, `estimated_duration_hours`

---

**Architecture**: Multi-agent coordinator pattern with MCP (flights), Tavily (web search), and SQLite (structured data)
