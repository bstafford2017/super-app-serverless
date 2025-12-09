import logging
from strands import Agent
from strands.tools import tool
from .config import model

logger = logging.getLogger()

@tool
def math_agent(query: str) -> str:
    """Expert in mathematics, calculations, and problem-solving."""
    logger.info("Math agent invoked")
    agent = Agent(
        system_prompt="You are a math expert. Solve mathematical problems and explain calculations clearly.",
        model=model
    )
    result = str(agent(query))
    logger.info("Math agent completed")
    return result
