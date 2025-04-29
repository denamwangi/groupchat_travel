import asyncio
from constants import MODEL_GEMINI_2_0_FLASH, MODEL_GPT_40, MODEL_CLAUDE_SONNET, SESSION_ID, APP_NAME, USER_ID
from google.adk.models.lite_llm import LiteLlm
from google.adk.agents import Agent
from google.adk.sessions import InMemorySessionService
from google.adk.runners import Runner
from google.genai import types
from app.agents.flight_agent import flight_agent
from app.agents.hello_agent import hello_agent
from app.tools.weather_tool import get_weather

root_agent_model = MODEL_GPT_40

weather_agent_team = Agent(
    name="weather_agent_v2",
    model=LiteLlm(root_agent_model),
    description="The main coordinator agent. Handles weather requests along with greetings and goodbyes",
    instruction=" You are the main weather agent coordinating a team. Your main responsibility is"
    "to provide weather information to a user. You will use the 'get_weather' tool ONLY to respond"
    "to explicit requests for weather e.g. 'what is the weather in Nairobi. You have specailized sub agents"
    "1. 'hello_agent': Handles initial greetings and provides a fun fact about kenya when a user says hello."
    "Delegate all greetings to this agent"
    "2. flight_agent: handles the flight travel requests and provides flight options"
    "If it is a greeting delegate to 'hello_agent'"
    "if it is travel related delegate to 'flight_agent' and if it is weather related, handle the response yourself using 'get_weather' using a southern belle persona"
    "For everything else, respond appropriately or state you cannot handle it.",
    tools=[get_weather],
    sub_agents=[hello_agent, flight_agent]
)
print(f" 🙂‍↔️Success! the root agent {weather_agent_team.name} has been created")


# make the actual call to the llm using async
async def call_agent_async(query: str, runner, user_id, session_id):
    print(f"\n >>> User Query: {query}")

    content = types.Content(role="user", parts=[types.Part(text=query)])

    final_response_text = "Agent did not produce any results sorry"

    async for event in runner.run_async(user_id=user_id, session_id=session_id, new_message=content):
        print(f" Event Info: Author: {event.author}, Type: {type(event).__name__}, Final: {event.is_final_response()} Content: {event.content}")
        print('_'*50)
        if event.is_final_response():
            if event.content and event.content.parts:
                final_response_text = event.content.parts[0].text
            elif event.actions and event.actions.escalate:
                final_response_text = f"Agent escalated: {event.error_message} or No specific error messgae"
            break
    print(f" <<< Agent Response: {final_response_text}")

async def run_team_conversation():
    # create a session
    session_service = InMemorySessionService()

    session = session_service.create_session(
        app_name=APP_NAME,
        user_id=USER_ID,
        session_id=SESSION_ID
    )

    print(f" Session created: App={session.app_name}  User: {session.user_id} session_id={session.id}")
    actual_root_agent = weather_agent_team
    # create a runner
    runner_agent_team = Runner(
        agent=actual_root_agent,
        app_name=APP_NAME,
        session_service=session_service
    )
    print(f"Runner created for agent {runner_agent_team.agent.name}")
    await call_agent_async("Hello! I want to go from New york to Nairobi next Wednesday. What are my flight options?",
                        runner=runner_agent_team,
                        user_id=USER_ID,
                        session_id=SESSION_ID)
    await call_agent_async("What's the weather there?",
                        runner=runner_agent_team,
                        user_id=USER_ID,
                        session_id=SESSION_ID)   
    await call_agent_async("What should I wear?",
                        runner=runner_agent_team,
                        user_id=USER_ID,
                        session_id=SESSION_ID)   


if __name__ == "__main__":
    try:
        asyncio.run(run_team_conversation())
    except Exception as e:
        print(f"Oops! An error occured: {e}")
