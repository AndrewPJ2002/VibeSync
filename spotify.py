import json
from os import path
from time import time
from sqlalchemy.util import b64encode
import requests

from models import Song

SPOTIFY_CLIENT_ID = "a641f9eda67c4d359d2172f1b5448158"
SPOTIFY_CLIENT_SECRET = "bc70f485418a48589266799890b0111d"


def store_spotify_key(key):
    with open("spotify_key.json", "w") as file:
        json.dump({"key": key, "timestamp": time()}, file)


def read_spotify_key():
    if path.exists("spotify_key.json"):
        with open("spotify_key.json", "r") as file:
            data = json.load(file)
            if time() - data["timestamp"] < 3600:
                print("hit")
                return data["key"]

    return None


def get_spotify_key():
    token = read_spotify_key()

    if token is not None:
        return token

    basic_token = b64encode(
        bytes(f"{SPOTIFY_CLIENT_ID}:{SPOTIFY_CLIENT_SECRET}", "utf-8")
    )

    res = requests.post(
        "https://accounts.spotify.com/api/token",
        headers={"Authorization": f"Basic {basic_token}"},
        data={"grant_type": "client_credentials"},
    )

    data = res.json()
    token = data["access_token"]
    store_spotify_key(token)
    return token


def spotify_headers():
    return {"Authorization": f"Bearer {get_spotify_key()}"}


def search_tracks(name):
    res = requests.get(
        "https://api.spotify.com/v1/search",
        headers=spotify_headers(),
        params={"q": name, "type": "track", "limit": 10},
    )

    songs = []

    for track in res.json()["tracks"]["items"]:
        song = Song()
        song.spotify_id = track["id"]
        song.title = track["name"]
        song.artist = track["artists"][0]["name"]
        songs.append(song)

    return songs
