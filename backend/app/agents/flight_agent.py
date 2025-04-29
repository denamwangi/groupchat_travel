from app.agents.constants import MODEL_GEMINI_2_0_FLASH, MODEL_GPT_40, MODEL_CLAUDE_SONNET, SESSION_ID, APP_NAME, USER_ID
from app.tools.flight_tool import get_flights
from google.adk.agents import Agent
from google.adk.models.lite_llm import LiteLlm

cheap_model = MODEL_GPT_40

flight_agent = Agent(
    name="flight_agent",
    model=LiteLlm(cheap_model),
    description="Generates flight options for a user from one city to another on a specifid departure date",
    instruction="You are a friendly tool that helps friends plan trips together. When a user gives you their origin, destination and dates"
    "call the 'get_flights' tool with the origin city, destination city, and departure_date and respond with flight options",
    tools=[get_flights]
)