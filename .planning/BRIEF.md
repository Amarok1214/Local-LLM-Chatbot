# Local LLM Chatbot with Knowledge Graph

**One-liner**: A chatbot that uses a local LLM (TinyLlama) and queries a knowledge graph to answer user questions on general topics.

## Problem

Build a chatbot that:
- Hosts a local LLM (no external API calls)
- Uses a knowledge graph for context-aware responses
- Mirrors the query-based approach from the prism project

## Success Criteria

- [ ] Local LLM runs and responds to prompts
- [ ] FastAPI server hosts LLM at `http://localhost:5005/generate`
- [ ] POST request to `/generate` returns LLM responses
- [ ] Knowledge graph created with general topic data
- [ ] Chatbot queries knowledge graph before generating responses
- [ ] Opencode connected to local LLM endpoint

## Constraints

- **Deadline**: Tomorrow (March 4, 2026)
- **Platform**: Windows
- **LLM**: TinyLlama or similar lightweight model (~1-2GB)
- **Tech Stack**: FastAPI, Uvicorn, local LLM (Ollama or llama.cpp)
- **Knowledge Graph**: Simple in-memory graph (networkx) or lightweight database

## Out of Scope

- Complex graph embedding/reranking (prism-level sophistication)
- Multiple LLM providers
- Production deployment
- User authentication

## Approach

1. Install Ollama (Windows) and pull TinyLlama
2. Create FastAPI server that wraps Ollama API
3. Build simple knowledge graph with networkx (nodes + edges)
4. Query graph based on user input → get context → send to LLM
5. Connect Opencode to local endpoint
