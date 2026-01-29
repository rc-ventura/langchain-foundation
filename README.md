# LangChain Foundations & MAS Study

This repository is a dedicated study space for evolving from basic LangChain concepts to building advanced Multi-Agent Systems (MAS) using the comprehensive LangChain ecosystem.

## 🎯 Study Goals

- **Foundation**: Master core LangChain primitives (PromptTemplates, ChatModels, Tools).
- **Orchestration**: Deep dive into LangGraph for building complex, stateful agent workflows.
- **MAS Architectures**: Implement multi-agent patterns (Supervisor, Hierarchical, Multi-Agent Collaboration).
- **Production Grade**: Apply LangSmith for observability, debugging, and evaluation of agent performance.

## 🚀 Ecosystem Overview

- **LangChain**: The core framework for building LLM applications.
- **LangGraph**: For orchestrating stateful, multi-actor applications (Agents).
- **LangSmith**: For observability, testing, and fine-tuning.
- **LangGraph Studio**: A specialized IDE for prototyping and visualizing agentic interfaces.

## 🛠️ Setup & Installation

This project uses `uv` for fast dependency management.

1. **Install dependencies**:
   ```bash
   uv sync
   ```

2. **Environment Configuration**:
   Copy `.env.example` to `.env` and fill in your API keys:
   ```bash
   cp .env.example .env
   ```
   *Required Keys*: `OPENAI_API_KEY`, `TAVILY_API_KEY`
   *Observability*: `LANGSMITH_API_KEY` (Set `LANGSMITH_TRACING=true`)

## 🖥️ Prototyping Interfaces (LangGraph Studio)

To prototype the "Personal Chef" agent without building a custom UI:

1. **Start the Development Server**:
   ```bash
   uv run langgraph dev
   ```
   *(This uses `langgraph.json` to serve the API locally)*

2. **Open LangGraph Studio**:
   - Download and open the [LangGraph Studio Desktop App](https://github.com/langchain-ai/langgraph-studio).
   - Point it to this repository folder.
   - You will see your graph visualized and a chat panel to interact with the agent.

## 📂 Modules

### Module 1: Personal Chef Agent
Located in `module-01/`.
- **Goal**: Master foundational prompting, tools, and basic agent flows.
- **Artifacts**: Jupyter notebooks (e.g., prompting, tools, web search).

### Module 2: MCP & Runtime Context
Located in `module-02/`.
- **Goal**: Learn MCP servers, runtime context, and stateful agent patterns.
- **Artifacts**: MCP server example, travel agent notebook, state/context notebooks.

### Module 3: Advanced Agent UX & Dynamic Behavior
Located in `module-03/`.
- **Goal**: Build richer UX flows and dynamic agent behaviors.
- **Artifacts**: Agent chat UI, message management, HITL, dynamic prompts/models.

## 🧳 Capstone Overview

### Travel Agent (Wedding Coordinator)
Location: `capstone/travel_agent`
- **Goal**: Multi-agent wedding planning with MCP (Kiwi), Tavily, and a playlist DB.
- **Run (CLI)**:
  ```bash
  uv run capstone/travel_agent/travel_agents.py
  ```
- **LangGraph Dev (UI)** (run inside the folder):
  ```bash
  langgraph dev
  ```
- **Config**: `capstone/travel_agent/langgraph.json` → `./travel_agents.py:get_coordinator`

### Nutrition Agent (Personal Chef)
Location: `capstone/nutrition_agent`
- **Goal**: Personalized meal planning and substitutions.
- **Artifacts**: `personal_chef.py` + `langgraph.json`

## 🔍 Observability (LangSmith)
To trace your agent's thought process:
1. Ensure `LANGSMITH_TRACING=true` in `.env`.
2. Run your agent (via Studio or script).
3. Check your project in the [LangSmith Dashboard](https://smith.langchain.com/) to see step-by-step execution, latency, and token usage.

---
*This repository is built for continuous learning and evolution toward advanced AI orchestration.*
