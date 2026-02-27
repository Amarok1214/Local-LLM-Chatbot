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
FALKORDB_PORT = int(os.getenv("FALKORDB_PORT", "6381"))

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
        # Small talk / Chitchat
        (
            "whats_up",
            "chitchat",
            "What's up is a casual greeting asking how someone is doing, similar to 'what's going on?'",
        ),
        (
            "how_was_your_day",
            "chitchat",
            "How was your day is a friendly question asking about someone's daily experiences.",
        ),
        (
            "whats_good",
            "chitchat",
            "What's good is Gen Z slang for asking what's happening or how someone is doing.",
        ),
        (
            "you_good",
            "chitchat",
            "You good? is a casual way of asking if someone is okay or doing well.",
        ),
        (
            "hows_life",
            "chitchat",
            "How's life is a casual question about someone's general wellbeing and life situation.",
        ),
        (
            "what_you_been_up_to",
            "chitchat",
            "What have you been up to is asking what someone has been doing lately.",
        ),
        (
            "lowkey",
            "gen_z",
            "Lowkey means secretly, quietly, or to a moderate degree. Like 'I lowkey love that song'.",
        ),
        (
            "highkey",
            "gen_z",
            "Highkey is the opposite of lowkey, meaning obviously or very much so.",
        ),
        (
            "fr_fr",
            "gen_z",
            "FR FR means 'for real for real', used to strongly emphasize something is true.",
        ),
        (
            "ngl",
            "gen_z",
            "NGL means 'not gonna lie', used before an honest or vulnerable statement.",
        ),
        (
            "mid",
            "gen_z",
            "Mid means average or mediocre, not good but not terrible either.",
        ),
        ("bussin", "gen_z", "Bussin means really good, usually used to describe food."),
        (
            "hits_different",
            "gen_z",
            "Hits different means something feels uniquely special or better in a particular context.",
        ),
        (
            "understood_the_assignment",
            "gen_z",
            "Understood the assignment means someone did exactly what was needed and did it well.",
        ),
        (
            "main_character",
            "gen_z",
            "Main character energy means acting like the protagonist of your own life story.",
        ),
        (
            "rent_free",
            "gen_z",
            "Living rent free means something or someone is stuck in your head without you wanting it.",
        ),
        (
            "era",
            "gen_z",
            "Era is used to describe a phase of life, like 'I'm in my study era' or 'villain era'.",
        ),
        (
            "delulu",
            "gen_z",
            "Delulu is short for delusional, used humorously when someone has unrealistic expectations.",
        ),
        (
            "touch_grass",
            "gen_z",
            "Touch grass means to go outside and disconnect from the internet for a while.",
        ),
        (
            "ick",
            "gen_z",
            "The ick is a sudden feeling of disgust or being turned off by someone.",
        ),
        (
            "situationship",
            "gen_z",
            "A situationship is a romantic relationship that isn't officially defined or labeled.",
        ),
        (
            "ghosting",
            "gen_z",
            "Ghosting means suddenly cutting off all communication with someone without explanation.",
        ),
        (
            "caught_in_4k",
            "gen_z",
            "Caught in 4K means being caught doing something bad with clear undeniable evidence.",
        ),
        (
            "npc",
            "gen_z",
            "NPC means someone acting like a Non-Playable Character, doing repetitive or mindless things.",
        ),
        (
            "glow_up",
            "gen_z",
            "Glow up means a major positive transformation in appearance or lifestyle.",
        ),
        (
            "ate",
            "gen_z",
            "Ate (and left no crumbs) means someone did something perfectly and impressively.",
        ),
        (
            "periodt",
            "gen_z",
            "Periodt is an emphatic version of 'period', used to end a statement with finality.",
        ),
        # Trivia & General Knowledge
        (
            "capitals",
            "trivia",
            "A capital city is the city where a country's government is located. Example: Tokyo is the capital of Japan, Paris is the capital of France, Manila is the capital of the Philippines.",
        ),
        (
            "philippines",
            "trivia",
            "The Philippines is an archipelago in Southeast Asia with Manila as its capital. It has over 7,000 islands.",
        ),
        (
            "largest_country",
            "trivia",
            "Russia is the largest country in the world by land area, covering over 17 million square kilometers.",
        ),
        (
            "smallest_country",
            "trivia",
            "Vatican City is the smallest country in the world, located inside Rome, Italy.",
        ),
        (
            "longest_river",
            "trivia",
            "The Nile River in Africa is often considered the longest river in the world at about 6,650 kilometers.",
        ),
        (
            "tallest_mountain",
            "trivia",
            "Mount Everest is the tallest mountain in the world at 8,849 meters above sea level, located in Nepal.",
        ),
        (
            "human_body",
            "trivia",
            "The human body has 206 bones, 32 teeth, and about 37 trillion cells. The heart beats about 100,000 times a day.",
        ),
        (
            "speed_of_light",
            "trivia",
            "The speed of light is approximately 299,792 kilometers per second. Nothing in the universe travels faster.",
        ),
        (
            "water_formula",
            "trivia",
            "Water is made of two hydrogen atoms and one oxygen atom, chemical formula H2O. It covers 71% of Earth's surface.",
        ),
        (
            "planets_count",
            "trivia",
            "There are 8 planets in our solar system: Mercury, Venus, Earth, Mars, Jupiter, Saturn, Uranus, and Neptune.",
        ),
        (
            "dna",
            "trivia",
            "DNA stands for deoxyribonucleic acid and carries genetic information in living organisms. It is shaped like a double helix.",
        ),
        (
            "gravity",
            "trivia",
            "Gravity is the force that attracts objects toward each other. Earth's gravity pulls things downward at 9.8 m/s².",
        ),
        (
            "photosynthesis",
            "trivia",
            "Photosynthesis is the process plants use to convert sunlight, water, and CO2 into food and oxygen.",
        ),
        (
            "boiling_point",
            "trivia",
            "Water boils at 100 degrees Celsius or 212 degrees Fahrenheit at sea level.",
        ),
        (
            "freezing_point",
            "trivia",
            "Water freezes at 0 degrees Celsius or 32 degrees Fahrenheit.",
        ),
        (
            "continents",
            "trivia",
            "There are 7 continents on Earth: Africa, Antarctica, Asia, Australia, Europe, North America, and South America.",
        ),
        (
            "oceans",
            "trivia",
            "There are 5 oceans on Earth: Pacific, Atlantic, Indian, Southern, and Arctic. The Pacific is the largest.",
        ),
        (
            "world_population",
            "trivia",
            "The world population is approximately 8 billion people as of 2024.",
        ),
        (
            "light_year",
            "trivia",
            "A light year is the distance light travels in one year, about 9.46 trillion kilometers.",
        ),
        (
            "periodic_table",
            "trivia",
            "The periodic table has 118 elements. Hydrogen is the lightest and most abundant element in the universe.",
        ),
        # Simple Math & Logic
        (
            "addition",
            "math",
            "Addition is combining numbers together. Example: 2 + 2 = 4. The result is called the sum.",
        ),
        (
            "subtraction",
            "math",
            "Subtraction is taking one number away from another. Example: 10 - 3 = 7. The result is called the difference.",
        ),
        (
            "multiplication",
            "math",
            "Multiplication is repeated addition. Example: 4 x 3 = 12. The result is called the product.",
        ),
        (
            "division",
            "math",
            "Division is splitting a number into equal parts. Example: 12 / 4 = 3. The result is called the quotient.",
        ),
        (
            "percentage",
            "math",
            "A percentage represents a fraction of 100. To find X% of a number: multiply by X then divide by 100. Example: 20% of 50 = (50 x 20) / 100 = 10.",
        ),
        (
            "area",
            "math",
            "Area is the amount of space inside a 2D shape. Rectangle: length x width. Circle: π x radius². Triangle: 0.5 x base x height.",
        ),
        (
            "perimeter",
            "math",
            "Perimeter is the total distance around a shape. Rectangle: 2 x (length + width). Circle circumference: 2 x π x radius.",
        ),
        (
            "pythagorean_theorem",
            "math",
            "The Pythagorean theorem states a² + b² = c² for right triangles, where c is the hypotenuse (longest side).",
        ),
        (
            "average",
            "math",
            "Average (mean) is the sum of all numbers divided by the count. Example: average of 2, 4, 6 = (2+4+6)/3 = 4.",
        ),
        (
            "prime_numbers",
            "math",
            "Prime numbers are only divisible by 1 and themselves. Examples: 2, 3, 5, 7, 11, 13, 17, 19, 23.",
        ),
        (
            "square_root",
            "math",
            "A square root is a number that when multiplied by itself gives the original number. Example: √16 = 4 because 4 x 4 = 16.",
        ),
        (
            "fractions",
            "math",
            "A fraction represents part of a whole. Example: 1/2 means one out of two equal parts. To add fractions, make denominators equal first.",
        ),
        (
            "order_of_operations",
            "math",
            "Order of operations (PEMDAS): Parentheses, Exponents, Multiplication/Division (left to right), Addition/Subtraction (left to right).",
        ),
        (
            "negative_numbers",
            "math",
            "Negative numbers are less than zero. Adding a negative = subtracting. Multiplying two negatives = positive.",
        ),
        (
            "exponents",
            "math",
            "An exponent means multiplying a number by itself. Example: 2³ = 2 x 2 x 2 = 8. Any number to the power of 0 = 1.",
        ),
        # Everyday Problem Solving
        (
            "time_zones",
            "practical",
            "Time zones divide the world into 24 regions. The Philippines is in UTC+8. New York is UTC-5. London is UTC+0.",
        ),
        (
            "unit_conversion",
            "practical",
            "Unit conversion: 1 kilometer = 1000 meters. 1 mile = 1.609 km. 1 inch = 2.54 cm. 1 kg = 2.205 pounds. 1 liter = 1000 ml.",
        ),
        (
            "cooking_tips",
            "practical",
            "Common cooking tips: preheat oven before baking. 1 cup = 240ml. 1 tablespoon = 15ml. 1 teaspoon = 5ml.",
        ),
        (
            "budgeting",
            "practical",
            "Budgeting means tracking income and expenses. The 50/30/20 rule: 50% needs, 30% wants, 20% savings.",
        ),
        (
            "password_tips",
            "practical",
            "A strong password uses uppercase, lowercase, numbers, and symbols and is at least 12 characters long. Never reuse passwords.",
        ),
        (
            "file_sizes",
            "practical",
            "File sizes: 1 KB = 1024 bytes, 1 MB = 1024 KB, 1 GB = 1024 MB, 1 TB = 1024 GB.",
        ),
        (
            "internet_speed",
            "practical",
            "Internet speed is measured in Mbps. Streaming HD video needs ~5 Mbps. 4K needs ~25 Mbps. Gaming needs ~10 Mbps.",
        ),
        (
            "first_aid",
            "practical",
            "Basic first aid: for cuts, clean the wound and apply pressure. For burns, run cool water for 10 minutes. For choking, use the Heimlich maneuver.",
        ),
        (
            "sleep_tips",
            "practical",
            "Adults need 7-9 hours of sleep per night. Avoid screens 1 hour before bed. Keep a consistent sleep schedule for better rest.",
        ),
        (
            "study_tips",
            "practical",
            "Effective study tips: use the Pomodoro technique (25 min study, 5 min break). Take notes, review regularly, and teach concepts to others.",
        ),
        (
            "temperature_conversion",
            "practical",
            "To convert Celsius to Fahrenheit: multiply by 9/5 then add 32. To convert Fahrenheit to Celsius: subtract 32 then multiply by 5/9.",
        ),
        (
            "time_management",
            "practical",
            "Time management tips: prioritize tasks by urgency and importance. Break big tasks into smaller steps. Avoid multitasking.",
        ),
        (
            "money_tips",
            "practical",
            "Money tips: track your spending, avoid impulse buys, build an emergency fund with 3-6 months of expenses, and invest early.",
        ),
        # Logic & Reasoning
        (
            "logical_thinking",
            "logic",
            "Logical thinking involves analyzing facts and drawing conclusions based on evidence, not emotions or assumptions.",
        ),
        (
            "cause_and_effect",
            "logic",
            "Cause and effect means one event causes another. Example: if it rains (cause), the ground gets wet (effect).",
        ),
        (
            "if_then",
            "logic",
            "If-then logic: If a condition is true, then a result follows. Example: If 2+2=4, then it is a true equation.",
        ),
        (
            "deduction",
            "logic",
            "Deduction is drawing specific conclusions from general rules. Example: All humans are mortal, Socrates is human, so Socrates is mortal.",
        ),
        (
            "problem_solving_steps",
            "logic",
            "Problem solving steps: 1) Identify the problem clearly, 2) Gather relevant information, 3) Think of possible solutions, 4) Pick the best one, 5) Evaluate results.",
        ),
        (
            "critical_thinking",
            "logic",
            "Critical thinking means questioning assumptions, evaluating evidence, and considering multiple perspectives before reaching a conclusion.",
        ),
        (
            "analogy",
            "logic",
            "An analogy compares two things to explain a concept. Example: A heart is to the body as a pump is to a water system.",
        ),
        (
            "pattern_recognition",
            "logic",
            "Pattern recognition is identifying repeating sequences. Example: 2, 4, 6, 8 — the pattern is adding 2 each time.",
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
        # Chitchat connections
        ("whats_up", "greeting", "is_a"),
        ("whats_good", "greeting", "is_a"),
        ("you_good", "greeting", "is_a"),
        ("hows_life", "greeting", "is_a"),
        ("how_was_your_day", "chitchat", "is_a"),
        ("what_you_been_up_to", "chitchat", "is_a"),
        # New gen_z connections
        ("lowkey", "tiktok", "popular_on"),
        ("highkey", "tiktok", "popular_on"),
        ("delulu", "tiktok", "popular_on"),
        ("situationship", "tiktok", "popular_on"),
        ("npc", "gaming", "originates_from"),
        ("glow_up", "social_media", "popular_on"),
        ("ghosting", "situationship", "related_to"),
        ("main_character", "tiktok", "popular_on"),
        ("era", "tiktok", "popular_on"),
        # Trivia connections
        ("gravity", "physics", "is_part_of"),
        ("photosynthesis", "biology", "is_part_of"),
        ("dna", "biology", "is_part_of"),
        ("water_formula", "chemistry", "is_part_of"),
        ("speed_of_light", "physics", "is_part_of"),
        ("tallest_mountain", "earth", "located_on"),
        ("longest_river", "earth", "located_on"),
        ("planets_count", "solar_system", "describes"),
        ("boiling_point", "chemistry", "related_to"),
        ("freezing_point", "chemistry", "related_to"),
        ("philippines", "capitals", "has_capital"),
        ("continents", "earth", "part_of"),
        ("oceans", "earth", "part_of"),
        ("periodic_table", "chemistry", "is_part_of"),
        ("light_year", "astronomy", "used_in"),
        # Math connections
        ("addition", "mathematics", "is_part_of"),
        ("subtraction", "mathematics", "is_part_of"),
        ("multiplication", "mathematics", "is_part_of"),
        ("division", "mathematics", "is_part_of"),
        ("percentage", "mathematics", "is_part_of"),
        ("area", "mathematics", "is_part_of"),
        ("perimeter", "mathematics", "is_part_of"),
        ("pythagorean_theorem", "mathematics", "is_part_of"),
        ("average", "mathematics", "is_part_of"),
        ("prime_numbers", "mathematics", "is_part_of"),
        ("square_root", "mathematics", "is_part_of"),
        ("fractions", "mathematics", "is_part_of"),
        ("order_of_operations", "mathematics", "is_part_of"),
        ("negative_numbers", "mathematics", "is_part_of"),
        ("exponents", "mathematics", "is_part_of"),
        # Logic connections
        ("logical_thinking", "problem_solving_steps", "uses"),
        ("cause_and_effect", "logical_thinking", "is_part_of"),
        ("if_then", "logical_thinking", "is_part_of"),
        ("deduction", "logical_thinking", "is_part_of"),
        ("problem_solving_steps", "logical_thinking", "requires"),
        ("critical_thinking", "logical_thinking", "is_part_of"),
        ("analogy", "logical_thinking", "is_part_of"),
        ("pattern_recognition", "logical_thinking", "is_part_of"),
        # Practical connections
        ("budgeting", "mathematics", "uses"),
        ("unit_conversion", "mathematics", "uses"),
        ("study_tips", "logical_thinking", "applies"),
        ("temperature_conversion", "mathematics", "uses"),
        ("time_management", "problem_solving_steps", "applies"),
        ("money_tips", "budgeting", "related_to"),
        ("cooking_tips", "unit_conversion", "uses"),
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


SMALL_TALK_PATTERNS = {
    "hi": ["greeting", "how_are_you", "hello", "hey"],
    "hello": ["greeting", "how_are_you", "hi", "hey"],
    "hey": ["greeting", "how_are_you", "hi", "hello"],
    "how are you": ["how_are_you", "you_good", "whats_up"],
    "how's your day": ["how_was_your_day", "hows_life"],
    "good morning": ["good_morning", "greeting"],
    "good afternoon": ["good_afternoon", "greeting"],
    "good evening": ["good_evening", "greeting"],
    "good night": ["good_night", "bye"],
    "bye": ["bye", "good_night"],
    "thanks": ["thanks", "thank_you"],
    "thank you": ["thanks", "thank_you"],
    "what's up": ["whats_up", "whats_good", "you_good"],
    "whats up": ["whats_up", "whats_good", "you_good"],
    # Problem solving & trivia triggers
    "what is": ["logical_thinking", "problem_solving_steps"],
    "what are": ["logical_thinking", "problem_solving_steps"],
    "how do i": ["problem_solving_steps", "study_tips"],
    "how to": ["problem_solving_steps", "cooking_tips"],
    "calculate": ["mathematics", "addition", "multiplication"],
    "compute": ["mathematics", "addition", "multiplication"],
    "convert": ["unit_conversion", "temperature_conversion"],
    "capital of": ["capitals", "philippines"],
    "how many": ["human_body", "planets_count", "continents"],
    "formula": ["pythagorean_theorem", "area", "perimeter"],
    "percentage": ["percentage", "mathematics"],
    "average": ["average", "mathematics"],
    "square root": ["square_root", "mathematics"],
    "prime": ["prime_numbers", "mathematics"],
    "solve": ["problem_solving_steps", "mathematics"],
    "explain": ["logical_thinking", "critical_thinking"],
    "difference between": ["logical_thinking", "critical_thinking"],
    "why is": ["cause_and_effect", "logical_thinking"],
    "how does": ["cause_and_effect", "logical_thinking"],
    "what causes": ["cause_and_effect", "logical_thinking"],
    "planet": ["planets_count", "solar_system"],
    "ocean": ["oceans", "earth"],
    "continent": ["continents", "earth"],
    "country": ["capitals", "largest_country"],
    "temperature": ["temperature_conversion", "boiling_point", "freezing_point"],
    "speed of light": ["speed_of_light", "physics"],
    "dna": ["dna", "biology"],
    "gravity": ["gravity", "physics"],
    "photosynthesis": ["photosynthesis", "biology"],
    "water": ["water_formula", "chemistry"],
    "budget": ["budgeting", "money_tips"],
    "save money": ["budgeting", "money_tips"],
    "study": ["study_tips", "time_management"],
    "sleep": ["sleep_tips"],
    "password": ["password_tips"],
    "file size": ["file_sizes"],
    "internet": ["internet_speed"],
    "first aid": ["first_aid"],
    "time zone": ["time_zones"],
}


def query_knowledge_graph(query: str, max_results: int = 3) -> str:
    """Query the knowledge graph for relevant facts."""
    graph = db.select_graph(GRAPH_NAME)
    query_lower = query.lower()

    # Check for small talk patterns first
    for pattern, topic_ids in SMALL_TALK_PATTERNS.items():
        if pattern in query_lower:
            topic_search = " OR ".join([f"n.id = '{tid}'" for tid in topic_ids])
            cypher_query = f"""
            MATCH (n:Topic)
            WHERE {topic_search}
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
                print(f"Small talk query error: {e}")

    # Fall back to keyword search
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


SYSTEM_PROMPT = """You are a friendly, helpful, and conversational AI assistant. 
You give clear and concise answers. 
You use a casual but professional tone. 
If you don't know something, you honestly say you don't know.
You are enthusiastic and enjoy helping people learn new things."""


@app.post("/generate", response_model=GenerateResponse)
async def generate(request: GenerateRequest):
    try:
        context = query_knowledge_graph(request.prompt)

        # Build prompt with system prompt and context
        if context:
            full_prompt = f"""{SYSTEM_PROMPT}

Relevant facts from knowledge base:
{context}

User: {request.prompt}
Assistant:"""
        else:
            # No context found - still include system prompt
            full_prompt = f"""{SYSTEM_PROMPT}

User: {request.prompt}
Assistant:"""

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
