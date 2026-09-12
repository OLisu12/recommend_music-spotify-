import os
import token

import requests
from dotenv import load_dotenv

load_dotenv()

CLIENT_ID = os.getenv("CLIENT_ID")
CLIENT_SECRET = os.getenv("CLIENT_SECRET")

TOKEN_URL = ("https://accounts.spotify.com/api/token")
SEARCH_URL = ("https://api.spotify.com/v1/search")

def get_access_token():
    response = requests.post(TOKEN_URL,
                             data={"grant_type": "client_credentials",
                                   "client_id": CLIENT_ID,
                                   "client_secret": CLIENT_SECRET},
                             timeout=10)
    response.raise_for_status()
    data = response.json()
    return data["access_token"]

def search_tracks_by_genre(token, genre, limit=10):
    headers = {"Authorization": f"Bearer {token}"}
    params = {"q": genre, "type": "track", "market":"KR",  "limit": limit}

    response = requests.get(SEARCH_URL, params=params, headers=headers, timeout=10)
    response.raise_for_status()
    data = response.json()

    return data.get("tracks", {}).get("items", [])

def get_top_tracks(genres, limit=10):
    token = get_access_token()
    track_scores = {}
    for genre, genre_score in genres:
        tracks = search_tracks_by_genre(token, genre, limit=limit)
        for rank, track in enumerate(tracks, start=1):
            track_id = track["id"]
            rank_score = (11-rank)
            total_score = (genre_score * 10 + rank_score)

            if track_id not in track_scores:
                track_scores[track_id] = {
                    "id": track_id,
                    "title": track["name"],
                    "artists": [track["artists"][0]["name"]],
                    "album": track["album"]["name"],
                    "url": track["external_urls"]["spotify"],
                    "score": total_score,
                    "genre": genre
                }
            else:
                track_scores[track_id]["score"] += total_score
                track_scores[track_id]["genre"] = genre

    result = sorted(track_scores.values(),
                     key=lambda item: item["score"],
                     reverse=True)

    return result[:limit]

