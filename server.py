from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import requests
import os
import falkordb

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

OLLAMA_BASE_URL = os.getenv("OLLAMA_BASE_URL", "http://localhost:11434")
MODEL_NAME = os.getenv("MODEL_NAME", "tinyllama")

FALKORDB_HOST = os.getenv("FALKORDB_HOST", "localhost")
FALKORDB_PORT = int(os.getenv("FALKORDB_PORT", "6379"))

GRAPH_NAME = "chatbot_knowledge"

db = falkordb.FalkorDB(host=FALKORDB_HOST, port=FALKORDB_PORT)


def setup_knowledge_graph():
    """Initialize the knowledge graph with nodes and edges."""
    graph = db.select_graph(GRAPH_NAME)

    nodes = [
        (
            "python",
            "technology",
            "Python is a high-level, interpreted programming language known for its readability and versatility.",
        ),
        (
            "machine_learning",
            "technology",
            "Machine learning is a subset of artificial intelligence that enables systems to learn and improve from experience.",
        ),
        (
            "deep_learning",
            "technology",
            "Deep learning is a subset of machine learning using neural networks with multiple layers.",
        ),
        (
            "neural_network",
            "technology",
            "A neural network is a computing system inspired by biological neural networks in the brain.",
        ),
        (
            "data_science",
            "technology",
            "Data science combines statistics, programming, and domain expertise to extract insights from data.",
        ),
        (
            "artificial_intelligence",
            "technology",
            "Artificial intelligence is the simulation of human intelligence by machines.",
        ),
        (
            "natural_language_processing",
            "technology",
            "Natural language processing (NLP) helps computers understand human language.",
        ),
        (
            "computer_vision",
            "technology",
            "Computer vision enables computers to interpret and analyze visual information from the world.",
        ),
        (
            "robotics",
            "technology",
            "Robotics combines engineering and computer science to design and build robots.",
        ),
        (
            "cloud_computing",
            "technology",
            "Cloud computing delivers computing services over the internet.",
        ),
        (
            "blockchain",
            "technology",
            "Blockchain is a distributed ledger technology that records transactions across many computers.",
        ),
        (
            "internet_of_things",
            "technology",
            "The Internet of Things (IoT) connects everyday devices to the internet.",
        ),
        (
            "coffee",
            "general",
            "Coffee is a brewed drink made from roasted coffee beans, one of the most popular beverages worldwide.",
        ),
        (
            "espresso",
            "general",
            "Espresso is a concentrated coffee made by forcing hot water through finely ground coffee.",
        ),
        (
            "latte",
            "general",
            "Latte is a coffee drink made with espresso and steamed milk.",
        ),
        (
            "cappuccino",
            "general",
            "Cappuccino is an espresso-based drink with equal parts espresso, steamed milk, and milk foam.",
        ),
        (
            "cafe",
            "general",
            "A cafe is a small restaurant serving light meals and beverages, especially coffee.",
        ),
        (
            "gaming",
            "entertainment",
            "Gaming is the act of playing electronic games, a popular form of entertainment worldwide.",
        ),
        (
            "video_games",
            "entertainment",
            "Video games are electronic games played on computers or consoles.",
        ),
        (
            "esports",
            "entertainment",
            "Esports is competitive gaming where players or teams compete in video games.",
        ),
        (
            "chess",
            "entertainment",
            "Chess is a strategic board game played by two players on a checkered board.",
        ),
        (
            "football",
            "sports",
            "Football (soccer) is a team sport played with a spherical ball between two teams.",
        ),
        (
            "basketball",
            "sports",
            "Basketball is a team sport where players score points by shooting a ball through a hoop.",
        ),
        (
            "tennis",
            "sports",
            "Tennis is a racket sport played individually or in doubles.",
        ),
        (
            "swimming",
            "sports",
            "Swimming is moving through water using arms and legs, an Olympic sport.",
        ),
        (
            "history",
            "academic",
            "History is the study of past events, civilizations, and societies.",
        ),
        (
            "world_war_ii",
            "academic",
            "World War II was a global conflict from 1939 to 1945 involving most of the world's nations.",
        ),
        (
            "ancient_rome",
            "academic",
            "Ancient Rome was a civilization that existed from 753 BC to 476 AD.",
        ),
        (
            "renaissance",
            "academic",
            "The Renaissance was a cultural movement in Europe from the 14th to 17th centuries.",
        ),
        (
            "physics",
            "academic",
            "Physics is the natural science studying matter, energy, and their interactions.",
        ),
        (
            "chemistry",
            "academic",
            "Chemistry is the scientific study of substances, their properties, and reactions.",
        ),
        (
            "biology",
            "academic",
            "Biology is the scientific study of living organisms and their interactions.",
        ),
        (
            "mathematics",
            "academic",
            "Mathematics is the abstract science of numbers, quantity, and space.",
        ),
        (
            "astronomy",
            "academic",
            "Astronomy is the scientific study of celestial objects and phenomena.",
        ),
        (
            "universe",
            "science",
            "The universe is all of space, time, matter, and energy that exists.",
        ),
        (
            "solar_system",
            "science",
            "The solar system consists of the Sun and eight planets orbiting it.",
        ),
        (
            "earth",
            "science",
            "Earth is the third planet from the Sun and the only known planet with life.",
        ),
        (
            "mars",
            "science",
            "Mars is the fourth planet from the Sun, known as the Red Planet.",
        ),
        (
            "moon",
            "science",
            "The Moon is Earth's only natural satellite, orbiting our planet.",
        ),
        (
            "black_hole",
            "science",
            "A black hole is a region in space where gravity is so strong that nothing can escape.",
        ),
        (
            "galaxy",
            "science",
            "A galaxy is a massive system of stars, gas, and dust held together by gravity.",
        ),
    ]

    edges = [
        ("python", "machine_learning", "used_in"),
        ("python", "data_science", "used_in"),
        ("python", "deep_learning", "used_in"),
        ("machine_learning", "deep_learning", "is_subset_of"),
        ("machine_learning", "neural_network", "uses"),
        ("machine_learning", "artificial_intelligence", "is_subset_of"),
        ("deep_learning", "neural_network", "based_on"),
        ("deep_learning", "natural_language_processing", "enables"),
        ("deep_learning", "computer_vision", "enables"),
        ("artificial_intelligence", "natural_language_processing", "includes"),
        ("artificial_intelligence", "computer_vision", "includes"),
        ("artificial_intelligence", "robotics", "powers"),
        ("artificial_intelligence", "data_science", "related_to"),
        ("cloud_computing", "artificial_intelligence", "provides_infrastructure"),
        ("internet_of_things", "cloud_computing", "connects_to"),
        ("coffee", "espresso", "used_to_make"),
        ("coffee", "latte", "used_in"),
        ("coffee", "cappuccino", "used_in"),
        ("espresso", "latte", "base_for"),
        ("espresso", "cappuccino", "base_for"),
        ("cafe", "coffee", "serves"),
        ("cafe", "espresso", "serves"),
        ("cafe", "latte", "serves"),
        ("gaming", "video_games", "includes"),
        ("gaming", "esports", "has"),
        ("video_games", "esports", "played_in"),
        ("chess", "gaming", "is_a"),
        ("football", "sports", "is_a"),
        ("basketball", "sports", "is_a"),
        ("tennis", "sports", "is_a"),
        ("swimming", "sports", "is_a"),
        ("history", "world_war_ii", "includes"),
        ("history", "ancient_rome", "includes"),
        ("history", "renaissance", "includes"),
        ("physics", "astronomy", "related_to"),
        ("chemistry", "biology", "related_to"),
        ("biology", "astronomy", "related_to"),
        ("mathematics", "physics", "used_in"),
        ("mathematics", "chemistry", "used_in"),
        ("mathematics", "computer_vision", "used_in"),
        ("universe", "solar_system", "contains"),
        ("solar_system", "earth", "contains"),
        ("solar_system", "mars", "contains"),
        ("earth", "moon", "has"),
        ("solar_system", "galaxy", "part_of"),
        ("universe", "galaxy", "contains"),
        ("universe", "black_hole", "contains"),
        ("astronomy", "black_hole", "studies"),
        ("astronomy", "galaxy", "studies"),
    ]

    try:
        for node_id, category, fact in nodes:
            query = """
            MERGE (n:Topic {id: $id})
            SET n.category = $category, n.fact = $fact
            """
            graph.query(query, {"id": node_id, "category": category, "fact": fact})

        for source, target, relation in edges:
            query = """
            MATCH (a:Topic {id: $source}), (b:Topic {id: $target})
            MERGE (a)-[r:RELATED {relation: $relation}]->(b)
            """
            graph.query(
                query, {"source": source, "target": target, "relation": relation}
            )

        print(
            f"Knowledge graph '{GRAPH_NAME}' initialized with {len(nodes)} nodes and {len(edges)} edges"
        )
    except Exception as e:
        print(f"Graph might already exist: {e}")


def query_knowledge_graph(query: str, max_results: int = 3) -> str:
    """Query the knowledge graph for relevant facts."""
    graph = db.select_graph(GRAPH_NAME)
    query_lower = query.lower()
    query_words = query_lower.split()

    search_terms = " OR ".join(
        [
            f"n.id CONTAINS '{word}' OR n.fact CONTAINS '{word}'"
            for word in query_words[:5]
        ]
    )

    cypher_query = f"""
    MATCH (n:Topic)
    WHERE {search_terms}
    RETURN n.id AS id, n.category AS category, n.fact AS fact
    LIMIT {max_results}
    """

    try:
        result = graph.query(cypher_query)
        if result.result_set:
            facts = [row[2] for row in result.result_set if row[2]]
            if facts:
                context_parts = [f"- {fact}" for fact in facts]
                return "Relevant facts from knowledge base:\n" + "\n".join(
                    context_parts
                )
    except Exception as e:
        print(f"Query error: {e}")

    return ""


setup_knowledge_graph()


class GenerateRequest(BaseModel):
    prompt: str


class GenerateResponse(BaseModel):
    response: str
    context_used: bool = False


@app.get("/")
async def root():
    return {"status": "running", "model": MODEL_NAME, "graph": GRAPH_NAME}


@app.post("/generate", response_model=GenerateResponse)
async def generate(request: GenerateRequest):
    try:
        context = query_knowledge_graph(request.prompt)

        if context:
            full_prompt = f"{context}\n\nUser question: {request.prompt}\nPlease provide a helpful answer based on the information above."
        else:
            full_prompt = request.prompt

        ollama_response = requests.post(
            f"{OLLAMA_BASE_URL}/api/generate",
            json={
                "model": MODEL_NAME,
                "prompt": full_prompt,
                "stream": False,
            },
            timeout=120,
        )

        if ollama_response.status_code != 200:
            raise HTTPException(status_code=500, detail="Ollama API error")

        result = ollama_response.json()

        return GenerateResponse(
            response=result.get("response", "").strip(), context_used=bool(context)
        )

    except requests.exceptions.ConnectionError:
        raise HTTPException(
            status_code=503,
            detail="Ollama is not running. Start it with 'ollama serve'",
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


if __name__ == "__main__":
    import uvicorn

    uvicorn.run(app, host="0.0.0.0", port=5005)
