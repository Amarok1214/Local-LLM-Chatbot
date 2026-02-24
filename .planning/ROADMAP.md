# Roadmap: Local LLM Chatbot with Knowledge Graph

**Project**: local-llm-chatbot
**Brief**: `.planning/BRIEF.md`
**Target**: v1.0 (MVP)

---

## Phases

| Phase | Name | Status |
|-------|------|--------|
| 01 | Foundation - Environment Setup | pending |
| 02 | LLM Server - FastAPI + Ollama | pending |
| 03 | Knowledge Graph - Data & Queries | pending |
| 04 | Integration - Graph + LLM Pipeline | pending |
| 05 | Testing & Verification | pending |

---

## Phase Overview

### 01-foundation
- Install Ollama on Windows
- Pull TinyLlama model
- Set up project structure with FastAPI dependencies
- Verify Ollama is running locally

### 02-llm-server  
- Create `server.py` with FastAPI
- Implement `/generate` endpoint wrapping Ollama
- Run server on port 5005
- Test with POST request

### 03-knowledge-graph
- Create simple knowledge graph with networkx
- Add general topic nodes and edges
- Implement query function to find related context

### 04-integration
- Connect knowledge graph queries to LLM prompts
- User message → query graph → get context → send to LLM → return response

### 05-testing
- Full end-to-end test
- Verify Opencode can call the API
- Confirm knowledge graph context improves responses

---

## Milestones

| Milestone | Phase | Target |
|-----------|-------|--------|
| v1.0 | All | Tomorrow (March 4, 2026) |

---

## Notes

- Similar structure to surplus_prism for consistency
- Simple knowledge graph (networkx) vs Graphiti for faster setup
- Lightweight LLM (TinyLlama ~1GB) for Windows compatibility
