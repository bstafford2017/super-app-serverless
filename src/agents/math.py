from strands import Agent
from strands.tools import tool
from .config import model

@tool
def math_agent(query: str) -> str:
    """Expert in mathematics, calculations, and problem-solving."""
    agent = Agent(
        system_prompt="You are a math expert. Solve mathematical problems and explain calculations clearly.",
        model=model
    )
    return str(agent(query))
