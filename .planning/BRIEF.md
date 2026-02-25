# Local LLM Chatbot with Knowledge Graph

**One-liner**: A chatbot that uses a local LLM (TinyLlama) and queries a knowledge graph to answer user questions on general topics.

## Problem

Build a chatbot that:
- Hosts a local LLM (no external API calls)
- Uses a knowledge graph for context-aware responses
- Mirrors the query-based approach from the prism project

## Success Criteria

- [x] Local LLM runs and responds to prompts
- [x] FastAPI server hosts LLM at `http://localhost:5005/generate`
- [x] POST request to `/generate` returns LLM responses
- [x] Knowledge graph created with general topic data
- [x] Chatbot queries knowledge graph before generating responses
- [x] Opencode connected to local LLM endpoint

**Status: ALL CRITERIA MET** ✅

## Constraints

- **Deadline**: Tomorrow (March 4, 2026)
- **Platform**: Windows
- **LLM**: TinyLlama (637MB via Ollama)
- **Tech Stack**: FastAPI, Uvicorn, FalkorDB (knowledge graph)
- **Knowledge Graph**: FalkorDB (similar to prism project approach)

## Out of Scope

- Complex graph embedding/reranking (prism-level sophistication)
- Multiple LLM providers
- Production deployment
- User authentication

## Approach

1. Install Ollama (Windows) and pull TinyLlama ✅
2. Create FastAPI server that wraps Ollama API ✅
3. Build knowledge graph with FalkorDB (nodes + edges) ✅
4. Query graph based on user input → get context → send to LLM ✅
5. Connect Opencode to local endpoint ✅

## Final Tech Stack

| Component | Technology |
|-----------|------------|
| LLM | TinyLlama (via Ollama) |
| API Server | FastAPI + Uvicorn |
| Knowledge Graph | FalkorDB |
| Python Client | falkordb |
| Server Port | 5005 |

## Repository

https://github.com/Amarok1214/Local-LLM-Chatbot

## Notes

- Project completed and pushed to GitHub
- All success criteria verified and working
- FalkorDB approach mirrors the prism project
- 40 topics in knowledge graph across 6 categories
