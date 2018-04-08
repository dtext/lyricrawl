class Song:
    def __init__(self, title: str, artist: str, duration: int, *args, **kwargs):
        self.title = title
        self.artist = artist
        self.duration = duration
