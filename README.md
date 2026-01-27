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
Located in `module-1/personal_chef.py`.
- **Goal**: A diet-focused agent that can substitute ingredients using web search.
- **Stack**: LangGraph `create_agent`, Tavily Search, OpenAI.
- **Configuration**: Defined in `langgraph.json`.

## 🔍 Observability (LangSmith)
To trace your agent's thought process:
1. Ensure `LANGSMITH_TRACING=true` in `.env`.
2. Run your agent (via Studio or script).
3. Check your project in the [LangSmith Dashboard](https://smith.langchain.com/) to see step-by-step execution, latency, and token usage.

---
*This repository is built for continuous learning and evolution toward advanced AI orchestration.*
