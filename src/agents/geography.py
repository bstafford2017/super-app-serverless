import logging
from strands import Agent
from strands.tools import tool
from .config import model

logger = logging.getLogger()

@tool
def geography_agent(query: str) -> str:
    """Expert in geography, countries, cities, and landmarks."""
    logger.info("Geography agent invoked")
    agent = Agent(
        system_prompt="You are a geography expert. Provide accurate information about places, countries, and landmarks.",
        model=model
    )
    result = str(agent(query))
    logger.info("Geography agent completed")
    return result
