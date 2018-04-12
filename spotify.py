import functools
import json
import os
import pickle

import requests
from appdirs import AppDirs

from errors import SpotifyAPIError
from oauth import implicit_flow
from secret import client_id
from song import Song

_last_song = None
_cache_dir = AppDirs(appname="lyricrawl").user_cache_dir


@functools.lru_cache(None)
def authentication():
    os.makedirs(_cache_dir, exist_ok=True)
    try:
        with open(_cache_dir + "/spotify.response", mode="rb") as file:
            response = pickle.load(file)
    except:
        response = implicit_flow("https://accounts.spotify.com/authorize", client_id,
                                 scope=["user-read-currently-playing", "user-read-playback-state"])
        try:
            with open(_cache_dir + "/spotify.response", mode="wb") as file:
                pickle.dump(file=file, obj=response)
        except:
            print("Could not save Spotify token. You need to authorize again next time.")
    return response["access_token"]


def make_request():
    response = requests.get("https://api.spotify.com/v1/me/player/currently-playing",
                            params={"access_token": authentication()})
    return json.loads(response.content.decode("utf-8"))


def currently_playing() -> (Song, int):
    global _last_song
    try:
        response = make_request()
        if "error" in response:
            # remove access token, retry
            os.remove(_cache_dir + "/spotify.response")
            response = make_request()
            if "error" in response:
                raise SpotifyAPIError("Spotify returned an error: \n" + str(response))
        # if "error" not in response, we should be fine
        spotify_id = response["item"]["id"]
        if _last_song == spotify_id:
            return None, 0
        _last_song = spotify_id
        song = Song(response["item"]["name"], response["item"]["artists"][0]["name"], response["item"]["duration_ms"])
        return song, response["progress_ms"]
    except:
        return None, 0
