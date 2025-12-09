import logging
from strands import Agent
from strands.tools import tool
from .config import model

logger = logging.getLogger()

@tool
def health_agent(query: str) -> str:
    """Expert in health, wellness, fitness, and nutrition."""
    logger.info("Health agent invoked")
    agent = Agent(
        system_prompt="You are a health expert. Provide general wellness and health information. Always recommend consulting healthcare professionals for medical advice.",
        model=model
    )
    result = str(agent(query))
    logger.info("Health agent completed")
    return result
