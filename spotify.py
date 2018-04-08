import functools
import json
import pickle

import requests

from oauth import implicit_flow
from secret import client_id
from song import Song


@functools.lru_cache(None)
def authentication():
    try:
        with open("spotify.response", mode="r") as file:
            response = pickle.load(file)
    except:
        response = implicit_flow("https://accounts.spotify.com/authorize", client_id,
                                 scope=["user-read-currently-playing", "user-read-playback-state"])
        try:
            with open("spotify.response", mode="w") as file:
                pickle.dump(file=file, obj=response)
        except:
            print("Could not save Spotify token. You need to authorize again next time.")
    return response["access_token"]


def currently_playing() -> (Song, int):
    response = requests.get("https://api.spotify.com/v1/me/player/currently-playing",
                            params={"access_token": authentication()})
    response = json.loads(response.content.decode("utf-8"))
    song = Song(response["item"]["name"], response["item"]["artists"][0]["name"], response["item"]["duration_ms"])
    return song, response["progress_ms"]
