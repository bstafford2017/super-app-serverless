from strands import Agent
from strands.tools import tool
from .config import model

@tool
def trivia_agent(query: str) -> str:
    """Expert in general trivia, fun facts, and interesting knowledge."""
    agent = Agent(
        system_prompt="You are a trivia expert. Provide interesting facts and trivia answers concisely.",
        model=model
    )
    return str(agent(query))
