class Song:
    def __init__(self, title: str, artist: str, duration: int, *args, **kwargs):
        self.title = title
        self.artist = artist
        self.duration = duration

    def __eq__(self, other):
        return (self is other or
                self.title == other.title
                and self.artist == other.artist
                and self.duration == other.duration)
