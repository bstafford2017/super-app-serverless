from strands import Agent
from strands.tools import tool
from .config import model

@tool
def sports_agent(query: str) -> str:
    """Expert in sports, athletes, teams, and sporting events."""
    agent = Agent(
        system_prompt="You are a sports expert. Provide accurate information about sports, athletes, and events.",
        model=model
    )
    return str(agent(query))
