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
        # Greetings & General
        (
            "greeting",
            "general",
            "A greeting is a way to say hello or acknowledge someone, like 'Hi', 'Hello', or 'Hey there!'",
        ),
        (
            "how_are_you",
            "general",
            "People ask 'How are you?' as a friendly way to check in on someone's wellbeing.",
        ),
        (
            "good_morning",
            "general",
            "Good morning is a greeting used in the morning hours, usually until noon.",
        ),
        (
            "good_afternoon",
            "general",
            "Good afternoon is a greeting used from noon until evening.",
        ),
        (
            "good_evening",
            "general",
            "Good evening is a greeting used in the evening hours.",
        ),
        ("good_night", "general", "Good night is used as a farewell before sleeping."),
        ("thanks", "general", "Thanks or thank you is an expression of gratitude."),
        ("bye", "general", "Bye is a casual farewell, short for 'Goodbye'."),
        # Gen Z Topics
        (
            "skibidi",
            "gen_z",
            "Skibidi is a viral internet meme and sound that became popular in 2024, used humorously in videos.",
        ),
        (
            "rizz",
            "gen_z",
            "Rizz means charisma, especially in romantic or social situations. Short for 'charisma'.",
        ),
        (
            "sigma",
            "gen_z",
            "Sigma is a term used online to describe a lone wolf who doesn't follow social norms, often humorously.",
        ),
        (
            "gyat",
            "gen_z",
            "Gyat is Gen Z slang meaning 'goddamn' and is often used when expressing excitement.",
        ),
        (
            "no_cap",
            "gen_z",
            "No cap means 'no lie' or 'for real', used to emphasize honesty.",
        ),
        ("bet", "gen_z", "Bet is Gen Z slang meaning 'okay', 'sure', or 'let's go'."),
        (
            "sheesh",
            "gen_z",
            "Sheesh is an expression of surprise or admiration, often said in an exaggerated way.",
        ),
        (
            "slay",
            "gen_z",
            "Slay means to do something exceptionally well or to look amazing.",
        ),
        (
            "vibe",
            "gen_z",
            "Vibe refers to the mood or atmosphere of a situation, or someone's energy.",
        ),
        ("aura", "gen_z", "Aura refers to a person's energy or magnetic presence."),
        (
            "stan",
            "gen_z",
            "Stan means to be a huge fan of someone or something, from Eminem's song 'Stan'.",
        ),
        (
            "goat",
            "gen_z",
            "GOAT means 'Greatest Of All Time', used to describe the best in any category.",
        ),
        ("lit", "gen_z", "Lit means something is exciting, fun, or cool."),
        (
            "fire",
            "gen_z",
            "Fire means something is really good or cool, like 'that's fire'.",
        ),
        (
            "based",
            "gen_z",
            "Based means being true to yourself and not caring about others' opinions.",
        ),
        ("w", "gen_z", "W means a win or success, the opposite of L."),
        ("L", "gen_z", "L means a loss or failure."),
        ("yap", "gen_z", "Yap means to talk a lot, often about unimportant things."),
        (
            "fanum_tax",
            "gen_z",
            "Fanum Tax is a meme about sharing food, where someone steals part of your meal.",
        ),
        (
            "brainrot",
            "gen_z",
            "Brainrot is Gen Z humor for content that rots your brain from too much internet use.",
        ),
        # Trending
        (
            "tiktok",
            "social_media",
            "TikTok is a popular short-video app where users create and share 15-60 second videos.",
        ),
        (
            "instagram",
            "social_media",
            "Instagram is a photo and video sharing app owned by Meta.",
        ),
        (
            "youtube",
            "social_media",
            "YouTube is a video platform where users watch and upload videos.",
        ),
        (
            "minecraft",
            "gaming",
            "Minecraft is a popular sandbox video game where players build with blocks.",
        ),
        ("fortnite", "gaming", "Fortnite is a popular battle royale video game."),
        (
            "roblox",
            "gaming",
            "Roblox is a gaming platform where users create and play games made by the community.",
        ),
        (
            "genshin_impact",
            "gaming",
            "Genshin Impact is a popular open-world action RPG game.",
        ),
        # Food
        (
            "pizza",
            "food",
            "Pizza is a popular food made with dough, sauce, cheese, and toppings.",
        ),
        (
            "burger",
            "food",
            "A burger is a sandwich with a meat patty between two buns.",
        ),
        ("sushi", "food", "Sushi is a Japanese dish with rice, fish, and seaweed."),
        ("ramen", "food", "Ramen is a Japanese noodle soup dish."),
        (
            "boba",
            "food",
            "Boba or bubble tea is a sweet tea drink with tapioca pearls.",
        ),
        (
            "mcdonalds",
            "food",
            "McDonald's is a fast food restaurant chain known for burgers and fries.",
        ),
        (
            "chicken_nuggets",
            "food",
            "Chicken nuggets are bite-sized pieces of chicken coated in breading.",
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
        # Gen Z connections
        ("rizz", "social_media", "often_discussed_on"),
        ("skibidi", "tiktok", "popular_on"),
        ("stan", "tiktok", "used_on"),
        ("gyat", "tiktok", "popular_on"),
        ("brainrot", "tiktok", "originates_from"),
        # Gaming connections
        ("gaming", "minecraft", "includes"),
        ("gaming", "fortnite", "includes"),
        ("gaming", "roblox", "includes"),
        ("gaming", "genshin_impact", "includes"),
        # Food connections
        ("pizza", "mcdonalds", "sold_at"),
        ("burger", "mcdonalds", "sold_at"),
        ("coffee", "cafe", "served_at"),
        ("boba", "cafe", "sold_at"),
        ("ramen", "cafe", "served_at"),
        ("sushi", "cafe", "served_at"),
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
