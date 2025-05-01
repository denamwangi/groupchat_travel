from google.adk.models.lite_llm import LiteLlm
from google.adk.agents import Agent, SequentialAgent
from pydantic import BaseModel, Field
from typing import Optional
from app.tools.music_tool import get_tracks_from_tags
from app.agents.constants import MODEL_GEMINI_2_0_FLASH, MODEL_GPT_40, MODEL_CLAUDE_SONNET, SESSION_ID, APP_NAME, USER_ID
from google.adk.models.lite_llm import LiteLlm



cheap_model = MODEL_CLAUDE_SONNET

class SpotifySearchTags(BaseModel):
    title: str = Field(..., description="A fun title for the playlist ")
    mood: str = Field(..., description="1-3 space separated descriptors of the type of mood the playlist should have e.g. 'happy emo' ")
    genre: Optional[str] = Field(None, description="The musical genre e.g. afrobeats, pop, R&B")
    


get_music_tags_agent = Agent(
    name="get_music_tags_agent",
    model=LiteLlm(cheap_model),
    description="Generates a playlist title and musical tags based on the destination city which will be used by  'get_playlist_agent' for a spotify tracks search query",
    instruction="You are a musical expert generating playlist tags based on a user's travel destination. "
                "Your output should include a mood and genre suitable for the city and time of year which 'get_playlist_agent' will use for the playlist. "
                "Respond in structured JSON using the SpotifySearchTags schema and use only the fields included."
                " Include 2-3 for each field. For example for Nairobi as the destination you might return" 
                "SpotifySearchTags(title='Breezy Summer in Paris' mood='upbeat happy' genre='afrobeats amapiano')"
                "Your output must be a pure JSON object and must not include any text, commentary, or Markdown formatting. "
                "Return only the JSON object with fields 'mood' and 'genre'. These will be used by 'get_playlist_agent'",
    output_key="spotify_search_tags",
)

get_playlist_agent = Agent(
    name="get_playlist_agent",
    model=LiteLlm(cheap_model),
    input_schema=SpotifySearchTags,
    description="Creates a spotify playlist for a travel destination",
    instruction="You are a musical expert that makes spotify playlists for travel destinations." 
                "You do this in two consecutive steps always in this order" \
                "1. First, delegate to 'get_music_tags_agent' to generate tags based on the destination"
                "2. Secondly, after 'get_music_tags_agent' responsds, call 'get_tracks_from_tags' which gets tracks based on those tags"
                "When a user asks for a playlist you MUST do both steps in order. you MUST call get_tracks_from_tags before you finish"
                "you do not need to pass mood and genre to 'get_tracks_from_tags'",                
    tools=[get_tracks_from_tags]
)

music_playlist_pipeline_agent = SequentialAgent(
    name="music_playlist_pipeline_agent",
    sub_agents=[get_music_tags_agent, get_playlist_agent]
)

# root_agent = music_playlist_pipeline_agent



# async def run_team_conversation():
#     # create a session
#     session_service = InMemorySessionService()

#     session = session_service.create_session(
#         app_name=APP_NAME,
#         user_id=USER_ID,
#         session_id=SESSION_ID
#     )

#     print(f" Session created: App={session.app_name}  User: {session.user_id} session_id={session.id}")
#     # actual_root_agent = music_playlist_pipeline_agent
#     # create a runner
#     runner_agent_team = Runner(
#         agent=music_playlist_pipeline_agent,
#         app_name=APP_NAME,
#         session_service=session_service
#     )
#     print(f"Runner created for agent {runner_agent_team.agent.name}")
#     await  call_agent_async("Hi! I'm going to Paris in December and need a playlist.",
#                         runner=runner_agent_team,
#                         user_id=USER_ID,
#                         session_id=SESSION_ID)   




# if __name__ == "__main__":
#     try:
#         asyncio.run(run_team_conversation())
#     except Exception as e:
#         print(f"Oops! An error occured: {e}")
