# Local LLM Chatbot with Knowledge Graph

A chatbot that uses a local LLM (TinyLlama) combined with a knowledge graph (FalkorDB) to answer user questions with context-aware responses.

## Features

- **Local LLM** - No external API calls, runs entirely offline using Ollama + TinyLlama
- **Knowledge Graph** - 40 topics stored in FalkorDB with relationships
- **Context-Aware** - Queries the knowledge graph before generating responses
- **FastAPI API** - Simple REST API at `http://localhost:5005`

## Tech Stack

| Component | Technology |
|-----------|------------|
| LLM | TinyLlama (via Ollama) |
| API Server | FastAPI + Uvicorn |
| Knowledge Graph | FalkorDB |
| Python | 3.10+ |

## Project Structure

```
local-llm-chatbot/
├── server.py           # Main FastAPI server with knowledge graph
├── chat.py             # CLI chat interface
├── index.html          # Web interface (open in browser)
├── requirements.txt    # Python dependencies
├── docker-compose.yml  # FalkorDB configuration
└── README.md          # This file
```

## Quick Start

### Prerequisites

1. **Ollama** - Download from https://ollama.com
2. **Docker Desktop** - For FalkorDB (optional, can use existing instance)

### Steps

1. **Start FalkorDB:**
```bash
docker compose up -d
```

2. **Start Ollama:**
```bash
ollama serve
ollama pull tinyllama
```

3. **Install dependencies:**
```bash
pip install -r requirements.txt
```

4. **Start the server:**
```bash
python -m uvicorn server:app --port 5005
```

5. **Use the chatbot:**

   **Option A - Web Interface (Recommended):**
   - Open `index.html` in your browser (double-click the file)
   - Or drag `index.html` into Chrome/Edge/Firefox
   - Type your question and click Send

   **Option B - Interactive Docs:**
   - Go to http://localhost:5005/docs
   - Click on `/generate`
   - Click "Try it out"
   - Enter `{"prompt": "Your question"}`
   - Click "Execute"

   **Option C - PowerShell:**
   ```powershell
   Invoke-RestMethod -Uri 'http://localhost:5005/generate' -Method POST -ContentType 'application/json' -Body '{"prompt": "What is machine learning?"}'
   ```

   **Option D - Command Prompt:**
   ```bash
   curl -X POST http://localhost:5005/generate -H "Content-Type: application/json" -d "{\"prompt\": \"What is machine learning?\"}"
   ```

## API Endpoints

| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | `/` | Server status |
| POST | `/generate` | Generate response |

### Generate Request

```json
{
  "prompt": "Your question here"
}
```

### Generate Response

```json
{
  "response": "The chatbot's answer...",
  "context_used": true
}
```

## Knowledge Graph Topics

The chatbot knows about:

- **Technology**: python, machine_learning, deep_learning, neural_network, artificial_intelligence, natural_language_processing, computer_vision, robotics, cloud_computing, blockchain, internet_of_things
- **Coffee**: coffee, espresso, latte, cappuccino, cafe
- **Entertainment**: gaming, video_games, esports, chess
- **Sports**: football, basketball, tennis, swimming
- **History**: history, world_war_ii, ancient_rome, renaissance
- **Science**: physics, chemistry, biology, mathematics, astronomy, universe, solar_system, earth, mars, moon, black_hole, galaxy

## How It Works

1. User sends a question to `POST /generate`
2. Server queries FalkorDB for relevant facts using Cypher
3. If facts found, they're added to the prompt
4. Prompt is sent to Ollama (TinyLlama)
5. Response is returned to the user

```
User Query → FastAPI → FalkorDB (get context) → Ollama → Response
```
