from strands import Agent
from strands.tools import tool
from .config import model

@tool
def geography_agent(query: str) -> str:
    """Expert in geography, countries, cities, and landmarks."""
    agent = Agent(
        system_prompt="You are a geography expert. Provide accurate information about places, countries, and landmarks.",
        model=model
    )
    return str(agent(query))
