import datetime
import zoneinfo
import asyncio
import os
from constants import MODEL_GEMINI_2_0_FLASH, MODEL_GPT_40, MODEL_CLAUDE_SONNET, SESSION_ID, APP_NAME, USER_ID
from google.adk.models.lite_llm import LiteLlm
from google.adk.agents import Agent
from google.adk.sessions import InMemorySessionService
from google.adk.runners import Runner
from google.genai import types
from app.agents.flight_agent import flight_agent

cheap_model = MODEL_GPT_40


def say_hello(name: str="user") -> str:
    """ Retrieves the opening greeting to the user

    Args:
        name (str): The name of the user (e.g "Dena")
    
    Returns:
        str: A warm welcome greeting to the user that includes the user name
    """
    print('>>>   getting hello')
    return f"Good day to you {name}! Did you know Kenya has 2 official languages? English and Kiswahili."


hello_agent = Agent(
    name="hello_agent",
    model=LiteLlm(cheap_model),
    description="Generates the initial greeting to the user along with a fun fact",
    instruction="You are an agent that warmly welcomes the user. You are the first interaction they have"
    "when the user asks a question, you call the 'say_hello' tool to answer initially and provide a fun fact about Kenya to them"
    "because in addition to saying hello, you like educating users on Kenya",
    tools=[say_hello]
)