from strands import Agent
from strands.tools import tool
from .config import model

@tool
def health_agent(query: str) -> str:
    """Expert in health, wellness, fitness, and nutrition."""
    agent = Agent(
        system_prompt="You are a health expert. Provide general wellness and health information. Always recommend consulting healthcare professionals for medical advice.",
        model=model
    )
    return str(agent(query))
