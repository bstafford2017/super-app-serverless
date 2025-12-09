import logging
from strands import Agent
from strands.tools import tool
from .config import model

logger = logging.getLogger()

@tool
def technology_agent(query: str) -> str:
    """Expert in technology, programming, and digital innovations."""
    logger.info("Technology agent invoked")
    agent = Agent(
        system_prompt="You are a technology expert. Explain tech concepts, programming, and innovations clearly.",
        model=model
    )
    result = str(agent(query))
    logger.info("Technology agent completed")
    return result
