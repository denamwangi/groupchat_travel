
import requests
import os
import base64

spotify_search_uri = "https://api.spotify.com/v1/search"
 
client_id = os.environ['SPOTIFY_KEY']
client_secret = os.environ['SPOTIFY_SECRET']

def generate_spotify_auth_header(client_id: str, client_secret: str):
    return base64.b64encode(f"{client_id}:{client_secret}".encode()).decode()

def get_spotify_token(auth_header: str):
    token_url = "https://accounts.spotify.com/api/token"
    token_response = requests.post(
        token_url,
        headers={
            "Authorization": f"Basic {auth_header}",
            "Content-Type": "application/x-www-form-urlencoded"
        },
        data={"grant_type": "client_credentials"}
    )
    return token_response

def get_tracks():
    auth_header = generate_spotify_auth_header(client_id, client_secret)
    print(f'auth header {auth_header}')

    token = get_spotify_token(auth_header)
    access_token = token.json()["access_token"]


    tracks_response = requests.get(
        spotify_search_uri,
        headers={
            "Authorization": f"Bearer {access_token}"
        },
        params={
            "q":"chill afrobeats",
            "type": "track",
            "limit":10,
        }
    )
    print(f'tracks response {tracks_response}')
    results = tracks_response.json()["tracks"]["items"]

    for track in results:
        name = track["name"]
        artists = track["artists"]
        print(f"name: {name} \n artists: {artists}")

if __name__ == "__main__":
    get_tracks()