import logging
from strands import Agent
from strands.tools import tool
from .config import model

logger = logging.getLogger()

@tool
def sports_agent(query: str) -> str:
    """Expert in sports, athletes, teams, and sporting events."""
    logger.info("Sports agent invoked")
    agent = Agent(
        system_prompt="You are a sports expert. Provide accurate information about sports, athletes, and events.",
        model=model
    )
    result = str(agent(query))
    logger.info("Sports agent completed")
    return result
