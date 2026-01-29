# Wedding Coordinator (LangGraph + MCP)

Multi-agent wedding planning system using LangGraph, MCP (Kiwi), and Tavily. This README reflects the **current** repository state.

## 📦 Structure

```
capstone/travel_agent/
├── langgraph.json
├── travel_agents.py
└── resources/
    └── Chinook.db
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
LANGCHAIN_PROJECT=wedding-coordinator
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
- `venue_agent` and `playlist_agent` are agents used inside tools.
- To avoid loops, each call uses `recursion_limit`:

```python
response = venue_agent.invoke(..., config={"recursion_limit": 20})
```

### Database (playlist)
- Local DB at: `capstone/travel_agent/resources/Chinook.db`
- Loaded via:

```python
db_path = Path(__file__).parent / "resources" / "Chinook.db"
```

## 🧩 Key functions

- `build_travel_agent()` → creates the travel agent with MCP tools
- `search_flights` → tool that calls the travel agent
- `search_venues` → tool that calls the venue agent
- `suggest_playlist` → tool that calls the playlist agent
- `build_coordinator()` → creates the coordinator (main graph)
- `get_coordinator()` → LangGraph Dev entrypoint

## ⚠️ Common errors

### 1. GraphRecursionError
Cause: sub-agent invoked inside a tool without a stop condition. Current mitigation:
- `recursion_limit` on invocations
- prompts like “Return the best option after you have found it.”

### 2. SQLite `unable to open database file`
Cause: relative path. Current fix:
- absolute path via `Path(__file__).parent / "resources" / "Chinook.db"`

## 📝 Example input

```
I'm from London and I'd like a wedding in Paris for 100 guests, jazz-genre
```

## 🔄 Recent updates

- MCP tools loaded via `build_travel_agent()` (async)
- `recursion_limit` applied to tools that call sub-agents
- Sub-agent prompts adjusted to avoid loops
- DB path fixed to `resources/Chinook.db`

---

If you want, I can add:
- interactive test script
- sample SQL for playlists
- MCP-free fallback mode
