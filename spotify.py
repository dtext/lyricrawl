import pickle

import requests
from oauthlib.oauth2 import BackendApplicationClient
from requests_oauthlib import OAuth2Session

from song import Song


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
    # requests.get("https://accounts.spotify.com/api/token", auth=authentication())
    return Song(title="Wet Sand", artist="Red Hot Chili Peppers", duration=5000), 3000
