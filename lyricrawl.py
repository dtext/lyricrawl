from time import sleep
import os
import pickle

import requests
from requests_oauthlib import OAuth2Session
from oauthlib.oauth2 import BackendApplicationClient


class Song:
    def __init__(self, title, artist, duration, *args, **kwargs):
        self.title = title
        self.artist = artist
        self.duration = duration


def run():
    try:
        while True:
            # request currently playing song from spotify
            (song, progress_ms) = currently_playing()

            if song is not None:
                # print lyrics
                clear_console()
                print(find_lyrics(song))
                wait_time = 2 + (song.duration - progress_ms) // 1000  # remaining + 2 second buffer
            else:
                wait_time = 10

            # wait for the specified time, waking up periodically to check for CTRL + C
            for i in range(wait_time):
                sleep(1)
    except KeyboardInterrupt:
        return 0
    except Exception as e:
        print("An error occured during execution:")
        print(str(e))
        return 1


def clear_console():
    return os.system("cls") if os.name == "win32" else os.system("clear")


def authentication():
    from secret import client_id, client_secret
    token_saver = lambda t: pickle.dump(obj=t, file="secret.token")
    try:
        token = pickle.load(file="secret.token")
    except pickle.PickleError:
        client = BackendApplicationClient(client_id=client_id)
        oauth = OAuth2Session(client=client)
        token = oauth.fetch_token(
            token_url='https://spotify.com/oauth2/token',
            client_id=client_id,
            client_secret=client_secret)
        token_saver(token)



def currently_playing() -> (Song, int):
    requests.get("https://accounts.spotify.com/api/token", auth=authentication())
    return Song(title="Wet Sand", artist="Red Hot Chili Peppers",  duration=5000), 3000


def find_lyrics(song: Song) -> str:
    return """
  \"{title}\" by {artist}
  ++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
  Roses are red
  Violets are blue
  This string is empty
  and so are you
    """.format(title=song.title, artist=song.artist)


if __name__ == "__main__":
    run()
