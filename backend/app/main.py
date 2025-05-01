from fastapi import FastAPI
from app.agents.flight_agent import travel_agent

app = FastAPI()

@app.get("/")
async def root():
    print(travel_agent)
    return {"message": "Hello from FastAPI!"}


@app.get("/callback")
async def root():
    print(travel_agent)
    return {"message": "Redirecting back to the app!"}