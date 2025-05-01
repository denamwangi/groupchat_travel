
import requests
import os
import json
import base64
import pdb
from pydantic import BaseModel, Field
from typing import Optional, List
from google.adk.models.lite_llm import LiteLlm
from google.adk.tools.tool_context import ToolContext


TEST_PLAYLIST_ID = '2IhD8FnT8hvkjezkZ2JR0P'
spotify_user_id = 'dmwangi-us'
spotify_search_uri = "https://api.spotify.com/v1/search"
spotify_create_playlist_uri = "https://api.spotify.com/v1/users/{spotify_user_id}/playlists"
spotify_add_tracks_uri = f"https://api.spotify.com/v1/playlists/{TEST_PLAYLIST_ID}/tracks"
 
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

auth_header = generate_spotify_auth_header(client_id, client_secret)
print(f'auth header {auth_header}')

token = get_spotify_token(auth_header)
access_token = token.json()["access_token"]

def _get_track_uris(tracks):
    track_ids = []
    track_uris = ''
    for track in tracks:
        name = track["name"]
        artists = track["artists"]
        id = track["id"]
        track_ids.append(id)
        track_uris += f"{track['uri']},"
        print(f"name: {name} \n uri: {track['uri']} \n artists: {artists[0]['name']}")
    print('.'*50)
    print('\n adding tracks to uris')


    return track_uris[:-1]

def _get_tracks(search_query: str) -> List[str]:
    # GET TRACKS BASED ON TAGS
    tracks_response = requests.get(
        spotify_search_uri,
        headers={
            "Authorization": f"Bearer {access_token}"
        },
        params={
            "q":search_query,
            "type": "track",
            "limit":10,
        }
    )
    print(f'tracks response {tracks_response}')
    return tracks_response.json()["tracks"]["items"]

def _create_playlist():
    print('>'*50)
    print('creating playlist...')
    # CREATE EMPTY PLAYLIST WITH FUN NAME
    create_playlist_response = requests.post(
        spotify_create_playlist_uri,
        headers={
            "Authorization": f"Bearer {access_token}",
            "Content-Type": "application/json"
        },
        json={
            
                "name": "New Test Playlist",
                "description": "Test playlist description",
                "public": True,
            
        }
    )
    print(create_playlist_response)
    return create_playlist_response

def _add_tracks_to_playlist(track_uris: str, playlist_id: str):
    print('>'*50)
    print('adding tracks to playlist')

    add_playlist_tracks_response = requests.get(
        spotify_add_tracks_uri,
        headers={
            "Authorization": f"Bearer {access_token}"
        },
        params={
            "q":track_uris
        }
    )
    return add_playlist_tracks_response


def get_tracks_from_tags(tool_context: ToolContext) -> str:
    """ Uses tags and fetches tracks for a Spotify playlist that match those tags

    Args:
        tool_context: Automatically provided by ADK.

    Returns:
        playlist link (str): Spotify link to playlist
    """

    print('.'*50)
    print('.'*50)

    spotify_search_tags = tool_context.state.to_dict().get('spotify_search_tags')
    tags = json.loads(spotify_search_tags)
    mood = tags.get('mood')
    genre = tags.get('genre')
    search_query = f"{mood} {genre}"


    tracks = _get_tracks(search_query)    
    track_uris = _get_track_uris(tracks)
    return "https://open.spotify.com/playlist/37i9dQZF1Eta3yIt7Xb0IB?si=3fjCpfHLQRyhpn0wOGOEOw"

    # CREATE EMPTY PLAYLIST WITH FUN NAME
    playlist = _create_playlist()
    playlist_id = TEST_PLAYLIST_ID
    # ADD TRACKS TO PLAYLIST
    add_playlist_tracks_response = _add_tracks_to_playlist(track_uris, playlist_id)
    print(add_playlist_tracks_response)

    return ['1234', '4545']




if __name__ == "__main__":
    tracks = _get_tracks('romantic cozy afrobeats amapiano jazz lounge')
    track_uris = _get_track_uris(tracks)
    # v2 = _create_playlist()
    # import pdb; pdb.set_trace()
    # v3 = _add_tracks_to_playlist('spotify:track:78Q5Tvh52OcWlukIy6vOL1,spotify:track:0cbPof9LM6kJJRdaFvQxmR', TEST_PLAYLIST_ID)