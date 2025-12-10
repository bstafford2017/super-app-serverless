import logging
from strands import Agent
from strands.tools import tool
from .config import model

logger = logging.getLogger()

@tool
def art_agent(query: str) -> str:
    """Expert in art, artists, art history, and creative expressions."""
    logger.info("Art agent invoked")
    agent = Agent(
        system_prompt="You are an art expert. Discuss art, artists, techniques, and art history knowledgeably.",
        model=model
    )
    result = str(agent(query))
    logger.info("Art agent completed")
    return result
