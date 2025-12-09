from strands import Agent
from strands.tools import tool
from .config import model

@tool
def art_agent(query: str) -> str:
    """Expert in art, artists, art history, and creative expressions."""
    agent = Agent(
        system_prompt="You are an art expert. Discuss art, artists, techniques, and art history knowledgeably.",
        model=model
    )
    return str(agent(query))
