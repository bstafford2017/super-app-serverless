import logging
from strands import Agent
from strands.tools import tool
from .config import model

logger = logging.getLogger()

@tool
def trivia_agent(query: str) -> str:
    """Expert in general trivia, fun facts, and interesting knowledge."""
    logger.info("Trivia agent invoked")
    agent = Agent(
        system_prompt="You are a trivia expert. Provide interesting facts and trivia answers concisely.",
        model=model
    )
    result = str(agent(query))
    logger.info("Trivia agent completed")
    return result
