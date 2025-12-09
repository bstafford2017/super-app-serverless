from strands import Agent
from strands.tools import tool
from .config import model

@tool
def technology_agent(query: str) -> str:
    """Expert in technology, programming, and digital innovations."""
    agent = Agent(
        system_prompt="You are a technology expert. Explain tech concepts, programming, and innovations clearly.",
        model=model
    )
    return str(agent(query))
