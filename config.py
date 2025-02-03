import os
from dotenv import load_dotenv

load_dotenv()

class Config:
    # LLM Configuration (using OpenAI as example)
    OPENAI_API_KEY = os.getenv("OPENAI_API_KEY", "your-api-key-here")
    MODEL_NAME = "gpt-4"
    TEMPERATURE = 0.7
    
    # Agent Configuration
    MAX_ITERATIONS = 5
    AGENT_TIMEOUT = 30
    
    # Memory Configuration
    MEMORY_SIZE = 100
    MEMORY_FILE = "agent_memory.json"
    
    # Visualization Configuration
    FIGURE_SIZE = (10, 6)
    STYLE = "seaborn-v0_8"
