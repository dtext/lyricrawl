# lyricrawl
Automatically crawl lyrics for the songs you are listening to on Spotify.

## How it works
Just call the app from a terminal/console like this:
```
python3 lyricrawl.py
```
The lyrics of the current song will be conveniently displayed in that beautiful terminal window.
The app updates in intervals of a few seconds and should always display the current lyrics.
To exit the app, just press <kbd>CTRL</kbd>+<kbd>C</kbd>.

## Setup
Create a new app using the [Spotify Developer Console](https://developer.spotify.com/).
Generate a client id and client secret for your application.
Clone (or download and unzip) this repository, then add a file called `secret.py` to the directory
with the following content, replacing `[client id here]` with the client id you just generated.
```
client_id = "[client id here]"
```
Install the requirements using pip by running:
```
pip install -r requirements.txt
```

## Disclaimer
I created this app for myself.
The software is provided as is, I do not offer any guarantee, support or anything at all, really.
If you know your way around, you can get this to work on your own.
