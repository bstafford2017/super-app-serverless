import logging
from strands import Agent
from .config import model
from .trivia import trivia_agent
from .math import math_agent
from .sports import sports_agent
from .technology import technology_agent
from .art import art_agent
from .geography import geography_agent
from .health import health_agent

logger = logging.getLogger()
logger.setLevel(logging.INFO)

logger.info("Initializing supervisor agent with 7 specialized agents")

supervisor = Agent(
    system_prompt="""You are a supervisor agent that routes questions to specialized experts.
    
Available experts:
- trivia_agent: general trivia and fun facts
- math_agent: mathematics and calculations
- sports_agent: sports, athletes, teams
- technology_agent: technology and programming
- art_agent: art and artists
- geography_agent: geography and places
- health_agent: health and wellness

Analyze the user's question and delegate to the most appropriate expert. Use conversation history to maintain context across interactions.""",
    model=model,
    tools=[trivia_agent, math_agent, sports_agent, technology_agent, art_agent, geography_agent, health_agent],
    conversation_history=True
)
